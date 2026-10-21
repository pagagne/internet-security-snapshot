"""ransomware.live leak-site postings, reduced to aggregate counts at capture.

Terms (docs/PERMISSIONS.md): no raw data is published in any form, victim names are
dropped at capture, and no polling more often than every 30 minutes. This module never
writes a victim name, domain, URL or description to disk: each month's list is reduced
in memory to counts by group, country and sector.

Uses the RANSOMWARE_LIVE_KEY secret (pro API); without it, the free API is used.
"""

from __future__ import annotations

import datetime as dt
import os
import time

import pandas as pd

from .http import get

PRO = "https://api-pro.ransomware.live/victims/"
FREE = "https://api.ransomware.live/v2/victims/{y}/{m:02d}"


def _month_list(year: int, month: int) -> list[dict]:
    key = os.environ.get("RANSOMWARE_LIVE_KEY")
    if key:
        data = get(PRO, params={"year": year, "month": f"{month:02d}"}, headers={"X-API-KEY": key}, timeout=120).json()
        if isinstance(data, dict):
            data = data.get("victims") or data.get("data") or []
        return data
    return get(FREE.format(y=year, m=month), timeout=120).json()


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
