"""Pre-filled fix dates for the review list. The author confirms or corrects each one.

Tried in order, using the CVE record's own links:
1. GitHub release tag link  -> the release's publish date
2. GitHub security advisory -> the advisory's publish date
3. GitHub commit link       -> the commit date
4. Otherwise                -> the CVE publication date, marked as an assumption
   (vendors usually publish the fix and the CVE together under coordinated disclosure)

Only GitHub's public API is queried (with GITHUB_TOKEN when set). Every pre-fill names
its source so the author can check it in one click.
"""

from __future__ import annotations

import os
import re
from functools import lru_cache

import requests

API = "https://api.github.com"
RELEASE = re.compile(r"github\.com/([^/]+)/([^/]+)/releases/tag/([^\s?#]+)")
ADVISORY = re.compile(r"github\.com/([^/]+)/([^/]+)/security/advisories/(GHSA-[\w-]+)")
COMMIT = re.compile(r"github\.com/([^/]+)/([^/]+)/commit/([0-9a-f]{7,40})")


@lru_cache(maxsize=2048)
def _get(path: str) -> dict | None:
    h = {"Accept": "application/vnd.github+json", "User-Agent": "internet-security-snapshot"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        r = requests.get(API + path, headers=h, timeout=30)
        return r.json() if r.ok else None
    except requests.RequestException:
        return None


def prefill(links: list[str], cve_published: str) -> tuple[str, str]:
    """Return (YYYY-MM-DD, source note)."""
    for url in links:
        if m := RELEASE.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/releases/tags/{m[3]}")
            if d and d.get("published_at"):
                return d["published_at"][:10], f"GitHub release {m[3]}"
        if m := ADVISORY.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/security-advisories/{m[3]}")
            if d and d.get("published_at"):
                return d["published_at"][:10], f"GitHub advisory {m[3]}"
        if m := COMMIT.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/commits/{m[3]}")
            date = ((d or {}).get("commit") or {}).get("committer", {}).get("date")
            if date:
                return date[:10], f"fix commit {m[3][:10]} (fix may ship later in a release)"
    return cve_published[:10], "ASSUMED same day as CVE publication; check the advisory link"
