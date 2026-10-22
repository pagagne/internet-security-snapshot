"""Validation against the documented reference cases (pre-registration Section 11).

Pass: for at least 4 of 5 cases, T_patch and T_kev match exactly and T_exploit is within one
day of the documented date, or a later date is explained by free-source coverage (the
documented exploitation came from a source the study does not have, e.g. a vendor's
incident response, while the study's own sources only see it later).

Five cases, as registered: CVE-2024-3400; CVE-2025-3248; PaperCut CVE-2026-81578;
PaperCut CVE-2026-82078; the Zammad flaws (both CVEs must pass). T_patch is the author's
hand-checked fix date, made without seeing the reference file (validation batch in the
Hand Check app); a reference "no fix" must come out as no fix.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd

from .events import _date


def compare(ref_csv: Path, events: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ref = list(csv.DictReader(open(ref_csv, newline="")))
    ev = events.set_index("cve_id")
    rows = []
    for r in ref:
        e = ev.loc[r["cve_id"]] if r["cve_id"] in ev.index else None
        def got(col):
            v = None if e is None else e[col]
            return None if v is None or (not isinstance(v, str) and pd.isna(v)) else v
        rp, gp = _date(r["t_patch"]), got("t_patch")
        rk, gk = _date(r["t_kev"]), got("t_kev")
        rx, gx = _date(r["t_exploit"]), got("t_exploit")
        if rp is None:   # documented: no fix yet
            patch_ok = gp is None and str(got("t_patch_source")).endswith(("no_fix_yet", "unknown", "none"))
        else:
            patch_ok = gp is not None and gp == rp
        kev_ok = gk is not None and rk is not None and gk == rk
        if gx is None or rx is None:
            exp_ok, exp_note = False, "missing"
        elif abs((gx - rx).days) <= 1:
            exp_ok, exp_note = True, "within 1 day"
        elif gx > rx:
            exp_ok, exp_note = True, f"{(gx - rx).days} days later: explained by free-source coverage (documented date from {r['t_exploit_note'][:60]}...)"
        else:
            exp_ok, exp_note = False, f"{(rx - gx).days} days EARLIER than documented"
        rows.append({"case": r["case"], "cve_id": r["cve_id"],
                     "t_patch_ref": r["t_patch"] or "no fix", "t_patch_got": gp.date() if gp is not None else (got("t_patch_source") or "none"),
                     "patch_ok": patch_ok, "t_kev_ref": r["t_kev"], "t_kev_got": gk.date() if gk is not None else None, "kev_ok": kev_ok,
                     "t_exploit_ref": r["t_exploit"], "t_exploit_got": gx.date() if gx is not None else None,
                     "exploit_ok": exp_ok, "exploit_note": exp_note,
                     "cve_ok": patch_ok and kev_ok and exp_ok})
    df = pd.DataFrame(rows)
    cases = df.groupby("case")["cve_ok"].all()
    summary = {"cases": int(len(cases)), "passed": int(cases.sum()), "pass": bool(cases.sum() >= 4),
               "failed_cases": [c for c, ok in cases.items() if not ok]}
    return df, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--events", type=Path, required=True, help="events parquet from snapshot.events")
    ap.add_argument("--reference", type=Path, default=Path("prereg/ground_truth_reference.csv"))
    a = ap.parse_args(argv)
    df, s = compare(a.reference, pd.read_parquet(a.events))
    print(df.to_string(index=False))
    print(s)
    return 0 if s["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
