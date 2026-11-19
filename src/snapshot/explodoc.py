"""The exploratory measures, one section each, for the manual (author, 19 Nov 2026: the details
written into config/exploratory.yaml are descriptive of each X measure and belong in the manual).

Built from config/exploratory.yaml, the single source; the status line keeps the dated note
written beside it in the file. Never contains figures: the file holds methods and decisions only.

    python -m snapshot.explodoc build     # write docs/EXPLORATORY_MEASURES.md
    python -m snapshot.explodoc check     # current?
"""
from __future__ import annotations

import hashlib
import re
import sys

import yaml

from .util import _repo_root

ROOT = _repo_root()
CONFIG = ROOT / "config" / "exploratory.yaml"
DOC = ROOT / "docs" / "EXPLORATORY_MEASURES.md"
SKIP = {"id", "name", "question", "sources", "added", "feeds_labels", "status", "method"}
MARK = "<!-- public-figure -->"
# Lines the privacy scan flags as possible exploratory figures, reviewed by the author on 19 Nov 2026
# and found to be method text only (source names such as "Unit 42", the fixed X25 list of 57
# protocols, a 100-star checking threshold, a sample of up to 100). Each exemption is tied to the
# exact text: if the field changes by one character, the mark falls away and the scan rechecks it.
REVIEWED = {
    ("X3", "sweep"): "4897457e3f85",
    ("X25", "method"): "e22cd2ccd8f5",
    ("X26", "method"): "bccbe4ebf59a",
}


def _fp(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _mark(mid: str, field: str, text: str) -> str:
    return f" {MARK}" if REVIEWED.get((mid, field)) == _fp(text) else ""


def _status_notes(raw: str) -> dict[str, str]:
    """The comment written after each measure's status line (dated decisions)."""
    notes, cur = {}, None
    for line in raw.splitlines():
        m = re.match(r"\s*- id:\s*(X\d+)", line)
        if m:
            cur = m.group(1)
        m = re.match(r"\s*status:\s*\S+\s*#\s*(.+)$", line)
        if m and cur:
            notes[cur] = m.group(1).strip()
    return notes


def _text(v) -> str:
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {_text(x)}" for k, x in v.items())
    return " ".join(str(v).split())


def doc_md() -> str:
    raw = CONFIG.read_text()
    d = yaml.safe_load(raw)
    notes = _status_notes(raw)
    ms = d["measures"]
    L = ["# Exploratory measures X1 to X{}".format(len(ms)), "",
         "Built from `config/exploratory.yaml` by `python -m snapshot.explodoc build`; do not edit by hand. "
         "Exploratory measures are reported beside the registered core and never decide a label "
         "(docs/RESEARCH_PLAN.md). Each section gives the question, its status with the dated note "
         "beside it, the sources and the method as decided; no figures appear here.", "",
         "| Measure | Name | Status |", "|---|---|---|"]
    L += [f"| [{m['id']}](#{m['id'].lower()}) | {m['name']} | {m['status']} |" for m in ms]
    for m in ms:
        L += ["", f"## {m['id']}", "", f"**{m['name']}**", "", f"*Question.* {_text(m['question'])}", "",
              f"*Status.* {m['status']}" + (f": {notes[m['id']]}" if m["id"] in notes else "") + ".",
              "", f"*Added* {m['added']}. *Sources:* {_text(m['sources'])}. "
              f"*Decides a label:* {'yes' if m.get('feeds_labels') else 'no'}."]
        if m.get("method"):
            t = _text(m["method"])
            L += ["", f"*Method.* {t}{_mark(m['id'], 'method', t)}"]
        for k, v in m.items():
            if k not in SKIP:
                t = _text(v)
                L += ["", f"*{k.replace('_', ' ').capitalize()}.* {t}{_mark(m['id'], k, t)}"]
    return "\n".join(L) + "\n"


def _plain(text: str) -> str:
    return re.sub(r"^(# [^\n]*?) \(updated [^)]*\)", r"\1", text, count=1)


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    new = doc_md()
    if cmd == "build":
        if not DOC.exists() or _plain(DOC.read_text()) != _plain(new):
            DOC.write_text(new)
        print("docs/EXPLORATORY_MEASURES.md written")
        return 0
    ok = DOC.exists() and _plain(DOC.read_text()) == _plain(new)
    print("exploratory measures current" if ok else
          "docs/EXPLORATORY_MEASURES.md out of date (run: python -m snapshot.explodoc build)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
