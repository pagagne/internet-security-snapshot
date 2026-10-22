"""Keeps the hand-drawn diagrams (docs/EVALUATION_FLOW.md, docs/diagrams/) honest.

Each diagram depends on a few files (docs/diagrams/sources.json). `stamp` records a
fingerprint of those files once the diagram has been reviewed; `check` compares and, when
a file has changed since, prints a GitHub warning annotation. It never fails a run.

  python -m snapshot.diagrams check
  python -m snapshot.diagrams stamp [diagram ...]   # after reviewing/updating the diagram
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

from .util import _repo_root

MANIFEST = "docs/diagrams/sources.json"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16] if path.exists() else "missing"


def _load(root: Path) -> dict:
    return json.loads((root / MANIFEST).read_text())


def stale(root: Path | None = None) -> list[tuple[str, str]]:
    """(diagram, changed file) pairs whose fingerprint no longer matches."""
    root = root or _repo_root()
    out = []
    for name, d in _load(root)["diagrams"].items():
        for f in d["depends_on"] + [d["source"]]:
            if d["fingerprints"].get(f) != _sha(root / f):
                out.append((name, f))
    return out


def stamp(names: list[str] | None = None, root: Path | None = None) -> None:
    root = root or _repo_root()
    m = _load(root)
    for name, d in m["diagrams"].items():
        if names and name not in names:
            continue
        d["fingerprints"] = {f: _sha(root / f) for f in d["depends_on"] + [d["source"]]}
        d["reviewed_on"] = dt.date.today().isoformat()
    (root / MANIFEST).write_text(json.dumps(m, indent=1) + "\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["check", "stamp"])
    ap.add_argument("names", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "stamp":
        stamp(a.names or None)
        print("Fingerprints recorded.")
        return 0
    s = stale()
    root = _repo_root()
    docs = {n: d["doc"] for n, d in _load(root)["diagrams"].items()}
    for name, f in s:
        print(f"::warning file={f},title=Diagram may be out of date::{f} changed since the "
              f"'{name}' diagram was last reviewed. Check {docs[name]}, then run "
              f"'python -m snapshot.diagrams stamp {name}'.")
    if not s:
        print("Diagrams: all sources unchanged since last review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
