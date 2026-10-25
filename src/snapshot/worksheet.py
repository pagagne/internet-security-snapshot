"""Spot-check worksheets for the external reviewer.

A worksheet lets someone with a spreadsheet, and no code, recompute one headline figure the way
the registered plan defines it: the definition in plain words, the inputs as a CSV, numbered
steps, and the value the code produced to compare against. The reviewer can also check a few
input rows against their public sources (each row carries the links).

    python -m snapshot.worksheet race-sample PROBE_CSV OUTDIR [--quarter 2026Q3]

`race-sample` builds the sample worksheet for the race measure T1(a) from the fix-date probe
(research/2026-10-23T1315Z-fixdate_probe on the run-reports branch). It is a SAMPLE: real
public data, but the vendor fix dates are the automatic pre-fill without the hand check, so the
figure is not a study result. The full set (one worksheet per headline figure, generated with
every release, plus the seeded draw) is the 20 Jan 2027 schedule item `reviewer-worksheets`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from snapshot.race import t1_kev_race

KEV_CATALOG = "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"


def _quarter(q: str) -> tuple[str, str, str]:
    y, n = int(q[:4]), int(q[-1])
    start = pd.Timestamp(y, 3 * n - 2, 1)
    end = start + pd.offsets.QuarterEnd(0)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), f"Q{n} {y}"


def fix_from_probe(r: pd.Series) -> tuple[str, str, str]:
    """(fix date, where it came from, link to check it), in the pre-fill's order:
    GitHub advisory or release; Microsoft Update Guide; Cisco advisory; Palo Alto advisory;
    the CVE record's disclosure date; else the CVE publication date (assumed)."""
    cve = r["cve_id"]
    val = lambda c: r.get(c) if isinstance(r.get(c), str) and r.get(c) else None
    if val("github"):
        src = val("github_src") or "GitHub"
        ghsa = src.split()[-1] if "GHSA-" in src else None
        link = f"https://github.com/advisories/{ghsa}" if ghsa else f"https://www.cve.org/CVERecord?id={cve}"
        return val("github")[:10], src, link
    if val("msrc_release"):
        return val("msrc_release")[:10], "Microsoft Update Guide release date", \
            f"https://msrc.microsoft.com/update-guide/vulnerability/{cve}"
    if val("cisco_initial"):
        return val("cisco_initial")[:10], f"Cisco advisory {val('cisco_sa')}", \
            f"https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/{val('cisco_sa')}"
    if val("pan_datepublic"):
        return val("pan_datepublic")[:10], "Palo Alto advisory", f"https://security.paloaltonetworks.com/{cve}"
    if val("datepublic"):
        return val("datepublic")[:10], "CVE record: disclosure date (datePublic)", f"https://www.cve.org/CVERecord?id={cve}"
    return val("published")[:10], "CVE publication date (assumed; no fix date found)", f"https://www.cve.org/CVERecord?id={cve}"


def race_inputs(probe: pd.DataFrame, quarter: str) -> pd.DataFrame:
    qs, qe, _ = _quarter(quarter)
    q = probe[(probe["kev_added"] >= qs) & (probe["kev_added"] <= qe)].copy()
    rows = []
    for _, r in q.sort_values(["kev_added", "cve_id"]).iterrows():
        d, src, link = fix_from_probe(r)
        rows.append({"cve": r["cve_id"], "vendor": r["vendor"], "product": r["product"],
                     "fix_date": d, "attack_date_kev_added": r["kev_added"][:10],
                     "fix_date_source": src, "check_fix_date_at": link,
                     "check_attack_date_at": f"{KEV_CATALOG} (search {r['cve_id']})"})
    return pd.DataFrame(rows)


def race_result(inputs: pd.DataFrame, quarter: str) -> dict:
    """The figure as the pipeline computes it (snapshot.race.t1_kev_race) from these inputs."""
    qs, qe, _ = _quarter(quarter)
    t = lambda c: pd.to_datetime(inputs[c])
    ev = pd.DataFrame({"t_kev": t("attack_date_kev_added"), "t_exploit": t("attack_date_kev_added"),
                       "t_patch": t("fix_date"), "fix_lo": t("fix_date"), "fix_hi": t("fix_date"),
                       "exploit_hi": t("attack_date_kev_added")})
    return t1_kev_race(ev, qs, qe)


def race_markdown(inputs: pd.DataFrame, res: dict, quarter: str, source: str) -> str:
    _, _, label = _quarter(quarter)
    days = (pd.to_datetime(inputs["attack_date_kev_added"]) - pd.to_datetime(inputs["fix_date"])).dt.days
    med = res["median_days_fix_to_exploit"]
    med_s = f"{med:g}"
    n0 = int((days <= 0).sum())
    assumed = int(inputs["fix_date_source"].str.startswith("CVE publication").sum())
    cols = ", ".join(f"`{c}`" for c in inputs.columns)
    return f"""# Sample spot-check worksheet: the race measure T1(a), {label}

**This is a sample.** It shows exactly what a spot check of one headline figure involves. It
uses real public data for {label} ({len(inputs)} flaws first added to CISA's Known Exploited
Vulnerabilities list), but the fix dates are the automatic first pass, before the hand check
that the study adds every quarter, so the result below is **not a study result**. In the
real review you get one worksheet like this for each headline figure, and three are drawn at
random for you to check.

You need a spreadsheet program (Excel, Google Sheets, LibreOffice). No programming. About
20-30 minutes.

## What the plan says this figure is

**T1(a), the race:** for every software flaw first added to CISA's Known Exploited
Vulnerabilities (KEV) list during the quarter, count the days from the date a fix was available
to the date attacks were known (the date CISA added it to the list). Report the **median** of
those day counts. A small or negative number means attackers are keeping pace with, or beating,
the fixes.

(Defined in the registered plan, OSF DOI 10.17605/OSF.IO/3XT82, with the 23 October 2026
decision recorded in `prereg/DEVIATIONS.md`; computed by `t1_kev_race` in
`src/snapshot/race.py`.)

## The inputs

`inputs.csv`, one row per flaw. Columns: {cols}.

- `fix_date`: when a fix was available, and `fix_date_source` says where that date comes from.
  {assumed} of the {len(inputs)} rows had no fix date in any free source and fall back to the
  flaw's publication date ("assumed"); the quarterly hand check replaces those where it can.
- `attack_date_kev_added`: the date CISA added the flaw to KEV.
- The two `check_..._at` columns are links for checking a row against its public source.

## Steps

1. Open `inputs.csv` in your spreadsheet. Make sure the two date columns are read as dates
   (in Google Sheets: Format > Number > Date).
2. Add a column **days** = `attack_date_kev_added` minus `fix_date`. In Excel or Sheets, if
   `fix_date` is column D and `attack_date_kev_added` is column E: in the first data row type
   `=E2-D2` and fill down. Format the column as a plain number.
3. Compute the **median** of the days column: `=MEDIAN(I2:I{len(inputs) + 1})` (use your days
   column's letter).
4. Compare with the code's value below. They should be identical.
5. Optional, exploratory measure X10: count rows where days is 0 or less
   (`=COUNTIF(I2:I{len(inputs) + 1},"<=0")`), the flaws attacked on or before the day a fix appeared.
6. Optional, the inputs themselves: pick three rows and open their two links. Does the
   advisory show a fix on `fix_date`? Does the KEV catalogue list the flaw on
   `attack_date_kev_added`? Note any row that doesn't match.

## The code's value, to compare with

| | Value |
|---|---|
| Flaws in the quarter | {res['n']} |
| Flaws with both dates | {res['n_measured']} |
| **Median days, fix to known attack** | **{med_s}** |
| Flaws with days of 0 or less (X10, optional) | {n0} of {res['n_measured']} |

If your median differs, write down both numbers and which rows you think cause it. In the real
review, a mismatch is traced together and published with your review.

## Why it can differ from the published preview

This sample takes the fix dates from the automatic first pass ({source}). The study's figure
uses the dates after the hand check, and reports the range the date uncertainty allows next to
the median. Those refinements change the number, not the steps you just followed.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("race-sample")
    r.add_argument("probe_csv"); r.add_argument("outdir"); r.add_argument("--quarter", default="2026Q3")
    a = ap.parse_args(argv)
    probe = pd.read_csv(a.probe_csv, dtype=str)
    inputs = race_inputs(probe, a.quarter)
    res = race_result(inputs, a.quarter)
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    inputs.to_csv(out / "inputs.csv", index=False)
    src = "the fix-date probe of 23 October 2026, research/2026-10-23T1315Z-fixdate_probe on the run-reports branch"
    (out / "README.md").write_text(race_markdown(inputs, res, a.quarter, src))
    print(f"{res['n']} flaws, median {res['median_days_fix_to_exploit']} days; wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
