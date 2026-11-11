"""Cross-reference check (author's request, 11 Nov 2026).

Every link from one study document to another must land: the file must exist, and a link to a
section (#anchor) must match a heading or an explicit anchor in that file. Links to the private
repository's files (exploratory/) are checked when its checkout is present. Web links are not
fetched.

    python -m snapshot.links check
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from .util import _repo_root

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ID = re.compile(r'<a\s+(?:id|name)="([^"]+)"')
SKIP_DIRS = ("docs/manual/", "tests/")
PUBLIC_BLOB = "https://github.com/pagagne/internet-security-snapshot/blob/main/"
PRIVATE_BLOB = "https://github.com/pagagne/snapshot-manual/blob/main/"


def slug(heading: str) -> str:
    """GitHub's heading anchor: lower case, punctuation dropped, spaces to hyphens."""
    h = re.sub(r"<[^>]+>", "", heading).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(text: str) -> set[str]:
    out, seen, fence = set(HTML_ID.findall(text)), {}, False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        m = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if m and not fence:
            s = slug(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1)))
            n = seen.get(s, 0)
            out.add(s if n == 0 else f"{s}-{n}")
            seen[s] = n + 1
    return out


def _files(root: Path) -> list[str]:
    try:
        files = subprocess.run(["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True,
                               check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        files = [p.relative_to(root).as_posix() for p in root.rglob("*.md")]
    priv = root / "exploratory"
    if priv.exists():
        files += sorted(p.relative_to(root).as_posix() for p in priv.rglob("*.md")
                        if "/sessions/" not in p.as_posix())
    return [f for f in files if not f.startswith(SKIP_DIRS)]


def check(root: Path) -> list[str]:
    problems, cache = [], {}
    for rel in _files(root):
        text = (root / rel).read_text(errors="replace")
        fence = False
        for n, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
            if fence or line.startswith("    "):
                continue
            for m in LINK.finditer(line):
                target = m.group(2)
                for blob, base in ((PUBLIC_BLOB, root), (PRIVATE_BLOB, root / "exploratory" / "..")):
                    if target.startswith(blob):
                        fpath = target[len(blob):].partition("#")[0]
                        if base.exists() and (blob == PUBLIC_BLOB or (root / "exploratory").exists()) \
                                and fpath and not (base / fpath).exists():
                            problems.append(f"{rel}:{n}: missing file {target}")
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue
                path, _, frag = target.partition("#")
                dest = (root / rel).parent / path if path else root / rel
                try:
                    dest_rel = dest.resolve().relative_to(root.resolve()).as_posix() if path else rel
                except ValueError:   # inside the private checkout (exploratory/ is a link to it)
                    dest_rel = None
                if path and not dest.exists() and dest_rel and dest_rel.startswith("exploratory/") \
                        and not (root / "exploratory").exists():
                    continue   # private files are not in the public checkout (CI)
                if path and not dest.exists():
                    problems.append(f"{rel}:{n}: missing file {path}")
                    continue
                if frag and dest.is_file() and dest.suffix == ".md":
                    key = dest.resolve()
                    if key not in cache:
                        cache[key] = anchors(dest.read_text(errors="replace"))
                    if frag.lower() not in cache[key] and frag not in cache[key]:
                        problems.append(f"{rel}:{n}: no section #{frag} in {dest_rel or path}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check"])
    ap.parse_args(argv)
    res = check(_repo_root())
    for r in res:
        print(r)
    if res:
        print(f"{len(res)} broken cross-references", file=sys.stderr)
        return 1
    print("Every cross-reference lands")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
