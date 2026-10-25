"""Research wrapper: one honeypot capture through the Research probe workflow (used to test
the collector before its own workflow is on main)."""
from __future__ import annotations

import argparse
from pathlib import Path

from ..collect import isc_honeypot


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    return isc_honeypot.main(["--out", str(a.out)])


if __name__ == "__main__":
    raise SystemExit(main())
