"""Quarterly evaluation of a pull's frozen bundle (built into the pull on 1 Nov 2026).

Runs the registered measures the free sources allow (I2, I3 option a, I5 with its NVD count
check, I7, I8; I1, I4, I6 reported as not computable) on the bundle the pull just froze, the same
code as the practice evaluation (snapshot.research.practice_eval). Results are private until the
author's review: the Quarterly pull saves them to the private repository (runs/evaluations/),
whose rebuild then makes the report page, charts and PDF (snapshot.reportpage).

    python -m snapshot.evaluate --bundle DATA/raw/2026Q4/provisional --out DIR
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .research.practice_eval import evaluate, report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bundle", required=True, type=Path)
    ap.add_argument("--private-bundle", type=Path, default=None,
                    help="the bundle's private part (data/private/<quarter>/<run>), e.g. VulnCheck KEV")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    R, ev = evaluate(a.bundle, private=a.private_bundle)
    (a.out / "evaluation.json").write_text(json.dumps(R, indent=1, default=str))
    ev.to_csv(a.out / "events.csv", index=False)
    (a.out / "summary.md").write_text(report(R))
    print(f"evaluation {R['quarter']} ({R['run']}): done")   # counts only in public logs
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
