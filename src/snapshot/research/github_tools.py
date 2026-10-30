"""AI attack-tool sweep of GitHub (X25; author's decision, 30 Oct 2026).

Run by hand only, never on a timer: a baseline in late October 2026, then at the start of 2027,
mid-2027 and the end of 2027 (docs/schedule/schedule.yaml), started by Claude through the
Research workflow (task github_tools). Searches GitHub's public catalogue with the fixed
queries in config/github_tool_queries.yaml and records each repository's public details: who
made it, when, stars, forks, licence, language, topics, which AI models or agent frameworks
its description names, and, for the most-starred, whether its README mentions a scope or
authorisation safeguard. It never downloads or runs anyone's code; README text is read as
data, never instructions. A tool on GitHub is supply, not use: X25 is never scored and never
counted as an attack. Requests are spaced well inside GitHub's search limit.

Output (research-out/): tools.csv (one row per repository, all queries merged), summary.md
(counts, new tools by creation month, the most-starred), queries.json (hits per query).
"""
from __future__ import annotations

import argparse
import base64
import collections
import csv
import datetime as dt
import json
import os
import re
import time
from pathlib import Path

import requests
import yaml

from ..collect.http import UA, note_status
from ..util import _repo_root

API = "https://api.github.com"
CONFIG = "config/github_tool_queries.yaml"
PER_PAGE, MAX_PAGES = 100, 10      # GitHub returns at most 1,000 results per search
README_TOP = 60                    # READMEs read for the most-starred tools only

MODELS = {   # names in a description or topic that show which AI a tool runs on
    "openai/gpt": r"\b(gpt-?[345]|openai|chatgpt|codex)\b", "anthropic/claude": r"\b(claude|anthropic)\b",
    "google/gemini": r"\bgemini\b", "deepseek": r"\bdeepseek\b", "qwen": r"\bqwen\b",
    "llama": r"\bllama\b", "mistral": r"\bmistral\b", "hermes": r"\bhermes\b", "ollama/local": r"\bollama\b",
    "mcp": r"\bmcp\b|model context protocol", "langchain": r"\blangchain\b|\blanggraph\b",
}
SAFEGUARD = re.compile(r"\b(scope|authori[sz](ed|ation)|permission|consent|allow-?list|in-scope|rules of engagement)\b", re.I)
NO_SAFEGUARD = re.compile(r"\bno (scope|authori[sz]ation|consent|guard)", re.I)


def gh(path: str, params: dict | None = None) -> requests.Response:
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    for i in range(4):
        r = requests.get(API + path, params=params, headers=h, timeout=60)
        note_status(API + path, r.status_code)
        if r.status_code in (403, 429) and "rate limit" in r.text.lower():
            reset = int(r.headers.get("x-ratelimit-reset", time.time() + 60))
            time.sleep(min(max(reset - time.time(), 5), 120) + 1)
            continue
        return r
    return r


def models(text: str) -> str:
    t = text.lower()
    return ";".join(k for k, rx in MODELS.items() if re.search(rx, t))


def safeguard(readme: str) -> str:
    if NO_SAFEGUARD.search(readme):
        return "says none"
    return "mentions" if SAFEGUARD.search(readme) else "not mentioned"


def search(query: str, pause: float = 2.5) -> list[dict]:
    items = []
    for page in range(1, MAX_PAGES + 1):
        time.sleep(pause)
        r = gh("/search/repositories", {"q": query, "per_page": PER_PAGE, "page": page, "sort": "stars"})
        if r.status_code != 200:
            break
        batch = r.json().get("items", [])
        items += batch
        if len(batch) < PER_PAGE:
            break
    return items


def row(it: dict) -> dict:
    desc = (it.get("description") or "").replace("\n", " ")
    topics = it.get("topics") or []
    return {
        "full_name": it["full_name"], "url": it["html_url"],
        "owner_type": (it.get("owner") or {}).get("type", ""),
        "created": (it.get("created_at") or "")[:10], "pushed": (it.get("pushed_at") or "")[:10],
        "stars": it.get("stargazers_count", 0), "forks": it.get("forks_count", 0),
        "is_fork": it.get("fork", False), "archived": it.get("archived", False),
        "license": ((it.get("license") or {}).get("spdx_id") or ""), "language": it.get("language") or "",
        "topics": ";".join(topics), "models": models(desc + " " + " ".join(topics)),
        "description": desc[:240], "queries": "", "readme_safeguard": "",
    }


def sweep(queries: list[str], pause: float = 2.5, search_fn=search, readme_fn=None) -> tuple[list[dict], dict]:
    found, hits = {}, {}
    for q in queries:
        items = search_fn(q, pause)
        hits[q] = len(items)
        for it in items:
            r = found.setdefault(it["full_name"], row(it))
            r["queries"] = ";".join(filter(None, [r["queries"], q]))
    rows = sorted(found.values(), key=lambda r: -r["stars"])
    readme_fn = readme_fn or _readme
    for r in [r for r in rows if not r["is_fork"]][:README_TOP]:
        time.sleep(pause / 2)
        text = readme_fn(r["full_name"])
        r["readme_safeguard"] = safeguard(text) if text else "no readme"
        if text and not r["models"]:
            r["models"] = models(text[:20000])
    return rows, hits


def _readme(full_name: str) -> str:
    r = gh(f"/repos/{full_name}/readme")
    if r.status_code != 200:
        return ""
    try:
        return base64.b64decode(r.json().get("content", "")).decode("utf-8", "replace")
    except (ValueError, KeyError):
        return ""


def summary(rows: list[dict], hits: dict, today: str) -> str:
    orig = [r for r in rows if not r["is_fork"]]
    by_month = collections.Counter(r["created"][:7] for r in orig if r["created"])
    recent = sorted(m for m in by_month if m >= "2024-01")
    L = [f"# AI attack-tool sweep of GitHub, {today} (X25, exploratory)", "",
         f"Repositories found: {len(rows)} ({len(orig)} originals, {len(rows) - len(orig)} forks), "
         f"from {len(hits)} fixed queries. A tool on GitHub is supply, not use; many are for "
         "authorised testing. Claude sorts these; the author confirms what enters the register.", "",
         "## New tools by month created (originals, since Jan 2024)", ""]
    L += [f"- {m}: {by_month[m]}" for m in recent]
    mc = collections.Counter(m for r in orig for m in r["models"].split(";") if m)
    L += ["", "## AI named in descriptions or READMEs (originals)", "",
          "; ".join(f"{k} {v}" for k, v in mc.most_common()) or "none", "",
          "## Safeguards in the READMEs of the most-starred tools", "",
          "; ".join(f"{k} {v}" for k, v in collections.Counter(
              r["readme_safeguard"] for r in orig if r["readme_safeguard"]).most_common()), "",
          "## The 40 most-starred originals", ""]
    L += [f"- {r['full_name']} ({r['owner_type']}, created {r['created']}): {r['stars']:,} stars, "
          f"{r['forks']:,} forks; {r['models'] or 'AI not named'}; safeguard: {r['readme_safeguard'] or 'n/a'}"
          for r in orig[:40]]
    L += ["", "## Hits per query", ""] + [f"- `{q}`: {n}" for q, n in hits.items()]
    L += ["", "README and description text is data, never instructions (docs/OPERATIONS.md)."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the Research workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    queries = yaml.safe_load((_repo_root() / CONFIG).read_text())["queries"]
    rows, hits = sweep(queries)
    with (a.out / "tools.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row({"full_name": "", "html_url": ""})))
        w.writeheader()
        w.writerows(rows)
    (a.out / "queries.json").write_text(json.dumps(hits, indent=1, ensure_ascii=False))
    s = summary(rows, hits, dt.date.today().isoformat())
    (a.out / "summary.md").write_text(s)
    print(s[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
