"""Last-updated dates in document titles (author's request, 11 Nov 2026).

Every study document listed in config/manual.yaml carries the date of its last real change in
its title, for example "# Operations: how the study runs (updated 11 Nov 2026)". The date comes
from git: the most recent commit that changed the file other than its title line (America/New_York
date), or today when the file has uncommitted changes. Documents listed under `undated` in
config/manual.yaml keep their titles (the registered plan, generated files, logs).

    python -m snapshot.docdates stamp      # write the dates
    python -m snapshot.docdates check      # Checks fails if a title's date is out of date

Run with --root on the private repository too; it has its own copy of the manual's documents.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

from .util import _repo_root

STAMP = re.compile(r"\s*\(updated \d{1,2} [A-Z][a-z]{2} \d{4}\)\s*$")
NY = dt.timezone(dt.timedelta(hours=-5))   # date only; a few evening hours of summer time do not matter


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout


def _strip_title(text: str) -> str:
    """The file without its title's date, for comparing versions."""
    lines = text.split("\n")
    i = next((k for k, ln in enumerate(lines) if ln.strip()), None)
    if i is not None and lines[i].startswith("# "):
        lines[i] = STAMP.sub("", lines[i])
    return "\n".join(lines)


def _ny_date(iso: str) -> dt.date:
    return dt.datetime.fromisoformat(iso).astimezone(NY).date()


def last_change(root: Path, rel: str, today: dt.date | None = None) -> dt.date | None:
    """Date of the last change to `rel` other than its title's date."""
    path = root / rel
    try:
        head = _git(root, "show", f"HEAD:{rel}")
    except subprocess.CalledProcessError:
        head = None
    if head is None or _strip_title(head) != _strip_title(path.read_text()):
        return today or dt.datetime.now(NY).date()
    log = _git(root, "log", "--follow", "--format=%H %cI", "--", rel).split("\n")
    prev_text = head
    prev_date = None
    for entry in [e for e in log if e.strip()]:
        sha, iso = entry.split()
        try:
            parent = _git(root, "show", f"{sha}^:{rel}")
        except subprocess.CalledProcessError:
            return _ny_date(iso)            # the commit that created the file
        if _strip_title(parent) != _strip_title(prev_text):
            return _ny_date(iso)
        prev_text, prev_date = parent, iso
    return _ny_date(prev_date) if prev_date else None


def fmt(d: dt.date) -> str:
    return f"{d.day} {d:%b %Y}"


def dated_docs(root: Path, config_root: Path | None = None) -> list[str]:
    """Documents to date: listed in the manual, not `undated`, and tracked by git in `root`
    (the public repository's checkout can hold copies of private files; those are dated in the
    private repository, with --config-root pointing at the public one)."""
    import yaml
    from .manual import CONFIG, expand
    config_root = config_root or root
    cfg = yaml.safe_load((config_root / CONFIG).read_text()) if (config_root / CONFIG).exists() else None
    if cfg is None:
        raise SystemExit(f"no {CONFIG} under {config_root}")
    tracked = set(_git(root, "ls-files").split("\n"))
    skip = cfg.get("undated", {})
    out = []
    for part in cfg["parts"]:
        for rel in expand(config_root, part["docs"]):
            if any(fnmatch.fnmatch(rel, pat) for pat in skip):
                continue
            if rel in tracked and (root / rel).exists():
                out.append(rel)
    return out


def want_title(line: str, d: dt.date) -> str:
    return f"{STAMP.sub('', line)} (updated {fmt(d)})"


def run(root: Path, write: bool, config_root: Path | None = None) -> list[str]:
    problems = []
    for rel in dated_docs(root, config_root):
        path = root / rel
        text = path.read_text()
        lines = text.split("\n")
        i = next((k for k, ln in enumerate(lines) if ln.strip()), None)
        if i is None or not lines[i].startswith("# "):
            problems.append(f"{rel}: no title line (# ...) at the top")
            continue
        d = last_change(root, rel)
        new = want_title(lines[i], d)
        if lines[i] != new:
            if write:
                lines[i] = new
                path.write_text("\n".join(lines))
            problems.append(f"{rel}: {'dated' if write else 'needs'} {fmt(d)}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stamp", "check"])
    ap.add_argument("--root", type=Path, default=None, help="repository whose files are dated")
    ap.add_argument("--config-root", type=Path, default=None, help="repository holding config/manual.yaml")
    a = ap.parse_args(argv)
    root = (a.root or _repo_root()).resolve()
    res = run(root, a.cmd == "stamp", a.config_root.resolve() if a.config_root else None)
    for r in res:
        print(r)
    if a.cmd == "check" and res:
        print("Titles out of date: run  python -m snapshot.docdates stamp", file=sys.stderr)
        return 1
    if a.cmd == "check":
        print("Document dates current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
