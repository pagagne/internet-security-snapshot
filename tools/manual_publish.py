"""Copies the GitHub edition of "The Snapshot" into a folder for the private manual repository
(author's decision, 30 Oct 2026: the manual is part of the report, so it is not public before
the report; the working documents stay public). Run after `python -m snapshot.manual build`.
Since 31 Oct 2026 the same private repository also holds the exploratory work (exploratory/ and
runs/); this script writes only README.md and docs/, and never touches those.

The folder gets docs/manual/README.md (contents with dropdowns), docs/manual/parts/*.md, the
single-file manual (for download), every picture the manual shows (same paths as here, so the
links work), and a top-level README pointing to the contents.

  python tools/manual_publish.py DEST
"""
from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from snapshot import manual as M  # noqa: E402

PIC = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def main(dest: Path) -> int:
    cfg = M.load(ROOT)
    files = [M.INDEX, cfg["output"]] + sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / M.PARTS_DIR).glob("*.md"))
    pics = set()
    for f in files:
        src = ROOT / f
        for target in PIC.findall(src.read_text()):
            if re.match(r"^[a-z]+:", target):
                continue
            # normpath, not resolve(): ./exploratory is a link into the private checkout
            p = Path(os.path.normpath(src.parent / target))
            if p.is_file() and ROOT in p.parents:
                pics.add(p.relative_to(ROOT).as_posix())
    for f in files + sorted(pics):
        if f.startswith("exploratory/"):
            continue   # already in the private repository, where the sweeps write them
        (dest / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, dest / f)
    (dest / "README.md").write_text(
        "# The Snapshot (private)\n\nThe study manual of the Internet Security Snapshot, kept private until the "
        "report is published (author's decision, 30 Oct 2026). Start at the contents: "
        "[docs/manual/README.md](docs/manual/README.md).\n\nGenerated automatically from the public study "
        "repository by its Manual publish workflow; do not edit here.\n\n"
        "## Exploratory work (private)\n\nSince 31 Oct 2026 this repository also holds every sweep made in addition "
        "to the core data (author's decision): `exploratory/` (the AI-attack log and catalogue, the monthly feed "
        "screens and their spreadsheets, the GitHub and Hugging Face tool sweeps and their charts) and `runs/` (the "
        "raw results of those runs). Nothing in them is published before the report.\n\n"
        "## Go-live draft (private)\n\n[`go-live/README.md`](go-live/README.md): the landing page as it is today plus "
        "the draft of what goes live with the report (author's request, 31 Oct 2026); rebuilt with the manual.\n")
    print(f"{len(files)} manual files and {len(pics)} pictures copied to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
