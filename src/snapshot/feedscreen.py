"""Monthly AI-attack feed screen (author's decision, 29 Oct 2026).

Reads every feed in config/feeds.yaml (RSS 1.0/2.0 or Atom, standard library only), keeps items
published in the last --days days that mention at least one AI term and one attack term in
the title or summary, and writes them as candidates for the X3 log. Nothing is logged
automatically: Claude sorts the candidates and the author keeps or excludes each in the
quarterly hand-check window. Requests are 1 s apart and name the study. Exploratory only.

  python -m snapshot.feedscreen --out DIR [--days 35]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import email.utils
import json
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml

from .collect.http import UA, note_status
from .util import _repo_root

CONFIG = "config/feeds.yaml"


def _text(el) -> str:
    return re.sub(r"<[^>]+>|\s+", " ", "".join(el.itertext()) if el is not None else "").strip()


def _date(s: str) -> dt.datetime | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def parse(xml: bytes) -> list[dict]:
    """Items from RSS 1.0, RSS 2.0 or Atom: title, link, date, summary."""
    root = ET.fromstring(xml)
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        f = {c.tag.split("}")[-1]: c for c in el}
        link = f.get("link")
        href = (link.get("href") or _text(link)) if link is not None else ""
        date = next((_text(f[k]) for k in ("pubDate", "published", "updated", "date") if k in f), "")
        summ = next((_text(f[k]) for k in ("description", "summary", "content", "encoded") if k in f), "")
        out.append({"title": _text(f.get("title")), "link": href, "date": _date(date), "summary": summ[:600]})
    return out


def _rx(terms: list[str]) -> re.Pattern:
    parts = [re.escape(t) if not t.isascii() else rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])" for t in terms]
    return re.compile("|".join(parts), re.I)


def screen(items: list[dict], ai: re.Pattern, attack: re.Pattern, since: dt.datetime) -> list[dict]:
    keep = []
    for it in items:
        if it["date"] and it["date"] < since:
            continue
        text = f"{it['title']} {it['summary']}"
        a, b = ai.search(text), attack.search(text)
        if a and b:
            keep.append({**it, "ai_term": a.group(0), "attack_term": b.group(0)})
    return keep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--days", type=int, default=35)
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the Research workflow
    a = ap.parse_args(argv)
    cfg = yaml.safe_load((_repo_root() / CONFIG).read_text())
    ai, attack = _rx(cfg["ai_terms"]), _rx(cfg["attack_terms"])
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    a.out.mkdir(parents=True, exist_ok=True)
    health, cands = [], []
    for f in cfg["feeds"]:
        time.sleep(1.0)
        try:
            r = requests.get(f["url"], headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"}, timeout=45)
            note_status(f["url"], r.status_code)
            items = parse(r.content) if r.ok else []
            hits = screen(items, ai, attack, since)
            health.append({"feed": f["name"], "status": r.status_code, "items": len(items), "candidates": len(hits)})
            cands += [{"feed": f["name"], **h} for h in hits]
        except Exception as e:  # noqa: BLE001 - a broken feed is recorded, never fatal
            health.append({"feed": f["name"], "status": "error", "items": 0, "candidates": 0, "error": repr(e)[:120]})
    seen, unique = set(), []
    for c in sorted(cands, key=lambda c: c["date"] or since, reverse=True):
        key = re.sub(r"\W+", " ", c["title"].lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)
    with (a.out / "candidates.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "feed", "title", "link", "ai_term", "attack_term"])
        for c in unique:
            w.writerow([(c["date"] or since).date(), c["feed"], c["title"], c["link"], c["ai_term"], c["attack_term"]])
    (a.out / "feed_health.json").write_text(json.dumps(health, indent=1, ensure_ascii=False))
    ok = sum(1 for h in health if h["status"] == 200 and h["items"])
    lines = [f"# AI-attack feed screen, last {a.days} days", "",
             f"Feeds read: {ok} of {len(health)} answered with items; candidates: {len(unique)} (after removing duplicates).",
             "", "Feeds that failed or returned nothing: " + (", ".join(
                 f"{h['feed']} ({h['status']})" for h in health if not (h["status"] == 200 and h["items"])) or "none"),
             "", "## Candidates (newest first)", ""]
    lines += [f"- {(c['date'] or since).date()} · {c['feed']} · [{c['title'][:140]}]({c['link']})" for c in unique[:150]]
    (a.out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:8]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
