"""Deep dive behind the 2026 surge (author's request, 8 Nov 2026; prompted by "The haystack tripled").

Four checks for the I5 evidence, run early: (A) where severity scores come from (issuer, CISA's
enrichment, or none) and CISA's "active exploitation" marks, by month; (B) how much NIST still
enriches (NVD analysis status and NVD scores) by month; (C) rejected records, by month and issuer,
to find bursts such as the fake records reported in July 2026; (D) exploited flaws: CISA KEV
additions by month in 2025 and 2026, how old the added flaws are, and how fast 2026 flaws reached
the list. Private; no label computed. Runs on the frozen bundle of the latest quarterly pull.

    python -m snapshot.research.cve_deep --bundle DIR --out DIR
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

from snapshot.research.cve_surge import _find_bundle


def _month(s) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce").dt.tz_localize(None).dt.to_period("M").astype(str)


def severity_sources(cve: pd.DataFrame, first: str = "2025-01") -> dict:
    df = cve[cve["state"] == "PUBLISHED"].copy()
    df["m"] = _month(df["date_published"])
    df = df[df["m"] >= first]
    scored = df["cvss_base"].notna()
    adp = df.get("has_cisa_adp", pd.Series(False, index=df.index)).fillna(False).astype(bool)
    out = {}
    for m, g in df.groupby("m"):
        s, a = scored[g.index], adp[g.index]
        out[m] = {"records": int(len(g)), "scored": int(s.sum()), "no_score": int((~s).sum()),
                  "cisa_enriched": int(a.sum()),
                  "ssvc_active": int((g.get("ssvc_exploitation") == "active").sum()) if "ssvc_exploitation" in g else 0,
                  "ssvc_poc": int((g.get("ssvc_exploitation") == "poc").sum()) if "ssvc_exploitation" in g else 0}
    return out


def nvd_enrichment(nvd: pd.DataFrame, first: str = "2025-01") -> dict:
    df = nvd.copy()
    df["m"] = _month(df["nvd_published"])
    df = df[df["m"] >= first]
    has_score = df[["nvd_cvss31", "nvd_cvss40"]].notna().any(axis=1)
    out = {}
    for m, g in df.groupby("m"):
        st = g["nvd_status"].fillna("(none)").value_counts().to_dict()
        out[m] = {"records": int(len(g)), "nvd_scored": int(has_score[g.index].sum()), "status": {k: int(v) for k, v in st.items()}}
    return out


def rejected(cve: pd.DataFrame, first: str = "2025-01") -> dict:
    df = cve[cve["state"] == "REJECTED"].copy()
    df["m"] = _month(df["date_updated"])
    df = df[df["m"] >= first]
    by_m = df.groupby("m").size().to_dict()
    top = df.groupby(["m", "cna"]).size().sort_values(ascending=False).head(15)
    return {"by_month": {k: int(v) for k, v in by_m.items()},
            "largest_bursts": [{"month": m, "cna": c, "rejected": int(n)} for (m, c), n in top.items()]}


def kev(kev_df: pd.DataFrame, cve: pd.DataFrame) -> dict:
    k = kev_df[kev_df["list"] == "cisa"].copy()
    k["added"] = pd.to_datetime(k["date_added"], utc=True, errors="coerce").dt.tz_localize(None)
    k["m"] = k["added"].dt.to_period("M").astype(str)
    k["cve_year"] = k["cve_id"].str.slice(4, 8)
    by_m = k[k["m"] >= "2024-01"].groupby("m").size().to_dict()
    pub = cve.set_index("cve_id")["date_published"]
    k["pub"] = pd.to_datetime(k["cve_id"].map(pub), utc=True, errors="coerce").dt.tz_localize(None)
    k["days"] = (k["added"] - k["pub"]).dt.days
    out = {"added_by_month": {m: int(v) for m, v in by_m.items()}}
    for y in ("2024", "2025", "2026"):
        ky = k[k["added"].dt.year == int(y)]
        out[f"added_{y}"] = {"total": int(len(ky)),
                             "jan_oct": int((ky["added"].dt.month <= 10).sum()),
                             "same_year_cves": int((ky["cve_year"] == y).sum()),
                             "older_cves": int((ky["cve_year"] < y).sum()),
                             "median_days_publish_to_kev_same_year": (float(ky.loc[ky["cve_year"] == y, "days"].median())
                                                                      if (ky["cve_year"] == y).any() else None)}
    p = cve[(cve["state"] == "PUBLISHED")].copy()
    p["y"] = pd.to_datetime(p["date_published"], utc=True, errors="coerce").dt.year
    for y in (2024, 2025, 2026):
        ids = set(p.loc[p["y"] == y, "cve_id"])
        hit = len(ids & set(k["cve_id"]))
        out[f"share_of_{y}_records_in_kev"] = {"records": len(ids), "in_kev": hit,
                                               "share": round(hit / len(ids), 5) if ids else None}
    return out


def report(R: dict, note: str) -> str:
    L = ["# Behind the 2026 surge: severity sources, NIST enrichment, rejected records, exploited flaws (private)", "",
         f"Author's request, 8 Nov 2026. {note}", "", "## A. Where severity scores come from (published records by month)", "",
         "| Month | Records | With a score | No score | CISA-enriched | CISA: active exploitation | CISA: proof of concept |",
         "|---|---|---|---|---|---|---|"]
    for m, v in R["severity"].items():
        L.append(f"| {m} | {v['records']:,} | {v['scored']:,} | {v['no_score']:,} | {v['cisa_enriched']:,} | {v['ssvc_active']:,} | {v['ssvc_poc']:,} |")
    statuses = sorted({s for v in R["nvd"].values() for s in v["status"]})
    L += ["", "## B. NIST enrichment (NVD records by publication month)", "",
          "| Month | Records | NVD-scored | " + " | ".join(statuses) + " |", "|---|---|---|" + "---|" * len(statuses)]
    for m, v in R["nvd"].items():
        L.append(f"| {m} | {v['records']:,} | {v['nvd_scored']:,} | " + " | ".join(f"{v['status'].get(s, 0):,}" for s in statuses) + " |")
    L += ["", "## C. Rejected records (by month of rejection)", "", "| Month | Rejected |", "|---|---|"]
    L += [f"| {m} | {n:,} |" for m, n in R["rejected"]["by_month"].items()]
    L += ["", "Largest bursts (month, issuer, rejected):", ""]
    L += [f"- {b['month']} · {b['cna']} · {b['rejected']}" for b in R["rejected"]["largest_bursts"]]
    K = R["kev"]
    L += ["", "## D. Exploited flaws (CISA KEV)", "", "| Year | Added | Jan-Oct | Same-year CVEs | Older CVEs | Median days, publication to KEV (same-year) |", "|---|---|---|---|---|---|"]
    for y in ("2024", "2025", "2026"):
        v = K[f"added_{y}"]
        L.append(f"| {y} | {v['total']:,} | {v['jan_oct']:,} | {v['same_year_cves']:,} | {v['older_cves']:,} | {v['median_days_publish_to_kev_same_year']} |")
    L += ["", "| Records published in | Records | In KEV | Share |", "|---|---|---|---|"]
    for y in (2024, 2025, 2026):
        v = K[f"share_of_{y}_records_in_kev"]
        L.append(f"| {y} | {v['records']:,} | {v['in_kev']:,} | " + (f"{v['share']:.3%}" if v['share'] is not None else "-") + " |")
    L += ["", "KEV additions by month are in `cve_deep.json`.", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--bundle", type=Path, default=Path(os.environ.get("PRACTICE_BUNDLE", "practice-bundle")))
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    b = _find_bundle(a.bundle)
    cve = pd.read_parquet(b / "cve/cve_records.parquet")
    R = {"severity": severity_sources(cve), "rejected": rejected(cve),
         "kev": kev(pd.read_parquet(b / "kev/kev_entries.parquet"), cve)}
    nvd_pq = b / "nvd/nvd_cves.parquet"
    R["nvd"] = nvd_enrichment(pd.read_parquet(nvd_pq)) if nvd_pq.exists() else {}
    man = json.loads((b / "manifest.json").read_text())
    note = f"Bundle: {man.get('quarter', '?')}."
    (a.out / "cve_deep.json").write_text(json.dumps(R, indent=1, default=str))
    (a.out / "summary.md").write_text(report(R, note))
    print("cve_deep: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
