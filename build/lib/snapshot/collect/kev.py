"""CISA Known Exploited Vulnerabilities, from the cisagov/kev-data git repository.

Two things are captured:
- the catalog as of the pull (one row per CVE, with CISA's dateAdded), and
- the first commit in which each CVE appeared, which is when the listing
  actually became public in the repository.

The repository's history starts after the catalog launched (November 2021), so
for older entries first_seen_commit_at is the first commit available and is
flagged as left-censored.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd

from ..util import parse_ts

REPO_URL = "https://github.com/cisagov/kev-data"
CATALOG = "known_exploited_vulnerabilities.json"


def clone(dest: Path) -> str:
    subprocess.run(["git", "clone", "-q", REPO_URL, str(dest)], check=True)
    return _git(dest, "rev-parse", "HEAD").strip()


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def _ids_at(repo: Path, sha: str) -> set[str] | None:
    try:
        raw = _git(repo, "show", f"{sha}:{CATALOG}")
        doc = json.loads(raw)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None
    return {v["cveID"] for v in doc.get("vulnerabilities", [])}


def first_seen(repo: Path) -> pd.DataFrame:
    """First commit time at which each CVE ID appears in the catalog file."""
    log = _git(repo, "log", "--reverse", "--format=%H %cI", "--", CATALOG).split("\n")
    seen: dict[str, tuple[str, bool]] = {}
    first_commit = True
    for line in filter(None, log):
        sha, when = line.split(" ", 1)
        ids = _ids_at(repo, sha)
        if ids is None:
            continue
        for cve in ids:
            if cve not in seen:
                seen[cve] = (when, first_commit)
        first_commit = False
    return pd.DataFrame(
        [{"cve_id": k, "first_seen_commit_at": parse_ts(v[0]), "left_censored": v[1]} for k, v in seen.items()]
    )


def catalog_table(repo: Path) -> pd.DataFrame:
    doc = json.loads((repo / CATALOG).read_text(encoding="utf-8"))
    rows = []
    for v in doc.get("vulnerabilities", []):
        rows.append(
            {
                "cve_id": v.get("cveID"),
                "list": "cisa",
                "vendor": v.get("vendorProject"),
                "product": v.get("product"),
                "date_added": parse_ts(v.get("dateAdded")),
                "due_date": parse_ts(v.get("dueDate")),
                "ransomware_use": v.get("knownRansomwareCampaignUse"),
                "cwes": v.get("cwes", []) or [],
            }
        )
    return pd.DataFrame(rows)


def build_table(repo: Path) -> pd.DataFrame:
    cat = catalog_table(repo)
    fs = first_seen(repo)
    return cat.merge(fs, on="cve_id", how="left")
