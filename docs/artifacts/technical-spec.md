# Quarterly Internet Security Snapshot: Technical Spec

Oct 24, 2026 · @Paul

This spec defines an **unfunded, quarterly snapshot** that tracks whether internet security is getting better or worse, and how AI is involved. It reports seven pre-registered tracking questions and uses only free data and free infrastructure; the only people involved are the author and Claude. At 06:00 UTC on the 1st of January, April, July and October, one automated job pulls the previous quarter's data, freezes it as a dated bundle and computes the results. A provisional evaluation is published that day. A final one follows a month later, once late KEV listings and corrections have arrived. Q4 2026 is a pilot quarter. Q1 2027 is the first confirmatory quarter, with its final evaluation on 1 May 2027.

## Summary and core design decisions

**The question.** The study does not try to prove that the internet will be cleaned up. It tracks one central race, quarter by quarter: are defenders closing internet-exposed vulnerabilities faster than attackers start exploiting them? Six further questions track how fast exposure disappears, how fast new flaws are exploited, how old the exploited flaws are, discovery pressure, visible harm, and how much vulnerability discovery is credited to AI.

**Design decisions**

1. **Unfunded by design.** No paid data, servers or staff. Every source is free to use non-commercially, and the pipeline runs on free services: a public GitHub repository with scheduled Actions, GitHub Pages, OSF and Zenodo. If a measure can't be done for free, it is cut or reported descriptively, never estimated.
2. **Quarterly evaluation, monthly detail.** Results are judged once a quarter, which gives each test more cases and fits a part-time schedule. Each quarterly pull still rebuilds the data month by month, and day by day where sources allow, so nothing is averaged away before analysis.
3. **Only sources that keep their own history.** A quarterly pull works only if the past can be rebuilt. Every scored source keeps its own history: the git histories of CVE, KEV and Vulnrichment; FIRST's daily EPSS archive; Shadowserver's dashboard time series; and the dated records at SEC EDGAR, Cloudflare Radar and ransomware.live.
4. **Fewer indicators, measured well.** Seven tracking questions built on eight indicators. Everything else is shown as context and never labelled.
5. **Rates, not counts.** Every scored number has an explicit denominator: the first published exposure count after a patch, the CVEs in a cohort, or the registrants filing with the SEC.
6. **Frozen and versioned.** Each pull is saved exactly as retrieved, with checksums. Git sources are frozen by commit hash rather than copied, because their public history is itself the record. Timestamps come from commit history, not from the current version of a record.
7. **Two-stage release.** Provisional on the 1st, final a month later, with later revisions logged.
8. **Cohort depth over breadth.** Up to four newly disclosed vulnerabilities a month, twelve a quarter, are chosen by a fixed rule (including one AI-credited flaw when there is one), tagged by root cause and followed for 90 days.
9. **Checkable by others.** The tracking questions and their definitions were registered on OSF on 20 October 2026 ([DOI 10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82)), pinned to GitHub tag `prereg-v1.0`. Code and data are public, and results are compared with independent sources.

**What it is not.** It is not continuous monitoring, a live feed or a vulnerability scanner; it never probes systems and runs no sensors of its own. It does not measure targeted or state-level intrusions, which leave little public trace. And no single quarter can confirm or refute the thesis; the main evidence is the trailing four quarters.

**Who does what.** The author owns the study: freezes the pre-registration, holds the accounts, approves every release and signs off every result. Claude writes and maintains the code, checks each run, drafts each evaluation from the frozen outputs, and flags where the data does not support a claim. Claude does not choose cohort CVEs or change thresholds; those come from the frozen rules. Claude is made by Anthropic, a company named in the report the study tests, so the frozen rules, public code and an external reviewer are the safeguards against that conflict of interest.

## Pre-registered tracking questions

This is a monitoring study, not a test of the cleanup thesis. What was frozen on OSF on 20 October 2026 is not a prediction but the definitions: what each measure is, what counts as better or worse, and when a change is called a direction. That stops anyone, including us, from choosing the flattering number afterwards. Where the author holds an expectation, it is recorded as a stated prediction that can turn out wrong. Any later change is published as a dated deviation, with the original kept alongside.

| ID | Question | Primary measure | Type | Better means | Author's stated prediction |
| --- | --- | --- | --- | --- | --- |
| T1 | **The race (central).** Are defenders closing exposed vulnerabilities faster than attackers exploit them? | (a) Median days from patch to first exploitation across cohort CVEs (negative means exploited before a patch existed). (b) Share of cohort CVEs with exposure data whose exposure halved before first exploitation | Directional | (a) Larger gap; (b) higher share | None |
| T2 | How fast do vulnerable systems disappear after a patch? | Median exposure half-life of cohort CVEs | Directional | Shorter | None |
| T3 | How fast are newly disclosed flaws exploited? | (a) Median days from disclosure to first exploitation; (b) share exploited on or before disclosure | Directional | (a) Longer; (b) lower | None |
| T4 | How old are the flaws being exploited? | Share of CVE-labeled exploitation aimed at CVEs over 12 months old | Descriptive | — | None |
| T5 | Is discovery pressure rising? | Year-over-year growth in published CVE records | Descriptive | — | Rising |
| T6 | Is visible harm rising or falling? | (a) Ransomware leak-site postings; (b) SEC Item 1.05 filings per 1,000 registrants, each labeled separately | Directional | Lower | None |
| T7 | How involved is AI in vulnerability discovery? | Share of CVEs published in the quarter whose credits name an AI tool | Descriptive | — | Rising |

**Labeling rule.** Each quarter, every primary measure is compared with its baseline, the median of the four preceding quarters, which gives a direction: up, down or unchanged. A question is labeled with a direction once its measure has moved the **same way for two consecutive quarters**. Directional questions are labeled **Improving** or **Worsening**; descriptive questions (T4, T5, T7) are labeled **Rising** or **Falling**, with no judgment of good or bad. Anything else is **No clear direction**. 90% bootstrap confidence intervals are published beside every value so readers can judge the noise, but they do not gate the label. The rule is deliberately loose so movement shows quickly; it will sometimes label noise as a direction, and the spec says so on every page. A label is never presented as proof of a cause, including AI.

**First labels.** The pilot quarter (Q4 2026) counts toward a two-quarter run, so the first labels can appear with Q1 2027. Any label that rests on the pilot quarter is flagged.

**Secondary comparisons, always reported, never labeled.** Within the cohort, AI-credited and other CVEs compared on severity, share allowing remote code execution, and time to exploitation; and the race broken down by root-cause class.

**What can be labeled, and when.** T1(a), T3, T4, T5, T6 and T7 can be labeled from the start, using backfilled history. T1(b) and T2 need Shadowserver exposure series and are labeled only once at least five cohort CVEs, counting the retrospective baseline cohort, have a usable series; until then they show "baseline building". T4 uses Shadowserver's honeypot statistics, with KEV additions by CVE age reported beside it as a weaker check.

## Indicators and their validity

Each indicator is checked against one question: does it measure what the tracking question needs, or something that merely moves with it? Each has a fixed denominator, a known bias, and a better proxy where one exists.

| ID | Indicator (feeds) | What it actually measures | Denominator | Known biases | Better proxy, used or noted |
| --- | --- | --- | --- | --- | --- |
| I1 | Exposure half-life (T1b, T2) | Days until Shadowserver's daily count of vulnerable instances for a CVE falls to half its first published value after the patch | First published vulnerable count on or after the patch date | Shadowserver scans only the CVEs it chooses, mostly high-profile edge devices; counts mix patched, offline and firewalled hosts; its fingerprinting method cannot be inspected; IPv6 and CDN-fronted hosts are undercounted | Licensed banner data with the study's own fingerprinting, out of scope while unfunded; coverage reported every quarter |
| I2 | Time from disclosure to first observed exploitation (T3) | Earliest dated record of exploitation in any free source, measured from disclosure | CVEs first exploited in the quarter (KEV additions plus cohort) | Opportunistic mass exploitation is visible, targeted attacks are not; CISA's KEV date is a confirmation date; free sources can lag commercial telemetry | Earliest of Shadowserver honeypot first-seen, VulnCheck KEV and CISA KEV, with each source's lag reported; compared with VulnCheck's published figures |
| I3 | Patch-to-exploitation gap and race outcome (T1) | Days from patch to first exploitation; whether exposure halved before exploitation | Cohort CVEs with a patch date; race outcome only for those with a usable exposure series | Few cases per quarter; depends on I1 and I2 quality; a missing patch date excludes the CVE | Pooled over trailing quarters; each CVE's full timeline published |
| I4 | Exploitation age mix (T4) | Share of observed exploitation by age of the targeted flaw | Shadowserver honeypot events with a CVE label in the quarter; secondary: KEV additions in the quarter | Honeypots see automated scanning; labels favor known, older flaws; KEV measures confirmation, not attempts | Both versions reported separately and never merged |
| I5 | Disclosure growth (T5) | Change in the number of CVE records published, not change in risk | Same quarter in prior years | AI-assisted discovery and CNA policy changes create jumps; the NVD backlog delays enrichment | Counted from CVE.org git history, not NVD; shown with and without the five largest CNAs; rejected records excluded |
| I6 | Source agreement on exploitation (methods check) | How far CISA KEV, VulnCheck KEV and Shadowserver agree on which flaws are exploited, and how late each is | CVEs with any exploitation signal in the trailing two quarters | Each source has different inclusion rules; VulnCheck is broader than CISA | Pairwise and three-way agreement scores, plus each source's median lag behind the earliest signal |
| I7 | Harm rate (T6) | (a) ransomware leak-site postings; (b) SEC Form 8-K Item 1.05 material-incident filings | (a) quarter totals, deduplicated; (b) per 1,000 active SEC reporting companies | Leak sites show only victims who did not pay, and trackers disagree on totals; SEC covers only US public companies and depends on materiality judgments | Postings deduplicated by ransomware.live, which keeps posts later deleted; the two series labeled separately |
| I8 | AI-credited discovery (T7) | Share of CVEs whose credits field names an AI tool or agent | (a) all CVEs published in the quarter; (b) those with any credit entry | Credits are optional and filled inconsistently; uncredited AI use is invisible; tool names can collide with personal names | Every match checked by hand; versioned term list; compared with independent AI-attribution trackers |

**Context only, not scored:** Cloudflare Radar bot share of HTTP requests and the verified-bot share of bot traffic; monthly Microsoft security fix count; EPSS distribution for the quarter's new CVEs.

**Explicitly not measured:** passkey adoption, which has no regular public data; whether an attack was AI-driven, which cannot be determined reliably from public data; open-model capability, which CAISI tracks; and anything that needs GreyNoise or commercial scan data, which require paid licences to publish.

## Evidence beyond the data: proven vs speculative

Some things the study cares about can't be measured from free data, above all whether attacks are AI-driven and how fast patching happens outside Shadowserver's coverage. This section summarizes what published research says about those gaps. It is refreshed each quarter and is never part of a label. A claim moves from speculative to proven only when a named dataset with a stated method supports it. Most figures below were read in news or vendor summaries rather than the full reports, so they are given as reported.

**Proven: measured, with a named data source**

- **Exploitation is coming earlier.** 29% of the 884 flaws VulnCheck saw exploited for the first time in 2025 were exploited on or before CVE publication, up from 23.6%. The rest of the timing pattern barely moved from 2024. ([VulnCheck 2026 State of Exploitation](https://wwv.vulncheck.com/hubfs/Research/2026-StateofExploitation.pdf?hsLang=en)) The study's T3 measures the same thing independently.
- **Patching is getting slower.** Median remediation time rose from 32 to 43 days; only 26% of critical KEV flaws were fully fixed in 2025; exploiting vulnerabilities is now 31% of breach entry points. ([Verizon DBIR 2026, via TechRepublic](https://www.techrepublic.com/article/news-verizon-dbir-vulnerability-exploitation-2026/))
- **Edge devices stay exposed for a long time.** 71% of affected Citrix environments were still unpatched after a year, with a median of 461 days to fix. This is Tenable's customer base, not the whole internet. ([Tenable, Aug 2026](https://www.tenable.com/blog/edge-infrastructure-under-siege))
- **Ransomware victims are rising, but trackers disagree on how fast.** GuidePoint counted a record 2,760 in Q3 2026, up 75% year over year ([via Webull](https://www.webull.com/news/15712183178626048)); Check Point counted 2,139 in Q2, up 33% year over year and flat on the quarter ([IT Brief](https://itbrief.co.uk/story/ransomware-victim-numbers-flat-as-active-groups-hit-record)).
- **One documented AI-run attack campaign.** A Chinese state-sponsored group used Claude to carry out an estimated 80–90% of hands-on work against about 30 targets; a handful of intrusions succeeded, and the AI's fabricated results got in the attackers' way. Reported by Anthropic itself, a conflict of interest to note. ([Anthropic, Nov 2025](https://www-cdn.anthropic.com/d7dd50dd1185f59be051b307150d877f2b82bd2c.pdf))

**Measured, but too early to call**

- **CVE volume roughly doubled** between January 2025 and August 2026, to about 10,700 a month. FIRST forecasts about 66,000 CVEs for 2026 and attributes part of the rise to AI discovery tools; the share needing urgent action has stayed flat. ([Help Net Security](https://www.helpnetsecurity.com/2026/06/15/first-2026-cve-forecast/); [GTIG figures, via AI Weekly](https://aiweekly.co/alerts/google-gtig-ai-found-software-vulnerabilities-enable-remote-code-execution-50))
- **Flaws tagged as AI-found were more severe:** 50% allowed remote code execution, against 26% of other CVEs. This is Google's tagged subset, and the tagging method isn't described in the summary.
- **CrowdStrike saw 2.5 times more detections tied to AI-agent behavior** than to human-triggered activity in parts of Q1 2026. Real telemetry, but how much was malicious isn't clear. ([CRN Asia](https://www.crnasia.com/news/2026/cybersecurity/crowdstrike-2026-threat-hunting-report-tracks-rise-in-ai-dri))
- **Discovery outpaces remediation inside large organizations.** Salesforce's security team describes machine-speed discovery against human-speed remediation, but gives almost no figures. ([Salesforce, Oct 2026](https://www.salesforce.com/blog/managing-agentic-security-at-scale/))

**Speculative: claims without data**

- **"AI will cut patch-to-exploit time to minutes"** and **"AI will dominate cybercrime in 2026"**: a vendor press release with no sample size or cases. ([ThreatDown](https://www.galvnews.com/cybercrime-enters-a-post-human-future-as-ai-drives-the-shift-to-machine-scale-attacks/article_7821536c-4c4e-5fc5-8337-eda63542b3a4.html))
- **How much vulnerability discovery AI now does.** Unknown. A tracker that counts only verified credits found about a dozen numbered CVEs, far below headline claims. ([Stingrai](https://www.stingrai.io/blog/ai-attributed-cve-tracker-2026-verified-credits)) The study's T7 measures this directly from CVE credits.

## Data sources and the quarterly pull

A scheduled GitHub Actions workflow runs at 06:00 UTC on the 1st of January, April, July and October and pulls the previous quarter from every source. Each file is saved as retrieved, with its SHA-256 checksum, retrieval time and source version recorded in the pull's manifest; git sources are recorded by commit hash. A second run one month later re-pulls the same quarter to catch late entries and corrections, and is saved alongside the first. Because the job runs on GitHub's servers, it does not depend on anyone's computer being switched on.

| Source | Pulled for the quarter | Keeps its own history? | Feeds | Cost and terms |
| --- | --- | --- | --- | --- |
| CVE.org records (CVEProject/cvelistV5) | Records committed during the quarter, pinned by commit | Yes, git history | I5, cohort T0 | Free |
| CISA KEV (JSON feed and cisagov/kev-data) | Catalog plus git history | Yes, git history | I2, I4, I6 | Free; US government work |
| CISA Vulnrichment (cisagov/vulnrichment) | Records committed during the quarter | Yes, git history | Cohort context | Free; CC0 |
| NVD API 2.0 | Records modified during the quarter | Yes, change-history API | Severity, product (CPE) matching | Free API key |
| FIRST EPSS | Every daily score file for the quarter | Yes, daily archive | Context; cohort EPSS(t) | Free |
| VulnCheck KEV (community tier) | Full export with date-added fields | Partly: entries are dated, removals are not kept | I2, I6 | Free account; redistribution restricted (verify) |
| Shadowserver public dashboard | Daily vulnerable-instance series for tracked CVEs; honeypot attack statistics by CVE | Yes, dashboard time series | I1, I2, I4, I6 | Free; reuse terms to confirm in writing |
| Vendor advisories (CSAF 2.0, MSRC CVRF API, PSIRT pages) | Advisories published or revised during the quarter | Yes: documents carry their own dates and revisions | Cohort T\_patch | Free |
| Public exploit sources (Exploit-DB, Metasploit, Nuclei templates, GitHub) | First-commit times for cohort CVEs | Yes, commit history | Cohort T\_poc | Free |
| Cloudflare Radar API | Daily bot series | Yes, API date ranges | Context | Free token; CC BY-NC |
| ransomware.live | Postings dated in the quarter; victim names dropped at capture | Yes, including posts later deleted from leak sites | I7a | Free API; check terms |
| SEC EDGAR | 8-K filings with Item 1.05 in the quarter, and the active-registrant count | Yes, full filing index | I7b | Free; fair-access rate limit |

**Backfill for baselines.** Before the first pull, the pipeline backfills monthly series from source histories: CVE publications from 2017, KEV from its 2021 launch, SEC Item 1.05 from its December 2023 start, ransomware postings from 2023, and Shadowserver series as far back as each is published. These backfills are frozen and published with the pilot evaluation.

**Gaps.** A source that fails on the 1st is retried for up to 48 hours. If it still fails, the evaluation is published without it, the gap is recorded in the manifest and shown on the page, and the final run fills it if it can. Gaps are never filled by estimation.

**Optional helper.** CVE Intel, the tool reviewed earlier, can be used for quick manual checks of single CVEs. It is not in the measurement path, because its risk score is its own formula and it does not keep raw history.

## Cohort protocol

Each month, up to four vulnerabilities disclosed that month are selected, at most twelve per quarter, and each is followed for 90 days. A fixed, automated rule makes the selection at the quarterly pull, by a seeded random draw within each slot (since 21 October 2026; see below). Selection never uses exploitation evidence, EPSS or any other outcome, because those are what the study measures.

**Eligibility.** A CVE qualifies if all of these hold:

1. It affects a product that runs on internet-facing systems.
2. The vendor rates it critical, or its CVSS base score is 8.0 or higher.
3. It was published between the 1st and the 25th of the month.

**Selection rule.** Each month, the CVE picked by a seeded random draw in each of four categories is selected: (a) firewalls, VPNs and remote-access gateways; (b) web applications, file-transfer and collaboration servers; (c) any other product; (d) **AI-credited**, a qualifying CVE whose credits name an AI tool, checked by hand against a versioned term list. A CVE is selected only once, and (d) is checked last. Category (a) comes first because Shadowserver most often publishes exposure series for edge devices. Category (d) gives a direct comparison of AI-found and human-found flaws in the race; in months with no AI-credited CVE it stays empty. Empty categories are recorded, never topped up by hand.

**How the draw works.** Each eligible CVE gets a key: the SHA-256 hash of the study name, the month, the category and the CVE ID. The CVE with the lowest key is picked. Anyone can recompute the order, it does not depend on publication date, and it never uses exploitation data. In categories (c) and (d), a drawn CVE that fails the hand check is recorded and the next in draw order is used. This replaced "first published" on 21 October 2026, before any cohort was selected, because picking the earliest flaw each month would favour vendors that publish early in the month (logged in the deviations file).

**Root-cause tag.** Every cohort CVE is tagged with a root-cause class from its CWE (CVE record first, then Vulnrichment, then NVD): memory safety; injection and code execution; authentication and access control; path traversal and file handling; deserialization; request forgery; credentials and insecure defaults; other or unknown. The tag is used only to break the race down by root cause, never for selection. The idea comes from Salesforce's observation that most findings trace back to a few shared root causes.

**Events tracked per CVE**, each with its source and timestamp:

| Event | Definition | Source |
| --- | --- | --- |
| T0 Disclosure | First commit of the CVE record, or the vendor advisory if earlier | CVE.org git, vendor advisory |
| T\_patch | First publicly available fix or vendor mitigation | Vendor CSAF or advisory |
| T\_poc | First public exploit or detection template | Exploit-DB, Metasploit, Nuclei, GitHub commit time |
| T\_exploit | First observed exploitation by any source | Earliest dated record in Shadowserver honeypot data, VulnCheck KEV or CISA KEV |
| T\_kev | Date added to CISA KEV, if ever | KEV git history |
| E(t) | Daily count of vulnerable instances | Shadowserver series, when one is published for the CVE |
| EPSS(t) | Daily exploit-probability score | FIRST EPSS archive |

**Tracking window.** Each CVE is followed for 90 days, so a CVE disclosed late in a quarter is completed in the next evaluation. Event dates are exact to the day, because they come from dated source records. Any event that has not happened by the evaluation date is treated as censored, not missing.

**Output per CVE.** A one-page timeline with all events on one time axis, the exposure curve where one exists, and a plain-language note on what was observed and what could not be.

## Analysis methods

All analysis runs from the frozen bundle in a pinned container, so the same inputs always give the same outputs.

### Exposure decay (I1)

For each cohort CVE with a Shadowserver series, the half-life is the first day the 7-day average vulnerable count falls below half the first count published on or after the patch date. An exponential-decay fit is shown alongside, as a check on noisy series. Across CVEs, the median half-life is estimated with Kaplan-Meier, treating CVEs that have not halved by the end of the window as censored. The study works only with these aggregate counts and never sees individual hosts.

### Time to exploitation and the race (I2, I3)

Kaplan-Meier curves of days from disclosure to first observed exploitation (T3) and from patch to first exploitation (T1a), censored at the evaluation date, shown per source and for the earliest signal. For each cohort CVE with exposure data, the race is *won* if exposure halved before first exploitation, *lost* if exploitation came first, and *open* if neither has happened. Results are also shown by root-cause class and for AI-credited versus other CVEs. Since 23 October 2026 (a logged deviation), the patch-to-exploitation figure T1(a) is computed on every CVE first added to CISA KEV in the quarter rather than on the cohort, which holds only 0.3 to 0.4 exploited CVEs a quarter; the cohort version is reported alongside for four quarters. Fix dates are carried as a range (earliest fix evidence to latest possible release) and attack dates by their latest possible date (KEV listing or CISA's active-exploitation assessment, whichever is earlier), so the zero-day share is reported as a range and the median as an upper bound.

### Seasonally adjusted baselines (T5, T6, T7)

Monthly series are log-transformed and decomposed into trend, seasonal and remainder parts with STL. The quarter is compared with two baselines: the same quarter in each prior year, and the trailing four quarters. A changepoint test (PELT) flags structural breaks, such as a CNA policy change, so they are not mistaken for trends.

### Uncertainty

Every headline number gets a 90% confidence interval from 2,000 bootstrap resamples, clustered by CVE. With at most twelve cohort CVEs a quarter, and fewer with exposure data, intervals will be wide. They are published beside each value but do not decide the label, which follows the two-quarter direction rule. Beside each label, a companion test (the mean of the last two quarters against the mean of the four before, at the 10% level) reports whether the move stands out from noise: by simulation, the two-quarter rule alone labels pure noise in about 48% of quarters, the test in about 10%.

### Source agreement (I6)

For CVEs with any exploitation signal in the trailing two quarters, the study reports pairwise Cohen's kappa and three-way Fleiss' kappa for CISA KEV, VulnCheck KEV and Shadowserver, plus each source's median lag behind the earliest signal. Large disagreement is flagged next to T1, T3 and T4 that quarter.

### Exploitation age mix (I4)

The age of each targeted CVE is computed from its disclosure date. The T4 measure is the share of CVE-labeled honeypot exploitation aimed at CVEs over 12 months old. The KEV version (additions during the quarter by CVE age) measures what was confirmed rather than attempted; it is reported beside the honeypot version and never merged with it.

### Tools

Python 3.12, DuckDB and Parquet for storage and queries, pandera for data validation, lifelines for survival analysis, statsmodels for STL decomposition, ruptures for changepoints, and Jupyter notebooks for the published analysis. All are free and open source, pinned in a lockfile and container image.

## Architecture

&#91;embedded content: Free sources in, one automated job a quarter, frozen bundles feeding every result, and the author approving each release.\]

The design rule is **capture first, interpret later**. Everything runs in one public GitHub repository. A scheduled Actions workflow pulls the quarter, saves each file exactly as served with a checksum manifest, and rebuilds every derived table from those frozen files, so any published number can be traced back to the bytes behind it. Raw files are attached to a release in the repository and, at each final evaluation, deposited on Zenodo with a DOI; git sources are pinned by commit hash. The evaluation pages are built with GitHub Pages. Claude works on the same repository, writing code, checking each run and drafting the evaluation, and the author approves every release before it is published.

## Data model

The raw layer stores files exactly as retrieved. The tables below form the normalized layer, stored as Parquet and queried with DuckDB. Every row carries `quarter` and `manifest_id`, so any number can be traced back to the exact file it came from.

| Table | Key fields | Grain |
| --- | --- | --- |
| snapshot\_manifest | manifest\_id, quarter, run (provisional, final), source, retrieved\_at, file\_path or commit\_hash, sha256, bytes, status (ok, retried, gap) | One row per file per run |
| cve | cve\_id, first\_commit\_at, published\_at, cna, state (published, rejected), cvss\_base, cwe, cpe\_products | One row per CVE per run |
| kev\_entry | cve\_id, list (cisa, vulncheck), date\_added, first\_seen\_commit\_at, ransomware\_flag | One row per CVE per list |
| epss\_daily | score\_date, cve\_id, epss, percentile, model\_version | One row per CVE per day |
| advisory | vendor, cve\_id, published\_at, fix\_released\_at, fixed\_versions, csaf\_id, url | One row per advisory and CVE |
| poc\_obs | cve\_id, source (exploitdb, metasploit, nuclei, github), first\_seen\_at | One row per first sighting per source |
| exploit\_obs | cve\_id, source (shadowserver\_honeypot, cisa\_kev, vulncheck\_kev), first\_seen\_at, daily\_count | One row per source per CVE per day |
| exposure\_series | cve\_id, date, vulnerable\_count, country (where published), series\_id | One row per CVE per day per country |
| cohort | month, cve\_id, category, selection\_rule\_version, t0, t\_patch, t\_poc, t\_exploit, t\_kev | One row per cohort CVE |
| harm\_ransom | posting\_date, group, sector, country, dedupe\_key | One row per deduplicated posting; no victim names |
| harm\_sec | filing\_date, cik, form, item\_105 (bool), amendment (bool) | One row per filing |
| context\_radar | date, bot\_share, verified\_bot\_share\_of\_bots | One row per day |
| metric\_result | quarter, release (provisional, final), metric\_id, value, ci\_low, ci\_high, baseline, status, code\_version, approved\_by | One row per metric per release |

**Privacy by design.** The study handles no host-level data at all: exposure comes only as aggregate counts that Shadowserver has already published. Ransomware victim names are dropped before storage.

## Evaluation pages

The public site is a static GitHub Pages site with one page per quarter, published as provisional on the 1st and finalized a month later, and an index that lines the quarters up for comparison. In reading order, each page has:

1. **Scorecard.** The seven tracking questions, each with its label (Improving, Worsening, Rising, Falling, No clear direction, or baseline building), this quarter's value and confidence interval, the baseline, and the direction in each of the last two quarters.
2. **Since last quarter.** What changed in each indicator, and which earlier cohort CVEs moved: newly exploited, newly listed in KEV, or past half exposure.
3. **Cohort timelines.** One row per cohort CVE on a shared time axis, from disclosure through patch, exploit code, first exploitation and KEV listing, with its exposure curve where one exists.
4. **The race.** Exposure curves for cohort CVEs with Shadowserver series, with the first-exploitation date marked on each.
5. **Exploitation age mix.** Share of exploitation by age of the targeted flaw, with the honeypot and KEV versions side by side.
6. **Pressure and harm.** Seasonally adjusted CVE publications and the two harm series, each against its baseline band.
7. **Source agreement.** Agreement scores and median lags for CISA, VulnCheck and Shadowserver.
8. **Context.** Bot share of traffic, monthly Microsoft fix count, EPSS distribution.
9. **Method and changes.** The pre-registration link, any deviations, gaps, rule-file versions, the release changelog, and who approved the release.
10. **Downloads.** The quarter's bundle and its DOI.

Every number has hover text naming its source, retrieval date and denominator. A banner marks the page provisional until the final run.

## Reproducibility and validation

The study is meant to be checked by people other than its authors. Three mechanisms make that possible.

### Quarterly release bundle

Deposited on Zenodo with a DOI at each final evaluation:

- Frozen raw files for every source whose terms allow redistribution: CVE records (or their commit list), CISA KEV and Vulnrichment, NVD extracts, EPSS and SEC filings
- For Shadowserver, VulnCheck and ransomware.live: the derived aggregates the terms allow, plus the exact query and retrieval date so others can fetch the originals
- The tagged code release, container image digest, rule files and manifest checksums
- A pinned software environment (a container built on a base image pinned by digest, with every package from a hash-locked list) that recomputes every published number from the frozen files; a scheduled job repeats the recomputation monthly and fails if any figure differs

The workflow reruns that command on every release and fails if any published number differs.

### Ground-truth test (before the first evaluation, then yearly)

The pipeline is run on past vulnerabilities whose exploitation timelines are documented in detailed public research, and its event dates are compared with the published accounts. Candidates include CVE-2024-3400 (PAN-OS), CVE-2025-3248 (Langflow, used by JadePuffer), the two PaperCut flaws exploited by AI agents in 2026, and the Zammad flaws from the DIVD breach. Reference dates are taken from the original write-ups and recorded in a fixed reference file before the pipeline runs.

The test passes if, for at least four of five cases, the pipeline's T\_patch and T\_kev match exactly, and its T\_exploit is within one day of the documented first exploitation or any later date is explained by free-source coverage. Results are published.

### Independent comparisons

Each evaluation compares its findings with sources the study does not control:

| Our measure | Compared against |
| --- | --- |
| Exposure half-life | Censys and Shodan research posts on the same flaws |
| Time to first exploitation | GreyNoise and VulnCheck published timelines; Mandiant time-to-exploit reports; vendor incident write-ups |
| KEV agreement and lag | ENISA's EU Vulnerability Database exploited list; CERT-In and NCSC advisories |
| Disclosure growth | CVE.org's published counts; Microsoft and Google release figures |
| Harm rate | Ransomware trackers' quarterly summaries; later, the Verizon DBIR and ENISA Threat Landscape for the same period |
| Bot context | Cloudflare's quarterly Radar reports |

An independent external reviewer (candidates and recruiting: Open questions, item 2) is invited to review the first confirmatory evaluation before its final release on 1 May 2027.

### Annual check against reference data

Once a year, the free quarterly results are compared with better reference data to show how well the free system tracked reality. The check is pre-registered now, before any reference data is seen, and it is reported rather than graded: there is no pass mark.

- **Period and timing.** Each check covers one calendar year and is published in March, after insurers' and payment analysts' annual reports appear. The first covers 2027 and comes out in March 2028, with the Q4 2026 pilot included as a labeled extra.
- **Exposure reference (T1b, T2).** Internet scan data with historical lookups: Censys research access, which is free to non-commercial researchers who publish, or a one-off licence. The race and exposure half-life are recomputed for every cohort vulnerability of the year. The scan data is used only here, never in the quarterly results, so it stays an independent yardstick. The application to Censys is on hold until after the pilot quarter, and it must be written by the author: Censys rejects AI-written requests.
- **Harm reference (T6).** Published annual figures for the same year: insurance claims frequency (Coalition), the share of ransomware victims paying (Coveware) and total ransom payments (Chainalysis). Raw claims or negotiation data would need a data-sharing agreement and is not required.
- **What is reported.** How many cohort vulnerabilities each source could measure; how far free and reference half-lives differ; how often race outcomes match; and, quarter by quarter, whether the free direction for T1b, T2 and T6 matches the reference direction.
- **The known divergence in harm.** Leak sites list only victims who don't pay, so a falling payment rate can raise leak-site counts while attacks stay flat. Recent figures already point that way: leak-site victims up sharply while payments held flat and the share paying fell to record lows. The check states whether the two moved apart, and which way.
- **If scan data isn't obtained** by 31 January of the publication year, the exposure part is skipped and the gap recorded. The harm part always runs, because its reference figures are published free.
- **Publishing.** Only comparison results and aggregates are published. The reference data can't be redistributed, so the annual check is the one part outsiders can't rerun from public files, and each check says so.

## Changes since registration (21–22 October 2026)

All changes below were made before any result or cohort was scored and are logged in `prereg/DEVIATIONS.md` where they touch a registered rule.

**Locked core and exploratory layer.** The core (seven tracking questions, cohort rules, AI-credit term list, root-cause map) is locked by checksum (`prereg/LOCKED.yaml`, baseline release `core-v1.1`); a test fails on any undocumented change. Core changes happen only at the March review, after old and new versions run side by side for four quarters. New ideas go to an exploratory layer (`config/exploratory.yaml`) that is reported separately and never decides a label. The final pre-pilot freeze is `core-v1.2`, due by 31 December 2026 after a decision session on 21 December (`docs/CORE_FREEZE_DECISIONS.md`).

**Exploratory measures.** X1 AI-credited share by lab; X2 watchlist matches; X3 a curated log of AI-run attack campaigns (11 entries, seeded with Cairn and the September 2026 PaperCut agent campaign, linked to CISA KEV where CVEs are named); X4 Cloudflare Radar bot and AI-crawler traffic; X5 flaws in AI software (1.6% of eligible Q3 2026 CVEs); X6–X11 fingerprints of AI-accelerated attacks that show whatever model the attacker used (speed in the tail, patch to public exploit code, breadth, bug types, zero-day share, exposed AI servers); X12 a log of open-weight model releases. Sources for attacker-side AI are listed in `exploratory/SOURCES.md`.

**T7 caveat.** T7 measures *disclosed* AI involvement. Discoveries made with privately run models are rarely credited, so T7 can lag real AI use.

**Data collection.** Collectors now cover CVE.org (with CISA Vulnrichment fields), CISA KEV, NVD (via a commit-pinned GitHub mirror of NVD's data, NVD's own feeds as fallback), EPSS, SEC 8-K Item 1.05 (original and amended filings searched separately), Cloudflare Radar and ransomware.live (aggregate counts only). A full quarterly pull takes about six minutes. VulnCheck stays off until written permission; Shadowserver awaits approval.

**Quality and resilience.** Every run produces a data-quality report (completeness, agreement between sources, cohort pool sizes, AI-credit review load) with drift checks (expected fields present, counts compared with the previous run). Each run's log, manifest, quality report and review list are saved to the `run-reports` branch with secrets scrubbed. Runs are tagged; the GitHub runner is pinned.

**Hand checks.** The author works through each quarter's review list in a private Hand Check app (`docs/HAND_CHECK_APP.md`): AI credits one at a time or grouped by category, slot c/d candidates in draw order, and pre-filled fix dates with their source. Answers are written to `review/decisions.csv`, the only hand input the evaluation reads; practice lists are kept separately. Decided credit texts carry over between quarters. Since 23 October, clear-cut AI credits are accepted by published rules, so most hand time goes to fix dates and the internet-facing check. Since 24 October, 20 earlier decisions of every kind are re-shown unmarked each quarter to measure consistency (re-shown answers never replace the originals), and a second, independent coder answers a blinded, weighted sample of 20 items; agreement is reported as raw agreement, Cohen's kappa, Gwet's AC1 and agreement on Yes and No, and for fix dates as the share within one day.

**The race on newly attacked flaws (23 October).** A back-test on Q2 and Q3 2026 found the registered cohort holds only 0.3 to 0.4 exploited CVEs a quarter, so its race median could almost never be computed. T1(a) is now computed on every CVE first added to CISA KEV in the quarter (75 to 100), with vendor-sourced fix dates and flagged cases hand-checked; the registered cohort version is reported alongside for four quarters. The share exploited before any fix existed stays exploratory (X10) and is a promotion candidate at the 15 March 2027 review. An EPSS-weighted cohort was back-tested and rejected: it breaks the rule that outcomes never select CVEs and still gives no usable estimate.

**AI credits (23 October).** T7's headline counts any credit that mentions an AI tool or a frontier AI lab; the registered measure (an AI tool named in a clear role) is computed automatically as the low end, and a direction is called only when both move the same way. The rule is re-evaluated on the pilot's data on 8 February 2027.

**Statistical review (24 October).** An external evaluation (EVAL-2026-ISS-01) was reviewed against the repository (`docs/STATISTICAL_REVIEW_2026-10-24.md`). Adopted, none of them changing the locked core: the lockfile promised in the registration (hash-locked packages, GitHub Actions pinned by commit, Python 3.12.15, the environment recorded in every manifest; logged as an implementation note); a container pinned by digest and a monthly rebuild check of the latest frozen bundle; fix and attack dates as ranges; the companion test beside each label; the hand-check reliability measures above; and X13, a whole-population comparison of AI-credited and other serious CVEs (in Q2 to Q3 2026, 0 of 102 AI-credited serious CVEs had reached KEV, so time to listing is reported pooled, with event counts, until enough events accrue). A first preview found CISA's active-exploitation assessment comes before the KEV listing for about a third of newly listed CVEs, so the KEV-based zero-day share may understate zero-days by about half; it is recomputed on the dry run before anything is published.

**Closing re-run (planned).** On 1 April 2028 all four 2027 quarters are recomputed once every 2027 cohort CVE has its full 90-day follow-up, and published as a completeness addendum to the March 2028 annual check. The scored labels are not changed.

## Licensing for public use

Being unfunded and non-commercial is what makes every source usable. Keep the site and data free, and treat any Substack writing as commentary that links to the site rather than reproducing its charts in paid posts. Entries marked "verify" must be confirmed in writing before the pilot evaluation.

| Source | Republish raw data? | Publish aggregates? | Attribution required | Note |
| --- | --- | --- | --- | --- |
| CVE.org records | Yes | Yes | CVE Terms of Use notice; CVE is a MITRE trademark | Allowed |
| CISA KEV and Vulnrichment | Yes | Yes | Credit CISA | US government work; CC0 |
| NVD | Yes | Yes | "Uses data from the NVD API but is not endorsed or certified by the NVD" | Allowed |
| FIRST EPSS | Yes | Yes | Credit FIRST and link first.org/epss | Allowed (verify current wording) |
| SEC EDGAR | Yes | Yes | None required | Public domain; follow fair-access rules |
| Shadowserver dashboard | No | Yes, with credit | Credit Shadowserver | Verify reuse terms |
| VulnCheck KEV (community) | No | Agreement scores only with permission | VulnCheck's attribution string | Verify; otherwise used internally only |
| Cloudflare Radar | Derived figures | Yes | Credit Cloudflare Radar | CC BY-NC: non-commercial use |
| ransomware.live | No | Counts only, no victim names | Credit ransomware.live | Check terms |

## Ethical limits

- **No scanning, no exploitation, no sensors.** The study never probes, tests or attacks any system, and runs no honeypots.
- **Aggregates only.** The study never handles host-level data; it uses counts others have already published.
- **No revictimization.** Ransomware victim names are dropped at capture and never published.
- **Responsible disclosure.** If the study comes across a previously unknown vulnerability or a live compromise in the data it pulls, it reports privately to the vendor or the relevant national CERT, and does not publish details until fixed.
- **AI involvement disclosed.** Claude writes the code and drafts each evaluation; the author approves every release. Each page says so, names the conflict of interest (Anthropic appears in the report), and links to the code that produced every number.

## Schedule

The pre-registration was frozen and registered on **20 October 2026**. Q4 2026 had already started by then, so it runs as a **pilot quarter**: evaluated and published in full, but labeled as a pilot. **Q1 2027 is the first confirmatory quarter.** The early-December deliverable becomes a **dry run on 1 December** using October and November data. It tests the pipeline end to end and gives a first look, clearly marked as unscored.

The full schedule is not repeated here, so that it is kept in one place. Every dated action item, with who is responsible (the author, the external reviewer, Claude or an automatic GitHub run), is in the [annual plan](../ANNUAL_PLAN.md), generated from `docs/schedule/schedule.yaml` together with the shared calendar feed and the milestone table in the README. How the schedule runs is described in [docs/OPERATIONS.md](../OPERATIONS.md).

## Costs

The study costs nothing in cash. It runs on free services and free data, plus the author's existing Claude account.

| Item | Service | Cost |
| --- | --- | --- |
| Scheduled pulls and analysis | GitHub Actions on a public repository | Free |
| Code and raw-file releases | GitHub public repository | Free |
| Evaluation pages | GitHub Pages | Free |
| Archive and DOI | Zenodo | Free |
| Pre-registration | OSF | Free |
| Data | All sources above | Free accounts and API keys |
| Code, checks and drafting | Claude | The author's existing account |

**Effort.** With Claude writing most of the code, the author's time before the dry run is roughly 15–25 hours: creating the accounts and repository, reviewing code, writing and freezing the pre-registration, and checking the backfill. Each quarter then takes about 4–6 hours: reviewing the run, checking the cohort, and approving the provisional and final evaluations. The heavy computing happens on GitHub, not in Claude, so a quarter needs only a session or two of Claude time. The November build may run into Claude plan usage limits on busy days, so it is best spread over several weeks.

**What being unfunded costs the study.** The exposure half of the race (T1b) and T2 depend on Shadowserver's coverage and may show "baseline building" for several quarters, though T1a, the patch-to-exploitation gap, works from the start. There is no GreyNoise data and no fingerprinting of our own. With one maintainer, a missed quarter is a real risk, which is why the runs are automated.

**The annual check.** The one possible cost is scan data for the annual check. If Censys grants free research access, it costs nothing beyond small query charges; otherwise it is a once-a-year licence, priced by quote. The harm comparison uses published reports and is free.

## Risks

| Risk | Likelihood | Effect | Mitigation |
| --- | --- | --- | --- |
| Shadowserver publishes no series for most cohort CVEs | High | T1b and T2 stay at "baseline building" | Edge devices selected first; pooling over four quarters; coverage reported each quarter |
| A free source changes its terms or closes its API | Medium | An indicator is lost | Each indicator has a fallback or is dropped with a dated deviation |
| A source shortens its history window | Low | A quarter can no longer be rebuilt | Pull promptly on the 1st; check history windows yearly |
| Events are lost between pulls (deleted posts, withdrawn KEV entries, revised advisories) | Medium | Undercounts in harm and exploitation | Sources that keep deletions; final re-run a month later; known blind spots documented |
| Source revises data after the pull | High | Numbers shift between provisional and final | Two-stage release; frozen bundles from both runs; changelog |
| Source outage on the 1st | Medium | A source missing from the evaluation | 48-hour retry; gap logged and filled at the final run where possible |
| Too few qualifying cohort CVEs | Medium | Short cohort, wide intervals | Report as short; pool across quarters; never hand-pick extras |
| Exploitation data sees only opportunistic attacks | Certain | T3, T4 and first-exploitation times miss targeted activity | State the limit on every page; triangulate the three sources |
| Small samples produce noisy swings | High | Over-reading one quarter | Confidence intervals published beside every label; the loose two-quarter rule stated on every page, with a companion test beside each label; direction history shown |
| CNA policy change or AI-generated report surge distorts CVE counts | Medium | T5 and T7 misread as real change | Changepoint flags; results with and without the five largest CNAs |
| Free tiers of GitHub or Zenodo change | Low | Pipeline or archive has to move | Containerized code runs anywhere, including a laptop |
| Author unavailable for a quarter | Medium | Evaluation delayed | Runs are automated; a late evaluation is published with a note, never skipped silently |
| Confirmation bias, including from an AI drafting the evaluation | Medium | Results read to fit expectations | Frozen rules; Claude drafts only from code outputs; author approval and external review; all seven questions always reported |

## Acceptance criteria

**Before the first evaluation**

- [x] Pre-registration frozen on OSF (done 20 October 2026), including the tracking questions, labeling rule, cohort rule, AI-credit term list, root-cause map and the T1b/T2 coverage rule
- [x] Public repository with pinned environment, and the scheduled workflow tested (test runs 21–22 October; environment pinned 24 October)
- [ ] Baselines backfilled, frozen and checksummed, including the retrospective cohort for Q4 2025 to Q3 2026
- [ ] Dry run on October–November data published by 1 December 2026, marked unscored
- [ ] Ground-truth test passed (at least four of five cases); the author records the fix dates on 16 November 2026
- [ ] Terms confirmed in writing for Shadowserver, VulnCheck and ransomware.live by the 21 December 2026 session, or the source excluded from the pilot

**Each quarter**

- [ ] Pull completed for every source within 48 hours of the 1st, with a complete manifest and every gap logged
- [ ] Provisional evaluation published on the 1st (by the 3rd if a source needed retries), final one month later
- [ ] All seven tracking questions reported with value, 90% interval, baseline, direction history and label, whatever the result
- [ ] Cohort of at least six CVEs across the quarter, or a documented short cohort
- [ ] Exposure coverage reported: how many cohort CVEs had a usable Shadowserver series
- [ ] `make reproduce` recreates every published number exactly
- [ ] Privacy check passed: no victim names or host identities in any public output
- [ ] Independent comparison table filled in, with disagreements explained
- [ ] Author approval recorded on each release; external reviewer sign-off for Q1 2027

## Open questions

1. **Substack.** Will posts about the study be free or paid? Free, or paid posts that only link to the site, keep the non-commercial sources usable. Project links are not shared publicly before 4 December 2026.
2. **External reviewer.** Answered in part: the author has a candidate (a physics graduate with data-science experience) and plans to recruit an undergraduate from Georgia universities, starting with the University of Georgia. To confirm by 15 March 2027; the review window is 3–28 April 2027.
3. **Institutional home.** Publishing under your name, an organization or a university partner affects how the results are received, which free research programmes you qualify for, and whether university career boards accept a posting.

Settled since 19 October: the GitHub repository is live (github.com/pagagne/internet-security-snapshot); Q4 2026 runs as the pilot and Q1 2027 as the first scored quarter; quarterly check-ins are on the author's calendar (approve the draft on the 2nd, hand checks from the 4th to the 28th, final-run check on the 2nd of the following month).
