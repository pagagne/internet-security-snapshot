"""Checks that every CVE ID recorded in the AI-attack logs is a real CVE record (29 Oct 2026).

Author's decision after TrendAI's "Not only ARTEX" report, which found AI tools inventing
vulnerability identifiers. Applies to exploratory/ai_attack_campaigns.csv and
exploratory/ai_attack_sweeps.csv. The format is checked offline by the tests; existence is
checked here against CVE.org's public record service, so it runs where outside access is
allowed: the Research probe (task cve_check), started by Claude when rows are added and at
each quarterly sweep. Never from Checks (repository only).

  python -m snapshot.cvecheck [--out DIR]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

from .util import _repo_root

LOGS = ["exploratory/ai_attack_campaigns.csv", "exploratory/ai_attack_sweeps.csv"]
CVE = re.compile(r"\bCVE-\d{4}-\d{4,}\b")
API = "https://cveawg.mitre.org/api/cve/{}"


def recorded_ids(root: Path | None = None) -> dict[str, list[str]]:
    """CVE ID -> files and rows it appears in."""
    root = root or _repo_root()
    seen: dict[str, list[str]] = {}
    for rel in LOGS:
        for n, row in enumerate(csv.reader((root / rel).open()), start=1):
            for cid in CVE.findall(" ".join(row)):
                seen.setdefault(cid, []).append(f"{rel}:{n}")
    return seen


def main(argv=None) -> int:
    import requests
    from .collect.http import UA
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the Research workflow
    a = ap.parse_args(argv)
    ids = recorded_ids()
    result, missing = {}, []
    for cid in sorted(ids):
        time.sleep(1.0)
        r = requests.get(API.format(cid), headers={"User-Agent": UA}, timeout=60)
        state = {200: "exists", 404: "NOT FOUND"}.get(r.status_code, f"unknown (HTTP {r.status_code})")
        if r.status_code == 200:
            state = "exists (" + r.json().get("cveMetadata", {}).get("state", "?") + ")"
        result[cid] = {"state": state, "where": ids[cid]}
        if r.status_code == 404:
            missing.append(cid)
    text = json.dumps(result, indent=1)
    print(text)
    if a.out:
        a.out.mkdir(parents=True, exist_ok=True)
        (a.out / "cve_check.json").write_text(text)
    if missing:
        print(f"::error title=CVE check::{len(missing)} recorded CVE ID(s) do not exist: {', '.join(missing)}")
        return 1
    print(f"All {len(result)} recorded CVE IDs exist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
