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
    token = os.environ.get("CLOUDFLARE_TOKEN")
    if not token:
        raise RuntimeError("CLOUDFLARE_TOKEN not set")
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
