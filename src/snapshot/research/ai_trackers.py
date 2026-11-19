"""One-time fetch of two outside AI-hacking trackers (author's decisions, 18 Nov 2026; exploratory).

1. hackingincidents.ai: the whole ledger (incidents.json and sources.json), published under the
   MIT licence of its maintainer's Substrate repository. Used once to check the coverage of the
   private AI-attack log; leads graded CONFIRMED or STRONG only; every missing case is entered
   in the log only from its own primary report, never from this file.
2. offsecharnesses.ai: its front, about, data and method pages (text only, for Claude to read
   the terms), plus any JSON or CSV file its data page links to. The comparison with the GitHub
   tool sweep happens only if those terms allow it.

robots.txt is honoured: a page it disallows is skipped and noted. One request a second. Output
is private (exploratory), in the author's private repository.

    python -m snapshot.research.ai_trackers --out DIR
"""
from __future__ import annotations

import argparse
import html
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests

from snapshot.collect.http import UA

INCIDENTS = "https://hackingincidents.ai/"
HARNESSES = "https://offsecharnesses.ai/"
PAGES = ["", "about/", "data/", "method/"]
PAUSE = 1.0


def text_of(page: str) -> str:
    """Readable text of an HTML page: scripts and styles dropped, tags removed, spaces folded."""
    page = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", page)
    page = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", page)
    page = html.unescape(re.sub(r"<[^>]+>", " ", page))
    return "\n".join(re.sub(r"[ \t]+", " ", ln).strip() for ln in page.splitlines() if ln.strip())


def data_links(base: str, page: str) -> list[str]:
    """Links on a page to JSON or CSV files on the same site."""
    host = urlparse(base).netloc
    out = []
    for href in re.findall(r'href="([^"]+)"', page):
        u = urljoin(base, href)
        if urlparse(u).netloc == host and re.search(r"\.(json|csv)(\?|$)", u, re.I) and u not in out:
            out.append(u)
    return out


class Fetcher:
    def __init__(self, log: list[str]):
        self.log, self.robots = log, {}

    def allowed(self, url: str) -> bool:
        root = "{0.scheme}://{0.netloc}/".format(urlparse(url))
        if root not in self.robots:
            rp = RobotFileParser()
            try:
                r = requests.get(root + "robots.txt", timeout=30, headers={"User-Agent": UA})
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            except requests.RequestException:
                rp.parse([])
            self.robots[root] = rp
        return self.robots[root].can_fetch(UA, url)

    def get(self, url: str) -> requests.Response | None:
        if not self.allowed(url):
            self.log.append(f"skipped (robots.txt): {url}")
            return None
        time.sleep(PAUSE)
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent": UA})
        except requests.RequestException as e:
            self.log.append(f"error {type(e).__name__}: {url}")
            return None
        self.log.append(f"{r.status_code} {len(r.content)} bytes: {url}")
        return r if r.status_code == 200 else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    f = Fetcher(log)

    # 1. The incidents ledger
    counts = {}
    for name in ("incidents.json", "sources.json"):
        r = f.get(INCIDENTS + name)
        if r is not None:
            (a.out / f"hackingincidents-{name}").write_bytes(r.content)
            try:
                d = r.json()
                rows = d if isinstance(d, list) else next((v for v in d.values() if isinstance(v, list)), [])
                counts[name] = len(rows)
                if name == "incidents.json":
                    grades = {}
                    for x in rows:
                        g = str(x.get("confidence", "")).upper()
                        grades[g] = grades.get(g, 0) + 1
                    counts["grades"] = grades
            except ValueError:
                counts[name] = "not JSON"
    for p in ("about/", "data/"):
        r = f.get(INCIDENTS + p)
        if r is not None:
            (a.out / f"hackingincidents-{p.strip('/')}.txt").write_text(text_of(r.text))

    # 2. The harness index: pages as text, and any data file its pages link to
    files = []
    for p in PAGES:
        r = f.get(HARNESSES + p)
        if r is None:
            continue
        (a.out / f"offsecharnesses-{p.strip('/') or 'front'}.txt").write_text(text_of(r.text))
        for u in data_links(HARNESSES + p, r.text):
            if u not in files:
                files.append(u)
    for u in files[:5]:
        r = f.get(u)
        if r is not None:
            (a.out / ("offsecharnesses-" + Path(urlparse(u).path).name)).write_bytes(r.content)

    L = ["# Outside AI-hacking trackers, one-time fetch", "",
         f"hackingincidents.ai: {json.dumps(counts)}",
         f"offsecharnesses.ai data files linked: {files or 'none found'}", "", "Requests:"]
    L += [f"- {x}" for x in log]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"ai_trackers: {len(log)} requests; incidents {counts.get('incidents.json')}; harness files {len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
