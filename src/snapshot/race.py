"""T1(a) the race and T3 time to exploitation (pre-registration Sections 2, 8, 9).

T1(a): days from T_patch to T_exploit across cohort CVEs (negative = exploited before a
       fix existed). Kaplan-Meier median, CVEs without observed exploitation censored at
       the end of their 90-day follow-up or the evaluation date, whichever is earlier.
       Race outcome per CVE: "lost" if exploited on or before T_patch (or with no fix),
       otherwise "open" until exploitation; "won" needs exposure data (T1b) and is not
       assigned here.
T3:    (a) median days from T0 to first exploitation for CVEs first exploited in the
       quarter; (b) share exploited on or before T0.
Uncertainty: 90% bootstrap intervals, 2,000 resamples, fixed seed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20261020
FOLLOW_UP_DAYS = 90
SHIFT = 400   # Kaplan-Meier needs non-negative durations; T1 values are shifted, then shifted back


def _km_median(durations: np.ndarray, observed: np.ndarray) -> float | None:
    from lifelines import KaplanMeierFitter
    if len(durations) == 0 or observed.sum() == 0:
        return None
    k = KaplanMeierFitter().fit(durations + SHIFT, event_observed=observed)
    m = k.median_survival_time_
    return None if not np.isfinite(m) else float(m - SHIFT)


def _boot(fn, n: int, reps: int = 2000) -> tuple[float | None, float | None]:
    rng = np.random.default_rng(SEED)
    vals = []
    for _ in range(reps):
        v = fn(rng.integers(0, n, n))
        if v is not None:
            vals.append(v)
    if len(vals) < reps * 0.5:
        return None, None
    return float(np.percentile(vals, 5)), float(np.percentile(vals, 95))


def t1_race(cohort_events: pd.DataFrame, eval_date) -> dict:
    """cohort_events: rows from snapshot.events for the quarter's cohort CVEs."""
    ev = pd.Timestamp(eval_date).normalize()
    d, obs, outcome = [], [], []
    na = lambda v: v is None or pd.isna(v)
    for r in cohort_events.itertuples():
        end = min(ev, r.t0 + pd.Timedelta(days=FOLLOW_UP_DAYS)) if not na(r.t0) else ev
        exploited = not na(r.t_exploit) and r.t_exploit <= end
        if na(r.t_patch):
            # no fix (yet): exploitation counts as before the patch; otherwise not measurable
            if exploited:
                # exploited with no fix by the end of follow-up: patch-to-exploit is at most
                # (T_exploit - end of follow-up), a negative value used as an upper bound
                d.append(float((r.t_exploit - end).days)); obs.append(1); outcome.append("lost (no fix)")
            else:
                outcome.append("open (no fix)")
            continue
        if exploited:
            d.append(float((r.t_exploit - r.t_patch).days)); obs.append(1)
            outcome.append("lost" if r.t_exploit <= r.t_patch else "exploited after fix")
        else:
            d.append(float((end - r.t_patch).days)); obs.append(0)
            outcome.append("open")
    d, obs = np.array(d), np.array(obs)
    med = _km_median(d, obs)
    lo, hi = _boot(lambda i: _km_median(d[i], obs[i]), len(d)) if len(d) else (None, None)
    return {"n": int(len(cohort_events)), "n_measured": int(len(d)), "exploited": int(obs.sum()),
            "median_days_patch_to_exploit": med, "ci90": (lo, hi),
            "outcomes": pd.Series(outcome).value_counts().to_dict()}


def t3_time_to_exploit(events: pd.DataFrame, quarter_start, quarter_end) -> dict:
    """events: rows for CVEs first exploited in the quarter (t_exploit within the quarter)."""
    qs, qe = pd.Timestamp(quarter_start), pd.Timestamp(quarter_end)
    e = events[events["t_exploit"].notna() & events["t0"].notna()]
    e = e[(e["t_exploit"] >= qs) & (e["t_exploit"] <= qe)]
    days = (e["t_exploit"] - e["t0"]).dt.days.to_numpy()
    if len(days) == 0:
        return {"n": 0}
    rng_med = lambda i: float(np.median(days[i]))
    lo, hi = _boot(rng_med, len(days))
    share = float((days <= 0).mean())
    slo, shi = _boot(lambda i: float((days[i] <= 0).mean()), len(days))
    return {"n": int(len(days)), "median_days_t0_to_exploit": float(np.median(days)), "ci90": (lo, hi),
            "share_exploited_on_or_before_t0": round(share, 3), "share_ci90": (slo, shi)}
