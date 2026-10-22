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
            prev = out.get(r["cve_id"])
            if not prev or r.get("answered_at", "") >= prev["answered_at"]:
                out[r["cve_id"]] = {"date": r.get("fix_date", ""), "status": r["fix_status"],
                                    "answered_at": r.get("answered_at", ""), "prefill": r.get("prefill_date", "")}
    return out


def build_events(cve: pd.DataFrame, kev: pd.DataFrame | None, fixes: dict[str, dict] | None = None,
                 prefills: dict[str, str] | None = None, other_exploit: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per CVE in `cve` (cve_records rows).

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
            t_patch, src = _date(prefills[r.cve_id]), "prefill (not hand-checked)"
        else:
            t_patch, src = None, "none"
        cands = []
        if r.cve_id in kev_dates:
            cands.append((kev_dates[r.cve_id], "cisa_kev"))
        cands += extra.get(r.cve_id, [])
        t_exp, exp_src = (min(cands) if cands else (None, ""))
        rows.append({"cve_id": r.cve_id, "t0": t0, "t_patch": t_patch, "t_patch_source": src,
                     "t_kev": kev_dates.get(r.cve_id), "t_exploit": t_exp, "t_exploit_source": exp_src,
                     "t_poc": None})
    return pd.DataFrame(rows)
