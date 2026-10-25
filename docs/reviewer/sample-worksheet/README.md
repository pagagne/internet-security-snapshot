# Sample spot-check worksheet: the race measure T1(a), Q3 2026

**This is a sample.** It shows exactly what a spot check of one headline figure involves. It
uses real public data for Q3 2026 (100 flaws first added to CISA's Known Exploited
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

`inputs.csv`, one row per flaw. Columns: `cve`, `vendor`, `product`, `fix_date`, `attack_date_kev_added`, `fix_date_source`, `check_fix_date_at`, `check_attack_date_at`.

- `fix_date`: when a fix was available, and `fix_date_source` says where that date comes from.
  51 of the 100 rows had no fix date in any free source and fall back to the
  flaw's publication date ("assumed"); the quarterly hand check replaces those where it can.
- `attack_date_kev_added`: the date CISA added the flaw to KEV.
- The two `check_..._at` columns are links for checking a row against its public source.

## Steps

1. Open `inputs.csv` in your spreadsheet. Make sure the two date columns are read as dates
   (in Google Sheets: Format > Number > Date).
2. Add a column **days** = `attack_date_kev_added` minus `fix_date`. In Excel or Sheets, if
   `fix_date` is column D and `attack_date_kev_added` is column E: in the first data row type
   `=E2-D2` and fill down. Format the column as a plain number.
3. Compute the **median** of the days column: `=MEDIAN(I2:I101)` (use your days
   column's letter).
4. Compare with the code's value below. They should be identical.
5. Optional, exploratory measure X10: count rows where days is 0 or less
   (`=COUNTIF(I2:I101,"<=0")`), the flaws attacked on or before the day a fix appeared.
6. Optional, the inputs themselves: pick three rows and open their two links. Does the
   advisory show a fix on `fix_date`? Does the KEV catalogue list the flaw on
   `attack_date_kev_added`? Note any row that doesn't match.

## The code's value, to compare with

| | Value |
|---|---|
| Flaws in the quarter | 100 |
| Flaws with both dates | 100 |
| **Median days, fix to known attack** | **8.5** |
| Flaws with days of 0 or less (X10, optional) | 22 of 100 |

If your median differs, write down both numbers and which rows you think cause it. In the real
review, a mismatch is traced together and published with your review.

## Why it can differ from the published preview

This sample takes the fix dates from the automatic first pass (the fix-date probe of 23 October 2026, research/2026-10-23T1315Z-fixdate_probe on the run-reports branch). The study's figure
uses the dates after the hand check, and reports the range the date uncertainty allows next to
the median. Those refinements change the number, not the steps you just followed.
