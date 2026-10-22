# T1, the race: why the registered version cannot be estimated, and the options
(for decision item 0, 21 Dec 2026; numbers from Q3 2026 test data, 2026-10-22)

## The question
Are defenders closing exploitable flaws faster than attackers start exploiting them?
Registered T1(a): median days from the fix (T_patch) to first exploitation (T_exploit),
across the cohort (up to 12 randomly drawn serious, internet-facing CVEs per quarter).

## The problem
Only exploited flaws can say anything about the race, and very few serious flaws are ever
exploited:

- Q3 2026: 9,812 cohort-eligible CVEs; 41 of them (0.42%) are on CISA's exploited list so far.
- A 12-pick cohort therefore expects 0.05 exploited flaws per quarter, about one every five
  years. In the test, 0 of 11 picks were exploited.
- With no exploited flaws, the median cannot be computed. T1(a) would be "no estimate"
  almost every quarter.

The random draw is still right for its purpose (an unbiased sample of serious flaws for
exposure tracking, T1(b) and T2), but too small and too rarely exploited for T1(a).

## Options

| | What T1(a) measures | Sample per quarter | Strengths | Weaknesses |
|---|---|---|---|---|
| **(a) All flaws first exploited in the quarter** (recommended) | For each CVE added to CISA KEV in the quarter: days from fix to first exploitation; share exploited before any fix existed | about 100 | Large enough to estimate every quarter; uses data already collected | Fix dates needed for about 100 CVEs: pre-filled automatically, with a random sample of about 15 hand-checked per quarter. Looks only at flaws that were exploited (answers "how fast after a fix are exploited flaws attacked", not "what share get exploited"). Overlaps T3 where fix and publication are the same day. |
| **(b) Keep as registered** | Cohort only | 0-1 exploited | No change to the plan | Almost always "no estimate"; the central question goes unanswered |
| **(c) Larger cohort** | Same as registered | would need roughly 2,000 picks for ~10 exploited | Keeps a random sample | Far too much hand work; still few events |

## What option (a) would have shown for Q3 2026 (preview)
Fix date approximated by the CVE publication date in this preview (the real version uses
pre-filled and hand-checked fix dates):

- 91 CVEs first exploited in Q3 with records available here (100 KEV additions in total)
- Median 5 days from fix to first exploitation
- 25% exploited on or before the fix (zero-days)
- 53% within 7 days, 31% after more than 30 days

## What changes if (a) is adopted
- T1(a) headline: share of the quarter's newly exploited flaws attacked before a fix
  existed, plus the median days from fix to exploitation (Kaplan-Meier not needed: every
  case has an exploitation date).
- Hand work: about 15 extra fix dates per quarter (about 15 minutes).
- The cohort stays as is for exposure (T1b, T2), the root-cause tag and AI-vs-human
  comparisons.
- Logged as a deviation, reported alongside the registered cohort version (which will
  mostly read "no estimate") for four quarters, per the change policy.
