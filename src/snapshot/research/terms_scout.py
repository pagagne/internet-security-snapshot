"""Research probe (29 Oct 2026): find a source's terms-of-use page from its home page.

Fetches each home page, lists the links whose text or address mentions a site policy, terms,
copyright or reuse (English and Japanese words), then fetches those pages and saves short
samples. Used first for JPCERT/CC (X19), whose policy addresses tried on 28 Oct returned 404.
Nothing here feeds any measure. Requests are 1 s apart and name the study.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

from ..collect.http import UA, note_status
from .source_scout import scrub

HOMES = {
    "jpcert_ja": "https://www.jpcert.or.jp/",
    "jpcert_en": "https://www.jpcert.or.jp/english/",
    "apnic_labs": "https://labs.apnic.net/",
}
WORDS = re.compile(r"policy|terms|copyright|legal|reuse|license|licence|ポリシー|規約|著作権|利用|サイトについて|免責", re.I)
LINK = re.compile(r"<a\s[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)


def get(url: str):
    r = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"}, timeout=60)
    note_status(url, r.status_code)
    r.encoding = r.apparent_encoding or r.encoding
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    summary: dict = {}
    for name, home in HOMES.items():
        time.sleep(1.0)
        try:
            r = get(home)
        except Exception as e:  # noqa: BLE001
            summary[name] = {"home": home, "error": repr(e)[:200]}
            continue
        links = []
        for href, text in LINK.findall(r.text):
            label = re.sub(r"<[^>]+>|\s+", " ", text).strip()
            if WORDS.search(label) or WORDS.search(href):
                links.append({"text": label[:80], "url": urljoin(home, href)})
        seen, pages = set(), []
        for l in links:
            if l["url"] in seen or not l["url"].startswith("http"):
                continue
            seen.add(l["url"])
            time.sleep(1.0)
            try:
                p = get(l["url"])
                body = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", p.text, flags=re.S | re.I)
                body = re.sub(r"\s+", " ", body)
                fname = f"{name}_{len(pages)}.txt"
                (a.out / fname).write_text(scrub(body[:12000]))
                pages.append({**l, "status": p.status_code, "sample": fname})
            except Exception as e:  # noqa: BLE001
                pages.append({**l, "error": repr(e)[:200]})
            if len(pages) >= 6:
                break
        summary[name] = {"home": home, "status": r.status_code, "links": links[:20], "pages": pages}
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1, ensure_ascii=False)[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
