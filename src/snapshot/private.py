"""Keep non-publishable data out of public run outputs (private by design, 27 Oct 2026).

    python -m snapshot.private data/raw data/private

For every source in config/sources.yaml whose `publish` switch is off, moves its folder out of
each bundle under RAW (data/raw/<quarter>/<run>/<pull name>) to the same place under PRIVATE.
The quarterly workflow uploads RAW as the public run download and sends PRIVATE only to the
author's private Google Drive backup. Manifests keep their entries (paths and checksums, no
data), so the private files can still be verified.
"""
from __future__ import annotations

import json
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
                _mark(src.parent, name)
    return moved


def _mark(bundle: Path, name: str) -> None:
    """Mark the moved files in the bundle's manifest as kept privately, so the rebuild check
    knows they are absent on purpose (checksums stay, for checking the private copy)."""
    man = bundle / "manifest.json"
    if not man.exists():
        return
    doc = json.loads(man.read_text())
    for e in doc.get("files", []):
        if (e.get("file_path") or "").startswith(f"{name}/"):
            e["kept_privately"] = True
    man.write_text(json.dumps(doc, indent=2) + "\n")


if __name__ == "__main__":
    raw, private = Path(sys.argv[1]), Path(sys.argv[2])
    for p in split(raw, private):
        print(f"[private] {p} (kept out of public outputs)")
    sys.exit(0)
