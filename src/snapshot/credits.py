"""One credits block for every output (schedule item credits-block, 19 Nov 2026).

Reads config/credits.yaml and prints the same block everywhere: each report page (and so its
PDF), docs/CREDITS.md, the landing page (README, between the credits markers) and, from 4 Dec,
the website. `check` fails if a written copy is out of date, or if a source the pull collects or
that has a permission switch has no credit.

    python -m snapshot.credits build     # rewrite docs/CREDITS.md and the README block
    python -m snapshot.credits check
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .util import _repo_root

ROOT = _repo_root()
CONFIG = ROOT / "config" / "credits.yaml"
DOC = ROOT / "docs" / "CREDITS.md"
README = ROOT / "README.md"
START, END = "<!-- credits:start -->", "<!-- credits:end -->"
PARTS = {"core": "Core data (scored)", "exploratory": "Exploratory measures", "context": "Context"}
# Collector or permission key -> credit key (every collected source must be credited)
REQUIRED = {"kev": "cisa_kev", "cve": "cve_program", "nvd": "nvd", "epss": "epss", "sec": "sec_edgar",
            "radar": "cloudflare_radar", "ransomware": "ransomware_live", "vulncheck": "vulncheck_kev",
            "apnic": "apnic_labs", "ransomware_live": "ransomware_live", "apnic_labs": "apnic_labs"}


def load(path: Path = CONFIG) -> list[dict]:
    items = (yaml.safe_load(path.read_text()) or {}).get("sources") or []
    keys = [s.get("key") for s in items]
    if len(keys) != len(set(keys)):
        raise ValueError("credits.yaml: duplicate key")
    for s in items:
        for f in ("key", "name", "credit", "link", "basis", "part"):
            if not s.get(f):
                raise ValueError(f"credits.yaml: {s.get('key')} has no {f}")
        if s["part"] not in PARTS:
            raise ValueError(f"credits.yaml: {s['key']} part must be one of {sorted(PARTS)}")
    return items


def block_md(items: list[dict] | None = None, heading: str = "## Data sources and credits") -> str:
    items = items if items is not None else load()
    L = [heading, "",
         "The study uses public and permissioned data. Every source whose data it uses is listed here, "
         "credited as its terms or its written permission ask; none of them endorses the study or its findings.", ""]
    for part, title in PARTS.items():
        rows = [s for s in items if s["part"] == part]
        if not rows:
            continue
        L += [f"**{title}**", ""]
        for s in rows:
            line = f"- {s['credit']} <{s['link']}>"
            if s.get("notice"):
                line += f" {s['notice']}"
            if s.get("from"):
                line += f" (figures from {s['from']})"
            L.append(line)
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def doc_md(items: list[dict] | None = None) -> str:
    items = items if items is not None else load()
    L = ["# Data sources and credits", "",
         "Built from `config/credits.yaml` by `python -m snapshot.credits build`; do not edit by hand. "
         "The same block is printed on every report page and its PDF, on the landing page and on the "
         "website. Terms and permissions behind each line: `docs/TERMS_OF_USE.md`, `docs/PERMISSIONS.md`.", "",
         block_md(items, heading="## The block as printed").rstrip(), "",
         "## Why each line is there", ""]
    L += [f"- **{s['name']}**: {s['basis']}." for s in items]
    return "\n".join(L) + "\n"


def _plain(text: str) -> str:
    """The doc without the title's "(updated ...)" stamp, which snapshot.docdates owns."""
    import re
    return re.sub(r"^(# [^\n]*?) \(updated [^)]*\)", r"\1", text, count=1)


def write_doc(items: list[dict] | None = None) -> None:
    new = doc_md(items)
    if DOC.exists() and _plain(DOC.read_text()) == new:
        return                                   # unchanged: keep the stamped title
    DOC.write_text(new)


def readme_with_block(text: str, items: list[dict] | None = None) -> str:
    if START not in text or END not in text:
        return text
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    return head + START + "\n" + block_md(items, heading="### Credits") + END + tail


def problems(items: list[dict] | None = None) -> list[str]:
    from . import pull, sources
    items = items if items is not None else load()
    have = {s["key"] for s in items}
    out = []
    for name in list(pull.PULLERS) + list(sources.load()):
        key = REQUIRED.get(name)
        if key is None and name in sources.load() and sources.load()[name].get("collect"):
            out.append(f"{name}: collected but not mapped to a credit (snapshot.credits.REQUIRED)")
        elif key and key not in have:
            out.append(f"{name}: no credit line ({key}) in config/credits.yaml")
    if not DOC.exists() or _plain(DOC.read_text()) != doc_md(items):
        out.append("docs/CREDITS.md is out of date (run: python -m snapshot.credits build)")
    if README.exists():
        t = README.read_text()
        if START not in t:
            out.append("README.md has no credits block markers")
        elif readme_with_block(t, items) != t:
            out.append("README.md credits block is out of date (run: python -m snapshot.credits build)")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    a = ap.parse_args(argv)
    items = load()
    if a.cmd == "build":
        write_doc(items)
        if README.exists():
            README.write_text(readme_with_block(README.read_text(), items))
        print(f"credits: {len(items)} sources written")
        return 0
    bad = problems(items)
    for b in bad:
        print(b)
    if not bad:
        print(f"credits current: {len(items)} sources, every collected source credited")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
