"""ransomware.live leak-site postings, reduced to aggregate counts at capture.

Permission granted 27 Oct 2026 (ticket #3425; conditions in docs/PERMISSIONS.md): the
dedicated api-pro endpoint with the author's personal token only; fair usage (and the study's
own rule: no polling more often than every 30 minutes); ransomware.live named as the source
wherever its data appears; no raw data published in any form. This module never writes a
victim name, domain, URL or description to disk: each month's list is reduced in memory to
counts by group, country and sector.

Needs the RANSOMWARE_LIVE_KEY secret; without it the pull records a gap (no free-API fallback:
condition 1).
"""

from __future__ import annotations

import datetime as dt
import os
import time

import pandas as pd

from .http import get

PRO = "https://api-pro.ransomware.live/victims/"
CREDIT = "Source: ransomware.live (https://www.ransomware.live), used with permission"


def _month_list(year: int, month: int) -> list[dict]:
    key = os.environ.get("RANSOMWARE_LIVE_KEY")
    if not key:
        raise RuntimeError("RANSOMWARE_LIVE_KEY not set: ransomware.live allows only its api-pro endpoint "
                           "with a personal token (condition 1, docs/PERMISSIONS.md)")
    data = get(PRO, params={"year": year, "month": f"{month:02d}"}, headers={"X-API-KEY": key}, timeout=120).json()
    if isinstance(data, dict):
        data = data.get("victims") or data.get("data") or []
    return data


def aggregate(victims: list[dict], year: int, month: int) -> pd.DataFrame:
    """Counts only. Duplicate postings of the same victim by the same group count once."""
    seen, rows = set(), []
    for v in victims:
        key = ((v.get("victim") or v.get("post_title") or "").strip().lower(), (v.get("group") or v.get("group_name") or "").lower())
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "group": key[1] or "unknown",
            "country": (v.get("country") or "unknown").upper() or "UNKNOWN",
            "sector": v.get("activity") or v.get("sector") or "unknown",
        })
    del seen, victims
    df = pd.DataFrame(rows, columns=["group", "country", "sector"])
    out = []
    for dim in ("all", "group", "country", "sector"):
        if dim == "all":
            out.append(pd.DataFrame([{"dimension": "all", "value": "all", "count": len(df)}]))
        else:
            c = df.groupby(dim).size().reset_index(name="count").rename(columns={dim: "value"})
            c.insert(0, "dimension", dim)
            out.append(c)
    agg = pd.concat(out, ignore_index=True)
    agg.insert(0, "month", f"{year}-{month:02d}")
    return agg


def build_table(months: list[tuple[int, int]], pause: float = 5.0) -> pd.DataFrame:
    frames = []
    for i, (y, m) in enumerate(months):
        if i:
            time.sleep(pause)
        frames.append(aggregate(_month_list(y, m), y, m))
    return pd.concat(frames, ignore_index=True)
