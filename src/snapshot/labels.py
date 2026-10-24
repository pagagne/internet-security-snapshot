"""Direction labels (prereg section 4) and the companion check reported beside them.

registered_label() is the registered rule and alone decides a label:
  1. each quarter's value is compared with its baseline, the median of the four preceding
     quarters, giving up, down or unchanged;
  2. a direction is labelled when the value has moved the same way for two consecutive
     quarters; otherwise "No clear direction".

companion_check() is a reporting addition (docs/STATISTICAL_REVIEW_2026-10-24.md, item 19 of
docs/CORE_FREEZE_DECISIONS.md). It never changes a label. Simulation: with no true change
the registered rule labels a direction in about 48% of quarters; this check supports a label
in about 10%. It compares the mean of the last two quarters with the mean of the four
before, using each quarter's published standard error, as a two-sided test at the 10% level,
and says "supported" only when the difference is significant and points the same way as
the label.
"""

from __future__ import annotations

import math
from statistics import median
from typing import Sequence

Z_90 = 1.6448536269514722  # two-sided 10% level


def direction(values: Sequence[float], t: int) -> int:
    """+1, -1 or 0: quarter t against the median of quarters t-4..t-1."""
    if t < 4:
        raise ValueError("need four preceding quarters")
    base = median(values[t - 4:t])
    d = values[t] - base
    return (d > 0) - (d < 0)


def registered_label(values: Sequence[float], better: str | None = None) -> str:
    """Label for the latest quarter under the registered rule.

    better: "higher" or "lower" for directional questions (Improving/Worsening);
    None for descriptive questions (Rising/Falling). Needs at least six quarters.
    """
    t = len(values) - 1
    d1, d2 = direction(values, t - 1), direction(values, t)
    if d1 != d2 or d2 == 0:
        return "No clear direction"
    if better is None:
        return "Rising" if d2 > 0 else "Falling"
    good = (d2 > 0) == (better == "higher")
    return "Improving" if good else "Worsening"


def companion_check(values: Sequence[float], ses: Sequence[float], label: str) -> dict:
    """Is the label supported by a two-quarters-versus-prior-four test at the 10% level?

    values, ses: the last six quarters' values and their published standard errors
    (oldest first). Returns z, the difference, and "supported" / "not supported" /
    "no label" (when the registered rule gave none).
    """
    if len(values) < 6 or len(ses) < 6:
        raise ValueError("need six quarters of values and standard errors")
    v, s = list(values[-6:]), list(ses[-6:])
    diff = (v[4] + v[5]) / 2 - sum(v[0:4]) / 4
    se = math.sqrt((s[4] ** 2 + s[5] ** 2) / 4 + sum(x ** 2 for x in s[0:4]) / 16)
    z = diff / se if se > 0 else math.inf * (1 if diff > 0 else -1 if diff < 0 else 0)
    if label == "No clear direction":
        verdict = "no label"
    else:
        # The label's direction in terms of the value itself (Improving can mean up or down,
        # depending on the question), taken from the registered comparison it rests on.
        sign = (diff > 0) - (diff < 0)
        label_sign = direction(values, len(values) - 1)
        verdict = "supported" if abs(z) > Z_90 and sign == label_sign else "not supported"
    return {"difference": diff, "z": z, "check": verdict}
