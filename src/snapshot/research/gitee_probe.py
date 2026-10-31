"""Research probe (31 Oct 2026): does the author's Gitee token let the study search Gitee?

The author opened a Gitee account without a bound phone (mainland numbers only) and stored a
personal access token, scope user_info only, as the secret GITEE_TOKEN. This probe makes a few
repository searches through Gitee's official API (v5) with that token and records only counts:
HTTP status, the total-count header, the items returned and which fields they carry. No
repository or user names are kept, and the token never appears in output (it is sent as a
parameter and every printed address is stripped of it). Requests are 3 s apart.

Output: research-out/gitee_probe.csv and summary.md (private: an exploratory task).
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path

import requests

from ..collect.http import UA, note_status

API = "https://gitee.com/api/v5/search/repositories"
QUERIES = ["渗透测试", "AI 渗透", "大模型 安全", "红队 智能体", "pentest agent"]   # pentest; AI pentest; LLM security; red team agent


def search(q: str, token: str) -> dict:
    rec = {"query": q}
    try:
        r = requests.get(API, params={"q": q, "per_page": 20, "page": 1, "access_token": token},
                         headers={"User-Agent": UA}, timeout=45)
    except requests.RequestException as e:
        rec["status"] = f"error {type(e).__name__}"
        return rec
    note_status(API, r.status_code)
    rec["status"] = r.status_code
    rec["total_count"] = r.headers.get("total_count", "")
    if r.status_code == 200:
        try:
            items = r.json()
        except ValueError:
            items = []
        rec["items"] = len(items) if isinstance(items, list) else 0
        if isinstance(items, list) and items:
            keys = set(items[0])
            rec["fields"] = ";".join(k for k in ("created_at", "stargazers_count", "forks_count", "description",
                                                 "language", "owner", "license") if k in keys)
    else:
        rec["message"] = (r.text or "")[:120].replace(token, "***")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("GITEE_TOKEN", "")
    if not token:
        (a.out / "summary.md").write_text("# Gitee probe\n\nGITEE_TOKEN missing.\n")
        print("GITEE_TOKEN missing")
        return 1
    rows = []
    for q in QUERIES:
        rows.append(search(q, token))
        time.sleep(3)
    cols = ["query", "status", "total_count", "items", "fields", "message"]
    with (a.out / "gitee_probe.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    ok = sum(r.get("status") == 200 for r in rows)
    L = ["# Gitee probe", "", f"Searches: {len(rows)}; answered: {ok}. Counts only; no names kept.", ""]
    L += [f"- {r['query']}: status {r.get('status')}; total {r.get('total_count', '-')}; items {r.get('items', '-')}"
          f"; fields {r.get('fields', '-')}" + (f"; message {r['message']}" if r.get('message') else "") for r in rows]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
