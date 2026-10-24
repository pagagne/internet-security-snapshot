"""Fix-date intervals, the exploitation upper bound, and the KEV-based race with bounds."""

import pandas as pd

from snapshot.events import build_events, fix_interval
from snapshot.race import t1_kev_race

T = pd.Timestamp


def test_fix_interval_rules():
    t0 = T("2026-07-01")
    assert fix_interval(t0, {"status": "confirmed", "date": "2026-07-03"}, None)[:2] == (T("2026-07-03"), T("2026-07-03"))
    lo, hi, basis = fix_interval(t0, {"status": "no_fix_yet", "date": "", "answered_at": "2026-08-01"}, None)
    assert (lo, hi) == (T("2026-08-01"), None) and basis == "author:no_fix_yet"
    # vendor-stated release date: a point
    assert fix_interval(t0, None, ("2026-07-02", "Microsoft Update Guide release date", False))[:2] == (T("2026-07-02"), T("2026-07-02"))
    # commit, or a vendor that changed its fixed releases later: lower bound only
    assert fix_interval(t0, None, ("2026-06-20", "fix commit abc (fix may ship later in a release)", True))[:2] == (T("2026-06-20"), None)
    # assumed from publication: disclosure date as lower bound, no upper bound
    lo, hi, basis = fix_interval(t0, None, ("2026-07-01", "ASSUMED same day as CVE publication; check the advisory link", True))
    assert (lo, hi) == (T("2026-07-01"), None) and basis.startswith("disclosure")
    # nothing known
    assert fix_interval(t0, None, None) == (t0, None, "no fix evidence")
    # author's answer wins over any pre-fill
    assert fix_interval(t0, {"status": "corrected", "date": "2026-07-09"}, ("2026-07-01", "x", False))[0] == T("2026-07-09")


def test_exploit_hi_uses_cisa_active_assessment_when_earlier():
    cve = pd.DataFrame([
        {"cve_id": "A", "date_published": "2026-07-01", "ssvc_exploitation": "active", "ssvc_timestamp": "2026-07-04T00:00:00Z"},
        {"cve_id": "B", "date_published": "2026-07-01", "ssvc_exploitation": "none", "ssvc_timestamp": "2026-07-02T00:00:00Z"},
    ])
    kev = pd.DataFrame([{"cve_id": "A", "date_added": "2026-07-20"}, {"cve_id": "B", "date_added": "2026-07-10"}])
    ev = build_events(cve, kev).set_index("cve_id")
    assert ev.loc["A", "t_exploit"] == T("2026-07-20")          # registered T_exploit unchanged
    assert ev.loc["A", "exploit_hi"] == T("2026-07-04") and ev.loc["A", "exploit_hi_source"] == "cisa_ssvc_active"
    assert ev.loc["B", "exploit_hi"] == T("2026-07-10")
    assert ev.loc["A", "fix_basis"] == "no fix evidence"


def test_kev_race_point_and_bounds():
    rows = [
        # fixed day 0, KEV day 10: days 10, not zero-day; fix known exactly
        dict(cve_id="a", t_kev=T("2026-07-11"), t_exploit=T("2026-07-11"), t_patch=T("2026-07-01"),
             t_patch_source="author:confirmed", fix_lo=T("2026-07-01"), fix_hi=T("2026-07-01"), exploit_hi=T("2026-07-11")),
        # attacked before its fix: zero-day for certain
        dict(cve_id="b", t_kev=T("2026-07-03"), t_exploit=T("2026-07-03"), t_patch=T("2026-07-05"),
             t_patch_source="author:corrected", fix_lo=T("2026-07-05"), fix_hi=T("2026-07-05"), exploit_hi=T("2026-07-03")),
        # fix date only assumed: could be a zero-day if the fix shipped after day 20
        dict(cve_id="c", t_kev=T("2026-07-21"), t_exploit=T("2026-07-21"), t_patch=T("2026-07-01"),
             t_patch_source="prefill (not hand-checked)", fix_lo=T("2026-07-01"), fix_hi=None, exploit_hi=T("2026-07-21")),
        # no fix at the author's check
        dict(cve_id="d", t_kev=T("2026-08-01"), t_exploit=T("2026-08-01"), t_patch=None,
             t_patch_source="author:no_fix_yet", fix_lo=T("2026-08-05"), fix_hi=None, exploit_hi=T("2026-08-01")),
        # outside the quarter
        dict(cve_id="e", t_kev=T("2026-10-02"), t_exploit=T("2026-10-02"), t_patch=T("2026-10-01"),
             t_patch_source="author:confirmed", fix_lo=T("2026-10-01"), fix_hi=T("2026-10-01"), exploit_hi=T("2026-10-02")),
    ]
    r = t1_kev_race(pd.DataFrame(rows), "2026-07-01", "2026-09-30")
    assert r["n"] == 4 and r["n_measured"] == 3
    assert r["median_days_fix_to_exploit"] == 10.0            # days 10, -2, 20
    assert r["zero_day_share_x10"] == 0.5                     # b and d of a, b, c, d
    b = r["bounds"]
    assert b["n"] == 4 and b["n_fix_date_bounded"] == 2
    assert b["zero_day_share_low"] == 0.5                     # b, d
    assert b["zero_day_share_high"] == 0.75                   # b, c, d
    assert b["median_days_high"] == 4.0                       # 10, -2, 20, -4
    assert b["median_days_low"] is None                       # two of four fixes have no upper date


def test_kev_race_when_no_fix_date_is_bounded():
    rows = [dict(cve_id=c, t_kev=T("2026-07-11"), t_exploit=T("2026-07-11"), t_patch=T("2026-07-01"),
                 t_patch_source="prefill (not hand-checked)", fix_lo=T("2026-07-01"), fix_hi=None,
                 exploit_hi=T("2026-07-11")) for c in "abc"]
    b = t1_kev_race(pd.DataFrame(rows), "2026-07-01", "2026-09-30")["bounds"]
    assert b["n_fix_date_bounded"] == 0 and b["median_days_low"] is None
    assert b["zero_day_share_low"] == 0.0 and b["zero_day_share_high"] == 1.0
