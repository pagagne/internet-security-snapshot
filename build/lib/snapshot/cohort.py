"""Monthly cohort selection by seeded random draw (cohort_rules.yaml v1.1).

The draw order for a slot is fixed by hashing the month, the slot and each CVE ID, so
anyone can recompute it. Hand-check decisions decide only whether a candidate is
skipped (not internet-facing, or not really AI-credited); they never choose the pick.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Callable, Iterable

from .util import load_config


@lru_cache(maxsize=1)
def _selection_cfg() -> dict:
    return load_config("cohort_rules.yaml")["selection"]


def draw_key(month: str, slot: str, cve_id: str) -> str:
    """Hex SHA-256 key that places a CVE in its slot's draw order."""
    prefix = _selection_cfg()["seed_prefix"]
    return hashlib.sha256(f"{prefix}|{month}|{slot}|{cve_id}".encode()).hexdigest()


def draw_order(month: str, slot: str, cve_ids: Iterable[str]) -> list[str]:
    """Eligible CVE IDs in random draw order (ties impossible in practice; ID breaks them)."""
    ids = sorted(set(cve_ids))
    return sorted(ids, key=lambda c: (draw_key(month, slot, c), c))


@dataclass
class SlotResult:
    slot: str
    pick: str | None
    pool_size: int
    skipped: list[tuple[str, str]] = field(default_factory=list)   # (cve_id, reason)
    pending: list[str] = field(default_factory=list)               # awaiting hand check


def select_month(
    month: str,
    pools: dict[str, list[str]],
    passes_check: Callable[[str, str], bool | None],
) -> list[SlotResult]:
    """Pick at most one CVE per slot for `month`.

    pools: slot -> eligible CVE IDs for that slot.
    passes_check(slot, cve_id): True = confirmed, False = rejected, None = not yet
    reviewed. Slots a and b need no hand check and should return True.
    Selection stops at the first unreviewed candidate, so a pick is never made past an
    item still awaiting review.
    """
    taken: set[str] = set()
    results = []
    for slot in _selection_cfg()["slot_order"]:
        res = SlotResult(slot=slot, pick=None, pool_size=len(pools.get(slot, [])))
        for cve in draw_order(month, slot, pools.get(slot, [])):
            if cve in taken:
                res.skipped.append((cve, "already picked in an earlier slot"))
                continue
            verdict = passes_check(slot, cve)
            if verdict is None:
                res.pending.append(cve)
                break
            if verdict:
                res.pick = cve
                taken.add(cve)
                break
            res.skipped.append((cve, "failed hand check"))
        results.append(res)
    return results
