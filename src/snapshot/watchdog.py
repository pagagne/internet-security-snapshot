"""Watchdog for timed runs GitHub may skip (author's decision, 29 Oct 2026).

GitHub sometimes drops a scheduled run at busy times. The study's essential timed workflows must
not depend on a person or a Claude session noticing, so the Schedule workflow (three runs a day)
calls `python -m snapshot.watchdog` after its own work. For each watched workflow it asks: was
it due in the last few days, has the grace period passed, and is there any run of it since it
was due? If there is none, it starts the workflow itself (through GitHub's API) and opens an
issue saying so. A marker in that issue makes sure it is started at most once per due date.

  python -m snapshot.watchdog [--date YYYY-MM-DD --time HH:MM] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess

from . import pull
from .schedule import dispatch_args

UTC = dt.timezone.utc

# file: (days of month or None for every day, months or None for every month, due time UTC,
#        how to start it: "api" (Schedule's dispatch), "button" (Run button), or "event:<type>"
#        (a repository_dispatch event, for workflows without a Run button))
WATCHED = {
    "quarterly-pull.yml": ({1}, {1, 2, 4, 5, 7, 8, 10, 11}, dt.time(6, 0), "api"),
    "honeypot.yml": ({2}, None, dt.time(9, 43), "api"),
    "backup.yml": ({3}, None, dt.time(10, 17), "button"),
    "rebuild-check.yml": ({10}, None, dt.time(7, 17), "button"),
    # Daily banner check (author, 1 Nov 2026, after GitHub skipped it that morning). Restarted
    # once if missing 4 hours after its time, so by Schedule's 15:37 UTC run; still one light
    # request per source per day. No issue opened (daily; the run itself is the record).
    "source-status.yml": (None, None, dt.time(11, 23), "event:source-status"),
}
QUIET = {"source-status.yml"}      # restarted without opening an issue
GRACE = dt.timedelta(hours=4)      # GitHub's late timers usually arrive well within this
LOOKBACK_DAYS = 3                  # catch up even if Schedule itself missed a day or two
MARKER = "<!-- watchdog: {} -->"


def due_times(name: str, now: dt.datetime) -> list[dt.datetime]:
    """Due moments of `name` in the look-back window whose grace period has passed."""
    days, months, at, _ = WATCHED[name]
    out = []
    for back in range(LOOKBACK_DAYS + 1):
        d = (now - dt.timedelta(days=back)).date()
        if (days is None or d.day in days) and (months is None or d.month in months):
            t = dt.datetime.combine(d, at, UTC)
            if t + GRACE <= now:
                out.append(t)
    if days is None:                # a daily run: only the latest missed one matters (no catch-up pile)
        out = out[:1]
    return out


def payload(name: str, due: dt.datetime) -> dict:
    """What to start: the pull gets its run type and quarter from its due date, never 'dry-run'."""
    w = {"workflow": name}
    if name == "quarterly-pull.yml":
        d = due.date()
        w["inputs"] = {"quarter": str(pull.infer_quarter(d)), "run": pull.infer_run(d)}
    return w


def start_args(name: str, due: dt.datetime, repo: str) -> list[str]:
    how = WATCHED[name][3]
    if how == "api":
        return dispatch_args(payload(name, due))
    if how.startswith("event:"):
        return ["api", "-X", "POST", f"repos/{repo}/dispatches", "-f", f"event_type={how[6:]}"]
    return ["api", "-X", "POST", f"repos/{repo}/actions/workflows/{name}/dispatches", "-f", "ref=main"]


def check(now: dt.datetime, dry: bool = False, gh=None) -> list[str]:
    gh = gh or (lambda args: subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout)
    repo = os.environ.get("GITHUB_REPOSITORY", "pagagne/internet-security-snapshot")
    issues = gh(["api", f"repos/{repo}/issues?labels=watchdog&state=all&per_page=100", "--jq", "[.[].body]"])
    done = set(re.findall(r"<!-- watchdog: (\S+) -->", issues))
    log = []
    for name in WATCHED:
        for due in due_times(name, now):
            key = f"{name}@{due:%Y-%m-%dT%H%MZ}"
            if key in done:
                continue
            since = due - dt.timedelta(minutes=30)
            runs = json.loads(gh(["api", f"repos/{repo}/actions/workflows/{name}/runs?created=>={since:%Y-%m-%dT%H:%M:%SZ}&per_page=5",
                                  "--jq", "[.workflow_runs[].id]"]) or "[]")
            if runs:
                continue
            log.append(f"start {key}")
            if dry:
                continue
            gh(start_args(name, due, repo))
            if name in QUIET:
                continue
            gh(["label", "create", "watchdog", "--color", "fbca04", "--description", "Started by the watchdog", "--force"])
            body = (f"GitHub did not start **{name}**, due {due:%a %d %b %Y %H:%M} UTC; no run had appeared "
                    f"{GRACE.seconds // 3600} hours later. The watchdog in the Schedule workflow started it now "
                    f"({json.dumps(payload(name, due).get('inputs', {}))}). Check its result in the Actions tab, "
                    "then close this issue.\n\nSee docs/SOP_MANUAL_RUNS.md (watchdog) and docs/WORKFLOWS.md.\n\n"
                    + MARKER.format(key))
            gh(["api", f"repos/{repo}/issues", "-f", f"title=[Watchdog] Started a skipped run: {name} ({due:%d %b %Y})",
                "-f", f"body={body}", "-f", "labels[]=watchdog", "-f", "labels[]=owner:author"])
    return log


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date"); ap.add_argument("--time", default="12:00")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    now = (dt.datetime.combine(dt.date.fromisoformat(a.date), dt.time.fromisoformat(a.time), UTC)
           if a.date else dt.datetime.now(UTC))
    for line in check(now, dry=a.dry_run) or ["watchdog: every timed run is accounted for"]:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
