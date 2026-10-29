"""Privacy scan: keeps private information out of the public repository (27 Oct 2026).

    python -m snapshot.privacy                 # the checked-out tree
    python -m snapshot.privacy --ref run-reports   # any branch or commit

Looks in every text file for things that must never be public (docs/OPERATIONS.md, "Private
by design"): keys and tokens, private keys, personal email addresses and phone numbers that
are not on the allow list, and figures from sources whose `publish` switch is off
(config/sources.yaml; today ransomware.live counts). Prints each finding as file:line and kind
(never the matched value in full) and exits 1 if there is any.

Runs on every push (Checks), daily on main and run-reports (Schedule), and in each sync review.
Allow-listed values are public addresses of organisations, kept in ALLOW below with a reason.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from . import sources as switches

PATTERNS = {
    "google client secret": r"GOCSPX-[A-Za-z0-9_-]{10,}",
    "google token": r"ya29\.[A-Za-z0-9_-]{20,}|\b1//0[A-Za-z0-9_-]{20,}",
    "github token": r"\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}",
    "aws key": r"\bAKIA[0-9A-Z]{16}\b",
    "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "oauth token field": r"\"(?:refresh_token|access_token)\"\s*:\s*\"[^\"]{10,}",
    "api key field": r"(?i)\b(?:api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]",
    "email address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone number": r"(?:\+1[ -]?)?\(\d{3}\)[ .-]?\d{3}[ .-]\d{4}\b|\+\d{1,3}[ .-]\d{2,4}[ .-]\d{3,4}[ .-]\d{3,4}\b",
}
# Figures from sources that may not be published yet (publish switch off).
PRIVATE_FIGURES = {
    "ransomware_live": r"monthly totals \[|'month': '\d{4}-\d{2}', 'count': \d+|\d[\d,]* postings, \d+ groups",
}
ALLOW = {
    # public addresses of organisations or services, not private individuals
    "noreply@anthropic.com": "commit attribution",
    "41898282+github-actions[bot]@users.noreply.github.com": "GitHub bot",
    "community@vulncheck.com": "VulnCheck's public request address",
    "contact@shadowserver.org": "Shadowserver's public contact address",
    "research-access-request@censys.com": "Censys's public research-access address",
    "psirt@cisco.com": "Cisco's public security address (vendor advisory sample)",
    "(706) 542-3375": "UGA Career Center employer-relations office line (public)",
    "internetsecuritysnapshot@gmail.com": "the study's own public contact address (created 29 Oct 2026)",
}
SKIP_SUFFIX = (".png", ".jpg", ".svg", ".ico", ".pdf", ".zip", ".parquet", ".gz", ".bundle", ".lock")
SKIP_PATHS = ("src/snapshot/privacy.py", "tests/test_privacy.py")


def _files(ref: str | None) -> list[tuple[str, str]]:
    if ref:
        names = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref], capture_output=True,
                               text=True, check=True).stdout.split("\n")
        read = lambda n: subprocess.run(["git", "show", f"{ref}:{n}"], capture_output=True,
                                        text=True, errors="replace").stdout
    else:
        try:
            names = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                                   check=True).stdout.split("\n")
        except (OSError, subprocess.CalledProcessError):
            # no git (e.g. inside the analysis container): every file under the current folder
            names = [p.as_posix() for p in Path(".").rglob("*")
                     if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts]
        read = lambda n: Path(n).read_text(errors="replace") if Path(n).is_file() else ""
    return [(n, read(n)) for n in names if n and not n.endswith(SKIP_SUFFIX) and n not in SKIP_PATHS]


def _allowed(kind: str, value: str) -> bool:
    if value in ALLOW:
        return True
    if kind == "email address":
        v = value.lower()
        return v.endswith(("@example.com", "@example.org", ".noreply.github.com", "@users.noreply.github.com"))
    return False


def scan_text(name: str, text: str) -> list[tuple[str, int, str]]:
    found = []
    pats = dict(PATTERNS)
    for key, s in switches.load().items():
        if not s["publish"] and key in PRIVATE_FIGURES:
            pats[f"{s['name']} figures (not yet publishable)"] = PRIVATE_FIGURES[key]
    for kind, pat in pats.items():
        for m in re.finditer(pat, text):
            if _allowed(kind, m.group(0)):
                continue
            line = text.count("\n", 0, m.start()) + 1
            found.append((name, line, kind))
    return found


def scan(ref: str | None = None) -> list[tuple[str, int, str]]:
    out = []
    for name, text in _files(ref):
        out += scan_text(name, text)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", help="branch or commit to scan (default: the checked-out files)")
    a = ap.parse_args(argv)
    hits = scan(a.ref)
    where = a.ref or "working tree"
    if not hits:
        print(f"Privacy scan ({where}): nothing private found.")
        return 0
    print(f"Privacy scan ({where}): {len(hits)} finding(s)")
    for name, line, kind in hits:
        print(f"- {name}:{line}: {kind}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
