"""NVD: CVEs published in a date range, with NVD's own scores, CWEs, CPE
products and the CISA KEV date NVD records (cisaExploitAdd).

Primary source: NVD's yearly JSON 2.0 feed files (one download per CVE-ID year, checked
against the published SHA-256). The API is slow and often times out for large windows
(the first test run spent 87 minutes on it), so it is only the fallback, with a time
budget. Uses the NVD_API_KEY secret when present.
"""

from __future__ import annotations

import datetime as dt
import os

import pandas as pd

import gzip
import hashlib
import json
import time

from .http import get

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
FEED = "https://nvd.nist.gov/feeds/json/cve/2.0/nvdcve-2.0-{year}.{ext}"
PAGE = 1000  # NVD allows 2000, but large pages are sometimes cut off mid-response


def _metric(metrics: dict, key: str) -> float | None:
    for m in metrics.get(key, []) or []:
        if m.get("type") == "Primary":
            return (m.get("cvssData") or {}).get("baseScore")
    items = metrics.get(key) or []
    return (items[0].get("cvssData") or {}).get("baseScore") if items else None


def parse(vuln: dict) -> dict:
    c = vuln["cve"]
    cwes = sorted({d["value"] for w in c.get("weaknesses", []) or [] for d in w.get("description", []) if d.get("value", "").startswith("CWE-")})
    products = set()
    for conf in c.get("configurations", []) or []:
        for node in conf.get("nodes", []) or []:
            for m in node.get("cpeMatch", []) or []:
                parts = m.get("criteria", "").split(":")
                if len(parts) > 4 and m.get("vulnerable"):
                    products.add(f"{parts[3]}|{parts[4]}")
    return {
        "cve_id": c["id"],
        "nvd_published": c.get("published"),
        "nvd_last_modified": c.get("lastModified"),
        "nvd_status": c.get("vulnStatus"),
        "nvd_cvss40": _metric(c.get("metrics", {}), "cvssMetricV40"),
        "nvd_cvss31": _metric(c.get("metrics", {}), "cvssMetricV31"),
        "nvd_cwe_ids": cwes,
        "nvd_products": sorted(products),
        "nvd_kev_added": c.get("cisaExploitAdd"),
    }


def _in_window(row: dict, start: dt.date, end: dt.date) -> bool:
    pub = (row.get("nvd_published") or "")[:10]
    return start.isoformat() <= pub <= end.isoformat()


def from_feeds(start: dt.date, end: dt.date, years_back: int = 2) -> tuple[pd.DataFrame, list[str]]:
    """CVEs published in [start, end] from the yearly feeds for CVE-ID years
    start.year - years_back .. end.year. Returns (table, feed versions)."""
    rows, versions = [], []
    for year in range(start.year - years_back, end.year + 1):
        meta = dict(line.split(":", 1) for line in get(FEED.format(year=year, ext="meta"), headers={"Accept": "*/*"}).text.splitlines() if ":" in line)
        raw = gzip.decompress(get(FEED.format(year=year, ext="json.gz"), headers={"Accept": "*/*"}, timeout=600).content)
        if hashlib.sha256(raw).hexdigest().upper() != meta.get("sha256", "").strip().upper():
            raise ValueError(f"NVD feed {year}: checksum mismatch")
        data = json.loads(raw)
        del raw
        rows += [r for r in (parse(v) for v in data.get("vulnerabilities", [])) if _in_window(r, start, end)]
        versions.append(f"{year}@{meta.get('lastModifiedDate', '?').strip()}")
        del data
    df = pd.DataFrame(rows)
    return (df.drop_duplicates("cve_id") if not df.empty else df), versions


def build_table(start: dt.date, end: dt.date, api_key: str | None = None, budget_s: float = 1800) -> pd.DataFrame:
    """API fallback, stopped after budget_s seconds (raises so the gap is recorded)."""
    t0 = time.monotonic()
    key = api_key or os.environ.get("NVD_API_KEY")
    headers = {"apiKey": key} if key else {}
    pause = 0.7 if key else 6.5
    rows = []
    w0 = start
    while w0 <= end:
        w1 = min(end, w0 + dt.timedelta(days=119))
        params = {
            "pubStartDate": f"{w0.isoformat()}T00:00:00.000",
            "pubEndDate": f"{w1.isoformat()}T23:59:59.999",
            "resultsPerPage": PAGE,
            "startIndex": 0,
        }
        total = None
        while total is None or params["startIndex"] < total:
            if time.monotonic() - t0 > budget_s:
                raise TimeoutError(f"NVD API time budget of {budget_s:.0f}s used up at index {params['startIndex']}")
            data = get(URL, params=params, headers=headers, timeout=60, tries=3, pause=pause).json()
            total = data.get("totalResults", 0)
            rows += [parse(v) for v in data.get("vulnerabilities", [])]
            params["startIndex"] += PAGE
        w0 = w1 + dt.timedelta(days=1)
    df = pd.DataFrame(rows)
    return df.drop_duplicates("cve_id") if not df.empty else df
