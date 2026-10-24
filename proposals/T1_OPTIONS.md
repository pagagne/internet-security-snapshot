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
- Because slots a and b draw from small, more-exploited pools (edge devices: 6 of 96 in Q3),
  the cohort does better than that average: the back-test below puts it at about 0.3-0.4
  exploited picks per quarter (slots a-c), a 27-33% chance of even one. (An earlier draft
  of this paper said 0.05, which ignored the slots; corrected 2026-10-22.) In the test, 0 of
  11 picks were exploited.
- With no exploited flaws, the median cannot be computed. T1(a) would be "no estimate"
  almost every quarter.

The random draw is still right for its purpose (an unbiased sample of serious flaws for
exposure tracking, T1(b) and T2), but too small and too rarely exploited for T1(a).

## Options

| | What T1(a) measures | Sample per quarter | Strengths | Weaknesses |
|---|---|---|---|---|
| **(a) All flaws first exploited in the quarter** (recommended) | For each CVE added to CISA KEV in the quarter: days from fix to first exploitation; share exploited before any fix existed | 75-100 | Large enough to estimate every quarter; uses data already collected | Fix dates needed for 75-100 CVEs: pre-filled from vendor sources (GitHub, Microsoft, Cisco, Palo Alto; 54 of 175 in Q2-Q3 2026), with flagged cases (fix possibly later than the advisory, or no source) hand-checked: about 60 a quarter, or a random sample of them. Looks only at flaws that were exploited (answers "how fast after a fix are exploited flaws attacked", not "what share get exploited"). Overlaps T3 where fix and publication are the same day. |
| **(b) Keep as registered** | Cohort only | 0-1 exploited | No change to the plan | Almost always "no estimate"; the central question goes unanswered |
| **(d) Weighted cohort** (back-tested below) | Same as registered, but picks favour flaws EPSS rates as likely to be exploited; re-weighted so it still describes all eligible flaws | 2-3 exploited of 9 race picks (6-7 of 18) | More exploited flaws in the cohort, which can then be followed end to end with exposure data | Estimates far too uncertain from one quarter (see below); breaks the locked rule that EPSS is never used for selection; the cohort's other figures would also need weighting |
| **(c) Larger cohort** | Same as registered | would need roughly 2,000 picks for ~10 exploited | Keeps a random sample | Far too much hand work; still few events |

## What option (a) would have shown (preview, corrected 2026-10-23)
Fix date approximated by the CVE publication date (the real version uses vendor-sourced and
hand-checked fix dates). Every CVE first added to KEV in the quarter is counted, including
older CVEs (an earlier version of this preview left those out):

| | Q2 2026 | Q3 2026 |
|---|---|---|
| CVEs first exploited in the quarter | 75 | 100 |
| Attacked on or before the fix (zero-day share, a minimum) | 16% | 23% |
| Median days from fix to first attack | at least 15 | at least 8 |

## What changes if (a) is adopted
- T1(a) headline: share of the quarter's newly exploited flaws attacked before a fix
  existed, plus the median days from fix to exploitation (Kaplan-Meier not needed: every
  case has an exploitation date).
- Hand work: about 60 flagged fix dates per quarter (mostly a quick "was the fix out at the advisory?" check), or a random sample of them; to be settled on 12 Nov.
- The cohort stays as is for exposure (T1b, T2), the root-cause tag and AI-vs-human
  comparisons.
- Logged as a deviation, reported alongside the registered cohort version (which will
  mostly read "no estimate") for four quarters, per the change policy.

## Back-test: weighted cohort (d) against the registered cohort and (a), Q2 and Q3 2026
Run 2026-10-22 (`src/snapshot/backtest_t1.py`, results in
`proposals/backtest_t1_2026Q2-Q3.json`). 2,000 simulated draws per design and quarter on
the real eligible CVEs, compared with the true value computed on every eligible CVE.
Simplifications: fix date = publication date; exploitation = CISA KEV only; EPSS from
weekly snapshots; the slot c internet-facing check and slot d are not simulated.

**True values** (all eligible CVEs exploited within 90 days):
Q2: 35 of 4,804 exploited; 14% before the fix; median 9 days.
Q3: 41 of 9,812 exploited; 24% before the fix; median 2 days.

**What one quarter's sample would show** (range = 90% of simulated quarters):

| Design | Race picks | Exploited picks (avg) | Share before fix: range | Median days: range |
|---|---|---|---|---|
| (b) registered, 1 per slot | 9 | Q2 0.3 / Q3 0.4 | 0-100% | 0-64 |
| (b) registered, 2 per slot | 18 | 0.6 / 0.9 | 0-100% | 0-64 |
| (d) EPSS at +7 days, floor 0.01, 1 per slot | 9 | 2.2 / 2.6 | 0-100% | 0-21 |
| (d) EPSS at +7 days, floor 0.001, 1 per slot | 9 | 3.3 / 3.2 | 1-100% | 0-21 |
| (d) EPSS at draw date, floor 0.01, 1 per slot | 9 | 2.9 / 2.8 | 0-100% | 0-64 |
| (d) EPSS at +7 days, floor 0.001, 2 per slot | 18 | 6.7 / 6.5 | 3-87% | 0-45 |
| (d) same, pooled over both quarters | 36 | 13.2 | 4-80% | 0-45 |
| **(a) all first exploited in the quarter** | none (all used) | Q2 75 / Q3 100 | **16% / 23%** | **at least 15 / 8** |

**Findings**
1. Weighting works as intended for its narrow goal: 7-10 times more exploited flaws in the
   cohort (2-3 per quarter instead of 0.3-0.4).
2. It does not give a usable race number. Even 18 weighted picks per quarter, or 36 over
   half a year, leave the zero-day share anywhere between a few percent and over 80%.
   Two reasons: few exploited picks, and large weights on the occasional low-EPSS
   exploited pick swing the estimate. EPSS a week after publication separates exploited
   flaws only moderately (top 10% of scores holds about 70% of later-exploited flaws).
3. Option (a) gives a stable number directly from about 60-90 flaws per quarter.
4. Cost of (d): it breaks `outcome_data_used_for_selection: false` (EPSS is named in the
   locked rule), and the cohort's other figures (root cause, AI vs human) would need the
   same re-weighting, making them noisier.

**Where (d) still adds value, a combined option (a+d)**: use (a) for the T1(a) number, and
the weighted draw only if the goal is to follow more exploited cohort flaws end to end
with exposure data (T1b: did exposed systems get patched before attacks started?), as
described cases rather than estimates. Whether that is worth breaking the EPSS rule is a
question for 21 Dec; it needs exposure data (Shadowserver) to pay off at all.

## Corrections and refinements from the research window (2026-10-23)
See `docs/RESEARCH_PLAN.md` (Findings) for details.
- The option (a) preview left out older CVEs first exploited in the quarter. Counting them,
  the median is at least 15 days (Q2) and 8 days (Q3), and the zero-day share 16% (Q2) and
  23% (Q3), instead of 8 / 5 days and 21% / 25%.
- KEV-based zero-day shares are lower bounds (KEV waits for remediation guidance; Mandiant's
  incident-response data finds 70% zero-days in 2023). VulnCheck's 23.4% for 1H 2026 is close
  to ours.
- T_exploit can be improved for free with CISA's "active exploitation" flag, which predates
  the KEV listing by a week or more for about 1 in 10 KEV CVEs.
- Fix dates: free vendor sources date 54 of 175 exploited CVEs (GitHub alone: 18); cases
  where the fix shipped after the advisory are detectable from revision histories and go to
  the hand check.

## Option (a) and exploratory measure X10 (decision items 0 and 7)
X10 ("exploited before a fix existed") and option (a)'s headline are the same number: the
share of the quarter's newly exploited CVEs attacked on or before the fix date. They differ
only in status. X10 is exploratory: reported, labelled, never decides Improving/Worsening.
Option (a) would make it part of the scored race (T1), so it would carry a label.

What the numbers support (Q2-Q3 2026 back-test):
- **Precision.** With 75-100 flaws a quarter, a share near 20% has a 90% interval of about
  plus or minus 7 percentage points. Only shifts larger than that can be called a trend.
- **Bias.** The share is a minimum: CISA lists a flaw only once a fix or guidance exists,
  and 88 of 175 fix dates still fall back to "assumed = publication". The CISA
  active-exploitation flag and vendor fix dates reduce both problems but do not remove them.
- **Stability.** 16% then 23% in consecutive quarters: inside the noise, so one year of
  quarters is needed before any label means much.

Ways to resolve the overlap on 21 Dec:
1. **Adopt (a), retire X10.** The zero-day share becomes the scored race headline; X10's id is
   kept as an alias so earlier references still resolve.
2. **Adopt (a) for the median days only; keep X10 exploratory.** The scored race uses the
   less biased timing figure; the zero-day share is reported but cannot set a label until a
   year of data shows it is stable. Can be promoted at the March 2027 review.
3. **Keep T1 as registered; keep X10 exploratory.** The zero-day share is reported every
   quarter but nothing about the race is scored.

## Decision (author, 23 Oct 2026)
Resolution 2 above: option (a) is adopted for the median days from fix to first attack,
measured on every CVE first added to CISA KEV in the quarter (older CVEs included). The
zero-day share stays exploratory as X10, reported every quarter, and is a promotion
candidate at the 15 March 2027 review once a year of data shows it is steady. The cohort
and the rule that EPSS never selects flaws are unchanged (option d not adopted). The
registered cohort version of T1(a) is reported alongside for four quarters. Logged in
`prereg/DEVIATIONS.md`; confirmed and frozen at the 21 December session.


## Note on the direction of the bounds (2026-10-24)
Two biases pull the option (a) median in opposite directions, so the previews' wording needs
a qualifier rather than a change:
- **Missing dates (why the previews say "at least").** Older CVEs first exploited in the
  quarter were counted without their publication dates (as "published before 2025"), so the
  Q2 and Q3 medians (15 and 8 days) are lower bounds. This disappears once option (a) fetches
  the record of every KEV addition, as planned.
- **KEV delay (the other way).** KEV lists a flaw after its first exploitation, so days from
  fix to KEV listing overstate days from fix to first attack. Once every date is fetched, the
  median is an upper bound, unless quiet fixes released before the advisory are common enough
  to outweigh the delay. The zero-day share stays a minimum for the same reason.
Fix and attack dates are to be stored as intervals (`docs/STATISTICAL_REVIEW_2026-10-24.md`,
point 6), so each published median and share carries both bounds.
