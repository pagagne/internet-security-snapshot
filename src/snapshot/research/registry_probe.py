"""Research probe (schedule item skill-registry-probe; author's decision 5 Nov 2026): what public
metadata do the main agent-skill registries offer? Never installs, downloads or runs a skill or
server; reads only public listing endpoints, a few pages at a time, and keeps aggregates only
(no publisher names: individuals are not studied).

  MCP   the Official MCP Registry, GET https://registry.modelcontextprotocol.io/v0/servers
        (Registry Data is CC0; preview service, data resets possible)
  Claw  ClawHub, GET https://clawhub.ai/api/v1/skills (public read API; reuse rules: cache, no
        aggressive polling, no mirroring of hidden or blocked content)

Writes summary.md: whether each endpoint answered, the fields offered, how far back publish dates
go, items per month, the share with a verified namespace or a security-scan field, and the field
names that could support a quarterly count. Private: method only.

    python -m snapshot.research.registry_probe --out DIR [--pages 30]
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

import requests

UA = "internet-security-snapshot research (registry metadata probe; contact via github.com/pagagne)"


def get(url: str, params: dict):
    try:
        r = requests.get(url, params=params, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=40)
        time.sleep(1.0)
        return r.status_code, (r.json() if r.ok else None)
    except (requests.RequestException, ValueError) as e:
        return type(e).__name__, None


def keys(obj, prefix="", out=None, depth=0):
    out = out if out is not None else set()
    if isinstance(obj, dict) and depth < 4:
        for k, v in obj.items():
            out.add(prefix + k)
            keys(v, prefix + k + ".", out, depth + 1)
    elif isinstance(obj, list) and obj and depth < 4:
        keys(obj[0], prefix + "[].", out, depth + 1)
    return out


def find(d, names):
    for n in names:
        cur = d
        for part in n.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur:
            return cur
    return None


def walk(name, url, list_key, cursor_param, next_names, date_names, pages):
    items, statuses, fields, cursor = [], Counter(), set(), None
    for _ in range(pages):
        params = {"limit": 100}
        if cursor:
            params[cursor_param] = cursor
        st, j = get(url, params)
        statuses[str(st)] += 1
        if not j:
            break
        batch = find(j, [list_key]) or []
        items += batch
        for it in batch[:3]:
            fields |= keys(it)
        cursor = find(j, next_names)
        if not cursor or not batch:
            break
    months = Counter(str(find(it, date_names) or "")[:7] for it in items)
    months.pop("", None)
    L = [f"## {name}", "", f"Endpoint: {url}", f"Responses: {dict(statuses)}; items read: {len(items)} "
         f"({'more pages remain' if cursor else 'end of list reached'}).", ""]
    if items:
        L += [f"Items per month (first {len(items)} read): " + ", ".join(f"{m} {c}" for m, c in sorted(months.items())), ""]
    L += ["Fields offered:", "", ", ".join(sorted(fields)) or "none", ""]
    return L, items


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path); ap.add_argument("--pages", type=int, default=30)
    ap.add_argument("--start"); ap.add_argument("--end")  # passed by the workflow; not used
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    L = ["# Agent-skill registry metadata probe", "", "Read-only; nothing installed or run; aggregates only.", ""]
    mcp_l, mcp = walk("Official MCP Registry", "https://registry.modelcontextprotocol.io/v0/servers", "servers",
                      "cursor", ["metadata.nextCursor", "metadata.next_cursor"],
                      ["_meta.io.modelcontextprotocol.registry/official.publishedAt", "server._meta.io.modelcontextprotocol.registry/official.publishedAt",
                       "_meta.io.modelcontextprotocol.registry/official.published_at", "publishedAt"], a.pages)
    L += mcp_l
    if mcp:
        ns = Counter(("github" if str(find(s, ["server.name", "name"]) or "").startswith("io.github.") else "domain")
                     for s in mcp)
        L += [f"Namespaces: GitHub-account {ns['github']}, verified domain {ns['domain']}.", ""]
    claw_l, claw = walk("ClawHub", "https://clawhub.ai/api/v1/skills", "items", "cursor",
                        ["nextCursor", "next_cursor"], ["createdAt", "created_at", "publishedAt", "updatedAt"], a.pages)
    L += claw_l
    if claw:
        flagged = Counter(str(find(s, ["moderation.status", "scan.status", "security.status", "moderationStatus"]) or "none")
                          for s in claw)
        L += ["Moderation or scan status values: " + ", ".join(f"{k} {v}" for k, v in flagged.most_common()), ""]
    L += ["Smithery: its API and accounts closed on 31 Oct 2026 (public directory only); not probed.", ""]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    (a.out / "registry_probe.json").write_text(json.dumps({"mcp": len(mcp), "clawhub": len(claw)}))
    print(f"registry probe: MCP {len(mcp)}, ClawHub {len(claw)} items read")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
