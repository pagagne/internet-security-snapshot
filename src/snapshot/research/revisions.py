"""Research task: revision drift between two quarterly pull runs (author, 23 Nov 2026).

The workflow downloads both runs' public bundles into revisions-old/ and revisions-new/
(client_payload old_run_id and run_id); this finds each bundle (the folder holding
manifest.json) and runs snapshot.revisions on them. Results are saved privately.

    python -m snapshot.research.revisions --out DIR
"""
from __future__ import annotations

import argparse
from pathlib import Path

from snapshot import revisions


def _bundle(root: Path) -> Path:
    found = sorted(root.rglob("manifest.json"))
    if not found:
        raise SystemExit(f"no bundle (manifest.json) under {root}")
    return found[0].parent


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--old", type=Path, default=Path("revisions-old"))
    ap.add_argument("--new", type=Path, default=Path("revisions-new"))
    ap.add_argument("--start")   # accepted for the research workflow; unused
    ap.add_argument("--end")
    a = ap.parse_args(argv)
    return revisions.main([str(_bundle(a.old)), str(_bundle(a.new)), "--out", str(a.out)])


if __name__ == "__main__":
    raise SystemExit(main())
