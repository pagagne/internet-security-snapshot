"""Resource profile of a full quarterly pull, measured on the GitHub runner.

    python -m snapshot.research.resource_profile --start 2026-07-01 --end 2026-09-30 --out DIR

Runs each source of the quarterly pull on its own (as `python -m snapshot.pull`, dry-run), and
the monthly ISC honeypot capture, and records per step: wall time, peak memory (max RSS of the
child process, from wait4) and bytes written. Also records the runner (CPUs, memory, free
disk). Sources that need secrets (Cloudflare Radar, ransomware.live) are skipped here; their
sizes are known from earlier runs. Used for the capacity estimate (docs/CAPACITY.md).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _quarter(end: str) -> str:
    y, m = int(end[:4]), int(end[5:7])
    return f"{y}Q{(m - 1) // 3 + 1}"


def _du(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.exists() else 0


def _run(cmd: list[str], log) -> dict:
    t0 = time.monotonic()
    proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    _, status, ru = os.wait4(proc.pid, 0)
    return {"seconds": round(time.monotonic() - t0, 1), "peak_rss_mb": round(ru.ru_maxrss / 1024, 1),
            "exit": os.waitstatus_to_exitcode(status)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", default="2026-07-01")
    ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    work = Path("/tmp/profile-data")
    q = _quarter(a.end)
    mem = next((l.split()[1] for l in open("/proc/meminfo") if l.startswith("MemTotal")), "0")
    runner = {"cpus": os.cpu_count(), "mem_total_mb": int(mem) // 1024,
              "disk_free_gb_before": round(shutil.disk_usage("/").free / 1e9, 1)}
    steps = {}
    with open(a.out / "steps.log", "w") as log:
        for src in ["kev", "cve", "nvd", "epss", "sec"]:
            d = work / src
            r = _run([sys.executable, "-m", "snapshot.pull", "--quarter", q, "--run", "dry-run",
                      "--sources", src, "--out", str(d)], log)
            r["bytes_written"] = _du(d)
            steps[f"pull:{src}"] = r
            print(src, r, flush=True)
        d = work / "honeypot"
        r = _run([sys.executable, "-m", "snapshot.collect.isc_honeypot", "--out", str(d)], log)
        r["bytes_written"] = _du(d)
        steps["honeypot_monthly"] = r
        print("honeypot", r, flush=True)
    runner["disk_free_gb_after"] = round(shutil.disk_usage("/").free / 1e9, 1)
    res = {"quarter": q, "runner": runner, "steps": steps,
           "total_seconds": round(sum(s["seconds"] for s in steps.values()), 1),
           "total_bytes": sum(s["bytes_written"] for s in steps.values()),
           "max_peak_rss_mb": max(s["peak_rss_mb"] for s in steps.values())}
    (a.out / "profile.json").write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
