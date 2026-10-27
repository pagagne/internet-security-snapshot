"""SANS Internet Storm Center web-honeypot capture (exploratory X14; 25 Oct 2026).

Downloads the two public daily files (https://isc.sans.edu/feeds_doc.html):
  urlcategories.txt  URL <tab> category <tab> details
  urlsummary.txt     URL <tab> first seen <tab> last seen <tab> count
and keeps aggregates only: per (category, details) the number of URLs, total requests and
the earliest first-seen / latest last-seen date; and per CVE ID mentioned in a URL, category
or details, the same. No URL, IP address or host is ever saved.

Credit: SANS Technology Institute, Internet Storm Center, https://isc.sans.edu
Terms: attribution required, no reselling; at most one download an hour (we take one a week).

    python -m snapshot.collect.isc_honeypot --out DIR
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path

import requests

from .http import UA, note_status

CATEGORIES = "https://isc.sans.edu/feeds/urlcategories.txt"
SUMMARY = "https://isc.sans.edu/feeds/urlsummary.txt"
CVE = re.compile(r"CVE-(\d{4})-(\d{4,7})", re.I)
CREDIT = "SANS Technology Institute, Internet Storm Center, https://isc.sans.edu"


def _lines(url: str):
    with requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=600) as r:
        note_status(url, r.status_code)
        r.raise_for_status()
        for raw in r.iter_lines():
            line = raw.decode("utf-8", "replace")
            if line and not line.startswith("#"):
                yield line


def _date(s: str):
    try:
        return dt.date.fromisoformat(s.strip()[:10])
    except ValueError:
        return None


def cves_in(*texts: str) -> set[str]:
    return {f"CVE-{m.group(1)}-{m.group(2)}" for t in texts for m in CVE.finditer(t or "")}


def aggregate(categories, summary) -> tuple[list[dict], list[dict], dict]:
    """categories: iterable of 'url\\tcategory\\tdetails'; summary: 'url\\tfirst\\tlast\\tcount'.
    Returns (rows per category/details, rows per CVE, counts)."""
    cat_of: dict[str, tuple[str, str, frozenset]] = {}
    for line in categories:
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        url, cat, det = parts[0], parts[1].strip(), (parts[2].strip() if len(parts) > 2 else "")
        cat_of[url] = (cat, det, frozenset(cves_in(url, cat, det)))
    by_cat = defaultdict(lambda: {"urls": 0, "requests": 0, "first_seen": None, "last_seen": None})
    by_cve = defaultdict(lambda: {"urls": 0, "requests": 0, "first_seen": None, "last_seen": None})
    n_summary = n_matched = 0
    for line in summary:
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        n_summary += 1
        url = parts[0]
        first, last = _date(parts[1]), _date(parts[2])
        try:
            count = int(parts[3])
        except ValueError:
            count = 0
        hit = cat_of.get(url)
        keys_cve = set(hit[2]) if hit else set()
        keys_cve |= cves_in(url) if not hit else set()
        if hit:
            n_matched += 1
            _add(by_cat[(hit[0], hit[1])], first, last, count)
        for c in keys_cve:
            _add(by_cve[c], first, last, count)
    rows_cat = [{"category": k[0], "details": k[1], **_fmt(v)} for k, v in sorted(by_cat.items())]
    rows_cve = [{"cve": k, **_fmt(v)} for k, v in sorted(by_cve.items())]
    return rows_cat, rows_cve, {"categorised_urls": len(cat_of), "summary_urls": n_summary,
                                "summary_urls_categorised": n_matched}


def _add(acc, first, last, count):
    acc["urls"] += 1
    acc["requests"] += count
    if first and (acc["first_seen"] is None or first < acc["first_seen"]):
        acc["first_seen"] = first
    if last and (acc["last_seen"] is None or last > acc["last_seen"]):
        acc["last_seen"] = last


def _fmt(v):
    return {k: (x.isoformat() if isinstance(x, dt.date) else x) for k, x in v.items()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    rows_cat, rows_cve, counts = aggregate(_lines(CATEGORIES), _lines(SUMMARY))
    for name, rows in (("categories.csv", rows_cat), ("cves.csv", rows_cve)):
        with open(a.out / name, "w", newline="") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader(); w.writerows(rows)
    meta = {"captured_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "credit": CREDIT, "sources": [CATEGORIES, SUMMARY], **counts,
            "categories": len(rows_cat), "cves": len(rows_cve)}
    (a.out / "meta.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
