"""GreyNoise research-access probe (author, 17 Nov 2026; exploratory X28).

GreyNoise granted Research Community Access on 17 Nov 2026 (non-commercial use, credit "Data provided
by GreyNoise", 90 days of history, unlimited lookups; docs/PERMISSIONS.md). Before any collector is
built, this task finds out what the key actually returns, for the flaws the study cares about: the
CVEs CISA added to its known-exploited list in the last 90 days (at most 25).

Per CVE: the CVE lookup (/v1/cve/{id}: which tier we get, exploitation activity counts, timeline
dates) and the tags for that CVE (/v3/tags?cve=...). Per tag found: its activity series
(/v3/tags/{id}/activity): how many points, which date range, which granularity, which count fields.
Plus one call listing every tag, to count how many tags carry a CVE (the cost of a daily snapshot).

Privacy: IP addresses are never written. Only status codes, field names, dates and counts are kept;
any value that looks like an IP address is dropped before saving. The key is never printed. One
request a second. Output is private (exploratory), in the author's private repository.

    python -m snapshot.research.greynoise_probe --out DIR
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import time
from pathlib import Path

import requests

from snapshot.collect.http import UA

API = "https://api.greynoise.io"
KEV = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
# IPv4, or IPv6 with at least three colons (so clock times such as 01:00:00 are not caught)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b|(?<![\w:])[0-9a-f]{0,4}(?::[0-9a-f]{0,4}){3,7}(?![\w:])", re.I)
PAUSE = 1.0
MAX_CVES = 25
# Tag used in GreyNoise's own example of a 90-day tag page (Martin Awabdeh, 18 Nov 2026)
EXAMPLE_TAG = "214d5217-0870-41f5-891e-f5edb255c3e9"


def range_variants(today: dt.date) -> list[dict]:
    """Parameter sets to try on the tag activity call, to find the 90-day history the website shows
    (18 Nov 2026: plain calls and start/end gave only the last day or two)."""
    d90 = (today - dt.timedelta(days=90)).isoformat()
    t = today.isoformat()
    return [{}, {"days": 90}, {"days": 90, "scope": "greynoise"}, {"days": 90, "granularity": "1d"},
            {"granularity": "1d"}, {"granularity": "24h"},
            {"start_date": d90, "end_date": t}, {"start_date": d90, "end_date": t, "granularity": "1d"},
            {"start_time": d90 + "T00:00:00Z", "end_time": t + "T00:00:00Z"},
            {"from": d90, "to": t}, {"lookback": "90d"}, {"time_window": "90d"}]


def scrub(x):
    """Drop every string that looks like an IP address, and any key that names IPs."""
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items()
                if not re.search(r"(^|_)ips?($|_)|ip_address|source_ip|raw_data", str(k), re.I)
                or re.search(r"count", str(k), re.I)}
    if isinstance(x, list):
        return [scrub(v) for v in x if not (isinstance(v, str) and IP_RE.search(v))]
    if isinstance(x, str) and IP_RE.search(x):
        return "[removed]"
    return x


def call(path: str, key: str, params: dict | None = None) -> tuple[int | None, object]:
    time.sleep(PAUSE)
    try:
        r = requests.get(API + path, params=params, timeout=60,
                         headers={"key": key, "Accept": "application/json", "User-Agent": UA})
    except requests.RequestException as e:
        return None, {"error": type(e).__name__}
    try:
        body = r.json()
    except ValueError:
        body = {"body": "not JSON"}
    if r.status_code != 200:
        msg = body.get("message") if isinstance(body, dict) else None
        return r.status_code, {"error": str(msg or body)[:300]}
    return r.status_code, body


def shape(obj, depth=0):
    """Field names and list lengths, two levels down; no values."""
    if isinstance(obj, dict):
        return {k: (shape(v, depth + 1) if depth < 2 else type(v).__name__) for k, v in obj.items()}
    if isinstance(obj, list):
        return {"list_len": len(obj), "item": shape(obj[0], depth + 1) if obj else None}
    return type(obj).__name__


def series_summary(body) -> dict:
    """Points, date range and count fields of a tag activity reply, whatever its layout."""
    rows = None
    if isinstance(body, list):
        rows = body
    elif isinstance(body, dict):
        for k in ("activity", "data", "results", "timeline", "series", "items"):
            if isinstance(body.get(k), list):
                rows = body[k]
                break
    out = {"shape": shape(scrub(body))}
    # Layout seen on 17 Nov 2026: {"activity": {"malicious": [{"start", "end", "timestamp", ...}]},
    # "aggregations": {"classification": {"malicious": n}}, "metadata": {"granularity",
    # "start_date", "end_date"}}: activity as time windows per classification, not daily counts.
    if isinstance(body, dict) and isinstance(body.get("activity"), dict):
        md = body.get("metadata") or {}
        out["metadata"] = {k: md.get(k) for k in ("granularity", "start_date", "end_date")}
        agg = (body.get("aggregations") or {}).get("classification") or {}
        out["aggregations"] = {k: v for k, v in agg.items() if isinstance(v, (int, float))}
        wins = {}
        for cls, lst in body["activity"].items():
            ws = [(w.get("start"), w.get("end")) for w in (lst or []) if isinstance(w, dict)]
            ws = [(a, b) for a, b in ws if isinstance(a, str)]
            if ws:
                wins[cls] = {"windows": len(ws), "first_start": min(a for a, _ in ws),
                             "last_end": max((b or a) for a, b in ws),
                             "sample": [{"start": a, "end": b} for a, b in sorted(ws)[:5]]}
        out["windows"] = wins
        starts = [w["first_start"] for w in wins.values()]
        out["points"] = sum(w["windows"] for w in wins.values())
        out["first"] = min(starts) if starts else None
        out["last"] = max(w["last_end"] for w in wins.values()) if wins else None
        out["first_day_with_activity"] = out["first"][:10] if out["first"] else None
        return out
    if not rows:
        out["points"] = 0
        return out
    dates, counts = [], {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        for k, v in row.items():
            if isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v) and re.search(r"time|date|day", k, re.I):
                dates.append(v[:19])
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                counts.setdefault(k, []).append(v)
    dates.sort()
    out.update(points=len(rows), first=dates[0] if dates else None, last=dates[-1] if dates else None,
               count_fields={k: {"n": len(v), "sum": sum(v), "max": max(v), "nonzero": sum(1 for x in v if x)}
                             for k, v in counts.items()})
    if len(dates) > 1:
        try:
            d0 = dt.datetime.fromisoformat(dates[0].replace("Z", ""))
            d1 = dt.datetime.fromisoformat(dates[1].replace("Z", ""))
            out["step_hours"] = round((d1 - d0).total_seconds() / 3600, 2)
        except ValueError:
            pass
    first_nonzero = None
    for row in rows:
        if isinstance(row, dict) and any(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
                                         for k, v in row.items() if "count" in k.lower() or k.lower() in ("hits", "value", "ips")):
            ds = [v for k, v in row.items() if isinstance(v, str) and re.match(r"\d{4}-\d{2}-\d{2}", v)]
            if ds:
                first_nonzero = min(ds)[:10] if first_nonzero is None else min(first_nonzero, min(ds)[:10])
    out["first_day_with_activity"] = first_nonzero
    return out


def recent_kev(days: int = 90) -> list[dict]:
    r = requests.get(KEV, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    rows = [v for v in r.json().get("vulnerabilities", []) if v.get("dateAdded", "") >= since]
    rows.sort(key=lambda v: v["dateAdded"], reverse=True)
    return [{"cve": v["cveID"], "kev_date": v["dateAdded"]} for v in rows[:MAX_CVES]]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("GREYNOISE_API_KEY", "")
    if not key:
        (a.out / "summary.md").write_text("GREYNOISE_API_KEY is not set for this run.\n")
        print("greynoise_probe: no key")
        return 1

    res: dict = {"run": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "calls": 0}

    # 0. History depth (author, 18 Nov 2026): which parameters, if any, give the 90 days the website shows
    tests = []
    for p in range_variants(dt.date.today()):
        st0, b0 = call(f"/v3/tags/{EXAMPLE_TAG}/activity", key, p); res["calls"] += 1
        r0 = {"params": p, "status": st0}
        if st0 == 200:
            sm = series_summary(b0)
            r0.update({k: sm.get(k) for k in ("metadata", "points", "first", "last")})
        else:
            r0["error"] = b0.get("error") if isinstance(b0, dict) else None
        tests.append(r0)
    res["range_tests"] = tests

    # 1. Every tag: how many carry a CVE (cost of a daily snapshot)
    st, body = call("/v3/tags", key); res["calls"] += 1
    tags = body.get("tags", []) if isinstance(body, dict) else []
    res["all_tags"] = {"status": st, "tags": len(tags),
                       "with_cve": sum(1 for t in tags if t.get("cves")),
                       "cves_covered": len({c for t in tags for c in (t.get("cves") or [])}),
                       "fields": sorted({k for t in tags[:50] for k in t}),
                       "error": body.get("error") if isinstance(body, dict) else None}
    by_cve: dict[str, list] = {}
    for t in tags:
        for c in t.get("cves") or []:
            by_cve.setdefault(c, []).append({"id": t.get("id"), "slug": t.get("slug"),
                                             "created_at": t.get("created_at"), "intention": t.get("intention")})

    # 2. The flaws CISA listed in the last 90 days
    flaws = recent_kev()
    res["kev_recent"] = len(flaws)
    rows = []
    tried_params = False
    for f in flaws:
        row = dict(f)
        st, cve = call(f"/v1/cve/{f['cve']}", key); res["calls"] += 1
        row["cve_status"] = st
        if st == 200 and isinstance(cve, dict):
            row["cve_tier"] = ("advanced" if "exploitation_activity" in cve else
                               "basic" if "timeline" in cve else "minimal")
            row["exploitation_activity"] = scrub(cve.get("exploitation_activity"))
            row["timeline"] = scrub(cve.get("timeline"))
            row["cve_fields"] = sorted(cve)
        else:
            row["cve_error"] = cve.get("error") if isinstance(cve, dict) else None
        # tags for this CVE (from the full list; one filtered call to confirm the filter works)
        tag_list = by_cve.get(f["cve"], [])
        if not tag_list:
            st2, tb = call("/v3/tags", key, {"cve": f["cve"]}); res["calls"] += 1
            row["tag_filter_status"] = st2
            if isinstance(tb, dict):
                tag_list = [{"id": t.get("id"), "slug": t.get("slug"), "created_at": t.get("created_at"),
                             "intention": t.get("intention")} for t in tb.get("tags", [])]
        row["tags"] = tag_list
        acts = []
        for t in tag_list[:3]:
            st3, act = call(f"/v3/tags/{t['id']}/activity", key); res["calls"] += 1
            s = {"slug": t["slug"], "status": st3}
            s.update(series_summary(act) if st3 == 200 else {"error": act.get("error") if isinstance(act, dict) else None})
            if st3 == 200 and not tried_params:
                # one try at a longer window, to learn whether the activity call takes dates
                p = {"start": (dt.date.today() - dt.timedelta(days=120)).isoformat(), "end": dt.date.today().isoformat()}
                st4, act4 = call(f"/v3/tags/{t['id']}/activity", key, p); res["calls"] += 1
                res["activity_with_dates"] = {"params": p, "status": st4,
                                              **(series_summary(act4) if st4 == 200 else
                                                 {"error": act4.get("error") if isinstance(act4, dict) else None})}
                tried_params = True
            acts.append(s)
        row["activity"] = acts
        rows.append(row)
    res["flaws"] = rows

    seen = [r for r in rows if r["tags"]]
    active = [r for r in rows if (r.get("exploitation_activity") or {}).get("activity_seen")]
    res["totals"] = {"flaws": len(rows), "with_a_tag": len(seen), "activity_seen": len(active)}
    (a.out / "greynoise_probe.json").write_text(json.dumps(scrub(res), indent=1, default=str))

    L = [f"# GreyNoise probe, {res['run']}", "",
         f"Calls: {res['calls']}, one a second. IP addresses never kept.", "",
         f"All tags: status {res['all_tags']['status']}, {res['all_tags']['tags']} tags, "
         f"{res['all_tags']['with_cve']} with a CVE, covering {res['all_tags']['cves_covered']} CVEs.",
         f"Flaws added to CISA's list in the last 90 days (up to {MAX_CVES}): {len(rows)}; "
         f"with a GreyNoise tag: {len(seen)}; GreyNoise activity seen: {len(active)}.", ""]
    L.append(f"History depth, tag {EXAMPLE_TAG} (GreyNoise's own 90-day example):")
    for r0 in res.get("range_tests", []):
        md = r0.get("metadata") or {}
        L.append(f"- params {r0['params'] or '(none)'}: status {r0['status']}"
                 + (f", {r0.get('points')} windows, {r0.get('first')} to {r0.get('last')}; metadata "
                    f"granularity {md.get('granularity')}, {md.get('start_date')} to {md.get('end_date')}"
                    if r0["status"] == 200 else f", {r0.get('error')}"))
    L.append("")
    if "activity_with_dates" in res:
        w = res["activity_with_dates"]
        L.append(f"Activity call with start/end dates: status {w.get('status')}, points {w.get('points')}, "
                 f"{w.get('first')} to {w.get('last')}.")
        L.append("")
    for r in rows:
        acts = "; ".join(f"{x['slug']}: {x.get('status')}, {x.get('points', 0)} points "
                         f"{x.get('first')}..{x.get('last')}, step {x.get('step_hours')} h, "
                         f"first active {x.get('first_day_with_activity')}" for x in r["activity"]) or "no tag"
        L.append(f"- {r['cve']} (KEV {r['kev_date']}): CVE lookup {r.get('cve_status')} "
                 f"({r.get('cve_tier', '-')}); {acts}")
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"greynoise_probe: {res['calls']} calls; {len(seen)} of {len(rows)} flaws tagged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
