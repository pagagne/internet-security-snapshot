"""OpenRouter key and Data API test (author, 14 Nov 2026; X26 probe, schedule item x26-autonomy-probe).

The author opened a free OpenRouter account on 13 Nov 2026 (no credit bought) and stored its key as
the GitHub secret OPENROUTER_API_KEY. This task settles whether the free key reaches the Data API
(docs: openrouter.ai/docs/cookbook/administration/data-api; data CC BY 4.0) before anything is
bought. It never calls a model and never prints the key: only HTTP status codes, the key's own
limits (is_free_tier, limit, usage, rate limit) and the shape of each dataset (row counts, field
names, the meta block, a few category and task names). Six requests in all, a second apart.

    python -m snapshot.research.openrouter_probe --out DIR
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

BASE = "https://openrouter.ai/api/v1"


def _call(path: str, key: str, params: dict | None = None) -> dict:
    try:
        r = requests.get(f"{BASE}{path}", params=params, timeout=60,
                         headers={"Authorization": f"Bearer {key}", "User-Agent": UA})
    except requests.RequestException as e:          # network problem: record the type only
        return {"path": path, "status": None, "error": type(e).__name__}
    out = {"path": path, "params": params or {}, "status": r.status_code}
    try:
        body = r.json()
    except ValueError:
        out["body"] = "not JSON"
        return out
    if r.status_code != 200:
        err = body.get("error") if isinstance(body, dict) else None
        out["error"] = (err.get("message") if isinstance(err, dict) else str(err))[:300] if err else str(body)[:300]
        return out
    out["meta"] = body.get("meta") if isinstance(body, dict) else None
    data = body.get("data") if isinstance(body, dict) else body
    if isinstance(data, list):
        out["rows"] = len(data)
        out["fields"] = sorted({k for row in data[:50] if isinstance(row, dict) for k in row})[:30]
        out["sample"] = data[:5]
    elif isinstance(data, dict):
        out["fields"] = sorted(data)[:40]
        out["sample"] = data
    return out


def key_status(key: str) -> dict:
    """The key's own limits, with the key's label and any hash removed."""
    res = _call("/key", key)
    if isinstance(res.get("sample"), dict):
        keep = ("is_free_tier", "limit", "limit_remaining", "usage", "usage_daily", "rate_limit",
                "is_provisioning_key", "limit_reset")
        res["sample"] = {k: v for k, v in res["sample"].items() if k in keep}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        (a.out / "summary.md").write_text("OPENROUTER_API_KEY is not set for this run.\n")
        print("openrouter_probe: no key")
        return 1
    end = dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=6)
    calls = [("key status", "/key", None),
             ("rankings, last 7 days", "/datasets/rankings-daily",
              {"start_date": start.isoformat(), "end_date": end.isoformat()}),
             ("rankings, January 2025", "/datasets/rankings-daily",
              {"start_date": "2025-01-01", "end_date": "2025-01-07"}),
             ("top apps", "/datasets/app-rankings", {"limit": 25}),
             ("task shares", "/classifications/task", {"window": "7d"}),
             ("benchmarks (agentic)", "/benchmarks", {"task_type": "agentic", "max_results": 5})]
    R = []
    for name, path, params in calls:
        res = key_status(key) if path == "/key" else _call(path, key, params)
        res["name"] = name
        R.append(res)
        time.sleep(1.0)
    (a.out / "openrouter_probe.json").write_text(json.dumps(R, indent=1, default=str))
    L = ["# OpenRouter key and Data API test", "",
         f"Run {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC. No model was called; the key is not shown.", ""]
    for res in R:
        line = f"- **{res['name']}** (`{res['path']}`): HTTP {res.get('status')}"
        if "rows" in res:
            line += f", {res['rows']} rows"
        if res.get("error"):
            line += f"; error: {res['error']}"
        L.append(line)
        if res["path"] == "/key" and isinstance(res.get("sample"), dict):
            L.append(f"  - key: {json.dumps(res['sample'], default=str)}")
        if res.get("meta"):
            L.append(f"  - meta: {json.dumps(res['meta'], default=str)[:400]}")
        if res.get("fields"):
            L.append(f"  - fields: {', '.join(map(str, res['fields']))}")
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print("openrouter_probe: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
