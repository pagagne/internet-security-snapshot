"""GreyNoise collector for exploratory X28 (author's decision, 18 Nov 2026: option B).

Research Community Access, granted 17 Nov 2026 (non-commercial use; credit "Data provided by
GreyNoise"; 90 days of history; unlimited lookups). What the 17-18 Nov probes showed: the tag
activity call returns only the last 24 hours, so history must be built up by the study itself;
the tag list carries each tag's creation date; the CVE lookup gives threat IP counts for the last
1, 10 and 30 days and the last-seen time.

Two modes, both writing only to the private repository (exploratory/greynoise/):

- quarterly: one call listing every tag (each CVE's earliest tag creation date = "GreyNoise
  detection date", not proof of first attack) plus one CVE lookup for each flaw CISA added to
  its known-exploited list in the quarter (about 75-100). About 100 requests a quarter.
- weekly (agreed by GreyNoise 18 Nov 2026; runs when GREYNOISE_WEEKLY is "on"): one CVE lookup for every CVE
  with a GreyNoise tag (about 3,300), one a second. Keeps the counts in a private rolling window
  of at most six months (older weekly files are deleted) and a permanent per-CVE record of the
  first week activity was seen.

Tag history (added 19 Nov 2026, schedule item greynoise-collector-90-days; corrected the same
day after the first test run): the tag activity call with days=90 returns one daily window for
every day of the 90, whether or not the tag saw activity, plus one total per classification over
the whole period ("aggregations"). So it gives a 90-day total per tag, not the days a tag was
active or its first active day (the 18 Nov reading of the windows as active days was wrong). The
quarterly run records those totals for the tags on the quarter's KEV flaws and on AI products and
the shared planes AI stacks use (X5 and X11, author's decisions 19 Nov 2026; agreed by GreyNoise
the same day). Quarterly only, as told to
GreyNoise: a 90-day view read once a quarter covers all but the first day or two of a 92-day
quarter, which is stated with the figures. Not added to the weekly sweep.

IP addresses and host data are never requested or kept; the key is never printed.

    python -m snapshot.collect.greynoise quarterly --quarter 2026Q4 --out DIR
    python -m snapshot.collect.greynoise weekly --out DIR
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import time
from pathlib import Path

import requests

from .http import UA

API = "https://api.greynoise.io"
KEV = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
PAUSE = 1.0
WINDOW_DAYS = 183           # the private rolling window (about six months)
COUNT_FIELDS = ("threat_ip_count_1d", "threat_ip_count_10d", "threat_ip_count_30d",
                "benign_ip_count_30d")
CVE_COLUMNS = ["cve", "activity_seen", *COUNT_FIELDS, "last_seen", "status"]
PUBLIC_KEYS = ("quarter", "date", "calls", "errors", "history_errors", "pruned_files")
HISTORY_DAYS = 90           # the longest view the tag activity call gives (tested 18 Nov 2026)
HISTORY_COLUMNS = ["tag_90d_malicious", "tag_90d_suspicious", "tag_90d_benign", "tag_90d_total"]

# AI-stack products and the shared control and data planes AI stacks rely on (X5 and X11; from the
# retired X29 proposal, author's decisions 19 Nov 2026). Matched against tag names and slugs only.
# Categories starting "shared:" are reported on their own line, never added to the AI figures.
AI_PRODUCTS = {
    "cluster/compute": r"\bray\b|anyscale|kubeflow|kuberay",
    "workflow/agent builders": r"langflow|\bn8n\b|flowise|\bdify\b|airflow|prefect|langchain|llamaindex",
    "ML ops/notebooks": r"mlflow|jupyter|clearml|h2o",
    "model servers/UIs": r"ollama|vllm|triton|torchserve|comfyui|open.?webui|litellm|anythingllm|gradio|llama.cpp|localai|bentoml",
    "vector DBs": r"qdrant|milvus|weaviate|chroma|pgvector",
    "AI gateways/MCP": r"\bmcp\b|model context protocol|\bllm\b|openai|ai gateway",
    "shared: Kubernetes/containers": r"kubernetes|\bk8s\b|kubelet|ingress-nginx|rancher|\bargo|docker api|containerd",
    "shared: object storage": r"minio|\bceph\b",
    "shared: remote support": r"screenconnect|connectwise|beyondtrust|anydesk|teamviewer|simplehelp|kaseya",
}
AI_COLUMNS = ["tag", "line", "categories", "created", "intention", "cves", *HISTORY_COLUMNS, "status"]


def ai_tags(tags: list[dict]) -> list[dict]:
    """Tags whose name or slug names an AI-stack or shared-plane product (metadata only)."""
    out = []
    for t in tags:
        text = f"{t.get('name', '')} {t.get('slug', '')}".lower()
        cats = [c for c, pat in AI_PRODUCTS.items() if re.search(pat, text)]
        if cats:
            out.append({"id": t.get("id"), "name": t.get("name"), "created_at": (t.get("created_at") or "")[:10],
                        "intention": t.get("intention"), "cves": t.get("cves") or [], "categories": cats})
    return sorted(out, key=lambda x: (x["categories"][0], x["created_at"]))


def totals(body) -> dict:
    """The 90-day totals per classification from a tag activity reply's "aggregations" block.
    The daily windows carry no counts and are listed for every day, so they are ignored."""
    agg = ((body or {}).get("aggregations") or {}).get("classification") if isinstance(body, dict) else None
    agg = agg if isinstance(agg, dict) else {}
    out = {f"tag_90d_{c}": int(agg.get(c) or 0) for c in ("malicious", "suspicious", "benign")}
    out["tag_90d_total"] = sum(out.values())
    return out


def tag_history(tag_id: str, key: str, get=None) -> tuple[dict, str]:
    """One call: the tag's totals per classification over the last 90 days."""
    get = get or _get
    body, status = get(f"/v3/tags/{tag_id}/activity", key, {"days": HISTORY_DAYS})
    return totals(body if status == "ok" else None), status


def _key() -> str:
    k = os.environ.get("GREYNOISE_API_KEY", "")
    if not k:
        raise SystemExit("GREYNOISE_API_KEY is not set (GitHub secret)")
    return k


def _get(path: str, key: str, params: dict | None = None, pause: float = PAUSE):
    time.sleep(pause)
    try:
        r = requests.get(API + path, params=params, timeout=60,
                         headers={"key": key, "Accept": "application/json", "User-Agent": UA})
    except requests.RequestException as e:
        return None, type(e).__name__
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    try:
        return r.json(), "ok"
    except ValueError:
        return None, "not JSON"


def all_tags(key: str, get=_get) -> list[dict]:
    body, _ = get("/v3/tags", key)
    return (body or {}).get("tags", [])


def tag_dates(key: str, get=_get, tags: list[dict] | None = None) -> dict[str, dict]:
    """CVE -> earliest tag creation date, number of tags and tag ids (one call)."""
    tags = all_tags(key, get) if tags is None else tags
    out: dict[str, dict] = {}
    for t in tags:
        for c in t.get("cves") or []:
            d = (t.get("created_at") or "")[:10]
            e = out.setdefault(c, {"tag_first_created": d, "tags": 0, "tag_ids": []})
            e["tags"] += 1
            if t.get("id"):
                e["tag_ids"].append(t["id"])
            if d and (not e["tag_first_created"] or d < e["tag_first_created"]):
                e["tag_first_created"] = d
    return out


def cve_row(cve: str, key: str, get=_get) -> dict:
    """Counts and last-seen for one CVE; nothing else from the reply is kept."""
    body, status = get(f"/v1/cve/{cve}", key)
    ea = (body or {}).get("exploitation_activity") or {}
    row = {"cve": cve, "activity_seen": ea.get("activity_seen", ""), "last_seen": ea.get("last_seen", ""),
           "status": status}
    for f in COUNT_FIELDS:
        row[f] = ea.get(f, "")
    return row


def quarter_bounds(q: str) -> tuple[dt.date, dt.date]:
    y, n = int(q[:4]), int(q[-1])
    start = dt.date(y, 3 * (n - 1) + 1, 1)
    end = (dt.date(y + (n == 4), (3 * n) % 12 + 1, 1) - dt.timedelta(days=1))
    return start, end


def kev_added(start: dt.date, end: dt.date) -> list[dict]:
    r = requests.get(KEV, timeout=60, headers={"User-Agent": UA})
    r.raise_for_status()
    rows = [{"cve": v["cveID"], "kev_date": v["dateAdded"]} for v in r.json().get("vulnerabilities", [])
            if start.isoformat() <= v.get("dateAdded", "") <= end.isoformat()]
    return sorted(rows, key=lambda x: (x["kev_date"], x["cve"]))


def quarterly(q: str, out: Path, key: str, get=_get, flaws: list[dict] | None = None) -> dict:
    start, end = quarter_bounds(q)
    flaws = flaws if flaws is not None else kev_added(start, end)
    tag_list = all_tags(key, get)
    tags = tag_dates(key, get, tag_list)
    calls = 1
    history: dict[str, tuple[dict, str]] = {}

    def hist(tid):
        nonlocal calls
        if tid not in history:
            history[tid] = tag_history(tid, key, get); calls += 1
        return history[tid]

    rows = []
    for f in flaws:
        t = tags.get(f["cve"], {})
        r = {"cve": f["cve"], "kev_date": f["kev_date"],
             "tag_first_created": t.get("tag_first_created", ""), "tags": t.get("tags", 0)}
        r.update(cve_row(f["cve"], key, get)); calls += 1
        # per CVE, the largest 90-day total among its tags (tags can overlap, so totals are not added)
        hs = [hist(tid)[0] for tid in t.get("tag_ids", [])]
        r.update({c: max((h[c] for h in hs), default=0) for c in HISTORY_COLUMNS})
        rows.append(r)
    out.mkdir(parents=True, exist_ok=True)
    cols = ["cve", "kev_date", "tag_first_created", "tags", *CVE_COLUMNS[1:], *HISTORY_COLUMNS]
    with (out / f"quarter-{q}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

    ai_rows = []
    for t in ai_tags(tag_list):
        h, status = hist(t["id"]) if t.get("id") else (totals(None), "no id")
        shared = all(c.startswith("shared:") for c in t["categories"])
        ai_rows.append({"tag": t["name"], "line": "shared planes" if shared else "AI stack",
                        "categories": "; ".join(t["categories"]), "created": t["created_at"],
                        "intention": t.get("intention") or "", "cves": " ".join(t["cves"]),
                        **{k: h[k] for k in HISTORY_COLUMNS},
                        "status": status})
    with (out / f"ai-tags-{q}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=AI_COLUMNS); w.writeheader(); w.writerows(ai_rows)

    tagged = [r for r in rows if r["tags"]]
    before = [r for r in tagged if r["tag_first_created"] and r["tag_first_created"] < r["kev_date"]]
    ai = [r for r in ai_rows if r["line"] == "AI stack"]
    return {"quarter": q, "flaws": len(rows), "tagged": len(tagged), "tag_before_kev": len(before),
            "activity_seen": sum(1 for r in rows if r["activity_seen"] is True),
            "tagged_with_90d_activity": sum(1 for r in tagged if r["tag_90d_total"]),
            "ai_tags": len(ai), "ai_tags_active": sum(1 for r in ai if r["tag_90d_total"]),
            "shared_tags": len(ai_rows) - len(ai),
            "shared_tags_active": sum(1 for r in ai_rows if r["line"] == "shared planes" and r["tag_90d_total"]),
            "history_errors": sum(1 for _, st in history.values() if st != "ok"), "calls": calls}


def update_first_seen(first: dict[str, dict], rows: list[dict], day: str) -> int:
    """Record the first sweep at which a CVE showed threat activity in the last 10 days."""
    new = 0
    for r in rows:
        try:
            active = int(r.get("threat_ip_count_10d") or 0) > 0
        except ValueError:
            active = False
        if active and r["cve"] not in first:
            first[r["cve"]] = {"cve": r["cve"], "first_sweep_with_activity": day,
                               "activity_from_or_after": (dt.date.fromisoformat(day) - dt.timedelta(days=10)).isoformat()}
            new += 1
    return new


def prune(weekly_dir: Path, today: dt.date, days: int = WINDOW_DAYS) -> int:
    """Delete weekly files older than the rolling window; returns how many."""
    n = 0
    for p in weekly_dir.glob("*.csv"):
        try:
            if (today - dt.date.fromisoformat(p.stem)).days > days:
                p.unlink(); n += 1
        except ValueError:
            continue
    return n


def weekly(out: Path, key: str, today: dt.date | None = None, get=_get) -> dict:
    today = today or dt.date.today()
    tags = tag_dates(key, get)
    rows = [cve_row(c, key, get) for c in sorted(tags)]
    wdir = out / "weekly"
    wdir.mkdir(parents=True, exist_ok=True)
    with (wdir / f"{today.isoformat()}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CVE_COLUMNS); w.writeheader(); w.writerows(rows)
    fpath = out / "first_seen.csv"
    first: dict[str, dict] = {}
    if fpath.exists():
        with fpath.open() as fh:
            first = {r["cve"]: r for r in csv.DictReader(fh)}
    new = update_first_seen(first, rows, today.isoformat())
    for c, t in tags.items():
        if c in first:
            first[c]["tag_first_created"] = t["tag_first_created"]
    cols = ["cve", "first_sweep_with_activity", "activity_from_or_after", "tag_first_created"]
    with fpath.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        w.writerows(sorted(first.values(), key=lambda r: r["cve"]))
    pruned = prune(wdir, today)
    errors = sum(1 for r in rows if r["status"] != "ok")
    return {"date": today.isoformat(), "cves": len(rows), "errors": errors, "new_first_seen": new,
            "first_seen_total": len(first), "pruned_files": pruned, "calls": len(rows) + 1}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["quarterly", "weekly"])
    ap.add_argument("--quarter")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    key = _key()
    if a.mode == "quarterly":
        if not a.quarter:   # the quarter that just ended
            t = dt.date.today().replace(day=1) - dt.timedelta(days=1)
            a.quarter = f"{t.year}Q{(t.month - 1) // 3 + 1}"
        s = quarterly(a.quarter, a.out, key)
    else:
        s = weekly(a.out, key)
    # The run log is public, and exploratory figures never go in public files (19 Nov 2026): the full
    # summary is saved privately beside the data; the log shows only how the run went.
    a.out.mkdir(parents=True, exist_ok=True)
    with (a.out / "last-run.txt").open("w") as fh:
        fh.write(", ".join(f"{k} {v}" for k, v in s.items()) + "\n")
    shown = {k: v for k, v in s.items() if k in PUBLIC_KEYS}
    print("GreyNoise", a.mode + ":", ", ".join(f"{k} {v}" for k, v in shown.items()),
          "(figures kept privately)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
