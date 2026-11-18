"""GreyNoise collector for exploratory X28 (author's decision, 18 Nov 2026: option B).

Research Community Access, granted 17 Nov 2026 (non-commercial use; credit "Data provided by
GreyNoise"; 90 days of history; unlimited lookups). What the 17-18 Nov probes showed: the tag
activity call returns only the last 24 hours, so history must be built up by the study itself;
the tag list carries each tag's creation date; the CVE lookup gives threat IP counts for the last
1, 10 and 30 days and the last-seen time.

Two modes, both writing only to the private repository (exploratory/greynoise/):

- quarterly: one call listing every tag (each CVE's earliest tag creation date = "GreyNoise
  detection date", not proof of first attack) plus one CVE lookup for each flaw CISA added to
  its known-exploited list in the quarter (about 75-100). About 100 requests a quarter.
- weekly (off until GreyNoise agrees to it; asked 18 Nov 2026): one CVE lookup for every CVE
  with a GreyNoise tag (about 3,300), one a second. Keeps the counts in a private rolling window
  of at most six months (older weekly files are deleted) and a permanent per-CVE record of the
  first week activity was seen.

IP addresses and host data are never requested or kept; the key is never printed.

    python -m snapshot.collect.greynoise quarterly --quarter 2026Q4 --out DIR
    python -m snapshot.collect.greynoise weekly --out DIR
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import time
from pathlib import Path

import requests

from .http import UA

API = "https://api.greynoise.io"
KEV = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
PAUSE = 1.0
WINDOW_DAYS = 183           # the private rolling window (about six months)
COUNT_FIELDS = ("threat_ip_count_1d", "threat_ip_count_10d", "threat_ip_count_30d",
                "benign_ip_count_30d")
CVE_COLUMNS = ["cve", "activity_seen", *COUNT_FIELDS, "last_seen", "status"]


def _key() -> str:
    k = os.environ.get("GREYNOISE_API_KEY", "")
    if not k:
        raise SystemExit("GREYNOISE_API_KEY is not set (GitHub secret)")
    return k


def _get(path: str, key: str, params: dict | None = None, pause: float = PAUSE):
    time.sleep(pause)
    try:
        r = requests.get(API + path, params=params, timeout=60,
                         headers={"key": key, "Accept": "application/json", "User-Agent": UA})
    except requests.RequestException as e:
        return None, type(e).__name__
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    try:
        return r.json(), "ok"
    except ValueError:
        return None, "not JSON"


def tag_dates(key: str, get=_get) -> dict[str, dict]:
    """CVE -> earliest tag creation date and number of tags (one call)."""
    body, _ = get("/v3/tags", key)
    out: dict[str, dict] = {}
    for t in (body or {}).get("tags", []):
        for c in t.get("cves") or []:
            d = (t.get("created_at") or "")[:10]
            e = out.setdefault(c, {"tag_first_created": d, "tags": 0})
            e["tags"] += 1
            if d and (not e["tag_first_created"] or d < e["tag_first_created"]):
                e["tag_first_created"] = d
    return out


def cve_row(cve: str, key: str, get=_get) -> dict:
    """Counts and last-seen for one CVE; nothing else from the reply is kept."""
    body, status = get(f"/v1/cve/{cve}", key)
    ea = (body or {}).get("exploitation_activity") or {}
    row = {"cve": cve, "activity_seen": ea.get("activity_seen", ""), "last_seen": ea.get("last_seen", ""),
           "status": status}
    for f in COUNT_FIELDS:
        row[f] = ea.get(f, "")
    return row


def quarter_bounds(q: str) -> tuple[dt.date, dt.date]:
    y, n = int(q[:4]), int(q[-1])
    start = dt.date(y, 3 * (n - 1) + 1, 1)
    end = (dt.date(y + (n == 4), (3 * n) % 12 + 1, 1) - dt.timedelta(days=1))
    return start, end


def kev_added(start: dt.date, end: dt.date) -> list[dict]:
    r = requests.get(KEV, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    rows = [{"cve": v["cveID"], "kev_date": v["dateAdded"]} for v in r.json().get("vulnerabilities", [])
            if start.isoformat() <= v.get("dateAdded", "") <= end.isoformat()]
    return sorted(rows, key=lambda x: (x["kev_date"], x["cve"]))


def quarterly(q: str, out: Path, key: str, get=_get, flaws: list[dict] | None = None) -> dict:
    start, end = quarter_bounds(q)
    flaws = flaws if flaws is not None else kev_added(start, end)
    tags = tag_dates(key, get)
    rows = []
    for f in flaws:
        r = {"cve": f["cve"], "kev_date": f["kev_date"],
             "tag_first_created": tags.get(f["cve"], {}).get("tag_first_created", ""),
             "tags": tags.get(f["cve"], {}).get("tags", 0)}
        r.update(cve_row(f["cve"], key, get))
        rows.append(r)
    out.mkdir(parents=True, exist_ok=True)
    cols = ["cve", "kev_date", "tag_first_created", "tags", *CVE_COLUMNS[1:]]
    with (out / f"quarter-{q}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    tagged = [r for r in rows if r["tags"]]
    before = [r for r in tagged if r["tag_first_created"] and r["tag_first_created"] < r["kev_date"]]
    return {"quarter": q, "flaws": len(rows), "tagged": len(tagged), "tag_before_kev": len(before),
            "activity_seen": sum(1 for r in rows if r["activity_seen"] is True), "calls": len(rows) + 1}


def update_first_seen(first: dict[str, dict], rows: list[dict], day: str) -> int:
    """Record the first sweep at which a CVE showed threat activity in the last 10 days."""
    new = 0
    for r in rows:
        try:
            active = int(r.get("threat_ip_count_10d") or 0) > 0
        except ValueError:
            active = False
        if active and r["cve"] not in first:
            first[r["cve"]] = {"cve": r["cve"], "first_sweep_with_activity": day,
                               "activity_from_or_after": (dt.date.fromisoformat(day) - dt.timedelta(days=10)).isoformat()}
            new += 1
    return new


def prune(weekly_dir: Path, today: dt.date, days: int = WINDOW_DAYS) -> int:
    """Delete weekly files older than the rolling window; returns how many."""
    n = 0
    for p in weekly_dir.glob("*.csv"):
        try:
            if (today - dt.date.fromisoformat(p.stem)).days > days:
                p.unlink(); n += 1
        except ValueError:
            continue
    return n


def weekly(out: Path, key: str, today: dt.date | None = None, get=_get) -> dict:
    today = today or dt.date.today()
    tags = tag_dates(key, get)
    rows = [cve_row(c, key, get) for c in sorted(tags)]
    wdir = out / "weekly"
    wdir.mkdir(parents=True, exist_ok=True)
    with (wdir / f"{today.isoformat()}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CVE_COLUMNS); w.writeheader(); w.writerows(rows)
    fpath = out / "first_seen.csv"
    first: dict[str, dict] = {}
    if fpath.exists():
        with fpath.open() as fh:
            first = {r["cve"]: r for r in csv.DictReader(fh)}
    new = update_first_seen(first, rows, today.isoformat())
    for c, t in tags.items():
        if c in first:
            first[c]["tag_first_created"] = t["tag_first_created"]
    cols = ["cve", "first_sweep_with_activity", "activity_from_or_after", "tag_first_created"]
    with fpath.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        w.writerows(sorted(first.values(), key=lambda r: r["cve"]))
    pruned = prune(wdir, today)
    errors = sum(1 for r in rows if r["status"] != "ok")
    return {"date": today.isoformat(), "cves": len(rows), "errors": errors, "new_first_seen": new,
            "first_seen_total": len(first), "pruned_files": pruned, "calls": len(rows) + 1}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["quarterly", "weekly"])
    ap.add_argument("--quarter")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    key = _key()
    if a.mode == "quarterly":
        if not a.quarter:   # the quarter that just ended
            t = dt.date.today().replace(day=1) - dt.timedelta(days=1)
            a.quarter = f"{t.year}Q{(t.month - 1) // 3 + 1}"
        s = quarterly(a.quarter, a.out, key)
    else:
        s = weekly(a.out, key)
    print("GreyNoise", a.mode + ":", ", ".join(f"{k} {v}" for k, v in s.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
