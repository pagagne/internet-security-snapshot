"""SEC EDGAR: Form 8-K filings reporting a material cybersecurity incident (Item 1.05),
for T6(b), and the registrant count used as the denominator.

The SEC requires a User-Agent naming the requester with a contact email. It is read
from the SEC_USER_AGENT secret (e.g. "Your Name you@example.com"); without it the SEC
refuses requests and this source is recorded as a gap. Company names are not stored.
"""

from __future__ import annotations

import datetime as dt
import os

import pandas as pd

from .http import get

SEARCH = "https://efts.sec.gov/LATEST/search-index"
TICKERS = "https://www.sec.gov/files/company_tickers.json"


def _headers() -> dict:
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua:
        raise RuntimeError("SEC_USER_AGENT not set (the SEC requires a contact User-Agent)")
    return {"User-Agent": ua}


# Two phrasings, unioned: filings cite the item number and/or its title.
QUERIES = ('"Item 1.05"', '"Material Cybersecurity Incidents"')
DIAG: dict = {}


def filings_105(start: dt.date, end: dt.date) -> pd.DataFrame:
    frames = [_search(q, start, end) for q in QUERIES]
    df = pd.concat(frames, ignore_index=True)
    return df.drop_duplicates("accession")


def _search(query: str, start: dt.date, end: dt.date) -> pd.DataFrame:
    rows, offset, total, hits_seen, forms = [], 0, None, 0, {}
    while total is None or offset < total:
        params = {"q": query, "forms": "8-K,8-K/A", "dateRange": "custom",
                  "startdt": start.isoformat(), "enddt": end.isoformat(), "from": offset}
        data = get(SEARCH, params=params, headers=_headers(), pause=0.2).json()
        hits = data["hits"]["hits"]
        total = min(data["hits"]["total"]["value"], 10000)
        for h in hits:
            s = h["_source"]
            hits_seen += 1
            f = s.get("form") or s.get("file_type") or "?"
            forms[f] = forms.get(f, 0) + 1
            items = s.get("items") or []
            if "1.05" not in items:
                continue
            rows.append({
                "accession": s.get("adsh") or h["_id"].split(":")[0],
                "form": s.get("form") or s.get("file_type"),
                "file_date": s.get("file_date"),
                "items": items,
                "cik": (s.get("ciks") or [None])[0],
            })
        if not hits:
            break
        offset += len(hits)
    DIAG[query] = {"total_hits": total, "hits_read": hits_seen, "forms": forms, "with_item_1_05": len(rows)}
    df = pd.DataFrame(rows, columns=["accession", "form", "file_date", "items", "cik"])
    return df.drop_duplicates("accession")


def registrant_count() -> int:
    data = get(TICKERS, headers=_headers()).json()
    return len({v["cik_str"] for v in data.values()})
