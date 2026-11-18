"""Save GitHub's run logs and stored outputs to Drive before GitHub deletes them (author's
decision, 18 Nov 2026; risk safeguard R26). GitHub deletes logs and artifacts after 90 days; the
weekly Backup run saves each log once it is 75 days old (a two-week margin), and copies any
quarterly-pull bundle that is not already on Drive. Diagram pictures are rebuilt on every change
and are not kept.

    python -m snapshot.archive logs RUNS.json ARCHIVED.txt     -> run ids to save, one per line
    python -m snapshot.archive artifacts ARTS.json DRIVE_RUNS.txt -> artifact ids to copy
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys

AGE_DAYS = 75
GITHUB_KEEPS = 90


def _age(created: str, now: dt.datetime) -> float:
    t = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
    return (now - t).total_seconds() / 86400


def logs_to_save(runs: list[dict], archived: set[str], now: dt.datetime) -> list[str]:
    """Finished runs between 75 and 90 days old whose log is not yet on Drive."""
    out = []
    for r in runs:
        rid = str(r["id"])
        if rid in archived or r.get("status") != "completed":
            continue
        if AGE_DAYS <= _age(r["created_at"], now) < GITHUB_KEEPS:
            out.append(rid)
    return sorted(out)


def artifacts_to_copy(arts: list[dict], drive_runs: list[str], now: dt.datetime) -> list[str]:
    """Pull bundles (snapshot-<run id>) at least 75 days old with no runs/...-run<id> on Drive."""
    have = {m.group(1) for d in drive_runs for m in [re.search(r"run(\d+)", d)] if m}
    have |= {m.group(1) for d in drive_runs for m in [re.search(r"artifact-(\d+)", d)] if m}
    out = []
    for a in arts:
        m = re.fullmatch(r"snapshot-(\d+)", a.get("name", ""))
        if not m or a.get("expired") or m.group(1) in have:
            continue
        if _age(a["created_at"], now) >= AGE_DAYS:
            out.append(str(a["id"]))
    return sorted(out)


def main(argv=None) -> int:
    a = argv or sys.argv[1:]
    now = dt.datetime.now(dt.timezone.utc)
    items = json.load(open(a[1]))
    other = [l.strip() for l in open(a[2]) if l.strip()]
    if a[0] == "logs":
        ids = {re.match(r"(\d+)", o.rsplit("/", 1)[-1]).group(1) for o in other
               if re.match(r"\d+", o.rsplit("/", 1)[-1])}
        print("\n".join(logs_to_save(items, ids, now)))
    else:
        print("\n".join(artifacts_to_copy(items, other, now)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
