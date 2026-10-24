# Internet Security Snapshot: Statistical Review of EVAL-2026-ISS-01 and 2027 Implementation Plan

Oct 24, 2026 · @Paul

## Bottom line

Do not adopt EVAL-2026-ISS-01 as written. Its headline change, EPSS-weighted sampling for Track A, was already back-tested in the repo on 22 Oct and rejected on 23 Oct for good reasons, and two of its ten items contradict the registered plan. About half of it is still worth taking, reframed as exploratory measures and quality checks that need no change to the locked core.

The evaluation reads as generic advice written without the repository: it treats bootstrap intervals, Kaplan-Meier censoring and Cohen's kappa as missing when the plan already has them, and it targets a 15 March 2027 change window while proposing side-by-side reporting from Q1 2027.

What to do, in order:

1. **Keep the 23 Oct decision** on the race: option (a) on every newly attacked flaw; no EPSS in selection. My re-run of the back-test with the proposal's exact weights is in the next sections.
2. **Fix the reproducibility gap now.** The pre-registration promises a pinned lockfile; the repo has none (`pyproject.toml` uses `>=` ranges). Add a lockfile and a pinned container before the 1 Dec dry run.
3. **Add a second coder** for a random slice of hand checks, scored with raw agreement and Gwet's AC1 alongside kappa, and raise the test-retest set from 5 to 20 items.
4. **Report fix-date and exploit-date uncertainty as bounds** (interval censoring), propagated into the race median.
5. **Put the labelling rule on the 21 Dec agenda.** A simulation shows it labels pure noise about 48% of the time; the proposal never examined it. A companion test cuts that to 10% without changing the registered rule.
6. **Add one exploratory population analysis**: time to KEV listing across all \~10,000 serious flaws a quarter, by AI-credit status. It has about 800 times more flaws than the 12-flaw cohort, but power depends on attacks: in Q2 to Q3 2026 none of the 102 AI-credited serious flaws reached KEV, so for now it can compare severity and bug type and give an upper bound on attack rate, not answer whether AI-found flaws are attacked sooner.

All of this fits the calendar you already have: no new sessions, about 20 minutes added to the 21 Dec agenda, and no change to the March 2027 window.

## How the proposal fits the project as it stands

The proposal diagnoses the right three weaknesses but prescribes against a version of the project that no longer exists. Checked against the repository at commit `eaec47b` (23 Oct 2026, 21:01):

**Diagnoses that hold**

- Track A's cohort yields 0.3 to 0.4 attacked flaws a quarter, too few for a race median. The repo found this first (`proposals/T1_OPTIONS.md`) and has already moved the race to Track B.
- KEV is a delayed, incomplete exploitation signal. The repo already treats the zero-day share as a minimum for this reason.
- Hand checks by one person are a validity risk. The current safeguard (five re-shown items a quarter) measures only consistency, and five items is too few to measure even that.

**Where it misreads the plan**

| Proposal says | Repo already has | Consequence |
| --- | --- | --- |
| Point estimates lack uncertainty | 90% bootstrap, 2,000 resamples, clustered by CVE (prereg §4.3, §9) | Item 3 is mostly done |
| Unexploited flaws should be censored | Kaplan-Meier with right-censoring for T1, T2, T3 (§9) | Item 1 adds covariates, not censoring |
| 5-quarter window invites seasonal artefacts | STL on monthly series backfilled from 2017 (CVE) and 2021 (KEV) | Item 5 solves a problem the design avoided |
| Kappa is absent | Cohen's and Fleiss' kappa already used for source agreement (I6) | Item 8 extends an existing tool |
| EPSS weighting is the fix for Track A | Back-tested 22 Oct, rejected 23 Oct; race moved to all newly attacked flaws | Item 2 reopens a closed, logged decision |
| Missing sources can be imputed | "Gaps are never filled by estimation" (prereg §6) | Item 7 would breach the registration |
| Strata are root-cause groups | Strata are product slots a to d by month; root cause is never used to select | The sampling maths is set up on the wrong frame |
| Change goes in at the 15 Mar 2027 review with side-by-side reports from Q1 2027 | Core changes before 31 Dec 2026 are still open; after that, March only | Timeline is internally inconsistent |

**Two claims that are wrong as stated**

- "Horvitz-Thompson weighting mathematically guarantees that overall population metrics remain unskewed." Unbiased in expectation, yes. But with one pick per stratum the variance balloons and cannot even be estimated from the sample (one unit per stratum leaves no within-stratum spread). The next section measures it.
- "Expected yield rises to \~2.5 to 3.5 flaws a quarter." That figure matches the repo's design with EPSS weights and a floor, not the proposal's square-root weights, which flatten selection. Re-run below: 1.2 to 1.5.

## EPSS importance sampling, re-tested

Even with the proposal's exact formula, EPSS weighting does not produce a usable race number, and it makes every other cohort figure noisier. I re-ran the repo's own back-test with fresh data; the uniform and repo-EPSS designs reproduce the committed results to two decimals (0.31 and 2.17 attacked picks in Q2), so the comparison is like for like.

&#91;embedded content: Re-run of src/snapshot/backtest\_t1.py on CVE records (cvelistV5), CISA KEV and weekly EPSS pulled 24 Oct 2026 · Q2 and Q3 2026\]

The square root flattens the weights, so fewer high-EPSS flaws are drawn than the proposal assumes. More importantly, yield was never the binding problem:

| What one quarter's weighted sample would show | Q2 2026 | Q3 2026 |
| --- | --- | --- |
| Chance of at least one attacked pick | 85% | 82% |
| Zero-day share, 90% of simulated quarters | 0% to 100% | 0% to 100% |
| Median days fix to attack, 90% range | 0 to 40 | -1 to 35 |
| True values (all eligible flaws) | 14%, 9 days | 24%, 2 days |
| Option (a), every newly attacked flaw | 21%, 8 days (n = 57) | 25%, 5 days (n = 91) |

**The cost to the rest of the cohort.** Within a stratum, the proposal's weights differ by a factor of 15 to 29 at the median and up to 58, so a single low-EPSS pick can swing a quarter. With the plain Horvitz-Thompson estimator the proposal specifies, the cohort's mean CVSS has a sampling SD of 1.28 to 2.11 against 0.34 for the registered draw (variance 15 to 38 times larger). This part is fixable: the normalised (Hajek) estimator, which divides by the sum of the weights rather than N, brings that inflation down to about 1.1 times. So it is a reason to reject the proposal's estimator, not weighting itself. What no estimator fixes is the race number, already computed with normalised weights in the table above: too few attacked picks to say anything in one quarter.

**Why EPSS cannot do better here.** In both quarters the top tenth of EPSS scores a week after publication held 69% to 73% of the flaws later attacked. The other 27% to 31% are exactly the picks that get huge weights and swing the estimate. There is also a circularity the proposal does not mention: EPSS is a model trained on exploitation evidence, and its model version changes over time, so selection probabilities would drift with the scoring model rather than with the threat.

**Where weighting could still earn its place.** If Shadowserver exposure data arrives, a small set of attacked flaws followed end to end (exposure before and after the attack) is valuable as described cases, not estimates. That is the repo's option (a+d). It can be revisited at the 15 Mar 2027 review if the permission comes through; it does not belong in the core now.

## The ten recommendations

Three adopted, two adapted, five rejected; none of the adopted or adapted items needs a change to the locked core.

| # | Recommendation | Verdict | Why | What to do instead | Core change? |
| --- | --- | --- | --- | --- | --- |
| 1 | Cox model, unexploited flaws right-censored | Adapt | Track B contains only attacked flaws, so there is nothing to censor; KEV's lateness is error in the event date, not censoring | Exploratory X13: time to KEV listing across all \~10,000 eligible flaws a quarter (Kaplan-Meier, then Cox with AI-credited, slot, root cause, CVSS). About 40 KEV events a quarter, none yet among AI-credited flaws (0 of 102 in Q2 to Q3 2026), so pool quarters, report event counts and an upper bound, and compare severity and bug type meanwhile; detecting a doubled hazard needs about 2,000 events | No |
| 2 | EPSS-weighted importance sampling | Reject | Re-run above: 1.2 to 1.5 attacked picks, race range 0% to 100% under any estimator; plain HT makes other figures 4 to 6 times noisier (Hajek fixes that part); breaks the locked no-EPSS rule | Keep option (a). Revisit (a+d) as described cases only if Shadowserver says yes | Would be |
| 3 | Bootstrap and Monte Carlo intervals | Adapt | Bootstrap is already registered; what is missing is input uncertainty | Monte Carlo over fix-date intervals (item 10) and the T7 floor-to-ceiling range. For medians of small samples, use the exact order-statistic interval, not the bootstrap, which is unreliable below \~20 cases | No |
| 4 | Bayesian misclassification model for AI share | Reject | Needs sensitivity and specificity against a ground truth. Re-asking the same coder measures consistency, not accuracy; with no truth the priors would decide the answer | Keep the floor-to-ceiling bounds, an honest partial-identification answer. Revisit if a validation set appears (finders' write-ups that state the method) | Would be |
| 5 | Bayesian structural time series | Reject | Monthly series already run from 2017 with STL; the weak point is the labelling rule, not the decomposition | Next section: a companion test on the label | No |
| 6 | Difference-in-differences or synthetic control for AI | Reject | No treatment date and no untreated unit: AI tools spread across all software at once, so parallel trends cannot be checked or defended | Keep the registered no-causal-claim wording. X13 gives an adjusted, descriptive AI-vs-other comparison | Would be |
| 7 | Multiple imputation for missing sources | Reject | A whole missing source is not missing-at-random item data, and imputing it breaches prereg section 6: gaps are never filled by estimation | Keep Plan 1 / Plan 2: report the gap | Would breach |
| 8 | Second annotator and Cohen's kappa | Adopt | Sound, and close to the promised external review. Kappa misleads at skewed prevalence: 28 agreements out of 30 can score kappa 0.46 | Second coder on 20 random hand-check items a quarter; report raw agreement, Gwet's AC1 and positive/negative agreement beside kappa; fix dates scored as agreement within one day. Raise re-shown items from 5 to 20 | No |
| 9 | Pin the environment in Docker by digest | Adopt | Prereg section 9 promises a pinned lockfile; the repo has none, and Actions are pinned by tag, not commit | Hash-locked requirements, a container pinned by digest, Actions pinned by commit SHA, the digest written into every manifest | No (bug fix) |
| 10 | Interval censoring of release and exploit dates | Adopt | True fix date lies between the earliest vendor evidence and the advisory; true attack date is on or before the KEV or CISA-flag date. Point dates hide this | Store both ends, report the race median as a bound pair, and fit Turnbull's estimator (lifelines fit\_interval\_censoring, already a dependency) | No |

Items marked Would be or Would breach could only enter at the 21 Dec session or a March review, under the side-by-side rule; I recommend none of them.

## The gap the proposal missed: the labelling rule

The registered rule calls a direction in about 48% of quarters when nothing has changed, so with seven questions almost every report will carry at least one false label. The pre-registration calls the rule loose; it has not measured how loose.

&#91;embedded content: Simulation by Claude, 24 Oct 2026 · independent normal noise unless stated; autocorrelated = AR(1), rho 0.5; script in Appendix\]

Under no change, the chance that at least one of the seven questions is labelled in a given quarter is 99%. Autocorrelation, which quarterly security series will have, raises the single-question rate to 61%. The rule does detect real trends quickly, which is what it was chosen for, but its labels cannot be read as evidence on their own.

The companion test compares the mean of the last two quarters with the mean of the four before, at 90%. It holds false alarms near 10% and still catches a half-SD-a-quarter trend 53% of the time and a one-SD trend 97% of the time.

**Recommendation for 21 Dec.** Keep the registered rule, so nothing registered changes, and report beside every label whether the companion test supports it (supported / not supported). This is a reporting addition, not a rule change, but it is worth logging before the freeze so it cannot look chosen after seeing results. For proportions such as T7 and the zero-day share, run the test on the published intervals (for X10, plus or minus about 7 points a quarter).

## Implementation plan

Everything that changes how the pilot is computed is built before the 1 Dec dry run and logged at the 21 Dec freeze session, so no addition can look chosen after seeing results. Claude does the building; your time is about 1 hour across the existing November sessions plus 20 minutes added to the 21 Dec agenda.

&#91;embedded content: Plan mapped onto the existing Snapshot calendar (24 Oct 2026 to 1 May 2027)\]

The RV trip (6 to 18 Dec) falls between the dry run and the freeze session, so all five build items must be merged by 4 Dec, the day of the landing-page session.

**What each item delivers and how it is checked**

1. **Reproducibility (by 20 Nov).** Hash-locked requirements file generated from `pyproject.toml`, a container image pinned by SHA-256 digest, every GitHub Action pinned to a commit SHA, and the image digest written into each run manifest. Check: two clean builds produce byte-identical outputs on the Q3 2026 test data. Logged as a bug fix against prereg section 9.
2. **Interval dates (by 27 Nov).** Each race flaw stores `fix_lo`, `fix_hi` (earliest vendor evidence to advisory) and `exploit_hi` (KEV date, or the CISA active-exploitation flag date when earlier). The report shows the race median as a pair of bounds plus Turnbull's estimate. Check: on Q2 to Q3 2026, recompute the previews with every older flaw's publication date fetched. The previews' 'at least 15 and 8 days' are correct lower bounds, because older flaws were counted without those dates; once they are in, KEV's delay makes the median an upper bound instead. The zero-day share stays a minimum.
3. **Companion label test (by 27 Nov).** Two-quarters-versus-prior-four test at 90% for every labelled question, published as supported or not supported. Check: reproduces the simulation's 10% false-alarm rate on synthetic null series in the test suite.
4. **Hand-check quality (by 27 Nov).** Re-shown items raised from 5 to 20 a quarter (about 8 extra minutes), and a blinded export of 20 random decisions for a second coder. Report raw agreement, AC1, positive and negative agreement, and kappa. The second coder can be the external reviewer you are lining up on 12 Jan.
5. **X13 exploratory survival analysis (by 4 Dec).** Time from publication to first KEV listing across all eligible serious flaws, by AI-credit status, slot, root cause and CVSS, backfilled for Q4 2025 to Q3 2026. Definition entered in `config/exploratory.yaml` with today's date before any result is computed. It replaces the 12-flaw secondary comparison. Severity, remote-code-execution share and bug type are well estimated now; time to KEV is reported pooled with its event count, and nothing is promoted until the AI-credited group has at least 10 to 20 events.

**What stays as it is.** The race on all newly attacked flaws, the no-EPSS selection rule, the zero-day share as exploratory X10, the T7 floor-to-ceiling range, and the March-only change window.

## Decisions for you

- [ ] Go-ahead for the five build items. This session has read-only access to the repo, so either attach it with push access or I prepare the changes as files for you to commit.
- [ ] Keep EPSS weighting out of the core (confirms the 23 Oct decision; nothing to log).
- [ ] Add two items to the 21 Dec agenda: item 19, the companion label test (report only); item 20, X13 and the hand-check agreement measures (exploratory and quality, no label effect).
- [ ] Second coder: ask the external reviewer candidate on 12 Jan, or name someone else.
- [ ] Open question: who wrote EVAL-2026-ISS-01, and should they get a written response? It names no author, so it cannot stand in for the external reviewer the pre-registration promises.

* [ ] Review the note added to proposals/T1\_OPTIONS.md: the previews' 'at least' is right (older flaws lacked publication dates); with those dates fetched, KEV's delay will make the median an upper bound.

The corrected wording for each evaluation point is in Review points (24 Oct).

## Appendix: methods

**Back-test re-run.** Population, follow-up and simplifications exactly as in `src/snapshot/backtest_t1.py` (fix date = publication date; exploitation = CISA KEV within 90 days; slot c internet-facing check and slot d not simulated). Data pulled 24 Oct 2026: cvelistV5 records for 2025 and 2026 (125,248 records, parsed with the repo's own `build_table`), CISA KEV JSON, 30 weekly EPSS files from 3 Apr to 23 Oct 2026. Proposal weights w = EPSS^0.5 + 0.01 with EPSS taken 7 days after publication (and, separately, at the draw date); one pick per slot and month; Hansen-Hurwitz re-weighting; 2,000 simulated quarters; seed 20261020 as in the repo. Non-race figures used the Horvitz-Thompson total divided by N.

**Label simulation.** 200,000 series of 7 quarters; registered rule as in prereg section 4 (direction = sign of the quarter minus the median of the four before; label when two consecutive directions agree). Companion test:

```latex
z = \frac{\tfrac{1}{2}(x_{t-1}+x_t) - \tfrac{1}{4}(x_{t-5}+\dots+x_{t-2})}{\sigma\sqrt{1/2 + 1/4}}, \qquad \text{supported if } |z| > 1.645 \text{ and the sign matches the label}
```

In practice σ is the quarter's published bootstrap standard error.

**Agreement example.** 30 items, both coders Yes on 27, No on 1, split on 2: raw agreement 93%, Cohen's kappa 0.46, Gwet's AC1 0.92, PABAK 0.87. Test-retest: if all n re-shown items match, the one-sided 90% lower bound on consistency is 0.1^(1/n): 63% at n = 5, 89% at n = 20.

**Scripts.** `label_sim.py` and `proposal_backtest.py`, with the JSON output, are in this session's workspace and can be added to `proposals/` with the build items.

## Sources

- [pagagne/internet-security-snapshot](https://github.com/pagagne/internet-security-snapshot), commit eaec47b (23 Oct 2026): `prereg/PREREGISTRATION.md`, `prereg/DEVIATIONS.md`, `proposals/T1_OPTIONS.md`, `proposals/backtest_t1_2026Q2-Q3.json`, `docs/CHANGE_POLICY.md`, `docs/CORE_FREEZE_DECISIONS.md`, `pyproject.toml`
- [OSF registration, DOI 10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82)
- [CVEProject/cvelistV5](https://github.com/CVEProject/cvelistV5)
- [CISA KEV data](https://github.com/cisagov/kev-data)
- [FIRST EPSS daily scores](https://epss.empiricalsecurity.com/)
- Attached: Internet Security Snapshot: How It Works (23 Oct 2026); EVAL-2026-ISS-01 Statistical Evaluation and Methodological Enhancement Program
