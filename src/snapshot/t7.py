"""T7 (AI-credited share) reported as a range.

- floor:   credits naming an AI tool in a clear published role pattern (lab names ignored):
           the narrow "AI tool named" figure, reported alongside the headline
- hand:    the headline (author's rule of 23 Oct 2026): any mention of an AI tool or a
           frontier AI lab counts (auto-accept v1.3), plus credits the author answered yes to
- ceiling: every CVE whose credit mentions any listed AI term, lab names included
           (equals the headline except for excluded or author-rejected credits)

All three share one denominator: CVEs published in the quarter. A direction (Rising or
Falling) is called only when floor and ceiling move the same way (decision item 14);
otherwise T7's direction is reported as unclear.
"""

from __future__ import annotations

import pandas as pd

from .autoaccept import auto_accept


def t7_range(cve: pd.DataFrame, author_yes: set[str] | None = None) -> dict:
    """cve: published CVEs of one quarter (cve_records rows). author_yes: credit texts
    (joined with ' | ', first 300 chars) the author answered yes to."""
    author_yes = author_yes or set()
    n = len(cve)
    cand = cve[cve["ai_credit_terms"].map(lambda x: len(x) > 0)]
    keys = cand["credit_values"].map(lambda v: " | ".join(list(v)))
    auto = cand.apply(lambda r: auto_accept(" | ".join(list(r["credit_values"])), list(r["credit_types"]), tools_only=True) is not None, axis=1)
    head = cand.apply(lambda r: auto_accept(" | ".join(list(r["credit_values"])), list(r["credit_types"])) is not None, axis=1)
    hand = auto | head | keys.map(lambda k: k[:300] in author_yes)
    share = lambda k: round(100 * k / n, 3) if n else None
    return {"cves": n, "floor": int(auto.sum()), "hand": int(hand.sum()), "ceiling": len(cand),
            "floor_pct": share(int(auto.sum())), "hand_pct": share(int(hand.sum())), "ceiling_pct": share(len(cand))}


def programme_evidence(cve: pd.DataFrame, floor_mask: pd.Series | None = None) -> int:
    """Floor plus credits from organizations with a dated AI-discovery programme active at
    publication (config/ai_programs.yaml). Exploratory (decision item 15)."""
    import re
    from .util import load_config
    progs = load_config("ai_programs.yaml")["programmes"]
    pub = pd.to_datetime(cve["date_published"], utc=True, errors="coerce").dt.date
    text = cve["credit_values"].map(lambda v: " | ".join(list(v)))
    hit = pd.Series(False, index=cve.index)
    for p in progs:
        start = pd.Timestamp(p["active_from"]).date()
        end = pd.Timestamp(p["active_to"]).date() if p.get("active_to") else None
        in_window = pub.map(lambda d: d is not None and d == d and d >= start and (end is None or d <= end))
        hit |= in_window & text.map(lambda t: bool(re.search(p["credit_regex"], t)))
    if floor_mask is not None:
        hit |= floor_mask
    return int(hit.sum())


def direction(history: list[dict], window: int = 4) -> str:
    """Direction label from the low end (floor) and the headline (hand; ceiling for older
    records): each compared with the median of the previous `window` quarters, two quarters
    running, both agreeing."""
    def edge(key):
        vals = [h[key] for h in history]
        if len(vals) < window + 2:
            return None
        moves = []
        for i in (-2, -1):
            prior = pd.Series(vals[i - window:i]).median()
            moves.append("up" if vals[i] > prior else "down" if vals[i] < prior else "flat")
        return moves[0] if moves[0] == moves[1] and moves[0] != "flat" else None
    f = edge("floor_pct")
    c = edge("hand_pct") if all("hand_pct" in h for h in history) else edge("ceiling_pct")
    if f and f == c:
        return "Rising" if f == "up" else "Falling"
    return "No clear direction" if f == c else "Unclear (low end and headline disagree)"
