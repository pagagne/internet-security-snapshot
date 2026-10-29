"""Research probe (29 Oct 2026): open-source AI attack frameworks on GitHub.

Author's request after TrendAI's "Not only ARTEX" report, in which attackers ran CyberStrikeAI,
an open-source AI-agent penetration-testing platform, against Japanese organisations. Question
for the 12 Nov research review: can the supply of such tools be tracked monthly (repositories,
stars, forks, releases), beside X12's curve of downloadable AI models? This probe only measures
what GitHub's public search returns; it downloads no tool and runs nothing. Public project
metadata only. Requests are 1 s apart.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import requests

from ..collect.http import UA, note_status

API = "https://api.github.com"
QUERIES = [   # fixed for the probe; refined at the 12 Nov review if adopted
    "CyberStrikeAI in:name,description",
    "topic:ai-pentest",
    "topic:pentest-agent",
    "topic:autonomous-pentesting",
    "llm penetration testing agent in:description",
    "ai red team agent exploit in:description",
]


def gh(path: str, params: dict | None = None):
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    r = requests.get(API + path, params=params, headers=h, timeout=60)
    note_status(API + path, r.status_code)
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    summary, repos = {}, {}
    for q in QUERIES:
        time.sleep(1.0)
        r = gh("/search/repositories", {"q": q, "sort": "stars", "order": "desc", "per_page": 20})
        js = r.json() if r.ok else {}
        summary[q] = {"status": r.status_code, "total": js.get("total_count")}
        for it in js.get("items", []):
            repos.setdefault(it["full_name"], {
                "stars": it["stargazers_count"], "forks": it["forks_count"],
                "created": it["created_at"][:10], "pushed": it["pushed_at"][:10],
                "language": it.get("language"), "license": (it.get("license") or {}).get("spdx_id"),
                "archived": it.get("archived"), "found_by": []})["found_by"].append(q)
    for name in sorted(repos, key=lambda n: -repos[n]["stars"])[:25]:   # release history for the top ones
        time.sleep(1.0)
        r = gh(f"/repos/{name}/releases", {"per_page": 100})
        rel = r.json() if r.ok else []
        repos[name]["releases"] = len(rel)
        repos[name]["first_release"] = min((x["published_at"] or "")[:10] for x in rel) if rel else None
        repos[name]["latest_release"] = max((x["published_at"] or "")[:10] for x in rel) if rel else None
    out = {"queries": summary, "repositories": repos}
    (a.out / "summary.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(summary, indent=1))
    top = sorted(repos.items(), key=lambda kv: -kv[1]["stars"])[:15]
    for n, v in top:
        print(f"{v['stars']:>7} stars {v['forks']:>6} forks  created {v['created']}  releases {v.get('releases')}  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
