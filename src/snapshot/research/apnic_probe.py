"""Research probe (schedule item x20-apnic-collector; author's go-ahead 19 Nov 2026): can the
APNIC Labs per-country DNSSEC-validation and RPKI (route origin validation) figures be read
cleanly by a small automated client, and how often are they updated?

APNIC granted written leave on 1 Nov 2026 (ticket 00177078): credit APNIC Labs, and keep the
figures an accurate representation of the source data. This probe only reads public pages:
robots.txt first (if it disallows these paths the probe stops and reads nothing else), then
the two index pages, a handful of country pages, and the first bytes of any linked data file.
About 40 requests at most, two seconds apart, with an identifying User-Agent. If the site
answers 403/429 or asks for a challenge, the probe stops: sites that refuse automated readers
are not worked around.

Writes summary.md (status, content types, data links found, dates seen on the pages, a short
text sample per page) and links.csv. Private: method only.

    python -m snapshot.research.apnic_probe --out DIR
"""
from __future__ import annotations

import argparse
import csv
import re
import time
import urllib.robotparser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

UA = "internet-security-snapshot research (APNIC Labs X20 probe, leave granted ticket 00177078; contact via github.com/pagagne)"
BASE = "https://stats.labs.apnic.net"
INDEX: list[str] = []   # 19 Nov 2026: pages already probed; now only the collector check
COUNTRIES: list[str] = []
DATA_HINT = re.compile(r"json-table\.pl|\.(csv|json|txt|tsv|dat|gz)(\?|$)|download|export|data=|[?&](d|f)=", re.I)
DATE_RX = re.compile(r"\b(20\d\d-\d\d-\d\d|\d{1,2} [A-Z][a-z]{2,8} 20\d\d|[A-Z][a-z]{2,8} \d{1,2},? 20\d\d)\b")
PCT_RX = re.compile(r"\b\d{1,3}(?:\.\d+)?%")
STOP_CODES = {401, 403, 429, 503}


class Stopped(Exception):
    pass


def fetch(sess, url, nbytes=None):
    time.sleep(2.0)
    try:
        r = sess.get(url, timeout=40, stream=True)
    except requests.RequestException as e:
        return {"url": url, "status": type(e).__name__, "ctype": "", "body": ""}
    body = r.raw.read(nbytes, decode_content=True) if nbytes else r.content
    text = body.decode(r.encoding or "utf-8", "replace") if isinstance(body, bytes) else str(body)
    low = text[:4000].lower()
    if r.status_code in STOP_CODES or "captcha" in low or "challenge-platform" in low or "cf-chl" in low:
        raise Stopped(f"{url} answered {r.status_code}{' with a challenge page' if r.status_code == 200 else ''}")
    return {"url": r.url, "status": r.status_code, "ctype": r.headers.get("Content-Type", ""),
            "last_modified": r.headers.get("Last-Modified", ""), "body": text}


def links(page):
    hrefs = re.findall(r"""(?:href|src)\s*=\s*["']([^"'#]+)["']""", page["body"], re.I)
    out = []
    for h in hrefs:
        u = urljoin(page["url"], h)
        if urlparse(u).netloc.endswith("apnic.net"):
            out.append(u)
    return sorted(set(out))


def visible(text):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--start")   # accepted for the research workflow; unused
    ap.add_argument("--end")
    ap.add_argument("--collector", action="store_true", help="also run snapshot.collect.apnic once")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# APNIC Labs probe (X20)", "",
             "Leave granted 1 Nov 2026 (ticket 00177078): credit APNIC Labs; figures as published.", ""]
    rows = []
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA})

    rp = urllib.robotparser.RobotFileParser()
    try:
        r = sess.get(BASE + "/robots.txt", timeout=30)
        lines.append(f"robots.txt: HTTP {r.status_code}")
        if r.ok:
            rp.parse(r.text.splitlines())
            lines += ["```", r.text.strip()[:1500], "```"]
        else:
            rp.parse([])
    except requests.RequestException as e:
        lines.append(f"robots.txt: {type(e).__name__}")
        rp.parse([])
    blocked = [p for p in INDEX if not rp.can_fetch(UA, BASE + p)]
    if blocked:
        lines += ["", f"**Stopped: robots.txt disallows {', '.join(blocked)}. Nothing else read.**"]
        (out / "summary.md").write_text("\n".join(lines) + "\n")
        return 0

    pages, seen_data = [], []
    try:
        targets = [BASE + p for p in INDEX]
        targets += [f"{BASE}/dnssec/{c}" for c in COUNTRIES] + [f"{BASE}/rpki/{c}" for c in COUNTRIES]
        for u in list(targets):
            pass
        for u in targets:
            if not rp.can_fetch(UA, u):
                lines.append(f"- skipped (robots): {u}")
                continue
            pg = fetch(sess, u)
            pages.append(pg)
            (out / (re.sub(r"[^A-Za-z0-9]+", "_", urlparse(u).path).strip("_") + ".html")).write_text(pg["body"])
            for l in links(pg):
                kind = "data" if DATA_HINT.search(l) else "page"
                rows.append({"from": u, "link": l, "kind": kind})
                if kind == "data" and l not in seen_data:
                    seen_data.append(l)
        for l in seen_data[:15]:
            if rp.can_fetch(UA, l):
                pg = fetch(sess, l)
                pg["is_data"] = True
                name = re.sub(r"[^A-Za-z0-9]+", "_", urlparse(l).path.split("/")[-1] + "_" + urlparse(l).query)
                (out / f"{name}.json").write_text(pg["body"])
                pages.append(pg)
    except Stopped as e:
        lines += ["", f"**Stopped: {e}. Not worked around.**"]

    lines += ["", "## Pages read", ""]
    for pg in pages:
        txt = visible(pg["body"]) if "html" in pg.get("ctype", "") else pg["body"]
        dates = sorted(set(DATE_RX.findall(txt)))[:8]
        pcts = PCT_RX.findall(txt)[:8]
        lines.append(f"### {pg['url']}")
        lines.append(f"- HTTP {pg['status']}, {pg.get('ctype','')}, {len(pg['body'])} chars"
                     + (f", Last-Modified {pg['last_modified']}" if pg.get("last_modified") else ""))
        lines.append(f"- dates seen: {', '.join(dates) or 'none'}")
        lines.append(f"- percentages seen (first 8): {', '.join(pcts) or 'none'}")
        lines.append(f"- sample: {txt[:600]!r}")
        if not pg.get("is_data"):
            for m in list(re.finditer(r"json|csv|download", pg["body"], re.I))[:6]:
                lines.append(f"- near '{m.group(0)}': {pg['body'][max(0, m.start()-250):m.end()+250]!r}")
        lines.append("")
    if True:   # 19 Nov 2026: run the collector once (the workflow passes no extra flags)
        from snapshot.collect import apnic
        try:
            for m, t in apnic.fetch().items():
                t.to_csv(out / f"collector_{m}.csv", index=False)
                lines.append(f"Collector check, {m}: {len(t)} countries, window {t.iloc[0]['window_start']}..{t.iloc[0]['window_end']}")
        except Exception as e:  # recorded, not worked around
            lines.append(f"Collector check failed: {type(e).__name__}: {e}")
        lines.append("")
    lines += ["## Data-like links found", ""] + [f"- {l}" for l in seen_data[:60]] + [""]
    lines.append(f"Requests: about {len(pages) + 1}; links recorded {len(rows)}.")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    with open(out / "links.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["from", "link", "kind"])
        w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
