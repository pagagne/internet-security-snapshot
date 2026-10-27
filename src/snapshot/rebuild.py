"""Rebuild check: can a run's figures be recomputed from its frozen bundle?

    python -m snapshot.rebuild data/raw/2026Q4/final

Run inside the pinned container (Dockerfile) by .github/workflows/rebuild-check.yml on a
schedule, against the most recent frozen bundle. Three checks:

1. Frozen data: every file listed in manifest.json still has its recorded SHA-256.
2. Data quality report: recomputed from the bundle and compared with the bundle's own
   quality.json (numbers at reporting precision; the drift flags, which depend on the
   previous run, are left out).
3. Published figures: when the bundle holds figures.json (written by the evaluation step),
   they are recomputed with snapshot.evaluate and compared at reporting precision.

Exit status 1 if anything differs, so the scheduled job fails visibly. The target is
identical published figures, not identical bytes: floating-point results and file
metadata can vary in the last digits (docs/STATISTICAL_REVIEW_2026-10-24.md, point 8).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from .util import sha256_file

DECIMALS = 6               # reporting precision for comparisons
SKIP_KEYS = {"drift_flags"}


def verify_files(bundle: Path) -> list[str]:
    man = bundle / "manifest.json"
    if not man.exists():
        return ["manifest.json missing"]
    problems = []
    for e in json.loads(man.read_text()).get("files", []):
        rel, want = e.get("file_path"), e.get("sha256")
        if not rel or not want or e.get("kept_privately"):
            continue   # private files are kept in the author's Drive backup, not the public bundle
        p = bundle / rel
        if not p.exists():
            problems.append(f"{rel}: missing")
        elif sha256_file(p) != want:
            problems.append(f"{rel}: checksum differs from the manifest")
    return problems


def _norm(x):
    if isinstance(x, float):
        return round(x, DECIMALS)
    if isinstance(x, dict):
        return {k: _norm(v) for k, v in x.items() if k not in SKIP_KEYS}
    if isinstance(x, (list, tuple)):
        return [_norm(v) for v in x]
    return x


def diff(a, b, path: str = "") -> list[str]:
    """Differences between two JSON-like values after rounding, as readable paths."""
    a, b = _norm(a), _norm(b)
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}/{k}: only in {'published' if k in a else 'recomputed'}")
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, f"{path}[{i}]")]
    return [] if a == b else [f"{path or '/'}: published {a!r}, recomputed {b!r}"]


def check_quality(bundle: Path) -> list[str]:
    from .quality import build
    pub = bundle / "quality.json"
    if not pub.exists():
        return []
    _, metrics = build(bundle)
    recomputed = json.loads(json.dumps(metrics, default=str))
    return [f"quality.json {d}" for d in diff(json.loads(pub.read_text()), recomputed)]


def check_figures(bundle: Path) -> tuple[list[str], str]:
    pub = bundle / "figures.json"
    if not pub.exists():
        return [], "no figures.json in this bundle yet (evaluation step not built)"
    if importlib.util.find_spec("snapshot.evaluate") is None:
        return ["figures.json present but snapshot.evaluate is not installed"], ""
    from . import evaluate  # type: ignore[attr-defined]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "figures.json"
        evaluate.main([str(bundle), "--out", str(out)])
        return [f"figures.json {d}" for d in diff(json.loads(pub.read_text()), json.loads(out.read_text()))], ""


def run(bundle: Path) -> tuple[list[str], list[str]]:
    problems, notes = verify_files(bundle), []
    problems += check_quality(bundle)
    figs, note = check_figures(bundle)
    problems += figs
    if note:
        notes.append(note)
    return problems, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundles", nargs="+", type=Path)
    a = ap.parse_args(argv)
    failed = False
    for b in a.bundles:
        problems, notes = run(b)
        print(f"## Rebuild check: {b}\n")
        print("\n".join(f"- {p}" for p in problems) if problems else "- Frozen files and recomputed figures match.")
        for n in notes:
            print(f"- Note: {n}")
        print()
        failed |= bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
