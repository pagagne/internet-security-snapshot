"""Auto-accept clear-cut AI credits (config/ai_credit_auto_accept.yaml).

Deterministic and public: the same credit text always gets the same answer, and every
auto-accepted row records the pattern that accepted it. Lab names qualify only in a
pattern marked `labs_allowed` (a stated collaboration with an AI lab, since v1.2).
"""

from __future__ import annotations

import hashlib
import re
from functools import lru_cache

from .classify import ai_credit_matches, lab_name_terms
from .util import load_config


@lru_cache(maxsize=1)
def _cfg():
    return load_config("ai_credit_auto_accept.yaml")


def _term_rx(term: str) -> str:
    return r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"


def auto_accept(credit_text: str, credit_types=(), suspended: frozenset = frozenset()) -> str | None:
    """Return the id of the rule that accepts this credit, or None (send to the author)."""
    cfg = _cfg()
    text = credit_text or ""
    for rx in cfg.get("send_to_author", []):
        if re.search(rx, text, re.IGNORECASE):
            return None
    labs = lab_name_terms()
    matched = ai_credit_matches(text.split(" | "))
    tools = [t for t in matched if t not in labs]
    if not matched:
        return None
    if tools and "tool" in set(credit_types or ()) and "credit_type_tool" not in suspended:
        return "credit_type_tool"
    for p in cfg["role_patterns"]:
        if p["id"] in suspended:
            continue
        for t in (matched if p.get("labs_allowed") else tools):
            if t in p.get("exclude_terms", []):
                continue
            rx = p["regex"].replace(r"{term}", _term_rx(t)).replace("\\b" + _term_rx(t), _term_rx(t))
            if re.search(rx, text, re.IGNORECASE):
                return p["id"]
    return None


def spot_check(keys: list[str], seed: str) -> set[str]:
    """Seeded random sample of auto-accepted credit texts shown to the author anyway."""
    cfg = _cfg()
    n = max(cfg.get("spot_check_min", 3), round(len(keys) * cfg.get("spot_check_share", 0.1)))
    ranked = sorted(keys, key=lambda k: hashlib.sha256(f"{seed}|{k}".encode()).hexdigest())
    return set(ranked[: min(n, len(keys))])
