"""Fingerprint and archive the primary reports behind the AI-attack log (author's safeguards,
29 Oct 2026).

For every source_url in exploratory/ai_attack_campaigns.csv: download the page (HTTPS, size
capped), record its SHA-256 and size, and ask the Internet Archive's Wayback Machine to save a
copy (or reuse an existing one). The result, research-out/ai_attack_sources.csv, is merged by
Claude into exploratory/ai_attack_sources.csv. If a report is later edited or deleted, the
archived copy shows what was logged. Web pages change in small ways (adverts, counters), so a
changed fingerprint is a prompt to compare the archived copy, not proof of tampering.
Requests are spaced; the page text is never stored.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import time
from pathlib import Path
from urllib.parse import quote

import requests

from ..collect.http import UA
from ..util import _repo_root

MAX = 10_000_000


def fingerprint(url: str) -> tuple[str, str, int]:
    if not url.startswith("https://"):
        return "not https", "", 0
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=60, stream=True)
        body = b""
        for chunk in r.iter_content(65536):
            body += chunk
            if len(body) > MAX:
                return "too large", "", len(body)
        return str(r.status_code), hashlib.sha256(body).hexdigest(), len(body)
    except requests.RequestException as e:
        return f"error {type(e).__name__}", "", 0


def archive(url: str) -> str:
    """An archived copy: the newest existing Wayback snapshot, or a new save."""
    try:
        j = requests.get("https://archive.org/wayback/available", params={"url": url},
                         headers={"User-Agent": UA}, timeout=60).json()
        snap = (j.get("archived_snapshots") or {}).get("closest") or {}
        if snap.get("available") and snap.get("url"):
            return snap["url"].replace("http://", "https://", 1)
        r = requests.get("https://web.archive.org/save/" + quote(url, safe=":/?=&%"),
                         headers={"User-Agent": UA}, timeout=120, allow_redirects=False)
        loc = r.headers.get("Content-Location") or r.headers.get("Location") or ""
        if loc:
            return loc if loc.startswith("http") else "https://web.archive.org" + loc
        return f"save requested (HTTP {r.status_code})"
    except (requests.RequestException, ValueError) as e:
        return f"error {type(e).__name__}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    root = _repo_root()
    urls = sorted({r["source_url"] for r in csv.DictReader((root / "exploratory/ai_attack_campaigns.csv").open())})
    today = dt.date.today().isoformat()
    rows = []
    for u in urls:
        time.sleep(2)
        status, sha, size = fingerprint(u)
        time.sleep(3)
        rows.append({"source_url": u, "checked": today, "http_status": status, "sha256": sha,
                     "bytes": size, "archive_url": archive(u)})
    with (a.out / "ai_attack_sources.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["source_url"])
        w.writeheader()
        w.writerows(rows)
    ok = sum(r["http_status"] == "200" for r in rows)
    arch = sum(r["archive_url"].startswith("https://web.archive.org") for r in rows)
    s = f"# Primary reports fingerprinted and archived\n\nReports: {len(rows)}; fetched: {ok}; archived copies: {arch}\n"
    (a.out / "summary.md").write_text(s)
    print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
