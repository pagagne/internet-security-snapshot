"""The README's workflow schedule (author's request, 31 Oct 2026): one row per GitHub workflow
saying when it runs, generated from the workflow files themselves so it cannot drift.

  python -m snapshot.workflows build    rewrite the table between the README markers
  python -m snapshot.workflows check    fail if the README table is out of date (a test runs this)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .util import _repo_root

BEGIN, END = "<!-- workflows:begin -->", "<!-- workflows:end -->"
DAYS = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _ordinal(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def cron_text(expr: str) -> str:
    """Plain words for the cron patterns the study uses (times are UTC)."""
    mi, hr, dom, mon, dow = expr.split()
    at = f"{int(hr):02d}:{int(mi):02d} UTC"
    if dom == "*" and mon == "*" and dow == "*":
        return f"daily at {at}"
    if dom == "*" and mon == "*":
        return f"{DAYS[int(dow) % 7]} at {at}"
    if mon == "*":
        return f"the {_ordinal(int(dom))} of each month at {at}"
    return f"{_ordinal(int(dom))} {'/'.join(MONTHS[int(m) - 1] for m in mon.split(','))} at {at}"


def rows(root: Path) -> list[tuple[str, str, str]]:
    out = []
    for f in sorted((root / ".github/workflows").glob("*.yml")):
        d = yaml.safe_load(f.read_text())
        on = d.get("on", d.get(True)) or {}
        when = "; ".join(cron_text(s["cron"]) for s in on.get("schedule", []) or []) if isinstance(on, dict) else ""
        also = []
        if isinstance(on, dict):
            if "push" in on:
                also.append("after changes to main")
            if "pull_request" in on:
                also.append("on pull requests")
            if "repository_dispatch" in on:
                also.append("started by the Schedule workflow or Claude")
            if "workflow_dispatch" in on:
                also.append("Run button")
        out.append((d["name"], when or "no timer", ", ".join(also) or "-"))
    return out


def table(root: Path) -> str:
    L = [BEGIN, "<!-- Generated from .github/workflows/*.yml by python -m snapshot.workflows build; do not edit here. -->",
         "| Workflow | Timer | Also runs |", "|---|---|---|"]
    L += [f"| {n} | {w} | {a} |" for n, w, a in rows(root)]
    L += ["", "Details for each workflow: [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md). Dates for scheduled runs "
          "without a timer (dry runs, sweeps, landing snapshots) are in the schedule above.", END]
    return "\n".join(L)


def build_readme(root: Path) -> str:
    text = (root / "README.md").read_text()
    a, b = text.index(BEGIN), text.index(END) + len(END)
    return text[:a] + table(root) + text[b:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    a = ap.parse_args(argv)
    root = _repo_root()
    new = build_readme(root)
    if a.cmd == "build":
        (root / "README.md").write_text(new)
        print("README workflow table written")
        return 0
    if (root / "README.md").read_text() != new:
        print("README workflow table out of date: run python -m snapshot.workflows build")
        return 1
    print("README workflow table current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
