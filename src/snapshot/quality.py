"""Data quality report for one frozen bundle (data/raw/<quarter>/<run>).

Checks completeness, agreement between sources, whether the cohort rules can be
applied, reporting delays, harm-data cleanliness and the AI-credit review load. It
reports rates and counts about the data, never study results, and nothing in it
feeds a label.

    python -m snapshot.quality data/raw/2026Q3/dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from .classify import is_ai_software, lab_name_only, product_category, unmatched_ai_signals
from . import sources as switches
from .util import Quarter, load_config


def pct(n, d) -> str:
    return f"{100 * n / d:.1f}%" if d else "n/a"


def _read(path: Path) -> pd.DataFrame | None:
    return pd.read_parquet(path) if path.exists() else None


def _has_names(affected) -> bool:
    """True if any vendor|product entry has a real name (not blank or 'n/a')."""
    junk = {"", "n/a", "na", "unknown", "-"}
    return any(any(part.strip().lower() not in junk for part in str(x).split("|")) for x in affected)


def _utc(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce")


def build(bundle: Path) -> tuple[str, dict]:
    man = json.loads((bundle / "manifest.json").read_text())
    q = Quarter.parse(man["quarter"])
    qs, qe = pd.Timestamp(q.start, tz="UTC"), pd.Timestamp(q.end, tz="UTC") + pd.Timedelta(days=1)
    L: list[str] = [f"# Data quality: {q} ({man['run']})", ""]
    M: dict = {"quarter": str(q), "run": man["run"]}

    # 1. Completeness ------------------------------------------------------------
    L += ["## 1. Sources", "", "| Source | Status | Note |", "|---|---|---|"]
    for e in man["files"]:
        L.append(f"| {e['source']} | {e['status']} | {(e.get('note') or '')[:140]} |")
    M["gaps"] = [e["source"] for e in man["files"] if e["status"] != "ok"]
    L.append("")

    cve = _read(bundle / "cve/cve_records.parquet")
    nvd = _read(bundle / "nvd/nvd_cves.parquet")
    kev = _read(bundle / "kev/kev_entries.parquet")

    qc = None
    if cve is not None:
        cve["date_published"] = _utc(cve["date_published"])
        qc = cve[(cve["state"] == "PUBLISHED") & (cve["date_published"] >= qs) & (cve["date_published"] < qe)].copy()
        n = len(qc)
        M["cve_published"] = n
        L += ["## 2. CVE records published in the quarter", "",
              f"- Published: **{n:,}**; rejected in the same window: {int(((cve['state'] == 'REJECTED') & (cve['date_published'] >= qs) & (cve['date_published'] < qe)).sum()):,}"]
        has_cvss = qc["cvss_base"].notna()
        has_cwe = qc["cwe_ids"].map(len) > 0
        has_aff = qc["affected"].map(_has_names)
        L += [f"- With a CVSS score in the CVE record: {pct(has_cvss.sum(), n)}",
              f"- With a CWE (weakness) ID: {pct(has_cwe.sum(), n)}; root cause 'other_unknown': {pct((qc['root_cause'] == 'other_unknown').sum(), n)}",
              f"- With vendor/product names: {pct(has_aff.sum(), n)}",
              f"- With CISA Vulnrichment (ADP): {pct(qc['has_cisa_adp'].sum(), n)}"]
        if "ssvc_exploitation" in qc:
            vc = qc["ssvc_exploitation"].fillna("none recorded").value_counts()
            L.append("- CISA exploitation status: " + ", ".join(f"{k} {v:,}" for k, v in vc.items()))
            lag = (_utc(qc["ssvc_timestamp"]) - qc["date_published"]).dt.total_seconds() / 86400
            if lag.notna().any():
                L.append(f"- Days from publication to CISA scoring: median {lag.median():.1f}, 90th percentile {lag.quantile(.9):.1f}")
        M.update(cvss_rate=float(has_cvss.mean()) if n else None, cwe_rate=float(has_cwe.mean()) if n else None)
        L.append("")

    # 3. NVD agreement and delays -------------------------------------------------
    if nvd is not None and qc is not None:
        ids_c, ids_n = set(qc["cve_id"]), set(nvd["cve_id"])
        L += ["## 3. NVD compared with CVE.org", "",
              f"- NVD CVEs published in the window: {len(ids_n):,}; in both: {len(ids_c & ids_n):,}; CVE.org only: {len(ids_c - ids_n):,}; NVD only: {len(ids_n - ids_c):,}"]
        st = nvd["nvd_status"].value_counts()
        L.append("- NVD status: " + ", ".join(f"{k} {v:,}" for k, v in st.items()))
        nvd["pub_month"] = pd.to_datetime(nvd["nvd_published"], errors="coerce").dt.to_period("M").astype(str)
        by = nvd.groupby("pub_month")["nvd_status"].apply(lambda s: (s == "Analyzed").mean())
        L.append("- Share analyzed by NVD, by publication month: " + ", ".join(f"{m} {v:.0%}" for m, v in by.items()))
        j = qc.merge(nvd, on="cve_id", how="inner")
        nvd_score = j["nvd_cvss40"].fillna(j["nvd_cvss31"])
        fill = (j["cvss_base"].isna() & nvd_score.notna()).sum()
        both = j["cvss_base"].notna() & nvd_score.notna()
        diff = (j.loc[both, "cvss_base"] - nvd_score[both]).abs()
        L += [f"- CVE record has no CVSS but NVD does: {fill:,} (NVD could fill these)",
              f"- Both scored: {both.sum():,}; differ by 1.0 or more: {pct((diff >= 1).sum(), both.sum())}; cross the 8.0 line differently: {((j.loc[both, 'cvss_base'] >= 8) != (nvd_score[both] >= 8)).sum():,}"]
        no_aff = ~j["affected"].map(_has_names)
        L.append(f"- No product names in CVE record but NVD has CPE products: {(no_aff & (j['nvd_products'].map(len) > 0)).sum():,}")
        L.append("")

    # 4. KEV dates agree? -----------------------------------------------------------
    if kev is not None:
        L += ["## 4. CISA KEV dates across sources", "", f"- KEV entries: {len(kev):,}"]
        if nvd is not None:
            k = kev.merge(nvd[["cve_id", "nvd_kev_added"]].dropna(), on="cve_id")
            if len(k):
                kd = pd.to_datetime(k["date_added"], utc=True).dt.date
                nd = pd.to_datetime(k["nvd_kev_added"], utc=True).dt.date
                L.append(f"- In KEV and NVD with a KEV date: {len(k):,}; same date: {pct((kd == nd).sum(), len(k))}")
        if qc is not None and "ssvc_exploitation" in qc:
            kq = set(kev["cve_id"]) & set(qc["cve_id"])
            act = set(qc.loc[qc["ssvc_exploitation"] == "active", "cve_id"])
            L.append(f"- Quarter CVEs in KEV: {len(kq):,}; marked 'active' by CISA Vulnrichment: {len(act):,}; in both: {len(kq & act):,}")
        L.append("")

    # 5. Can the cohort rules be applied? -----------------------------------------
    if qc is not None and len(qc):
        el = load_config("cohort_rules.yaml")["eligibility"]
        sev = qc["cvss_severity"].fillna("").str.upper()
        elig = qc[((qc["cvss_base"] >= el["min_cvss_base"]) | (sev == "CRITICAL"))
                  & (qc["date_published"].dt.day <= el["publish_day_max"])].copy()
        elig["slot"] = elig["affected"].map(product_category) if len(elig) else pd.Series(dtype=str)
        elig["month"] = elig["date_published"].dt.strftime("%Y-%m") if len(elig) else pd.Series(dtype=str)
        L += ["## 5. Cohort pools (eligible CVEs per month)", "",
              "Slot c still needs the internet-facing hand check, slot d the AI-credit check.", ""]
        if len(elig):
            piv = elig.pivot_table(index="month", columns="slot", values="cve_id", aggfunc="count", fill_value=0)
            d = elig[elig["ai_credit_terms"].map(lambda x: len(x) > 0)].groupby("month").size()
            L += ["| Month | a edge | b web/collab | c other | d AI candidates |", "|---|---|---|---|---|"]
            for m in piv.index:
                L.append(f"| {m} | {piv.loc[m].get('a_edge', 0)} | {piv.loc[m].get('b_web_collab', 0)} | {piv.loc[m].get('c_other', 0):,} | {int(d.get(m, 0))} |")
            no_names = (~elig["affected"].map(_has_names)).sum()
            L += ["", f"- Eligible CVEs without product names (fall to slot c by default): {no_names:,} of {len(elig):,}", ""]
            M["pools"] = {m: {k: int(v) for k, v in piv.loc[m].items()} | {"d": int(d.get(m, 0))} for m in piv.index}
        else:
            L += ["- No eligible CVEs in this bundle.", ""]
        if len(elig):
            ai_sw = elig["affected"].map(is_ai_software)
            L += ["## 5b. X5 (exploratory): flaws in AI software", "",
                  f"- Eligible CVEs affecting AI software: {int(ai_sw.sum()):,} of {len(elig):,} ({pct(int(ai_sw.sum()), len(elig))})"]
            if kev is not None:
                kq = qc[qc["cve_id"].isin(set(kev["cve_id"]))]
                k_ai = kq["affected"].map(is_ai_software).sum() if len(kq) else 0
                L.append(f"- Quarter CVEs in KEV affecting AI software: {int(k_ai)} of {len(kq)}")
            L.append("")

        # 6. AI-credit review load
        cand = qc[qc["ai_credit_terms"].map(lambda x: len(x) > 0)]
        strings = {tuple(v) for v in cand["credit_values"]}
        unmatched = qc["credit_values"].map(lambda v: bool(unmatched_ai_signals(list(v)))).sum()
        L += ["## 6. AI-credit review load", "",
              f"- Candidates: {len(cand):,} ({pct(len(cand), len(qc))} of CVEs); distinct credit texts to review: {len(strings):,}",
              f"- Matched only on a lab name (stricter review): {cand['ai_credit_terms'].map(lab_name_only).sum():,}",
              f"- AI-looking credits matching no term (watchlist scan): {unmatched:,}", ""]

    # 7. EPSS ----------------------------------------------------------------------
    ep = _read(bundle / "epss/epss_scores.parquet")
    if ep is not None:
        days = pd.to_datetime(ep["date"]).dt.date.nunique()
        L += ["## 7. EPSS", "", f"- Days captured: {days}; rows: {len(ep):,}; file size: {(bundle / 'epss/epss_scores.parquet').stat().st_size / 1e6:.1f} MB"]
        if qc is not None and len(ep):
            last = ep[ep["date"] == ep["date"].max()]
            L.append(f"- Quarter CVEs with a score on the last day: {pct(len(set(qc['cve_id']) & set(last['cve'].astype(str))), len(qc))}")
        L.append("")

    # 8. Harm data -----------------------------------------------------------------
    rw = _read(bundle / "ransomware/ransomware_counts.parquet")
    if rw is not None and not switches.may_publish("ransomware_live"):
        # The quality report is public; figures wait for written permission.
        L += ["## 8. Ransomware leak-site counts (aggregates)", "",
              f"- Collected ({len(rw):,} aggregate rows); figures withheld until ransomware.live gives written permission (config/sources.yaml).", ""]
        rw = None
    if rw is not None:
        L += ["## 8. Ransomware leak-site counts (aggregates)", ""]
        for m, g in rw.groupby("month"):
            tot = int(g.query("dimension == 'all'")["count"].sum())
            unk_c = int(g.query("dimension == 'country' and value in ['UNKNOWN', '']")["count"].sum())
            unk_s = int(g.query("dimension == 'sector' and value in ['unknown', 'Not Found', '']")["count"].sum())
            L.append(f"- {m}: {tot:,} postings, {g.query('dimension == \"group\"').shape[0]} groups; unknown country {pct(unk_c, tot)}, unknown sector {pct(unk_s, tot)}")
        L.append("")
    sec = bundle / "sec/sec_summary.json"
    if sec.exists():
        s = json.loads(sec.read_text())
        L += ["## 9. SEC 8-K Item 1.05", "", f"- {s['filings_item_1_05']} filings ({s['original_8k']} original 8-Ks) against {s['registrants_company_tickers']:,} registrants: {s['per_1000_registrants']} per 1,000"]
        for q, d in (s.get("search_diagnostics") or {}).items():
            L.append(f"- Search {q}: {d.get('total_hits')} hits, {d.get('hits_read')} read, forms {d.get('forms')}, with Item 1.05: {d.get('with_item_1_05')}")
        L.append("")
    radar = sorted((bundle / "radar").glob("*.json")) if (bundle / "radar").exists() else []
    if radar:
        L += ["## 10. Cloudflare Radar", ""]
        for p in radar:
            ok = json.loads(p.read_text()).get("success")
            L.append(f"- {p.stem}: {'ok' if ok else 'error'}")
        L.append("")
    M["counts"], M["fields"] = source_counts(bundle)
    return "\n".join(L), M


# Fields each source must keep providing; a missing or all-empty field is flagged.
EXPECTED_FIELDS = {
    "cve/cve_records.parquet": ["cve_id", "state", "date_published", "cvss_base", "cwe_ids", "affected",
                                "credit_values", "has_cisa_adp", "ssvc_exploitation"],
    "nvd/nvd_cves.parquet": ["cve_id", "nvd_published", "nvd_status", "nvd_cvss31", "nvd_cwe_ids", "nvd_products"],
    "kev/kev_entries.parquet": ["cve_id", "date_added", "vendor", "product"],
    "epss/epss_scores.parquet": ["cve", "date", "epss", "percentile"],
    "sec/sec_8k_item105.parquet": ["accession", "form", "file_date", "items"],
    "ransomware/ransomware_counts.parquet": ["month", "dimension", "value", "count"],
}
DROP_FLAG = 0.5   # flag a count that falls below half (or more than doubles) the previous run's


def source_counts(bundle: Path) -> tuple[dict, dict]:
    counts, fields = {}, {}
    for rel, cols in EXPECTED_FIELDS.items():
        p = bundle / rel
        if not p.exists():
            continue
        df = pd.read_parquet(p)
        counts[rel] = len(df)
        fields[rel] = {c: ("missing" if c not in df.columns else "empty" if df[c].isna().all() else "ok") for c in cols}
    radar = bundle / "radar"
    if radar.exists():
        counts["radar/series_ok"] = sum(1 for f in radar.glob("*.json") if json.loads(f.read_text()).get("success"))
    return counts, fields


def drift_section(metrics: dict, previous: dict | None) -> list[str]:
    L = ["## 11. Drift checks", ""]
    flags = []
    for rel, cols in (metrics.get("fields") or {}).items():
        for c, st in cols.items():
            if st != "ok":
                flags.append(f"**{rel}: field `{c}` is {st}** (source format may have changed)")
    if previous:
        prev_counts = previous.get("counts") or {}
        same_q = previous.get("quarter") == metrics.get("quarter")
        for rel, n in (metrics.get("counts") or {}).items():
            p = prev_counts.get(rel)
            if p in (None, 0):
                continue
            ratio = n / p
            if same_q and (ratio < DROP_FLAG or ratio > 1 / DROP_FLAG):
                flags.append(f"**{rel}: {n:,} rows vs {p:,} in the previous run of {previous.get('quarter')}**")
            elif not same_q and n == 0:
                flags.append(f"**{rel}: 0 rows** (previous run had {p:,})")
        for src in metrics.get("gaps", []):
            if src not in (previous.get("gaps") or []):
                flags.append(f"**{src}: gap this run, ok in the previous run**")
        L.append(f"Compared with the previous run ({previous.get('quarter')} {previous.get('run')}).")
    else:
        L.append("No previous run to compare with; field checks only.")
    L += [""] + ([f"- {f}" for f in flags] if flags else ["- No drift flagged."]) + [""]
    metrics["drift_flags"] = flags
    return L


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bundles", nargs="+", type=Path)
    ap.add_argument("--previous", type=Path, help="quality.json from the previous run (drift checks)")
    args = ap.parse_args(argv)
    for b in args.bundles:
        try:
            md, metrics = build(b)
            prev = json.loads(args.previous.read_text()) if args.previous and args.previous.exists() else None
            md += "\n" + "\n".join(drift_section(metrics, prev))
        except Exception as exc:  # the report must never hide a failed run
            md, metrics = f"# Data quality: {b}\n\nReport failed: {type(exc).__name__}: {exc}\n", {"error": str(exc)}
        (b / "quality.md").write_text(md)
        (b / "quality.json").write_text(json.dumps(metrics, indent=2, default=str))
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
