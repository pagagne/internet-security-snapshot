"""Research probe (author, 15 Nov 2026): the Wayback Machine part of fixdate_wide, retried slowly.

In fixdate_wide most Wayback CDX lookups failed to connect. This retry asks once every 4 seconds,
waits and tries again after a connection error (10 s, then 30 s), and stops for good after 8
failures in a row (no working around a refusal; any 403 or 429 also stops it). For every CVE
first added to CISA KEV between --start and --end it looks up the first capture with HTTP 200 of
up to three vendor-advisory, patch or release-notes links in the CVE record, and compares it with
today's pre-filled date and the CVE publication date. A capture is an upper bound: the page
existed by then. Private: method only.

    python -m snapshot.research.fixdate_wayback --start 2026-04-01 --end 2026-10-31 --out DIR
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests

from ..fixdates import prefill_exploited
from .fixdate_wide import CDX, REF_TAGS, UA, _d, days
from .prefill_coverage import CVE_RAW, KEV_URL, bucket

PAUSE, BACKOFF, STOP_AFTER = 4.0, (10, 30), 8
stats = {"ok": 0, "no_capture": 0, "error": 0, "stopped": False}
_fail_run = 0


def cdx_first(url: str) -> str:
    global _fail_run
    if stats["stopped"]:
        return ""
    for wait in (0, *BACKOFF):
        time.sleep(wait or PAUSE)
        try:
            r = requests.get(CDX.format(u=quote(url, safe="")), headers={"User-Agent": UA}, timeout=60)
        except requests.RequestException:
            continue
        if r.status_code in (403, 429):
            stats["stopped"] = True
            return ""
        _fail_run = 0
        try:
            j = r.json() if r.ok and r.text.strip() else []
        except ValueError:
            j = []
        if len(j) > 1 and j[1]:
            stats["ok"] += 1
            ts = j[1][0]
            return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
        stats["no_capture"] += 1
        return ""
    stats["error"] += 1
    _fail_run += 1
    if _fail_run >= STOP_AFTER:
        stats["stopped"] = True
    return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-04-01"); ap.add_argument("--end", default="2026-10-31")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    kev = pd.DataFrame(requests.get(KEV_URL, headers={"User-Agent": UA}, timeout=60).json()["vulnerabilities"])
    kev = kev[(kev["dateAdded"] >= a.start) & (kev["dateAdded"] <= a.end)]
    rows = []
    for k in kev.itertuples():
        y, n = k.cveID.split("-")[1:]
        try:
            rec = requests.get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=k.cveID), timeout=40).json()
        except (requests.RequestException, ValueError):
            rec = {}
        cna = (rec.get("containers") or {}).get("cna") or {}
        refs = cna.get("references") or []
        pub = _d((rec.get("cveMetadata") or {}).get("datePublished")) or k.dateAdded
        d0, src, _ = prefill_exploited(k.cveID, [r.get("url", "") for r in refs], k.vendorProject, pub,
                                       _d(cna.get("datePublic")))
        tagged = [r.get("url", "") for r in refs if REF_TAGS & set(r.get("tags") or [])][:3]
        caps = [c for c in (cdx_first(u) for u in tagged) if c]
        g = min(caps) if caps else ""
        base = bucket(src)
        rows.append({"cve_id": k.cveID, "vendor": k.vendorProject, "kev_added": k.dateAdded, "published": pub,
                     "baseline": base, "baseline_date": d0, "tagged_refs": len(tagged), "wayback_first": g,
                     "wb_minus_baseline": days(g, d0) if g else None, "wb_minus_published": days(g, pub) if g else None,
                     "kev_minus_wb": days(k.dateAdded, g) if g else None})
    df = pd.DataFrame(rows)
    df.to_csv(a.out / "fixdate_wayback.csv", index=False)
    has = df["wayback_first"].astype(bool)
    real = ~df["baseline"].isin(["assumed", "CNA disclosure date"])
    wb = df.loc[has, "wb_minus_baseline"]
    L = [f"# Wayback first captures, slow retry: KEV additions {a.start} to {a.end}", "",
         f"Flaws: {len(df)}; with a tagged advisory/patch/release-notes link: {int((df['tagged_refs'] > 0).sum())}; "
         f"with a first capture: {int(has.sum())}.",
         f"Lookups: captured {stats['ok']}, no capture {stats['no_capture']}, failed {stats['error']}; "
         f"stopped early: {'yes' if stats['stopped'] else 'no'}.", "",
         "## Capture against today's pre-filled date (days, capture minus date)", "",
         f"- Real vendor or GitHub date: {int((has & real).sum())} flaws; within 1 day "
         f"{int((has & real & (df['wb_minus_baseline'].abs() <= 1)).sum())}; capture more than 1 day earlier "
         f"{int((has & real & (df['wb_minus_baseline'] < -1)).sum())} (the date may be too late).",
         f"- Disclosure-only or assumed: {int((has & ~real).sum())} flaws; capture more than 1 day earlier than the "
         f"suggested date {int((has & ~real & (df['wb_minus_baseline'] < -1)).sum())}.",
         f"- Median capture minus date: {wb.median() if len(wb) else 'n/a'}.", "",
         "## Does the capture change which side of the line a flaw is on?", "",
         f"- KEV addition before the capture: {int((df['kev_minus_wb'] < 0).sum())}; "
         f"within 7 days after it: {int(df['kev_minus_wb'].between(0, 7).sum())}.", "",
         "Captures are upper bounds and inputs to the hand check, never replacements. Research only."]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"wayback retry: {len(df)} flaws, {stats['ok']} captures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
