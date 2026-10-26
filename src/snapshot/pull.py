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
import time
import traceback
from pathlib import Path

import json
import os

from . import sources as switches
from .collect import cve, epss, kev, nvd, radar, ransomware, sec
from .util import Manifest, Quarter, utcnow

SOURCES = ("kev", "cve", "nvd", "epss", "sec", "radar", "ransomware")
# Set by main(): the quarter being pulled, the last day with complete data, EPSS step.
CTX: dict = {}


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


def _window() -> tuple[dt.date, dt.date]:
    q: Quarter = CTX["quarter"]
    return q.start, min(q.end, CTX["yesterday"])


def pull_nvd(out: Path, manifest: Manifest, work: Path) -> None:
    start, end = _window()
    try:
        table, how = nvd.from_mirror(start, end, work)
    except Exception as exc:
        print(f"[pull] nvd mirror failed ({type(exc).__name__}: {exc}); falling back to NVD's feed files")
        table, versions = nvd.from_feeds(start, end)
        how = "NVD JSON 2.0 feeds " + ", ".join(versions)
    dest = out / "nvd"
    dest.mkdir(parents=True, exist_ok=True)
    pq = dest / "nvd_cves.parquet"
    table.to_parquet(pq, index=False)
    manifest.add_file("nvd", pq, how,
                      note=f"{len(table)} CVEs published {start}..{end}; key={'yes' if os.environ.get('NVD_API_KEY') else 'no'}")


def pull_epss(out: Path, manifest: Manifest, work: Path) -> None:
    q: Quarter = CTX["quarter"]
    # Follow-up runs past the quarter end so cohort CVEs get up to 90 days of scores.
    end = min(q.end + dt.timedelta(days=92), CTX["yesterday"])
    table, notes, models = epss.build_table(q.start, end, min_year=q.start.year - 1, step_days=CTX["epss_step"])
    dest = out / "epss"
    dest.mkdir(parents=True, exist_ok=True)
    pq = dest / "epss_scores.parquet"
    table.to_parquet(pq, index=False)
    days = table["date"].nunique() if len(table) else 0
    model_versions = sorted({m.split(",")[0].replace("model_version:", "") for m in models})
    manifest.add_file("epss", pq, f"FIRST EPSS model {', '.join(model_versions) or 'n/a'}",
                      status="ok" if not notes else "partial",
                      note=f"{days} days {q.start}..{end}, step {CTX['epss_step']}d; CVE IDs from {q.start.year - 1} on; {len(notes)} day(s) missing")
    for n in notes:
        manifest.add_gap("epss", n)


def pull_sec(out: Path, manifest: Manifest, work: Path) -> None:
    start, end = _window()
    table = sec.filings_105(start, end)
    print(f"[pull] sec search diagnostics: {json.dumps(sec.DIAG)}")
    regs = sec.registrant_count()
    dest = out / "sec"
    dest.mkdir(parents=True, exist_ok=True)
    pq = dest / "sec_8k_item105.parquet"
    table.to_parquet(pq, index=False)
    summary = dest / "sec_summary.json"
    summary.write_text(json.dumps({
        "window": [start.isoformat(), end.isoformat()],
        "filings_item_1_05": int(len(table)),
        "original_8k": int((table["form"] == "8-K").sum()) if len(table) else 0,
        "registrants_company_tickers": regs,
        "search_diagnostics": sec.DIAG,
        "per_1000_registrants": round(1000 * int((table["form"] == "8-K").sum()) / regs, 3) if regs and len(table) else 0.0,
    }, indent=2))
    manifest.add_file("sec_edgar", pq, f"EDGAR full-text search, retrieved {utcnow()}", note=f"{len(table)} filings")
    manifest.add_file("sec_edgar", summary, f"company_tickers.json, retrieved {utcnow()}", note=f"{regs} registrants")


def pull_radar(out: Path, manifest: Manifest, work: Path) -> None:
    start, end = _window()
    dest = out / "radar"
    dest.mkdir(parents=True, exist_ok=True)
    for name, data in radar.fetch(start, end).items():
        path = dest / f"{name}.json"
        path.write_text(json.dumps(data, indent=1))
        manifest.add_file("cloudflare_radar", path, f"Radar API, retrieved {utcnow()}")


def pull_ransomware(out: Path, manifest: Manifest, work: Path) -> None:
    start, end = _window()
    months, d = [], start.replace(day=1)
    while d <= end:
        months.append((d.year, d.month))
        d = (d + dt.timedelta(days=32)).replace(day=1)
    table = ransomware.build_table(months)
    dest = out / "ransomware"
    dest.mkdir(parents=True, exist_ok=True)
    pq = dest / "ransomware_counts.parquet"
    table.to_parquet(pq, index=False)
    totals = table[table["dimension"] == "all"][["month", "count"]].to_dict("records")
    manifest.add_file("ransomware_live", pq, f"ransomware.live API, retrieved {utcnow()}",
                      note=f"aggregate counts only, no victim names; monthly totals {totals}")


PULLERS = {"kev": pull_kev, "cve": pull_cve, "nvd": pull_nvd, "epss": pull_epss,
           "sec": pull_sec, "radar": pull_radar, "ransomware": pull_ransomware}


def _annotate(level: str, source: str, text: str) -> None:
    """On GitHub Actions, post a public run annotation per source (status and duration)."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        msg = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::{level} title=pull {source}::{msg}", flush=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quarter", help="e.g. 2026Q4 (default: previous quarter)")
    ap.add_argument("--run", choices=["provisional", "final", "dry-run"], help="default: inferred from today")
    ap.add_argument("--sources", default="", help=f"comma list from {SOURCES} (default: all whose "
                    "switch in config/sources.yaml is on)")
    ap.add_argument("--out", default="data/raw", help="output root")
    ap.add_argument("--epss-step", type=int, default=1, help="days between EPSS samples (default 1 = daily)")
    args = ap.parse_args(argv)

    today = dt.datetime.now(dt.timezone.utc).date()
    run = args.run or infer_run(today)
    quarter = Quarter.parse(args.quarter) if args.quarter else infer_quarter(today)
    CTX.update(quarter=quarter, yesterday=today - dt.timedelta(days=1), epss_step=args.epss_step)
    out = Path(args.out) / str(quarter) / run
    out.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(quarter, run, out)
    manifest.switches = {k: {f: v[f] for f in ("permission", "collect", "publish")}
                         for k, v in switches.load().items()}
    off = switches.disabled_pulls()
    names = [s.strip() for s in args.sources.split(",") if s.strip()] or list(SOURCES)
    for name in names:
        if name not in PULLERS:
            print(f"unknown source: {name}", file=sys.stderr)
            return 2

    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name in names:
            if name in off:  # switched off in config/sources.yaml: recorded, not a gap
                print(f"[pull] {name}: switched off in config/sources.yaml; skipped")
                _annotate("notice", name, "switched off in config/sources.yaml; not collected")
                continue
            print(f"[pull] {name} -> {out}")
            t0 = time.monotonic()
            try:
                PULLERS[name](out, manifest, Path(tmp))
                _annotate("notice", name, f"ok in {time.monotonic() - t0:.0f}s")
            except Exception as exc:  # recorded as a gap, never silently skipped
                failures += 1
                traceback.print_exc()
                manifest.add_gap(name, f"{type(exc).__name__}: {exc}")
                _annotate("error", name, f"gap after {time.monotonic() - t0:.0f}s: {type(exc).__name__}: {str(exc)[:500]}")
    path = manifest.write()
    print(f"[pull] manifest: {path} ({failures} gap(s))")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
