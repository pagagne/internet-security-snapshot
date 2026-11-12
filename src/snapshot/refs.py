"""Single-source references (author's request, 11 Nov 2026: "updating one location updates all
references").

A date or a source's permission status written in a document can be tied to the one place it
is kept, so changing that place changes every copy:

    <!-- date:dry-run -->1 Dec<!-- /date -->              the date of schedule item dry-run
    <!-- date:freeze -->29 Dec 2026<!-- /date -->         with the year when the text shows one
    <!-- date:hand-check-window@1 -->4–28 Jan<!-- /date -->  first occurrence; a span when the
                                                          item lasts several days
    <!-- status:vulncheck -->Granted<!-- /status -->       permission in config/sources.yaml (capital kept)

Dates come from docs/schedule/schedule.yaml, statuses from config/sources.yaml. The marks are
invisible on GitHub and in the manual. `stamp` rewrites the text between the marks; `check`
fails (in the Checks workflow) when any copy no longer matches its source, or names an item that
does not exist (also any "schedule item `id`" written in a document). Records of what happened (INQUIRIES, decisions, session logs) keep the dates
they had at the time and are not marked.

    python -m snapshot.refs stamp
    python -m snapshot.refs check
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

from .util import _repo_root

NAMED = re.compile(r"schedule item `([\w-]+)`")
MARK = re.compile(r"<!-- (date|status):([\w.-]+)(?:@(\d+))? -->(.*?)<!-- /\1 -->")
SKIP_DIRS = ("docs/manual/", "tests/")


def _fmt(d: dt.date, year: bool) -> str:
    return f"{d.day} {d:%b}" + (f" {d.year}" if year else "")


def _span(d: dt.date, days: int, year: bool) -> str:
    if days <= 1:
        return _fmt(d, year)
    e = d + dt.timedelta(days=days - 1)
    if e.month == d.month:
        return f"{d.day}–{_fmt(e, year)}"
    return f"{_fmt(d, year and d.year != e.year)} – {_fmt(e, year)}"


def sources_of(root: Path) -> tuple[dict, dict]:
    from .schedule import expand, load
    occ: dict[str, list[dict]] = {}
    for o in expand(load(root / "docs/schedule/schedule.yaml")):
        occ.setdefault(o["id"], []).append(o)
    src = yaml.safe_load((root / "config/sources.yaml").read_text())["permissioned"]
    return occ, {k: v["permission"] for k, v in src.items()}


def want(kind: str, key: str, nth: str | None, current: str, occ: dict, perm: dict) -> str | None:
    if kind == "status":
        v = perm.get(key)
        return v.capitalize() if v and current[:1].isupper() else v
    items = occ.get(key)
    if not items:
        return None
    i = int(nth or 1) - 1
    if i >= len(items):
        return None
    o = items[i]
    year = bool(re.search(r"\b20\d\d\b", current))
    return _span(o["date"], o["days"], year)


def _files(root: Path) -> list[Path]:
    try:
        rel = subprocess.run(["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True,
                             check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        rel = [p.relative_to(root).as_posix() for p in root.rglob("*.md")]
    out = [root / r for r in rel if not r.startswith(SKIP_DIRS)]
    priv = root / "exploratory"
    if priv.exists():
        out += sorted(p for p in priv.rglob("*.md") if "/sessions/" not in p.as_posix())
    return out


def run(root: Path, write: bool) -> list[str]:
    occ, perm = sources_of(root)
    problems = []
    for path in _files(root):
        text = path.read_text(errors="replace")
        if "<!-- date:" not in text and "<!-- status:" not in text and "schedule item `" not in text:
            continue
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)

        def fix(m: re.Match) -> str:
            kind, key, nth, cur = m.groups()
            new = want(kind, key, nth, cur, occ, perm)
            line = text.count("\n", 0, m.start()) + 1
            if new is None:
                problems.append(f"{rel}:{line}: no {'schedule item' if kind == 'date' else 'source'} "
                                f"'{key}{'@' + nth if nth else ''}'")
                return m.group(0)
            if new != cur:
                problems.append(f"{rel}:{line}: {kind}:{key} says '{cur}', source says '{new}'")
                return m.group(0).replace(f"-->{cur}<!--", f"-->{new}<!--", 1)
            return m.group(0)

        for m in NAMED.finditer(text):
            if m.group(1) not in occ:
                problems.append(f"{rel}:{text.count(chr(10), 0, m.start()) + 1}: no schedule item '{m.group(1)}'")
        new_text = MARK.sub(fix, text)
        if write and new_text != text:
            path.write_text(new_text)
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stamp", "check"])
    a = ap.parse_args(argv)
    res = run(_repo_root(), a.cmd == "stamp")
    for r in res:
        print(r)
    if a.cmd == "check":
        if res:
            print("Written dates or statuses differ from their source: run  python -m snapshot.refs stamp",
                  file=sys.stderr)
            return 1
        print("Every marked date and status matches its source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
