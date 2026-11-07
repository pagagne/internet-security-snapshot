"""Where the 2026 surge in published CVE records comes from (author's decision, 7 Nov 2026).

Breaks the published records (rejected excluded) down by quarter from 2024 to date: who issued
the ID (CNA), severity, the study's root-cause group, and AI credit; the share of the five
largest CNAs and the count without them (the registered T5 sensitivity, Section 9); and the
monthly count from 2017 (the I5 backfill curve). Evidence for core-freeze item 25 (I5 / T5),
read privately; no label is computed. Runs on the frozen bundle of the latest quarterly pull.

    python -m snapshot.research.cve_surge --bundle DIR --out DIR
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd

TOP = 15


def _find_bundle(root: Path) -> Path:
    hits = sorted(root.rglob("manifest.json"))
    if not hits:
        raise SystemExit(f"no manifest.json under {root}")
    return hits[0].parent


def published(cve: pd.DataFrame) -> pd.DataFrame:
    df = cve[cve["state"] == "PUBLISHED"].copy()
    df["pub"] = pd.to_datetime(df["date_published"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df[df["pub"].notna()]
    df["quarter"] = df["pub"].dt.to_period("Q").astype(str)
    df["month"] = df["pub"].dt.to_period("M").astype(str)
    df["cna"] = df["cna"].fillna("(none)")
    df["severity"] = df["cvss_severity"].fillna("NONE").str.upper()
    df["root_cause"] = df["root_cause"].fillna("other_unknown")
    df["ai_credited"] = df.get("ai_credited", pd.Series(False, index=df.index)).fillna(False).astype(bool)
    return df


def breakdown(df: pd.DataFrame, first: str = "2024Q1") -> dict:
    q = df[df["quarter"] >= first]
    quarters = sorted(q["quarter"].unique())
    out = {"quarters": quarters, "total": q.groupby("quarter").size().to_dict()}
    top = q["cna"].value_counts().head(TOP).index.tolist()
    out["by_cna"] = {c: q[q["cna"] == c].groupby("quarter").size().reindex(quarters, fill_value=0).to_dict() for c in top}
    out["other_cnas"] = q[~q["cna"].isin(top)].groupby("quarter").size().reindex(quarters, fill_value=0).to_dict()
    out["by_severity"] = q.groupby(["quarter", "severity"]).size().unstack(fill_value=0).to_dict(orient="index")
    out["by_root_cause"] = q.groupby(["quarter", "root_cause"]).size().unstack(fill_value=0).to_dict(orient="index")
    out["ai_credited"] = q.groupby("quarter")["ai_credited"].sum().astype(int).to_dict()
    # registered sensitivity: without each quarter's five largest CNAs
    s = {}
    for qq, g in q.groupby("quarter"):
        top5 = g["cna"].value_counts().head(5)
        s[qq] = {"top5": top5.index.tolist(), "top5_share": round(top5.sum() / len(g), 4),
                 "without_top5": int(len(g) - top5.sum())}
    out["without_top5"] = s
    out["monthly_since_2017"] = df[df["month"] >= "2017-01"].groupby("month").size().to_dict()
    return out


def report(R: dict, bundle_note: str) -> str:
    qs = R["quarters"]
    L = ["# Where the 2026 surge in published CVE records comes from (private)", "",
         f"Evidence for core-freeze item 25 (I5 / T5); no label computed. {bundle_note}", "",
         "## Published records per quarter", "",
         "| Quarter | Total | Five largest CNAs' share | Without the five largest | AI-credited |",
         "|---|---|---|---|---|"]
    for q in qs:
        w = R["without_top5"][q]
        L.append(f"| {q} | {R['total'][q]:,} | {w['top5_share']:.0%} | {w['without_top5']:,} | {R['ai_credited'].get(q, 0):,} |")
    L += ["", "## By issuing CNA (largest overall since 2024)", "",
          "| CNA | " + " | ".join(qs) + " |", "|---|" + "---|" * len(qs)]
    for c, v in R["by_cna"].items():
        L.append(f"| {c} | " + " | ".join(f"{v[q]:,}" for q in qs) + " |")
    L.append("| (all others) | " + " | ".join(f"{R['other_cnas'][q]:,}" for q in qs) + " |")
    for key, title in (("by_severity", "By severity (CVSS, best available)"), ("by_root_cause", "By root-cause group")):
        cols = sorted({k for v in R[key].values() for k in v})
        L += ["", f"## {title}", "", "| Quarter | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
        for q in qs:
            L.append(f"| {q} | " + " | ".join(f"{R[key][q].get(c, 0):,}" for c in cols) + " |")
    L += ["", "## Five largest CNAs each quarter", ""]
    L += [f"- {q}: {', '.join(R['without_top5'][q]['top5'])}" for q in qs]
    L += ["", "The monthly count since 2017 is in `cve_surge.json` (`monthly_since_2017`).", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")      # unused; kept for the Research workflow
    ap.add_argument("--bundle", type=Path, default=Path(os.environ.get("PRACTICE_BUNDLE", "practice-bundle")))
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    b = _find_bundle(a.bundle)
    man = json.loads((b / "manifest.json").read_text())
    note = f"Bundle: {man.get('quarter', '?')} {man.get('run', man.get('kind', ''))}, pulled {man.get('pulled_at', man.get('created', '?'))}."
    R = breakdown(published(pd.read_parquet(b / "cve/cve_records.parquet")))
    (a.out / "cve_surge.json").write_text(json.dumps(R, indent=1, default=str))
    (a.out / "summary.md").write_text(report(R, note))
    print(f"cve_surge: {len(R['quarters'])} quarters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
