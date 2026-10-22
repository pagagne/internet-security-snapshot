"""Cloudflare Radar: weekly attack-traffic context series (layer 3 and layer 7).

Uses the CLOUDFLARE_TOKEN secret (Account > Radar > Read). Stored as the raw JSON
responses; these are context series and never decide a label.
"""

from __future__ import annotations

import datetime as dt
import os

from .http import get

BASE = "https://api.cloudflare.com/client/v4/radar"
SERIES = {
    "attacks_layer7_timeseries": "/attacks/layer7/timeseries",
    "attacks_layer3_timeseries": "/attacks/layer3/timeseries",
    "attacks_layer7_by_vertical": "/attacks/layer7/summary/vertical",
    # X4 (exploratory): automated and AI traffic
    "http_bot_class_timeseries": "/http/timeseries_groups/bot_class",
    "ai_bots_by_user_agent_timeseries": "/ai/bots/timeseries_groups/user_agent",
}


def fetch(start: dt.date, end: dt.date) -> dict[str, dict]:
    raw = os.environ.get("CLOUDFLARE_TOKEN") or ""
    # The saved secret may hold more than one line (e.g. a token name and the token);
    # try each line and keep the first that Radar accepts.
    candidates = [line.strip() for line in raw.splitlines() if line.strip()]
    if not candidates:
        raise RuntimeError("CLOUDFLARE_TOKEN not set")
    import requests
    token, codes = None, []
    for cand in candidates:
        r = requests.get(BASE + "/http/summary/bot_class", params={"dateRange": "7d", "format": "json"},
                         headers={"Authorization": f"Bearer {cand}", "User-Agent": "internet-security-snapshot"}, timeout=60)
        if r.ok:
            token = cand
            break
        # Status and Cloudflare's error codes only; the token itself is never printed.
        try:
            errs = [f"{e.get('code')}:{e.get('message')}" for e in r.json().get("errors", [])][:2]
        except Exception:
            errs = []
        codes.append(f"line {len(codes) + 1} (length {len(cand)}): HTTP {r.status_code} {errs}")
    if token is None:
        raise RuntimeError("Cloudflare Radar rejected CLOUDFLARE_TOKEN: " + "; ".join(codes))
    params = {"dateStart": f"{start.isoformat()}T00:00:00Z",
              "dateEnd": f"{(end + dt.timedelta(days=1)).isoformat()}T00:00:00Z", "format": "json"}
    out = {}
    for name, path in SERIES.items():
        p = dict(params)
        if "timeseries" in name:
            p["aggInterval"] = "1w"
        try:
            out[name] = get(BASE + path, params=p, headers={"Authorization": f"Bearer {token}"}).json()
        except Exception as exc:  # one series failing must not lose the others
            out[name] = {"success": False, "error": f"{type(exc).__name__}: {exc}"}
    return out
