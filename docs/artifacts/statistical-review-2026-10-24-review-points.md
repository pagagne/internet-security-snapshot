# Review points, 24 Oct 2026

Nine justifications for the evaluation, corrected against the re-run back-test and the repo. Fixes from the draft notes: the race bounds are now stated precisely (the previews are lower bounds because older flaws lacked publication dates; KEV's delay pushes the final measure the other way), and the zero-day share spans roughly 0 to 100% in every nine-pick design.

## 1. Modest yield gain, no usable race estimate

The square-root weighting (√EPSS + 0.01) flattens selection compared with linear EPSS weighting. Re-running the back-test on Q2 to Q3 2026 data, attacked-flaw yield rises from about 0.35 to about 1.4 per quarter, not the claimed 2.5 to 3.5. That is too few to estimate the race: across simulated quarters the zero-day share ranged from 0% to 100%, and the median days from fix to attack from 0 to 40 (Q2) and -1 to 35 (Q3). The proposal's plain Horvitz-Thompson estimator also makes some cohort figures far noisier (mean CVSS variance 15 to 38 times higher), though a normalised (Hájek) estimator removes most of that (about 1.1 times). If EPSS weighting is ever revisited at a March review, for following attacked flaws end to end once Shadowserver data arrives, it should use the Hájek estimator.

## 2. Model dependence and design drift

EPSS is a predictive model of exploitation that FIRST retrains and re-versions (four versions since 2021). Weighting selection by it makes the sample depend on the current model version and partly on early exploitation signals. Weighted estimates stay unbiased, but the composition and precision of each quarter's sample would shift with model updates. Quarter-to-quarter comparisons would then mix threat changes with model changes, and each draw would require recording the exact EPSS version and score date to be reproducible.

## 3. Departure from the registered selection rule

The registration states that selection never uses EPSS or other outcome measures (section 7.2). EPSS weighting would reverse that principle; under the change policy it could only enter as a logged deviation with four quarters of side-by-side reporting, for little gain. The 23 Oct decision instead measures the race on every flaw first added to CISA KEV in the quarter (75 to 100), leaving Track A's random selection untouched. That removes the need to sample attacked flaws, but not the uncertainty: estimates still carry bootstrap intervals (about ±7 points on the zero-day share), KEV-based dates make the zero-day share a minimum and overstate the median days (the true first attack comes earlier), and the measure describes attacked flaws only, not the share of serious flaws that get attacked.

## 4. Primary race metric: Track B rather than Track A

**What is compared:** measuring the race (median days from fix to first attack) on every flaw first added to CISA KEV in the quarter (Track B, 75 to 100 flaws) versus the sampled cohort (Track A).

**Justification:** Track A yields too few attacked flaws to estimate a median: 0.3 to 0.4 a quarter under the registered draw, about 1.4 under the proposed √EPSS weights and 2.2 to 2.6 under linear EPSS weights. With nine race picks a quarter, the zero-day share spans roughly 0 to 100% across simulated quarters in every design. Track B covers every newly listed attacked flaw, so no sampling design is involved and an estimate exists every quarter, with precision of about ±7 points on the zero-day share. Track A's random selection is untouched; the redefinition of T1(a) is logged as a deviation (23 Oct 2026) and reported beside the registered version for four quarters.

**Limits:** the measure describes attacked flaws only, not the share of serious flaws attacked; it covers all KEV additions, including older and lower-severity CVEs; and because KEV dates come after the first attack, the zero-day share is a minimum and the median days is overstated: an upper bound once every flaw's publication date is fetched (the Q2 to Q3 previews are lower bounds only because older flaws lacked those dates).

## 5. False alarm rate of the directional labelling rule

**What is evaluated:** how often the registered rule (same side of the 4-quarter baseline median for two consecutive quarters) assigns a direction label when nothing has changed.

**Justification:** in 200,000 simulated series with no true change, the rule labels a direction in 48% of quarters under independent normal noise and 61% under moderate autocorrelation (AR(1), ρ = 0.5); across seven questions, at least one false label appears in about 99% of quarters. A companion two-sided test at the 10% level, comparing the mean of the last two quarters with the mean of the four before, holds false alarms to 10% (14% under the same autocorrelation). The cost is slower detection: a trend of 0.5 SD a quarter is flagged 53% of the time, against 76% by the registered rule; trends of 1 SD a quarter are flagged about 97% of the time by both.

**Proposal:** keep the registered rule and report beside each label whether the test supports it, using each quarter's bootstrap standard error; a reporting addition, logged at the 21 Dec 2026 session before any quarter is scored.

## 6. Date uncertainty: intervals, not points

**What is evaluated:** whether fix and attack dates should be stored as single dates or as bounds.

**Justification:** fix dates are uncertain in both directions (quiet patches before the advisory; advisories before the patch ships), so each is stored as an interval \[fix\_lo, fix\_hi\]. Attack dates have only an upper bound: the KEV listing or CISA active-exploitation flag, whichever is earlier, so each attack time is left-censored at exploit\_hi. The zero-day share is then reported as a range (definite zero-days to definite plus uncertain cases), and the race median as an upper bound with its range. Turnbull's estimator can be shown as a sensitivity analysis, noting that it assumes detection delay is unrelated to the outcome, which KEV's longer delay for zero-days violates. The Q2 to Q3 2026 previews ('at least 15 and 8 days') are correctly labelled lower bounds, because older flaws were counted without their publication dates; once those dates are fetched, KEV's delay makes the median an upper bound instead, unless quiet early fixes outweigh it.

## 7. Reliability of hand checks

**What is evaluated:** raising the re-shown items from 5 to 20 a quarter, and adding a second, blinded coder for 20 items a quarter.

**Justification:** with 5 re-shown items, even perfect agreement only supports consistency of at least 63% (one-sided 90% bound); with 20 it supports at least 89%. Re-showing measures one coder's consistency; only a second coder can reveal a systematic bias, so both are needed. Yes/no checks (internet-facing, AI-credit edge cases) are reported as raw agreement, Gwet's AC1, Cohen's kappa, and agreement on Yes and No separately, because kappa understates agreement when one answer dominates. Fix dates are reported as the share within one day and the median difference in days. Items for the second coder oversample uncertain cases and are weighted back for the overall figure; results are pooled over the year for the March review.

## 8. Reproducibility: pinned environment and a standing check

**What is evaluated:** whether each quarter's published figures can be recomputed from its frozen data bundle.

**Justification:** the registration promises package versions pinned in a lockfile (section 9), but pyproject.toml uses >= ranges with no lockfile, and workflows pin GitHub Actions by movable major-version tags and Python by minor version, so the environment drifts between runs. The fix: a hash-locked requirements file, a container pinned by SHA-256 digest and archived with each Zenodo release, Actions pinned by commit SHA, and the digest written into every run manifest. Because floating-point results and file metadata can still vary, the target is identical published figures at reporting precision, verified by a scheduled job that rebuilds the latest quarter from its frozen bundle in a clean container. Committed build folders are removed.

## 9. AI-credited versus other flaws: population-level comparison

**What is evaluated:** moving the comparison from the 12-flaw cohort to all serious flaws published in the quarter (about 5,000 to 10,000).

**Justification:** the cohort holds at most three AI-credited flaws a quarter, too few for any comparison. Across the full population, flaws are plentiful (21 and 81 AI-credited serious flaws in Q2 and Q3 2026) but KEV listings are rare: none of the AI-credited flaws and 76 of about 14,500 others were listed within 90 days. Precision for time-to-KEV comparisons depends on events, not flaws: detecting a doubled hazard with 80% power needs about 2,000 events, years of data at current rates. The analysis therefore (1) compares severity, remote-code-execution share and bug type, which need no events and are already well estimated; (2) reports time to KEV listing pooled across quarters, with event counts and an upper bound while AI-credited events are few (0 of 102: at most about 3% at 95%); (3) adjusts for product slot, vendor type, CVSS and bug type, under both AI-credit definitions; and (4) makes no causal claim, since AI tools search different code than attackers target.
