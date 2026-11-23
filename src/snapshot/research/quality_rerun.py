"""Research task: rerun the data-quality report on a quarterly pull run's frozen public bundle
(run zero fix, 23 Nov 2026). The workflow downloads the bundle of client_payload.run_id into
practice-bundle/; this runs snapshot.quality on it and writes quality.md and quality.json.
Public: the same report a pull publishes in its run report.

    python -m snapshot.research.quality_rerun --out DIR
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from snapshot import quality


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--bundles", type=Path, default=Path("practice-bundle"))
    ap.add_argument("--start")
    ap.add_argument("--end")
    a = ap.parse_args(argv)
    found = sorted(a.bundles.rglob("manifest.json"))
    if not found:
        raise SystemExit(f"no bundle under {a.bundles}")
    a.out.mkdir(parents=True, exist_ok=True)
    for m in found:
        b = m.parent
        quality.main([str(b), "--hold-issue", str(a.out / f"hold-{b.name}.json")])
        for f in ("quality.md", "quality.json"):
            shutil.copy(b / f, a.out / f"{b.parent.name}-{b.name}-{f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
