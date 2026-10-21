"""EPSS scores (FIRST.org), daily, for the cohort's exploit-likelihood curves.

Primary source: the daily CSV files published by Cyentia for FIRST
(epss_scores-YYYY-MM-DD.csv.gz). Fallback: the FIRST API, one page set per day.
Only CVE IDs from the quarter's year and the year before are kept, which covers every
cohort CVE the quarter can follow while keeping the file small.
"""

from __future__ import annotations

import datetime as dt
import gzip
import io

import pandas as pd

from .http import get

CSV_URL = "https://epss.cyentia.com/epss_scores-{d}.csv.gz"
API_URL = "https://api.first.org/data/v1/epss"


def _keep(df: pd.DataFrame, min_year: int) -> pd.DataFrame:
    years = pd.to_numeric(df["cve"].str.slice(4, 8), errors="coerce")
    return df[years >= min_year]


def day_from_csv(day: dt.date) -> tuple[pd.DataFrame, str]:
    r = get(CSV_URL.format(d=day.isoformat()), headers={"Accept": "*/*"}, timeout=120, tries=2)
    raw = gzip.decompress(r.content).decode()
    first, _, rest = raw.partition("\n")
    model = first.lstrip("#").strip() if first.startswith("#") else ""
    body = rest if first.startswith("#") else raw
    return pd.read_csv(io.StringIO(body)), model


def day_from_api(day: dt.date, page: int = 10000) -> tuple[pd.DataFrame, str]:
    frames, offset, total = [], 0, None
    while total is None or offset < total:
        r = get(API_URL, params={"date": day.isoformat(), "limit": page, "offset": offset}, pause=0.5).json()
        total = int(r.get("total", 0))
        frames.append(pd.DataFrame(r.get("data", [])))
        offset += page
        if not r.get("data"):
            break
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["cve", "epss", "percentile"])
    return df[["cve", "epss", "percentile"]], "api"


def build_table(start: dt.date, end: dt.date, min_year: int, step_days: int = 1, prefer_api: bool = False):
    """Return (table, notes). Days that fail are listed in notes, never filled in."""
    frames, notes, models = [], [], set()
    day = start
    while day <= end:
        try:
            df, model = (day_from_api(day) if prefer_api else day_from_csv(day))
        except Exception as exc:
            try:
                df, model = day_from_api(day)
            except Exception as exc2:
                notes.append(f"{day}: missing ({type(exc).__name__}; API {type(exc2).__name__})")
                day += dt.timedelta(days=step_days)
                continue
        models.add(model)
        df = _keep(df, min_year).copy()
        df["date"] = day
        df["epss"] = df["epss"].astype("float32")
        df["percentile"] = df["percentile"].astype("float32")
        frames.append(df[["cve", "date", "epss", "percentile"]])
        day += dt.timedelta(days=step_days)
    table = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["cve", "date", "epss", "percentile"])
    table["cve"] = table["cve"].astype("category")
    return table, notes, sorted(models)
