"""Per-CVE event dates (pre-registration Section 7.4).

T0         CVE record publication (first commit of the record; an earlier vendor advisory
           date, when recorded, replaces it)
T_patch    the author's hand-checked fix date (review/decisions.csv); else the pre-fill,
           marked as such; "no fix yet" stays empty with that status
T_kev      CISA KEV dateAdded
T_exploit  earliest dated record in Shadowserver honeypot data, VulnCheck KEV or CISA KEV.
           Only CISA KEV is available today (VulnCheck stays off until written permission,
           Shadowserver awaits approval), so T_exploit = T_kev for now and the source used
           is recorded per CVE.
T_poc      not yet collected (Exploit-DB, Metasploit, Nuclei, GitHub; see exploratory X7)

Dates are calendar dates (UTC). Events not observed by the evaluation date are left
empty; callers censor them.

Bounds (docs/STATISTICAL_REVIEW_2026-10-24.md, point 6; decision item 20). Beside the
registered dates, each row carries what is known about their uncertainty:
fix_lo, fix_hi  the fix was released no earlier than fix_lo and no later than fix_hi.
                Author-checked and vendor-stated release dates give fix_lo = fix_hi.
                Otherwise fix_lo is the earliest dated fix evidence (a fix commit), or the
                public disclosure date (assuming no fix precedes disclosure unless a source
                shows one), and fix_hi is empty: the fix may have shipped later.
exploit_hi      first exploitation happened on or before this date: the earliest of the
                registered exploitation sources and CISA's "active exploitation" assessment
                (Vulnrichment), which does not wait for remediation guidance. There is no
                lower bound in free data. exploit_hi is reporting-only; T_exploit keeps its
                registered definition.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

EXPLOIT_SOURCES = ("cisa_kev", "vulncheck_kev", "shadowserver")


def _date(x):
    if x is None or (isinstance(x, float) and pd.isna(x)) or x == "":
        return None
    try:
        return pd.Timestamp(x).tz_localize(None).normalize() if pd.Timestamp(x).tzinfo else pd.Timestamp(x).normalize()
    except (ValueError, TypeError):
        return None


def load_fix_decisions(decisions_csv: Path) -> dict[str, dict]:
    """cve_id -> latest author fix decision {date, status} from review/decisions.csv."""
    out: dict[str, dict] = {}
    if not decisions_csv or not Path(decisions_csv).exists():
        return out
    with open(decisions_csv, newline="") as f:
        for r in csv.DictReader(f):
            if r.get("decided_by", "author") != "author" or not r.get("fix_status"):
                continue
            if str(r.get("retest", "")).strip().lower() in ("true", "1", "yes"):
                continue   # re-shown items measure consistency; the original answer stands
            prev = out.get(r["cve_id"])
            if not prev or r.get("answered_at", "") >= prev["answered_at"]:
                out[r["cve_id"]] = {"date": r.get("fix_date", ""), "status": r["fix_status"],
                                    "answered_at": r.get("answered_at", ""), "prefill": r.get("prefill_date", "")}
    return out


def fix_interval(t0, fx: dict | None, prefill) -> tuple:
    """(fix_lo, fix_hi, basis) for one CVE; see the module docstring.

    fx: the author's decision (load_fix_decisions), if any.
    prefill: a date string (source not recorded), or (date, source note, needs_hand_check)
    as returned by snapshot.fixdates.prefill_exploited.
    """
    if fx and fx["status"] in ("confirmed", "corrected") and _date(fx["date"]) is not None:
        d = _date(fx["date"])
        return d, d, f"author:{fx['status']}"
    if fx and fx["status"] == "no_fix_yet":
        return _date(fx.get("answered_at")) or t0, None, "author:no_fix_yet"
    if fx and fx["status"] == "unknown":
        return t0, None, "author:unknown"
    if isinstance(prefill, (tuple, list)):
        d, note, needs_check = _date(prefill[0]), str(prefill[1]), bool(prefill[2])
        if d is None:
            return t0, None, "no fix evidence"
        if note.startswith("ASSUMED") or "fix date not stated" in note:
            return d, None, "disclosure date, fix not dated"
        if needs_check:
            return d, None, f"earliest evidence, may ship later: {note}"
        return d, d, f"vendor-stated: {note}"
    if prefill:
        return _date(prefill), None, "pre-fill, source not recorded"
    return t0, None, "no fix evidence"


def build_events(cve: pd.DataFrame, kev: pd.DataFrame | None, fixes: dict[str, dict] | None = None,
                 prefills: dict | None = None, other_exploit: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per CVE in `cve` (cve_records rows).

    prefills: cve_id -> date string, or -> (date, source note, needs_hand_check) from
    snapshot.fixdates.prefill_exploited (needed for informative fix bounds).
    other_exploit: optional rows (cve_id, source, date) from VulnCheck or Shadowserver,
    when those sources become available.
    """
    fixes, prefills = fixes or {}, prefills or {}
    kev_dates = {}
    if kev is not None and len(kev):
        for r in kev.itertuples():
            d = _date(r.date_added)
            if d is not None and (r.cve_id not in kev_dates or d < kev_dates[r.cve_id]):
                kev_dates[r.cve_id] = d
    extra: dict[str, list[tuple]] = {}
    if other_exploit is not None:
        for r in other_exploit.itertuples():
            d = _date(r.date)
            if d is not None:
                extra.setdefault(r.cve_id, []).append((d, r.source))
    rows = []
    for r in cve.itertuples():
        t0 = _date(r.date_published)
        fx = fixes.get(r.cve_id)
        if fx and fx["status"] in ("confirmed", "corrected"):
            t_patch, src = _date(fx["date"]), f"author:{fx['status']}"
        elif fx and fx["status"] == "no_fix_yet":
            t_patch, src = None, "author:no_fix_yet"
        elif fx and fx["status"] == "unknown":
            t_patch, src = None, "author:unknown"
        elif r.cve_id in prefills:
            pf = prefills[r.cve_id]
            t_patch, src = _date(pf[0] if isinstance(pf, (tuple, list)) else pf), "prefill (not hand-checked)"
        else:
            t_patch, src = None, "none"
        cands = []
        if r.cve_id in kev_dates:
            cands.append((kev_dates[r.cve_id], "cisa_kev"))
        cands += extra.get(r.cve_id, [])
        t_exp, exp_src = (min(cands) if cands else (None, ""))
        # Upper bound on first exploitation: also CISA's "active" assessment, when dated
        hi_cands = list(cands)
        if str(getattr(r, "ssvc_exploitation", "") or "").lower() == "active":
            ts = _date(getattr(r, "ssvc_timestamp", None))
            if ts is not None:
                hi_cands.append((ts, "cisa_ssvc_active"))
        exp_hi, exp_hi_src = (min(hi_cands) if hi_cands else (None, ""))
        fix_lo, fix_hi, basis = fix_interval(t0, fx, prefills.get(r.cve_id))
        rows.append({"cve_id": r.cve_id, "t0": t0, "t_patch": t_patch, "t_patch_source": src,
                     "t_kev": kev_dates.get(r.cve_id), "t_exploit": t_exp, "t_exploit_source": exp_src,
                     "t_poc": None, "fix_lo": fix_lo, "fix_hi": fix_hi, "fix_basis": basis,
                     "exploit_hi": exp_hi, "exploit_hi_source": exp_hi_src})
    return pd.DataFrame(rows)
