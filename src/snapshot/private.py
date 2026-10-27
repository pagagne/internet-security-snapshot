"""Keep non-publishable data out of public run outputs (private by design, 27 Oct 2026).

    python -m snapshot.private data/raw data/private

For every source in config/sources.yaml whose `publish` switch is off, moves its folder out of
each bundle under RAW (data/raw/<quarter>/<run>/<pull name>) to the same place under PRIVATE.
The quarterly workflow uploads RAW as the public run download and sends PRIVATE only to the
author's private Google Drive backup. Manifests keep their entries (paths and checksums, no
data), so the private files can still be verified.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from . import sources as switches


def private_pulls() -> set[str]:
    return {s["pull"] for s in switches.load().values() if s.get("pull") and not s["publish"]}


def split(raw: Path, private: Path) -> list[Path]:
    moved = []
    for name in sorted(private_pulls()):
        for src in sorted(raw.glob(f"*/*/{name}")):
            if src.is_dir():
                dest = private / src.relative_to(raw)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
                moved.append(dest)
    return moved


if __name__ == "__main__":
    raw, private = Path(sys.argv[1]), Path(sys.argv[2])
    for p in split(raw, private):
        print(f"[private] {p} (kept out of public outputs)")
    sys.exit(0)
