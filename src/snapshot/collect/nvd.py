"""NVD API 2.0: CVEs published in a date range, with NVD's own scores, CWEs, CPE
products and the CISA KEV date NVD records (cisaExploitAdd).

Uses the NVD_API_KEY secret when present (50 requests / 30 s), else the public rate.
Windows are split to NVD's 120-day maximum.
"""

from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from .http import get

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
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


def build_table(start: dt.date, end: dt.date, api_key: str | None = None) -> pd.DataFrame:
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
            data = get(URL, params=params, headers=headers, timeout=120, pause=pause).json()
            total = data.get("totalResults", 0)
            rows += [parse(v) for v in data.get("vulnerabilities", [])]
            params["startIndex"] += PAGE
        w0 = w1 + dt.timedelta(days=1)
    df = pd.DataFrame(rows)
    return df.drop_duplicates("cve_id") if not df.empty else df
