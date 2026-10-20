# Pre-registration: Quarterly Internet Security Snapshot

**Status:** DRAFT. To be frozen on OSF no later than 31 October 2026, 23:59 UTC.
**Author:** Paul (GitHub: PAGAGNE). Code and drafting assistance: Claude (Anthropic).
**Version:** 0.2 (draft). Reframed from thesis-testing to monitoring.

Once frozen, this file is not edited. Any change is recorded in `prereg/DEVIATIONS.md`
with a date and reason, and the frozen original stays in place.

---

## 1. Purpose

This study does not set out to prove or disprove that the internet is being cleaned up.
It tracks, quarter by quarter, **whether internet security is getting better or worse,
and how AI is involved**, using free public data.

The central question is: **are defenders closing internet-exposed vulnerabilities faster
than attackers start exploiting them?**

What this pre-registration fixes in advance is not a prediction but the definitions:
what each measure is, what counts as "better" or "worse", and when a change is called a
direction. That prevents choosing flattering numbers after the fact. Where the author
holds an expectation, it is recorded as a stated prediction that can turn out wrong.

## 2. Design summary

- Unit of evaluation: the calendar quarter.
- Data: free sources that keep their own history (Section 6).
- Runs: an automated pull at 06:00 UTC on 1 January, 1 April, 1 July and 1 October
  covering the previous quarter (provisional), and a re-run one month later (final).
- Pilot quarter: Q4 2026 (this plan is frozen after Q4 began). Its results are
  published and labeled **pilot**.
- First confirmatory quarter: Q1 2027 (provisional 1 April 2027, final 1 May 2027).
- Dry run: 1 December 2026 on October–November 2026 data, unscored.

## 3. Tracking questions

Each question has one primary measure. "Directional" questions are labeled
**Improving**, **Worsening** or **No clear direction** (Section 4). "Descriptive"
questions are labeled **Rising**, **Falling** or **No clear direction**, with no
judgment of good or bad.

| ID | Question | Primary measure | Type | Better means | Author's stated prediction |
|---|---|---|---|---|---|
| T1 | **The race (central).** Are defenders closing exposed vulnerabilities faster than attackers exploit them? | (a) Median days from T_patch to T_exploit across cohort CVEs (negative = exploited before a patch existed). (b) Share of cohort CVEs with a usable exposure series whose exposure halved before T_exploit. | Directional | (a) larger; (b) higher | None |
| T2 | How fast do vulnerable systems disappear after a patch? | Median exposure half-life of cohort CVEs (I1) | Directional | Shorter | None |
| T3 | How fast are newly disclosed flaws exploited? | (a) Median days from T0 to first exploitation for CVEs first exploited in the quarter; (b) share exploited on or before T0 | Directional | (a) longer; (b) lower | None |
| T4 | How old are the flaws being exploited? | Share of CVE-labeled exploitation targeting CVEs older than 12 months (I4) | Descriptive | — | None |
| T5 | Is discovery pressure rising? | Year-over-year growth in published CVE records (I5) | Descriptive | — | Rising |
| T6 | Is visible harm rising or falling? | (a) Ransomware leak-site postings; (b) SEC 8-K Item 1.05 filings per 1,000 registrants (each labeled separately) | Directional | Lower | None |
| T7 | How involved is AI in vulnerability discovery? | Share of CVEs published in the quarter whose credits name an AI tool (I8) | Descriptive | — | Rising |

Secondary, always reported, never labeled: within the cohort, AI-credited versus other
CVEs compared on CVSS, share allowing remote code execution, and T3 timing; T1 broken
down by root-cause class (Section 7.3).

## 4. Labeling rule

1. Each quarter, the primary measure is compared with its **baseline**: the median of
   the four preceding quarters (Section 10). The comparison gives a direction: up,
   down, or unchanged (exactly equal).
2. A question is labeled with a direction (**Improving / Worsening**, or **Rising /
   Falling**) when its measure has moved in the **same direction for two consecutive
   quarters**. Otherwise it is **No clear direction**.
3. 90% bootstrap confidence intervals (2,000 resamples, clustered by CVE where the unit
   is a CVE) are published beside every value. They inform the reader but do not gate
   the label.
4. The pilot quarter (Q4 2026) counts toward a two-quarter run, so the first labels can
   appear at Q1 2027. Any label that rests on the pilot quarter is flagged.
5. All seven questions are reported every quarter, whatever the result. A label is
   never described as proof of a cause, including AI.

## 5. Availability rules

- **T3, T4, T5, T6, T7:** labeled from the start, using backfilled history.
- **T1(a):** labeled from the start; it needs only dated events, not exposure data.
- **T1(b), T2:** need Shadowserver exposure series. They are labeled only once at
  least five cohort CVEs (current plus retrospective baseline, Section 10) have a usable
  series. Until then they are reported with status **baseline building**.
- **T4:** primary source is Shadowserver honeypot statistics; KEV additions by CVE age
  are reported beside it as a weaker secondary measure and never merged with it.

## 6. Data sources

All free. Each pull records retrieval time, SHA-256 and source version; git sources are
pinned by commit hash.

| Source | Use |
|---|---|
| CVE.org records (CVEProject/cvelistV5, git) | T5; T7 (credits field); cohort T0, CWE |
| CISA KEV (cisagov/kev-data, git, and JSON feed) | T3, T4 (secondary), agreement checks |
| CISA Vulnrichment (cisagov/vulnrichment, git) | CWE and CVSS where the CVE record lacks them |
| NVD API 2.0 | Severity, CWE and product matching (fallback) |
| FIRST EPSS daily archive | Context; cohort EPSS(t) |
| VulnCheck KEV (community) | T1, T3; agreement checks |
| Shadowserver public dashboard | T1(b), T2 exposure series; T1, T3, T4 honeypot statistics |
| Vendor advisories (CSAF, MSRC, PSIRT pages) | Cohort T_patch |
| Exploit-DB, Metasploit, Nuclei templates, GitHub | Cohort T_poc |
| Cloudflare Radar | Context only |
| ransomware.live | T6(a) |
| SEC EDGAR | T6(b) |

A source that is unavailable is recorded as a gap. Gaps are never filled by estimation.

## 7. Cohort protocol

### 7.1 Eligibility
A CVE is eligible if: (1) it affects a product deployed on internet-facing systems;
(2) the vendor rates it critical, or its CVSS base score is ≥ 8.0; and (3) it was
published between the 1st and the 25th of its month.

### 7.2 Selection
Each month, in order of publication, the first eligible CVE in each of four categories
is selected, using the versioned rule file `config/cohort_rules.yaml`:

- (a) firewalls, VPNs and remote-access gateways;
- (b) web applications, file-transfer and collaboration servers;
- (c) any other product;
- (d) **AI-credited:** an eligible CVE whose credits name an AI tool (per
  `config/ai_credit_terms.yaml`), not already selected in (a)–(c).

Categories are filled independently; a CVE is selected once only, in the first category
it matches, with (d) checked last. Empty categories are recorded as empty and never
filled by hand. The cohort is at most four CVEs a month, twelve a quarter.

Selection never uses exploitation evidence, EPSS or any other outcome measure.

### 7.3 Root-cause tag
Every cohort CVE is tagged with a root-cause class from its CWE (CVE record first, then
Vulnrichment, then NVD), mapped by `config/root_cause_map.yaml`: memory safety;
injection and code execution; authentication and access control; path traversal and
file handling; deserialization; request forgery; credentials and insecure defaults;
other or unknown. The tag is recorded for analysis only and is not used for selection.

### 7.4 Events and follow-up
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
| I2 | Days from T0 to first observed exploitation | CVEs first exploited in the quarter (KEV additions plus cohort) |
| I3 | Days from T_patch to T_exploit; race outcome (won, lost, open) | Cohort CVEs with T_patch; race outcome only for those with a usable series |
| I4 | Share of CVE-labeled exploitation targeting CVEs > 12 months old | Shadowserver honeypot events with CVE labels in the quarter |
| I5 | Year-over-year growth in published CVE records (rejected excluded) | Same quarter in prior years |
| I6 | Agreement among CISA KEV, VulnCheck KEV and Shadowserver (Cohen's and Fleiss' kappa) and median lags | CVEs with any exploitation signal in the trailing two quarters |
| I7 | (a) ransomware postings; (b) SEC 8-K Item 1.05 filings per 1,000 active registrants | (a) quarter totals, deduplicated; (b) active registrants |
| I8 | Share of CVEs whose credits name an AI tool | (a) all CVEs published in the quarter; (b) those with any credit entry |

I6 is a methods check, reported every quarter and never labeled. Context only, never
labeled: Cloudflare Radar bot shares; monthly Microsoft fix count; EPSS distribution of
the quarter's new CVEs.

**AI-credit matching (I8, category d).** A CVE counts as AI-credited when an entry in
its credits array matches a term in `config/ai_credit_terms.yaml`. Every match is
checked by hand, and the term list is versioned; terms added after the freeze are
logged as deviations and applied to past quarters only in a labeled sensitivity
analysis. Known limit: AI involvement that is not credited is invisible to this measure.

## 9. Analysis plan

- **I1 / T2:** per-CVE half-life as defined; median across CVEs by Kaplan-Meier, CVEs not
  halved by day 90 right-censored.
- **I2, I3 / T1, T3:** Kaplan-Meier for time-to-event measures, censored at the
  evaluation date; per source and for the earliest signal.
- **T5, T6, T7:** monthly series, log-transformed, decomposed with STL; the quarter's
  seasonally adjusted value is compared with its baseline. PELT changepoints flagged.
  T5 also reported excluding the five largest CNAs (sensitivity only).
- **Uncertainty:** 90% bootstrap intervals, 2,000 resamples, seed fixed in code.
- **Software:** Python 3.12; lifelines, statsmodels, ruptures, DuckDB; versions pinned in
  the lockfile at the frozen commit.

## 10. Baselines

Backfilled before the dry run and frozen with checksums: CVE publications and credits
from 2017; KEV from November 2021; SEC Item 1.05 from December 2023; ransomware postings
from 2023; Shadowserver series as far back as published.

**Retrospective cohort.** To give T1 and T2 a baseline from the start, the frozen
selection rule (Section 7) is applied to Q4 2025 through Q3 2026, and those cohorts are
followed with the same event definitions. They are labeled **retrospective** and used
only as baseline.

## 11. Validation

Before the first labeled evaluation, the pipeline is run on five documented cases
(CVE-2024-3400; CVE-2025-3248; the two PaperCut flaws exploited by AI agents in 2026;
the Zammad flaws from the DIVD breach). Reference dates are recorded in
`prereg/ground_truth_reference.csv` before the run. Pass: for ≥ 4 of 5 cases, T_patch and
T_kev match exactly and T_exploit is within one day of the documented date, or a later
date is explained by free-source coverage.

## 12. Known limitations stated in advance

- **Loose labeling rule.** Two quarters in the same direction is chosen to show
  movement quickly. It will sometimes label noise as a direction; confidence intervals
  are published so readers can judge.
- **Exposure coverage.** Exposure data covers only CVEs Shadowserver chooses to track.
- **Visibility.** Exploitation data sees opportunistic, automated activity, not targeted
  intrusions.
- **Exploit chains.** The CVSS ≥ 8.0 filter excludes chains of individually low-severity
  flaws, which free data cannot track.
- **AI attribution.** I8 sees only credited AI discovery. Whether an attack was
  AI-driven cannot be measured from free data; that evidence is summarised separately
  in the spec as proven or speculative and is not labeled.
- **Small samples.** At most twelve cohort CVEs a quarter.
- **Conflict of interest.** Claude, made by Anthropic, writes the code and drafts the
  evaluations; Anthropic is named in the report this study grew from. Safeguards: this
  frozen plan, public code, author approval of every release, and an external reviewer
  for the first confirmatory quarter.
