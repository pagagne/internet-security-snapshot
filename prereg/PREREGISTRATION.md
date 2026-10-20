# Pre-registration: Quarterly Internet Security Snapshot

**Status:** DRAFT — to be frozen on OSF no later than 31 October 2026, 23:59 UTC.
**Author:** Paul (GitHub: PAGAGNE). Code and drafting assistance: Claude (Anthropic).
**Version:** 0.1 (draft)

Once frozen, this file is not edited. Any change is recorded in `prereg/DEVIATIONS.md`
with a date and reason, and the frozen original stays in place.

---

## 1. Research question

The combined report argues that the internet will be cleaned up, but painfully. This
study tests that claim with one central question: **are defenders closing
internet-exposed vulnerabilities faster than attackers start exploiting them?** Four
supporting hypotheses test whether exploited weaknesses are old, whether discovery
pressure is peaking, and whether visible harm is falling.

## 2. Design summary

- Unit of evaluation: the calendar quarter.
- Data: free sources that keep their own history (Section 6).
- Runs: an automated pull at 06:00 UTC on 1 January, 1 April, 1 July and 1 October
  covering the previous quarter (provisional), and a re-run one month later (final).
- Pilot quarter: Q4 2026. This plan is frozen after Q4 began, so Q4 results are
  published but labelled **pilot** and do not count toward the confirmatory record.
- First confirmatory quarter: Q1 2027 (provisional 1 April 2027, final 1 May 2027).
- Dry run: 1 December 2026 on October–November 2026 data, unscored.

## 3. Hypotheses

| ID | Hypothesis | Supports cleanup if | Weakens cleanup if | Report timeline expects |
|---|---|---|---|---|
| H1 | Defenders are winning the race: for cohort vulnerabilities, exposure halves before exploitation starts. | Share of cohort CVEs whose vulnerable count halved before first observed exploitation is above the trailing-four-quarter baseline. | Share is below baseline, or 0% for two consecutive quarters. | Low, under 20% |
| H2 | Exposure is shrinking faster after patches. | Median exposure half-life of cohort CVEs is shorter than the trailing-four-quarter median. | Median half-life is longer than baseline. | No improvement yet |
| H3 | Exploited weaknesses are old. | At least 60% of CVE-labelled honeypot exploitation (Shadowserver) targets CVEs more than 12 months old. | Under 40% does. | At least 60% |
| H4 | Discovery pressure is peaking. | Seasonally adjusted year-over-year growth in published CVEs for the quarter is below the trailing-four-quarter average growth. | Growth is above it. | Still accelerating |
| H5 | Visible harm is falling. | Seasonally adjusted ransomware leak-site postings AND SEC 8-K Item 1.05 filings per 1,000 registrants are both below baseline. | Either is above baseline. | At or above baseline |

H3 values between 40% and 60% are recorded as **inconclusive** regardless of the
confidence interval.

### Interpretation of mixed results (fixed in advance)

- H3 supported while H1 and H2 are not: supports the report's core claim that fixes are
  known but remediation capacity is the bottleneck.
- H5 falls before H1 and H2 improve: the drop is attributed more plausibly to
  enforcement or takedowns than to better hygiene, and is flagged as such.

## 4. Decision rule

1. For each hypothesis, compute the quarter's value and a 90% bootstrap confidence
   interval (2,000 resamples; clustered by CVE where the unit is a CVE).
2. Status is **supports cleanup** or **weakens cleanup** only if the whole interval lies
   on one side of the baseline; otherwise **inconclusive**.
3. Multiplicity: Holm correction across the five hypotheses each quarter, applied to
   the one-sided bootstrap p-values.
4. The headline evidence is the **trailing four quarters**. A single quarter is
   reported as a signal, not a verdict.
5. All five hypotheses are reported every quarter, whatever the result.

## 5. Scoring availability rules

- **H4, H5:** scored from the pilot quarter (years of history exist).
- **H1, H2:** scored only once at least five cohort CVEs in the trailing four quarters
  have a usable Shadowserver exposure series (Section 7.3). Until then they are
  reported descriptively with status **baseline building**.
- **H3:** scored from Shadowserver honeypot statistics. KEV additions by CVE age are
  reported alongside as a secondary, weaker measure and are never merged with it.

## 6. Data sources

All free. Each pull records retrieval time, SHA-256 and source version; git sources are
pinned by commit hash.

| Source | Use |
|---|---|
| CVE.org records (CVEProject/cvelistV5, git) | I5; cohort T0 |
| CISA KEV (cisagov/kev-data, git, and JSON feed) | I2, I4 (secondary), I6 |
| CISA Vulnrichment (cisagov/vulnrichment, git) | Cohort context |
| NVD API 2.0 | Severity and product matching |
| FIRST EPSS daily archive | Context; cohort EPSS(t) |
| VulnCheck KEV (community) | I2, I6 |
| Shadowserver public dashboard | I1 exposure series; I2, I4, I6 honeypot statistics |
| Vendor advisories (CSAF, MSRC, PSIRT pages) | Cohort T_patch |
| Exploit-DB, Metasploit, Nuclei templates, GitHub | Cohort T_poc |
| Cloudflare Radar | Context only |
| ransomware.live | I7a |
| SEC EDGAR | I7b |

A source that is unavailable is recorded as a gap. Gaps are never filled by estimation.

## 7. Cohort protocol

### 7.1 Eligibility
A CVE is eligible if: (1) it affects a product deployed on internet-facing systems;
(2) the vendor rates it critical, or its CVSS base score is ≥ 8.0; and (3) it was
published between the 1st and the 25th of its month.

### 7.2 Selection
Each month, in order of publication, the first eligible CVE in each of three categories
is selected: (a) firewalls, VPNs and remote-access gateways; (b) web applications,
file-transfer and collaboration servers; (c) any other product. Empty categories are
recorded as empty and never filled by hand. Category assignment uses the versioned rule
file `config/cohort_rules.yaml`, frozen with this document.

### 7.3 Events and follow-up
Each cohort CVE is followed for 90 days from T0. Events: T0 (first commit of the CVE
record or earlier vendor advisory), T_patch, T_poc, T_exploit (earliest dated record in
Shadowserver honeypot data, VulnCheck KEV or CISA KEV), T_kev, E(t) (Shadowserver daily
vulnerable count, if published) and EPSS(t). Events not yet observed at evaluation are
right-censored. A Shadowserver series is **usable** if it has a published count on or
within 7 days after T_patch and at least 30 days of subsequent data.

## 8. Indicators

| ID | Indicator | Denominator |
|---|---|---|
| I1 | Exposure half-life: first day the 7-day mean vulnerable count falls below 50% of the first count on/after T_patch | First published count on/after T_patch |
| I2 | Time from T0 to first observed exploitation | Cohort CVEs plus all CVEs added to KEV in the quarter |
| I3 | Race outcome: won (I1 reached before T_exploit), lost, open | Cohort CVEs with a usable exposure series |
| I4 | Share of CVE-labelled exploitation targeting CVEs > 12 months old | Shadowserver honeypot events with CVE labels in the quarter |
| I5 | Year-over-year growth in published CVE records (rejected excluded) | Same quarter in prior years; trailing four quarters |
| I6 | Agreement among CISA KEV, VulnCheck KEV and Shadowserver (Cohen's and Fleiss' kappa) and median lags | CVEs with any exploitation signal in the trailing two quarters |
| I7 | (a) ransomware postings; (b) SEC 8-K Item 1.05 filings per 1,000 active registrants | (a) seasonal baseline; (b) active registrants |

Context only, never scored: Cloudflare Radar bot shares; monthly Microsoft fix count;
EPSS distribution of the quarter's new CVEs.

## 9. Analysis plan

- **I1/H2:** per-CVE half-life as defined; median across CVEs by Kaplan-Meier, CVEs not
  halved by day 90 right-censored.
- **I2:** Kaplan-Meier from T0 to first exploitation, censored at evaluation date; per
  source and earliest signal.
- **H4, H5:** monthly series log-transformed and decomposed with STL; quarter compared
  with the same quarter in prior years and the trailing four quarters; PELT changepoint
  flags reported. H4 also reported excluding the five largest CNAs (sensitivity only).
- **Uncertainty:** 90% bootstrap intervals, 2,000 resamples, seed fixed in code.
- **Software:** Python 3.12; lifelines, statsmodels, ruptures, DuckDB; versions pinned in
  the lockfile at the frozen commit.

## 10. Baselines

Backfilled before the dry run and frozen with checksums: CVE publications from 2017;
KEV from November 2021; SEC Item 1.05 from December 2023; ransomware postings from 2023;
Shadowserver series as far back as published. For H1 and H2 the baseline is built from
the study's own cohort once the Section 5 threshold is met.

## 11. Validation

Before the first scored evaluation, the pipeline is run on five documented cases
(CVE-2024-3400; CVE-2025-3248; the two PaperCut flaws exploited by AI agents in 2026;
the Zammad flaws from the DIVD breach). Reference dates are recorded in
`prereg/ground_truth_reference.csv` before the run. Pass: for ≥ 4 of 5 cases, T_patch and
T_kev match exactly and T_exploit is within one day of the documented date, or a later
date is explained by free-source coverage.

## 12. Known limitations stated in advance

- Exposure data covers only CVEs Shadowserver chooses to track.
- Exploitation data sees opportunistic, automated activity, not targeted intrusions.
- Small samples: nine cohort CVEs a quarter at most.
- Conflict of interest: Claude, made by Anthropic, writes the code and drafts the
  evaluations; Anthropic is named in the report under test. Safeguards: this frozen
  plan, public code, author approval of every release, and an external reviewer for the
  first confirmatory quarter.
