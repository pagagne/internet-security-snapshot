"""APNIC Labs: per-country DNSSEC validation and RPKI route-origin filtering (exploratory X20).

Written leave granted 1 Nov 2026 (APNIC helpdesk ticket 00177078): credit APNIC Labs, and keep
the figures an accurate representation of the source data. APNIC's own data files also say
"re-use with attribution permitted". Every chart and table built from these figures carries
the line in CREDIT.

Two public pages are read once per pull, the DNSSEC and the RPKI world maps; each holds the full
per-country table that APNIC publishes for its current window (DNSSEC: a 30-day average; RPKI:
a 7-day span), with region, rates, samples and weights. The figures are stored exactly as
published, with the window dates printed on the page. Tested 19 Nov 2026 (research task
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


def fetch() -> dict[str, pd.DataFrame]:
    out = {}
    for measure, path in PAGES.items():
        r = get(BASE + path, headers={"Accept": "text/html"}, pause=2.0)
        r.encoding = r.encoding or "iso-8859-1"
        df = parse(measure, r.text)
        df["retrieved"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        out[measure] = df
    return out
