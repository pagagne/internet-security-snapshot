"""Quarterly pull: fetch sources, freeze outputs, write the manifest.

Usage:
    python -m snapshot.pull                       # previous quarter, run inferred from today
    python -m snapshot.pull --quarter 2026Q4 --run provisional
    python -m snapshot.pull --sources kev,cve --out data/raw

Run type: pulls in January/April/July/October are 'provisional'; pulls in
February/May/August/November are 'final' (Section 2 of the pre-registration).
Any other month is a 'dry-run'.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

from .collect import cve, kev
from .util import Manifest, Quarter

SOURCES = ("kev", "cve")


def infer_run(today: dt.date) -> str:
    if today.month in (1, 4, 7, 10):
        return "provisional"
    if today.month in (2, 5, 8, 11):
        return "final"
    return "dry-run"


def infer_quarter(today: dt.date) -> Quarter:
    """Provisional and final runs both happen in the following quarter, so the
    quarter being measured is always the most recent one that has ended."""
    return Quarter.previous_to(today)


def pull_kev(out: Path, manifest: Manifest, work: Path) -> None:
    repo = work / "kev-data"
    sha = kev.clone(repo)
    dest = out / "kev"
    dest.mkdir(parents=True, exist_ok=True)
    raw = dest / kev.CATALOG
    shutil.copyfile(repo / kev.CATALOG, raw)
    manifest.add_file("cisa_kev", raw, f"cisagov/kev-data@{sha}")
    table = kev.build_table(repo)
    pq = dest / "kev_entries.parquet"
    table.to_parquet(pq, index=False)
    manifest.add_file("cisa_kev", pq, f"cisagov/kev-data@{sha}", note=f"{len(table)} entries")


def pull_cve(out: Path, manifest: Manifest, work: Path) -> None:
    repo = work / "cvelistV5"
    sha = cve.clone(repo)
    dest = out / "cve"
    dest.mkdir(parents=True, exist_ok=True)
    table = cve.build_table(repo)
    pq = dest / "cve_records.parquet"
    table.to_parquet(pq, index=False)
    manifest.add_file(
        "cve_org",
        pq,
        f"CVEProject/cvelistV5@{sha}",
        note=f"{len(table)} records; raw JSON pinned by commit, not copied",
    )


PULLERS = {"kev": pull_kev, "cve": pull_cve}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quarter", help="e.g. 2026Q4 (default: previous quarter)")
    ap.add_argument("--run", choices=["provisional", "final", "dry-run"], help="default: inferred from today")
    ap.add_argument("--sources", default=",".join(SOURCES), help=f"comma list from {SOURCES}")
    ap.add_argument("--out", default="data/raw", help="output root")
    args = ap.parse_args(argv)

    today = dt.datetime.now(dt.timezone.utc).date()
    run = args.run or infer_run(today)
    quarter = Quarter.parse(args.quarter) if args.quarter else infer_quarter(today)
    out = Path(args.out) / str(quarter) / run
    out.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(quarter, run, out)

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name in [s.strip() for s in args.sources.split(",") if s.strip()]:
            if name not in PULLERS:
                print(f"unknown source: {name}", file=sys.stderr)
                return 2
            print(f"[pull] {name} -> {out}")
            try:
                PULLERS[name](out, manifest, Path(tmp))
            except Exception as exc:  # recorded as a gap, never silently skipped
                failures += 1
                traceback.print_exc()
                manifest.add_gap(name, f"{type(exc).__name__}: {exc}")
    path = manifest.write()
    print(f"[pull] manifest: {path} ({failures} gap(s))")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
