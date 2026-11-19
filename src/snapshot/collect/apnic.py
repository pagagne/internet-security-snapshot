"""APNIC Labs: per-country DNSSEC validation and RPKI route-origin filtering (exploratory X20).

Written leave granted 1 Nov 2026 (APNIC helpdesk ticket 00177078): credit APNIC Labs, and keep
the figures an accurate representation of the source data. APNIC's own data files also say
"re-use with attribution permitted". Every chart and table built from these figures carries
the line in CREDIT.

Period (author, 19 Nov 2026: the whole quarter, 90 days). DNSSEC: the world-map table for the
90-day window ending on the quarter's last day (one page). The page reads its date setting with
the month one too high (asking for 30/08 returns the window ending 30/09; found 19 Nov 2026), so
the collector asks both ways and keeps only a table whose printed window ends on the quarter's
last day; otherwise it records a gap. RPKI: the world map takes no date or window, so the
per-country time series is read instead (one small file per country, two seconds apart) and the
row dated the quarter's last day kept, with APNIC's 112-day window, the published window nearest
to 90 days (noted with every figure). A quarter not yet over (a dry run) takes the latest data.
Figures are stored exactly as published, with their window dates. Tested 19 Nov 2026 (research task
apnic_probe): no robots.txt, no blocking, both pages served to an identified client. If a page
answers with a block or a challenge, the pull records a gap; it is not worked around.
"""

from __future__ import annotations

import datetime as dt
import re

import pandas as pd

from .http import get

BASE = "https://stats.labs.apnic.net"
PAGES = {"dnssec": "/dnssec", "rpki": "/rpki"}
CREDIT = "Source: APNIC Labs (stats.labs.apnic.net), used with permission; figures as published."

# One table row: ["<a ...>CC</a>","<a ...>Country</a>, <a ...>Region</a>, <a ...>Continent</a>",{v: 99.65, ...}, ..., samples, weight, weighted]
ROW = re.compile(r'^\["<a href=\\"/(?:dnssec|rpki)/(?P<cc>[A-Z0-9]{2})\\">[^"]*?</a>","(?P<place>.*?)",(?P<rest>.*)\],?\s*$')
LINK_TEXT = re.compile(r"<a [^>]*>(.*?)</a>")
VAL = re.compile(r"\{v:\s*(-?[\d.]+)")
WINDOW = re.compile(r"(\d+) day (average|span) \((\d\d)/(\d\d)/(\d{4}) - (\d\d)/(\d\d)/(\d{4})\)")
CHALLENGE = ("captcha", "challenge-platform", "cf-chl", "access denied")

COLUMNS = {"dnssec": ["dnssec_validating_pct", "dnssec_partial_pct", "dnssec_total_pct"],
           "rpki": ["rpki_irov_filtering_pct"]}


def parse(measure: str, html: str) -> pd.DataFrame:
    """The per-country table of one world-map page, as published."""
    low = html[:5000].lower()
    if any(c in low for c in CHALLENGE):
        raise RuntimeError(f"APNIC {measure} page answered with a block or challenge; not worked around")
    w = WINDOW.search(html)
    if not w:
        raise ValueError(f"APNIC {measure}: window dates not found on the page")
    days, kind, d1, m1, y1, d2, m2, y2 = w.groups()
    start, end = dt.date(int(y1), int(m1), int(d1)), dt.date(int(y2), int(m2), int(d2))
    # Only the sortable country table (after its header row) is read, not the map data.
    header = {"dnssec": "'CC', 'Country', 'DNSSEC Validates'", "rpki": "'CC', 'Country', 'I-RoV Filtering'"}[measure]
    at = html.find(header)
    if at < 0:
        raise ValueError(f"APNIC {measure}: country table not found")
    rows = []
    for line in html[at:].splitlines()[1:]:
        line = line.strip()
        if line.startswith("]"):
            break
        m = ROW.match(line)
        if not m:
            continue
        place = LINK_TEXT.findall(m.group("place").replace('\\"', '"'))
        vals = [float(v) for v in VAL.findall(m.group("rest"))]
        tail = re.sub(r"\{[^}]*\}", "", m.group("rest")).strip(", ")
        nums = [t for t in (x.strip() for x in tail.split(",")) if t]
        cols = COLUMNS[measure]
        if len(vals) < len(cols) or len(nums) < 3:
            continue
        rec = {"measure": measure, "cc": m.group("cc"),
               "country": place[0] if place else "", "region": place[1] if len(place) > 1 else "",
               "continent": place[2] if len(place) > 2 else "",
               **dict(zip(cols, vals[:len(cols)])),
               "samples": int(float(nums[0])), "weight": float(nums[1]), "weighted_samples": int(float(nums[2])),
               "window_days": int(days), "window_kind": kind,
               "window_start": start.isoformat(), "window_end": end.isoformat()}
        rows.append(rec)
    if not rows:
        raise ValueError(f"APNIC {measure}: no country rows parsed")
    return pd.DataFrame(rows)


DNSSEC_DAYS = 90
RPKI_WINDOW = "112"   # APNIC's RPKI series offers 7, 14, 28 and 112 days; 112 is nearest to 90
RPKI_JSON = BASE + "/cgi-bin/rpki-json-table.pl"


def _page(path: str, params: dict | None = None) -> str:
    r = get(BASE + path, params=params, headers={"Accept": "text/html"}, pause=2.0)
    r.encoding = r.encoding or "iso-8859-1"
    return r.text


def dnssec(end: dt.date | None) -> pd.DataFrame:
    """The DNSSEC table for the 90 days ending on END (None: the latest 90 days)."""
    if end is None:
        return parse("dnssec", _page(PAGES["dnssec"], {"w": DNSSEC_DAYS}))
    quirk = f"{end.day:02d}/{end.month - 1:02d}/{end.year}" if end.month > 1 else None
    plain = f"{end.day:02d}/{end.month:02d}/{end.year}"
    tried = []
    for d in [x for x in (quirk, plain) if x]:
        df = parse("dnssec", _page(PAGES["dnssec"], {"d": d, "w": DNSSEC_DAYS}))
        got = df.iloc[0]["window_end"]
        tried.append(f"d={d} -> {got}")
        if got == end.isoformat() and int(df.iloc[0]["window_days"]) == DNSSEC_DAYS:
            return df
    raise ValueError(f"APNIC dnssec: no table for the 90 days ending {end} ({'; '.join(tried)})")


def rpki(end: dt.date | None, codes: list[str]) -> pd.DataFrame:
    """Per country, the published 112-day RPKI filtering rate on END (or the latest day)."""
    import requests
    rows, missing = [], []
    for cc in codes:
        try:
            r = get(RPKI_JSON, params={"x": cc}, pause=2.0, tries=2)
            data = r.json().get("data") or []
        except (requests.RequestException, ValueError):
            missing.append(cc)
            continue
        pick = [x for x in data if end is None or x.get("date", "") <= end.isoformat()]
        if not pick:
            missing.append(cc)
            continue
        x = pick[-1]
        w = x.get(RPKI_WINDOW) or {}
        if "filter_rate" not in w:
            missing.append(cc)
            continue
        rows.append({"measure": "rpki", "cc": cc, "rpki_irov_filtering_pct": round(float(w["filter_rate"]), 2),
                     "samples": int(w.get("seen") or 0), "window_days": int(RPKI_WINDOW), "window_kind": "sliding",
                     "window_end": x["date"],
                     "window_start": (dt.date.fromisoformat(x["date"]) - dt.timedelta(days=int(RPKI_WINDOW) - 1)).isoformat(),
                     "note": "APNIC's 112-day window, the published window nearest to 90 days"})
    if not rows:
        raise ValueError("APNIC rpki: no country series read")
    df = pd.DataFrame(rows)
    df.attrs["missing"] = missing
    return df


def fetch(end: dt.date | None = None) -> dict[str, pd.DataFrame]:
    """END: the quarter's last day, or None while the quarter is not over (latest data)."""
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    d = dnssec(end)
    world = parse("rpki", _page(PAGES["rpki"]))       # the country list, with names and regions
    names = world.set_index("cc")[["country", "region", "continent"]]
    r = rpki(end, list(world["cc"]) + ["XA"])
    r = r.join(names, on="cc")
    r.loc[r["cc"] == "XA", ["country", "region", "continent"]] = ["World", "", ""]
    for df in (d, r):
        df["retrieved"] = stamp
    return {"dnssec": d, "rpki": r}
