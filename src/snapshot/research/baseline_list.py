"""Baseline-year review list (schedule item baseline-list-ready, 20 Nov 2026).

Pre-registration Section 10: the retrospective cohort, Q4 2025 to Q3 2026, is drawn with the
frozen selection rule and hand-checked (23-24 Nov 2026) so the patching measures have a baseline
in the pilot. This task clones the CVE List and CISA's KEV history at today's commits (both
recorded), builds the same tables the quarterly pull builds, and runs snapshot.review for each
of the four quarters: the seeded draw with backups, the AI-credit texts, and the race list
(every flaw first added to KEV in the quarter), with fix dates pre-filled from the same sources
as the quarterly run. Nothing is scored here; the lists go to the private repository and are
then loaded into the Hand Check app.

    python -m snapshot.research.baseline_list --out DIR
"""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import pandas as pd

from snapshot import review
from snapshot.collect import cve, kev

QUARTERS = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # accepted for the research workflow; unused
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        cve_sha = cve.clone(work / "cvelistV5")
        cve_table = cve.build_table(work / "cvelistV5")
        cpq = a.out / "cve_records.parquet"
        cve_table.to_parquet(cpq, index=False)
        kev_sha = kev.clone(work / "kev-data")
        kpq = a.out / "kev_entries.parquet"
        kev.build_table(work / "kev-data").to_parquet(kpq, index=False)
    lines = ["# Baseline-year review lists", "",
             f"CVE List commit {cve_sha}; KEV history commit {kev_sha}.", ""]
    for q in QUARTERS:
        out = a.out / f"review-{q}.csv"
        review.main(["--cve", str(cpq), "--kev", str(kpq), "--quarter", q, "--out", str(out),
                     "--decisions", "review/decisions.csv"])
        d = pd.read_csv(out, dtype=str).fillna("")
        counts = d["task"].value_counts().to_dict()
        lines.append(f"- {q}: {len(d)} rows; " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    # the parquet copies are large and public data; keep only the lists and the summary
    cpq.unlink(); kpq.unlink()
    (a.out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
