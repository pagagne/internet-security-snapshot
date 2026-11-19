"""X26 probe: how much people hand over to AI (schedule item x26-autonomy-probe, 19 Nov 2026).

One test reading of each free signal named in config/exploratory.yaml (X26), so the author can
decide which to keep (issue #77). Exploratory: results go to the private repository only.

1. Software work (GitHub search): pull requests opened in one month by AI coding agents that
   leave a mark in the pull request itself (an app account, or a branch-name prefix the tool uses
   by default), how many were merged, beside all pull requests that month. For agents with their
   own app account, a sample of merged pull requests is checked for commits by anyone other than
   the agent ("merged with no human change"). Counts and shares only: no repository or user names
   are kept.
2. Web tasks (Cloudflare Radar): AI bot traffic grouped by crawl purpose, to see whether fetches
   made on a user's behalf are separated; several endpoint forms are tried and their status kept.
3. Conversations (Anthropic Economic Index on Hugging Face): the dataset's licence, files and
   release dates, and whether a task-delegation ("automation" versus "augmentation") share is
   published. Conflict of interest: Claude does the study's analysis.

Pauses: 8 s between GitHub searches (the search API's secondary limit tripped at 3 s on 19 Nov),
1 s elsewhere. Never prints keys.

    python -m snapshot.research.x26_probe --start 2026-10-01 --end 2026-10-31 --out DIR
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
from pathlib import Path

import requests

from snapshot.collect.http import UA

GH = "https://api.github.com"
RADAR = "https://api.cloudflare.com/client/v4/radar"
HF = "https://huggingface.co/api/datasets/Anthropic/EconomicIndex"
SEARCH_PAUSE = 8.0
SAMPLE = 20

# Agents that mark their pull requests (dated list, 19 Nov 2026). "author" = the agent's own app
# account (exact); "head" = the default branch prefix (estimate: users can rename branches, and
# other tools may reuse a prefix).
AGENTS = {
    "GitHub Copilot coding agent": {"author": "app/copilot-swe-agent"},
    "Devin": {"author": "app/devin-ai-integration"},
    "Google Jules": {"author": "app/google-labs-jules"},
    "OpenAI Codex (branch codex/)": {"head": "codex/"},
    "Cursor background agent (branch cursor/)": {"head": "cursor/"},
    "Claude Code (branch claude/)": {"head": "claude/"},
}
AGENT_LOGINS = {"copilot-swe-agent", "Copilot", "devin-ai-integration[bot]", "google-labs-jules[bot]"}

RADAR_TRIES = ["/ai/bots/summary/crawl_purpose", "/ai/bots/timeseries_groups/crawl_purpose",
               "/ai/bots/summary/user_agent", "/bots/crawlers/summary/crawl_purpose"]


def _get(url: str, headers: dict, params: dict | None = None, pause: float = 1.0):
    time.sleep(pause)
    try:
        r = requests.get(url, params=params, headers={"User-Agent": UA, **headers}, timeout=60)
    except requests.RequestException as e:
        return None, type(e).__name__
    try:
        body = r.json()
    except ValueError:
        body = None
    return body, (r.status_code if r.status_code != 200 else "ok")


def gh_headers() -> dict:
    t = os.environ.get("GITHUB_TOKEN", "")
    return {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {t}"} if t else {})}


def query(agent: dict, start: str, end: str, merged: bool = False) -> str:
    q = ["is:pr", f"created:{start}..{end}"]
    if "author" in agent:
        q.append(f"author:{agent['author']}")
    if "head" in agent:
        q.append(f"head:{agent['head']}")
    if merged:
        q.append("is:merged")
    return " ".join(q)


def human_changed(commits: list[dict]) -> bool:
    """True if any commit's GitHub author or committer is someone other than the agent or GitHub's
    web-flow (which commits on everyone's behalf). Names are compared, never stored."""
    for c in commits:
        for role in ("author", "committer"):
            login = ((c.get(role) or {}).get("login")) or ""
            if login and login not in AGENT_LOGINS and login != "web-flow":
                return True
    return False


def github_part(start: str, end: str, get=_get, pause: float = SEARCH_PAUSE) -> dict:
    h = gh_headers()
    out = {"window": [start, end], "all_prs": None, "agents": {}}
    body, st = get(f"{GH}/search/issues", h, {"q": f"is:pr created:{start}..{end}", "per_page": 1}, pause)
    out["all_prs"] = (body or {}).get("total_count") if st == "ok" else f"error {st}"
    for name, a in AGENTS.items():
        row = {"query": query(a, start, end), "kind": "exact (own account)" if "author" in a else "estimate (branch prefix)"}
        b1, s1 = get(f"{GH}/search/issues", h, {"q": row["query"], "per_page": 1}, pause)
        b2, s2 = get(f"{GH}/search/issues", h, {"q": query(a, start, end, True), "per_page": SAMPLE if "author" in a else 1}, pause)
        row["opened"] = (b1 or {}).get("total_count") if s1 == "ok" else f"error {s1}"
        row["merged"] = (b2 or {}).get("total_count") if s2 == "ok" else f"error {s2}"
        row["incomplete_results"] = bool((b1 or {}).get("incomplete_results") or (b2 or {}).get("incomplete_results"))
        if "author" in a and s2 == "ok":
            checked = changed = errors = 0
            for it in (b2 or {}).get("items", [])[:SAMPLE]:
                url = ((it.get("pull_request") or {}).get("url"))
                if not url:
                    continue
                commits, sc = get(url + "/commits", h, {"per_page": 100}, 1.0)
                if sc != "ok" or not isinstance(commits, list):
                    errors += 1
                    continue
                checked += 1
                changed += human_changed(commits)
            row["sample"] = {"checked": checked, "with_human_commit": changed, "errors": errors,
                             "note": "most recent merged pull requests in the window as search returns them; not random"}
        out["agents"][name] = row
    return out


def radar_part(get=_get) -> dict:
    t = os.environ.get("CLOUDFLARE_TOKEN", "")
    if not t:
        return {"status": "no CLOUDFLARE_TOKEN"}
    h = {"Authorization": f"Bearer {t}"}
    res = {}
    for path in RADAR_TRIES:
        body, st = get(RADAR + path, h, {"dateRange": "12w", "format": "json"})
        r = {"status": st}
        if st == "ok":
            result = (body or {}).get("result") or {}
            r["keys"] = sorted(result.keys())[:12]
            for k in ("summary_0", "serie_0"):
                if isinstance(result.get(k), dict):
                    r[k] = {kk: (vv if not isinstance(vv, list) else f"list of {len(vv)}")
                            for kk, vv in list(result[k].items())[:15]}
        else:
            r["errors"] = [e.get("message") for e in ((body or {}).get("errors") or [])][:3]
        res[path] = r
    return res


def hf_part(get=_get) -> dict:
    body, st = get(HF, {})
    if st != "ok":
        return {"status": st}
    card = body.get("cardData") or {}
    files = [s.get("rfilename") for s in body.get("siblings") or []]
    return {"status": "ok", "license": card.get("license"), "last_modified": body.get("lastModified"),
            "gated": body.get("gated"), "files": len(files),
            "release_folders": sorted({f.split("/")[0] for f in files if "/" in f}),
            "automation_files": [f for f in files if any(w in f.lower() for w in ("automation", "collaboration", "augment"))][:20]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-10-01")
    ap.add_argument("--end", default="2026-10-31")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    res = {"run": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "github": github_part(a.start, a.end), "radar": radar_part(), "economic_index": hf_part()}
    (a.out / "x26_probe.json").write_text(json.dumps(res, indent=2, default=str))
    g = res["github"]
    L = ["# X26 probe", "", f"Run {res['run']}; GitHub window {a.start} to {a.end}.", "",
         f"All pull requests opened: {g['all_prs']}", ""]
    for n, r in g["agents"].items():
        s = r.get("sample")
        L.append(f"- {n} [{r['kind']}]: opened {r['opened']}, merged {r['merged']}"
                 + (f"; sample {s['checked']} merged, {s['with_human_commit']} with a human commit" if s else ""))
    L += ["", "## Cloudflare Radar", ""] + [f"- {p}: {r}" for p, r in res["radar"].items()]
    L += ["", "## Anthropic Economic Index (conflict of interest)", "", json.dumps(res["economic_index"], indent=1)]
    (a.out / "x26_probe.md").write_text("\n".join(L) + "\n")
    print("x26_probe done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
