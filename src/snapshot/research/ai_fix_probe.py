"""AI-written security fixes: can they be told apart? (schedule item ai-fix-probe, author's decision
19 Nov 2026: probe first, decide before building).

Takes a fixed random sample of GitHub fix commits named in CVE records (the CVE List at today's
commit), published in two windows a year apart, and checks each commit for visible marks of an AI
tool: commit-message trailers and footers (Co-authored-by an AI tool, "Generated with ..."), the
commit's author or committer being a known agent account, and the pull request that brought it in
being opened by an agent account. Counts and mark labels only: no names, messages or repository
names are kept. Exploratory; results go to the private repository.

    python -m snapshot.research.ai_fix_probe --out DIR
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import tempfile
import time
from pathlib import Path

import pandas as pd
import requests

from snapshot.collect import cve as cvecol
from snapshot.collect.http import UA

GH = "https://api.github.com"
WINDOWS = {"2025H1": ("2025-01-01", "2025-06-30"), "2026H1": ("2026-01-01", "2026-06-30")}
SAMPLE = 150
SEED = 20261119
COMMIT = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/commit/([0-9a-f]{7,40})")

# Visible marks (dated list, 19 Nov 2026). Matched case-insensitively in the commit message.
MESSAGE_MARKS = {
    "co-author: Claude": r"co-authored-by:.*(claude|noreply@anthropic\.com)",
    "co-author: Copilot": r"co-authored-by:.*(copilot|copilot-swe-agent)",
    "co-author: Cursor": r"co-authored-by:.*cursor",
    "co-author: Codex/OpenAI": r"co-authored-by:.*(codex|openai)",
    "co-author: Devin": r"co-authored-by:.*devin",
    "co-author: Jules/Gemini": r"co-authored-by:.*(jules|gemini)",
    "co-author: aider/other": r"co-authored-by:.*(aider|openhands|sweep|cline|windsurf|codeium)",
    "footer: generated with": r"generated (with|by) (\[)?(claude|copilot|cursor|codex|chatgpt|gpt|gemini|aider)",
}
AGENT_LOGINS = {"Copilot", "copilot-swe-agent", "copilot-swe-agent[bot]", "devin-ai-integration[bot]",
                "google-labs-jules[bot]", "cursor[bot]", "cursoragent", "claude[bot]", "openhands-agent",
                "codex[bot]", "chatgpt-codex-connector[bot]"}


def headers() -> dict:
    t = os.environ.get("GITHUB_TOKEN", "")
    return {"Accept": "application/vnd.github+json", "User-Agent": UA, **({"Authorization": f"Bearer {t}"} if t else {})}


def marks(message: str, author: str, committer: str, pr_user: str) -> list[str]:
    out = [k for k, pat in MESSAGE_MARKS.items() if re.search(pat, message or "", re.I | re.M)]
    if author in AGENT_LOGINS or committer in AGENT_LOGINS:
        out.append("agent account made the commit")
    if pr_user in AGENT_LOGINS:
        out.append("agent account opened the pull request")
    return out


def sample(cve: pd.DataFrame, n: int = SAMPLE, seed: int = SEED) -> dict[str, list[tuple]]:
    pub = pd.to_datetime(cve["date_published"], utc=True, errors="coerce").dt.tz_localize(None)
    out = {}
    for name, (s, e) in WINDOWS.items():
        w = cve[(pub >= pd.Timestamp(s)) & (pub <= pd.Timestamp(e) + pd.Timedelta(days=1))]
        cands = []
        for r in w.itertuples():
            links = list(r.fix_links if r.fix_links is not None else []) + list(r.ref_links if r.ref_links is not None else [])
            for u in links:
                m = COMMIT.match(u or "")
                if m:
                    cands.append((r.cve_id, m.group(1), m.group(2), m.group(3)))
                    break
        rnd = random.Random(f"{seed}-{name}")
        out[name] = rnd.sample(cands, min(n, len(cands)))
    return out


def check(owner: str, repo: str, sha: str, get=None) -> tuple[list[str] | None, str]:
    get = get or (lambda url: requests.get(url, headers=headers(), timeout=60))
    try:
        r = get(f"{GH}/repos/{owner}/{repo}/commits/{sha}")
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        c = r.json()
        p = get(f"{GH}/repos/{owner}/{repo}/commits/{sha}/pulls")
        pr_user = ((p.json() or [{}])[0].get("user") or {}).get("login", "") if p.status_code == 200 and p.json() else ""
    except (requests.RequestException, ValueError) as e:
        return None, type(e).__name__
    return marks((c.get("commit") or {}).get("message", ""), (c.get("author") or {}).get("login", ""),
                 (c.get("committer") or {}).get("login", ""), pr_user), "ok"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        sha = cvecol.clone(Path(tmp) / "cvelistV5")
        cve = cvecol.build_table(Path(tmp) / "cvelistV5")
    S = {"cve_list_commit": sha, "seed": SEED, "windows": {}}
    for name, picks in sample(cve).items():
        res = {"sampled": len(picks), "checked": 0, "errors": 0, "with_any_mark": 0, "marks": {}}
        for _, owner, repo, c in picks:
            m, st = check(owner, repo, c)
            time.sleep(0.8)
            if m is None:
                res["errors"] += 1
                continue
            res["checked"] += 1
            res["with_any_mark"] += bool(m)
            for k in m:
                res["marks"][k] = res["marks"].get(k, 0) + 1
        S["windows"][name] = res
    (a.out / "ai_fix_probe.json").write_text(json.dumps(S, indent=1))
    L = ["# AI-written fixes probe (exploratory, private)", "", f"CVE List commit {sha}; seed {SEED}.", ""]
    for name, r in S["windows"].items():
        L.append(f"- {name}: {r['with_any_mark']} of {r['checked']} checked fix commits carry a visible AI mark "
                 f"({r['errors']} unreadable); marks: {r['marks']}")
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print("ai_fix_probe done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
