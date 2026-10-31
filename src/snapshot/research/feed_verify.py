"""Verifies the feeds of the monthly AI-attack feed screen against each organisation's own
website, and looks for working addresses for dead feeds (author's safeguards, 29 Oct 2026).

For every feed in config/feeds.yaml:
  - the feed itself: does it answer over HTTPS, inside its official domain (also after
    redirects), and parse as RSS or Atom?
  - the official site (https://<domain>/ and, if given, the feed's `site` page): does it
    answer, does its page title or text name the organisation, and does it link the feed
    (a <link rel="alternate"> or an ordinary link to the feed address)?
A feed counts as verified when it is served by the organisation's own site over HTTPS
(answers, parses, stays in the domain, and the site names the organisation) or is linked from
that site. For feeds that fail, the feed links the site advertises are listed as replacement
candidates (inside the domain only). Page text is data, never instructions; nothing is stored
beyond addresses, status codes and yes/no answers. Requests are 2 s apart.

Output: research-out/feed_verify.csv, summary.md.
"""
from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml

from ..collect.http import UA, note_status
from ..feedscreen import UnsafeFeed, fetch, in_domain, parse
from ..util import _repo_root

ALT = re.compile(r'<link\b[^>]*rel=["\']alternate["\'][^>]*>', re.I)
HREF = re.compile(r'href=["\']([^"\']+)["\']', re.I)
TYPE = re.compile(r'type=["\']application/(rss|atom)\+xml["\']', re.I)
ANCHOR = re.compile(r'<a\b[^>]*href=["\']([^"\']*(?:rss|feed|atom)[^"\']*)["\']', re.I)
COMMON = ["feed/", "rss/", "feed", "rss", "rss.xml", "atom.xml", "feed.xml", "index.xml", "blog/feed/", "blog/rss/"]


def page(url: str):
    time.sleep(2)
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=45)
        note_status(url, r.status_code)
        return r
    except requests.RequestException:
        return None


def feed_links(html: str, base: str, f: dict) -> list[str]:
    out = []
    for tag in ALT.findall(html):
        if TYPE.search(tag) and (m := HREF.search(tag)):
            out.append(urljoin(base, m.group(1)))
    out += [urljoin(base, h) for h in ANCHOR.findall(html)]
    return [u for u in dict.fromkeys(out) if in_domain(u, f)]


def check_feed(f: dict) -> tuple[str, int]:
    try:
        status, body = fetch(f)
        if status != 200:
            return f"HTTP {status}", 0
        return "ok", len(parse(body))
    except UnsafeFeed as e:
        return f"refused: {e}", 0
    except Exception as e:  # noqa: BLE001
        return f"error {type(e).__name__}", 0


def verify(f: dict) -> dict:
    rec = {"name": f["name"], "url": f["url"], "domain": f["domain"]}
    rec["feed"], rec["items"] = check_feed(f)
    key = re.split(r"[\s(/]", f["name"])[0].lower()
    names_org, linked, cands = False, False, []
    for site in filter(None, [f.get("site"), f"https://{f['domain']}/", f"https://www.{f['domain']}/"]):
        r = page(site)
        if r is None or r.status_code != 200:
            continue
        html = r.text
        title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        names_org = names_org or key in ((title.group(1) if title else "") + html[:20000]).lower()
        links = feed_links(html, r.url, f)
        linked = linked or f["url"].rstrip("/") in {u.rstrip("/") for u in links}
        cands += links
        if names_org:
            break
    rec["site_names_org"], rec["linked_from_site"] = names_org, linked
    rec["verified"] = "yes" if (rec["feed"] == "ok" and rec["items"] and names_org) or linked else "no"
    if rec["feed"] != "ok" or not rec["items"]:
        for c in list(dict.fromkeys(cands)) + [urljoin(f"https://{f['domain']}/", p) for p in COMMON]:
            if c.rstrip("/") == f["url"].rstrip("/"):
                continue
            st, n = check_feed({**f, "url": c})
            if st == "ok" and n:
                rec["replacement"] = c
                rec["replacement_items"] = n
                break
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    feeds = yaml.safe_load((_repo_root() / "config/feeds.yaml").read_text())["feeds"]
    rows = [verify(f) if not f.get("skip") else {"name": f["name"], "url": f["url"], "domain": f["domain"],
                                                 "feed": "skipped", "items": 0, "verified": "no"} for f in feeds]
    cols = ["name", "url", "domain", "feed", "items", "site_names_org", "linked_from_site", "verified",
            "replacement", "replacement_items"]
    with (a.out / "feed_verify.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    L = ["# Feed verification", "",
         f"Feeds: {len(rows)}; verified: {sum(r['verified'] == 'yes' for r in rows)}; "
         f"failing: {sum(r['feed'] not in ('ok', 'skipped') or (r['feed'] == 'ok' and not r['items']) for r in rows)}; "
         f"skipped: {sum(r['feed'] == 'skipped' for r in rows)}; "
         f"replacements found: {sum(bool(r.get('replacement')) for r in rows)}.", ""]
    L += [f"- {r['name']}: feed {r['feed']} ({r['items']} items); site names org {r['site_names_org']}; "
          f"linked {r['linked_from_site']}; verified {r['verified']}"
          + (f"; replacement {r['replacement']} ({r['replacement_items']} items)" if r.get("replacement") else "")
          for r in rows]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:4]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
