# Decision notes: I5 / T5 and the 2026 surge in the baseline year (updated 7 Nov 2026)

For the core-freeze decision session, 21 December 2026 (`docs/CORE_FREEZE_DECISIONS.md`,
item 25). Raised by the author on 1 November 2026. Written by Claude in method terms; the
supporting figures are prepared privately for the session and are not repeated here.

## Why this needs a decision

- **The count is right.** From 1 Nov 2026, every quarterly pull checks our count of published
  CVE records against NVD's own count for the quarter and the same quarter in the three
  earlier years (data quality report, section 2b, flagged above 5%). On the Q3 2026 practice
  run the counts agreed within a fraction of a percent, and whole calendar-year totals agreed
  with a published independent review. So the sharp rise seen in 2026 is a real change in
  volume, not a counting error.
- **The rise falls inside the baseline year.** The registered rule (Section 4) compares each
  quarter with the median of the four quarters before it, and labels a direction after two
  consecutive quarters on the same side. The pilot (Q4 2026) counts toward the run, so the
  first growth label can appear with the Q1 2027 report on 1 April 2027, flagged as resting on
  the pilot. Its baseline is the four quarters of 2026, backfilled from history.
- **What that does to the label.** If I5 is scored as a growth rate, the 2026 baseline holds
  very high growth rates. A 2027 that stays at the new, higher volume but grows more slowly
  would read as **Falling** discovery pressure, although more flaws are being published than
  ever. If I5 is scored as a level, the same 2027 would read as **Rising** until the baseline
  catches up. The two readings can point in opposite directions, so the choice matters.
- **The registration is not consistent on the form.** Section 6 defines I5 as "year-over-year
  growth in published CVE records" against the same quarter in prior years. Section 9 says T5
  is analysed as a monthly series, log-transformed and seasonally adjusted (STL), with the
  quarter's adjusted value compared with its baseline and PELT changepoints flagged. That
  describes a level, not a growth rate. This has to be settled before any quarter is scored,
  whatever is decided about the surge.

## Options

1. **Keep the registered rule; settle the form as the seasonally adjusted level (Section 9).**
   Treat Section 6's wording as the descriptive figure reported beside it. The surge shows up as
   a flagged changepoint; labels follow the registered rule. Logged as a clarification.
2. **Keep the registered rule; settle the form as the year-over-year growth rate (Section 6).**
   Report the level beside it. Expect "Falling" or "No clear direction" through 2027 if the
   volume holds steady at the new height; the report explains why.
3. **Change the baseline for T5 only** (for example, eight quarters, or a baseline that starts
   after a flagged changepoint). A rule change after the data has been seen: logged as a
   deviation and reported side by side with the registered rule for four quarters
   (`docs/CHANGE_POLICY.md`).
4. **Report T5 without a label for 2027** ("baseline building after a changepoint"), labelling
   from Q1 2028 once a full year after the surge is in the baseline. Also a deviation.

## Claude's recommendation

Option 1. Section 9 is the more detailed, method-level text and was written for exactly this
kind of series; the level of the seasonally adjusted series is what "discovery pressure"
means; and the registered changepoint flag already exists to mark a break like 2026's. The
year-over-year growth rate stays in the report as the descriptive figure the reader expects,
beside the label. This keeps the registered baseline and label rule untouched, avoids choosing
a rule after seeing the trend, and needs only a dated clarification, not a deviation. The
companion check (item 19) beside the label then shows whether the movement is beyond noise.

## Evidence Claude brings to the session (private, ready by 14 December)

- Quarterly counts of published records from 2017 to Q4 2026 (the backfill), with the NVD
  cross-check for each quarter.
- The 2026 quarters as both growth rates and seasonally adjusted levels, and where Q4 2026
  sits against each baseline median.
- PELT changepoints on the monthly series, and the T5 sensitivity excluding the five largest
  CNAs (Section 9), to show whether the surge comes from a few CNAs.
- What each option would have labelled for the pilot quarter, computed on the 15 December
  full dry run, so the choice is made on method, not on a result we prefer.

## Q4 2026 is only partly in at the decision (author, 7 Nov 2026)

On 14 December, when the evidence is prepared, the pilot quarter (October to December 2026)
is about two and a half months complete, and the full quarter arrives only with the pilot pull
on 1 January 2027, after the core is locked. This does not block the decision, which is about
the form I5 takes (level or growth rate), not about a final figure. The evidence states plainly
which months are in, shows the partial quarter as it stands and, where an option needs a full
quarter, a projection from the months in hand, marked as a projection. The breakdown of where
the 2026 surge comes from (by issuing CNA, severity, root cause and AI credit, each quarter from
2024, with the registered "five largest CNAs excluded" sensitivity) is run early, from November,
as the private research task `cve_surge`.

## After the decision

The chosen form and any wording fix go into `prereg/DEVIATIONS.md` (clarification or
deviation, dated 21 Dec 2026), the freeze tag `core-v1.2`, and the OSF update.
