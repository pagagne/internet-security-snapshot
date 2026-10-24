# Is AI Cleaning Up the Internet? A Primary-Data Threat Assessment

Oct 19, 2026 · @Paul

## Key judgments

**Bottom line: AI is making the internet less secure in the near term and has not started a cleanup. It has made vulnerabilities far cheaper to find, for both sides, without yet making them faster to exploit or measurably harder to exploit. The likeliest path to 2031 is a fragmented internet in which large platforms get safer and the long tail gets worse.**

1. **No cleanup is underway (high confidence).** None of the five cleanup indicators set before the evidence is met, and two are moving the wrong way: KEV additions hit 100 in 2026 Q3, ransomware leak-site victims rose 75% year on year in two independent counts, and Cloudflare saw DDoS volume, malicious email and bot traffic all climb in 2026.
2. **Time-to-exploit has not accelerated (moderate confidence).** About half of fresh KEV flaws are listed within 7 days of disclosure in every quarter since 2023; median lag is 3 days before 2025 and 4 days since (p = 0.13). The floor was already near zero for edge devices before capable AI agents.
3. **AI's clearest effect is on supply (high confidence).** NVD published 37,595 CVEs in 2026 Q3, 3.1 times a year earlier. Exploitation per known bug fell; exploitation in absolute terms rose 20% above the pre-AI trend over 2025–26, almost all of it in 2026 Q3.
4. **AI's share is bounded at roughly 1–20%, central 5–15%, of exploitation growth and under 5% of measured losses (low confidence).** Direct attribution floors are near 1%; the trend excess is a ceiling that also absorbs other causes.
5. **The US directive changed deadlines, not yet outcomes (high / low confidence).** KEV remediation windows fell from 21 to 3 days; the drop began in March 2026, three months before BOD 26-04. Internet-wide, vulnerable hosts take a median 88 days to halve, against a 7-day target; 2026 flaws halve faster (55 days vs 126 for 2025), but the difference is not yet significant (p = 0.14).
6. **Capability claims run 2–3 orders of magnitude ahead of attributable impact (moderate confidence).** Labs report tens of thousands of AI-found bugs; documented AI-run intrusions number in the dozens of campaigns; AI-linked losses are 4% of IC3's total.
7. **The defender bottleneck has moved from finding bugs to fixing them (moderate confidence).** 14% of one lab's disclosed high/critical findings were patched at its first update, and maintainers asked for slower disclosure.

| Outcome (dominant regime) | By 2028 | By 2031 |
| --- | --- | --- |
| Permanent arms race | 40% | 25% |
| Fragmentation | 35% | 30% |
| Walled gardens | 12% | 22% |
| Cleanup | 5% | 15% |
| Attacker breakout | 8% | 8% |

The thesis holds on "painfully". "Cleaned up" is a minority outcome even by 2031 unless consolidation into walled gardens counts, in which case it reaches about 37%.

## 1. Framing: the thesis made falsifiable

The thesis — "the internet will be cleaned up, painfully, on an unknown timeline" — is split below into six questions that data can answer no. The cleanup indicators and their thresholds were written before any dataset was opened, and they are not revised later in this report.

### Falsifiable questions

| # | Question | What would falsify a "yes" | Primary data |
| --- | --- | --- | --- |
| Q1 | Has AI shortened time-to-exploit beyond the pre-2025 trend? | 2025–26 exploitation lags sit inside the 95% prediction band of a 2022–24 trend | KEV × CVE record dates |
| Q2 | Does AI discovery produce more fixed bugs than exploited bugs? | AI-credited CVEs reach KEV at a rate ≥ the base KEV/CVE rate (≈1.4–2.7%) | CVE credits, KEV, lab disclosures |
| Q3 | Are defenders remediating faster, and did BOD 26-04 or CERT-In's blueprint cause it? | No level or slope break in remediation at the policy dates; no treated–control gap | KEV due dates, exposure scans |
| Q4 | Is harm falling? | Ransomware victims, IC3 losses and material 8-K filings flat or rising through 2026 | Leak-site counts, IC3, EDGAR |
| Q5 | Is the attack surface shrinking? | Exposed edge-device counts and the share of KEV in old bug classes do not fall | Censys/Shodan/Shadowserver, KEV CWEs |
| Q6 | Is security diverging by tier (fragmentation)? | Improvement is uniform across vendors and sectors, not concentrated in a few platforms | KEV by vendor; victim sectors |

### Cleanup indicators, set before the evidence

"Cleanup" means **all of C1–C3 and at least one of C4–C5 met for four consecutive quarters**. Anything less is not a cleanup, however encouraging.

| ID | Indicator | Threshold for "cleanup" | Baseline |
| --- | --- | --- | --- |
| C1 | Exploitation before or on disclosure day (share of new KEV entries) | < 15% | 2023–24 |
| C2 | New KEV entries per quarter while CVE volume is flat or rising | ≥ 25% below the 2025 quarterly mean | 2025 |
| C3 | Ransomware leak-site victims per quarter | ≥ 30% below the 2025 quarterly mean | 2025 |
| C4 | Median time to remediate a KEV flaw on internet-facing assets (exposure half-life) | ≤ 7 days | 2024 |
| C5 | Share of new KEV entries in memory-corruption, injection and path-traversal classes | ≥ one-third lower | 2023–24 |

## 2. Method and data access

The quantitative core is built from three primary datasets I could reach directly; everything else is graded secondary evidence. Six requested datasets were blocked by this workspace's network allowlist, and they are exactly the ones needed to measure defender patch speed.

### What was reached and what was not

| Dataset | Status | How used | What you would need to supply |
| --- | --- | --- | --- |
| [CISA KEV catalog](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json) v2026.10.16 (1,748 entries) | Reached (official GitHub mirror) | Exploitation events, due dates, ransomware flag, CWE | — |
| [CVE JSON 5 records](https://github.com/CVEProject/cvelistV5) for all 1,748 KEV CVEs | Reached | Publication dates, credits, CISA SSVC enrichment | — |
| [NVD API 2.0](https://services.nvd.nist.gov/rest/json/cves/2.0) quarterly totals, 2022Q1–2026Q3 | Reached (totals only) | Denominators: CVEs at risk per cohort | Full NVD feed for per-CVE CVSS/CPE |
| EPSS daily scores | Blocked | Not used | `epss_scores-YYYY-MM-DD.csv.gz`, monthly snapshots 2023–2026 |
| OSV.dev | Blocked | Not used | `all.zip` for PyPI, npm, Go, crates.io |
| GreyNoise / Shadowserver first-seen | API blocked; published reports read | Case evidence only | Supplied 19 Oct as a dashboard export; used in Section 3.4 |
| Censys / Shodan exposure | Blocked; published reports read | Context only | Weekly counts of exposed, unpatched hosts per KEV edge CVE |
| Cloudflare Radar | API blocked | Press-reported figures, graded down | Radar API token or CSV exports |
| SEC EDGAR full-text search | Blocked | Tracker compiled from EDGAR | EDGAR search export for "Item 1.05" |
| Ransomware leak sites | Blocked | Vendor counts (GuidePoint) | ransomware.live dump or similar |
| FBI IC3 | Report summary read | Annual losses | — |

### Analytic steps

1. **Join.** Each KEV entry was joined to its CVE record. *Exploitation lag* = KEV listing date − CVE publication date. KEV listing is an upper bound on first exploitation, so lags here overstate true time-to-exploit.
2. **Backlog filter.** "Fresh" entries have a lag between −30 and 365 days. This removes the 2021–22 load of decade-old CVEs that would otherwise dominate early quarters.
3. **Survival analysis.** Every CVE NVD published in a quarter is treated as at risk; the event is KEV listing; unlisted CVEs are censored at the catalog date. Curves are read only up to each cohort's minimum follow-up, so the Kaplan–Meier estimate is exact there. The output is cumulative KEV listings per 1,000 published CVEs at 0, 7, 30 and 90 days, with Wilson 95% intervals.
4. **Pre-AI baseline.** A linear trend is fitted to 2023Q1–2024Q4 — after the KEV launch backlog, before agentic coding models were in wide use — and projected through 2026Q3 with 95% prediction intervals. Observed minus baseline is an *upper bound* on the AI-attributable share, because other causes moved in the same window.
5. **Policy tests.** Interrupted time series (segmented OLS, Newey–West errors, lag 3) on monthly KEV remediation windows, with breaks at the first 14-day month (March 2026) and BOD 26-04 (June 2026). A difference-in-differences design for CERT-In was specified but could not be run (no country-level exposure data).
6. **Structured judgment.** Analysis of Competing Hypotheses across five outcomes, a pre-mortem, Admiralty grades for every source (reliability A–F × credibility 1–6), and confidence words used as: *high* = several independent primary sources agree; *moderate* = one primary source or agreeing secondary sources; *low* = inference or a single graded-down source.

Code and data are in the attached bundle; `python3 code/build_table.py && python3 code/analysis.py` reproduces every number in Sections 3–4 from the raw files.

## 3. Findings

### 3.1 Time-to-exploit has not accelerated (Q1)

**Judgment: through 2026 Q3 there is no measurable AI-driven acceleration in time-to-exploit (moderate confidence).** The floor was already near zero for edge devices before capable AI agents existed, so there is little room left to compress.

&#91;embedded content: CISA KEV v2026.10.16 joined to cvelistV5 publication dates; fresh = listed −30 to 365 days after publication; code: analysis.py §1\]

- Among CVEs listed within 90 days, the median lag was 3 days for 2022–24 publication cohorts (n = 303) and 4 days for 2025Q1–2026Q2 cohorts (n = 255). The distributions do not differ (Mann–Whitney p = 0.13; KS p = 0.48).
- About one-third of fresh KEV entries are listed within one day of publication in every quarter since 2023 (31–38% in 2025–26). Listings on or before the CVE's publication date were 25% of fresh entries in 2026 Q3, against 28% in 2023–24.
- VulnCheck's independent dataset agrees on direction: 23.4% of 1H 2026 KEVs were exploited on or before disclosure, against 28.9% in 2025 ([VulnCheck](https://www.vulncheck.com/blog/state-of-exploitation-1h-2026), B2).
- The clearest AI-orchestrated campaign, against PaperCut, launched five days after the vendor advisory and one day after CISA listed the flaws ([GreyNoise](https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf), B2). That is n-day weaponization at the speed human crews already achieve; the change is cost, not speed.

### 3.2 More bugs, more exploited bugs, lower rate per bug

**Judgment: AI is flooding the supply of known vulnerabilities, and exploited-flaw volume rose above trend in 2026 Q3 (high confidence on the counts; low confidence on cause).**

&#91;embedded content: CISA KEV v2026.10.16; trend fitted on 2023Q1–2024Q4; code: analysis.py §3\]

- NVD published 37,595 CVEs in 2026 Q3, 3.1 times the 12,207 of 2025 Q3; 2026 Q1–Q3 totals 74,721.
- Survival analysis over all published CVEs: KEV listings within 30 days per 1,000 CVEs fell from 3.3–4.2 (2023 Q2–Q4) to 2.0–2.2 (2025 Q3–2026 Q2). The per-bug hazard falls because the denominator explodes, not because exploitation slows.
- The 2026 Q3 spike (91 fresh entries) is broad: Microsoft 12, Cisco 7, Linux 5, then Citrix, JFrog, Fortinet and SonicWall at 4 each. Same-day listings were concentrated in edge and security appliances (Citrix NetScaler, Ivanti Connect Secure, PAN-OS, F5 BIG-IP, Check Point, Cisco ISE).
- One lab's output shows the scale: Project Glasswing logged 23,019 open-source findings in about a month, disclosed 530 high/critical ones, and saw 75 (14%) patched ([Anthropic](https://www.anthropic.com/research/glasswing-initial-update), B3). Discovery is no longer the bottleneck; verification and patching are.

### 3.3 How much is AI? Bounds, not a point

**Judgment: AI plausibly accounts for 5–15% of the 2025–26 growth in exploitation activity and under 5% of measured losses (low confidence).** Every direct measure is a floor and the trend excess is a ceiling; the truth sits between.

| Measure | Value | Bound | Confidence |
| --- | --- | --- | --- |
| Fresh KEV additions above the 2023–24 trend, 2025Q1–2026Q3 | 78 of 390 (20%) | Ceiling: also absorbs CVE volume, CISA listing effort, more reporters | Low |
| AI-discovered CVEs confirmed exploited, 1H 2026 ([VulnCheck](https://www.vulncheck.com/blog/state-of-exploitation-1h-2026)) | 14 of 495 KEVs (2.8%) | Floor on the discovery side | Moderate |
| KEV CVEs whose CVE record credits an AI tool or AI lab, 2025–26 | 5 of 509 (1.0%) | Floor: credits are sparse; Horizon3.ai humans excluded | Moderate |
| KEV CVEs with documented AI-agent mass exploitation, 2026 ([GreyNoise](https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf)) | 2 of 264 (0.8%) | Floor | Moderate |
| IC3 losses linked to AI, 2025 | $893M of $20.9B (4.3%) | Floor: victim self-report | Moderate |

The exploitation rate of AI-found bugs (14 of 1,061, 1.3%) is about the same as the base rate of KEV per CVE in 1H 2026 (1.4%). AI-found bugs are so far neither safer nor more dangerous than others; follow-up is short.

### 3.4 Patch speed and the policy tests (Q3)

**Judgment: BOD 26-04 demonstrably changed federal deadlines (high confidence). Internet-wide, vulnerable hosts are remediated far more slowly: exposure takes about three months to halve, though 2026 flaws are halving faster than 2025's (moderate confidence).**

&#91;embedded content: CISA KEV v2026.10.16, dueDate − dateAdded; segmented regression in analysis.py §4\]

- **US test (interrupted time series, monthly, Jan 2024–Oct 2026).** The mean window drops by 5.3 days in March 2026 (p < 0.001) and then falls a further 1.9 days a month (p < 0.001). At BOD 26-04 the share of 3-day windows jumps by 56 points (p < 0.001). Every one of the 18 entries added in October 2026 carries a 3-day deadline; 87 entries are flagged for forensic triage.
- **Attribution caveat.** The break starts three months before the directive ([Tenable](https://www.tenable.com/blog/cisa-bod-26-04-FAQ-vulnerability-remediation-impact), B2, dates BOD 26-04 to 10 June 2026). A June-only ITS would credit the directive with a change CISA was already making. Full Table 1 compliance is not due until about December 2026, so the outcome test belongs in 2027.
- **India test (difference-in-differences).** CERT-In's [blueprint](https://www.cert-in.org.in/s2cMainServlet?pageid=GUIDLNVIEW02&refcode=CISG-2026-02) (CISG-2026-02, 25 May 2026) sets 12 hours for exploited internet-facing flaws, per [The Hacker News](https://thehackernews.com/2026/05/cert-in-mandates-12-hour-patching-for.html) (C3); its binding status is unclear. The design is specified but was not run, by choice, in favour of the internet-wide exposure test below: treated = Indian hosts, controls = comparable economies, outcome = log exposed-vulnerable hosts on days 0–30 for each KEV edge CVE, pre = Jan–May 2026, post = Jun–Oct 2026. It needs one Shadowserver dashboard export per country.
- **Point evidence agrees with the scan data below.** More than 20,000 NetScaler instances were visible and potentially at risk at the late-September 2026 disclosure ([Cybersecurity Dive](https://www.cybersecuritydive.com/news/cisa-citrix-netscaler-customers-patch-new-flaws-disclosed/832741/), citing Shadowserver, B3). Glasswing patches that shipped took about two weeks on average; 86% of disclosed findings were unpatched at the update.

### Exposure decay: how fast vulnerable hosts disappear

For 118 CVEs that Shadowserver began scanning in 2025–26, I measured how long each CVE's count of vulnerable hosts took to fall to half its peak. CVEs not yet halved are censored at the end of the data; six series that collapsed to zero overnight are treated as scan changes, not patching.

&#91;embedded content: Shadowserver public dashboard export (scan, http\_vulnerable, exchange sources; 14 countries summed; daily unique IPs, indicative); 118 CVE tags first detected 2025-01-15 to 2026-10-18; code: exposure\_decay.py\]

- **C4 is far from met.** The median exposure half-life is 88 days overall. Only 9 of 118 CVEs (8%) halved within the 7-day target.
- **2026 is faster, but not yet significantly.** The median is 126 days for 2025 flaws (n = 47) and 55 days for 2026 flaws (n = 71); log-rank p = 0.14. The first month looks the same in both years; the gap opens between days 30 and 120.
- **Exploited flaws are not patched faster.** KEV-listed CVEs halve in a median 94 days, against 78 for the rest.
- **The fastest cases are auto-updating software**: WordPress plugins and GitLab halved within 4 days. Edge appliances and mail servers (SmarterMail, Zimbra) mostly held above 70% after a month.
- Shadowserver sums daily unique-IP counts, so absolute figures are indicative; ratios to each CVE's own peak are less affected. The series are the sum of the 14 countries selected, not a global total.

### 3.5 Harm is rising (Q4)

**Judgment: every measure of impact that can be counted rose in 2025–26 including material 8-K filings after a regulatory dip in 2025 (high confidence).**

| Indicator | Latest | Change | Grade |
| --- | --- | --- | --- |
| Ransomware leak-site victims ([GuidePoint GRIT](https://www.guidepointsecurity.com/blog/ransomware-insights-q3-2026/)) | 2,760 (GRIT), 2,940 (ransomware.live) in Q3 2026 | +75% YoY; 112 groups (+47%) | B3 |
| FBI IC3 reported losses ([Help Net Security summary](https://www.helpnetsecurity.com/2026/04/07/online-crime-financial-losses-fbi-report/)) | $20.9B in 2025 | +26% YoY | A2 |
| Cloudflare DDoS attacks over 1 Tbps ([SiliconANGLE](https://siliconangle.com/2026/08/11/cloudflare-says-1-tbps-ddos-attacks-grew-sixfold-second-quarter/)) | 805 in Q2 2026 | 6.2× Q1 | B2 |
| Zero-days exploited in the wild ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/)) | 90 in 2025 | 78 (2024), 100 (2023): inside the 60–100 band | A2 |
| Form 8-K Item 1.05 filings ([Cherry Hill tracker](https://www.cherryhilladvisory.com/sec-cybersecurity-disclosure-rule-two-year-review), from EDGAR) | 15 original filings in 2026 to 18 Oct (EDGAR) | EDGAR: 22 (2024) → 8 (2025) → 15 (2026 YTD) | C2 |

Material 8-K filings dipped in 2025 because of 2024 SEC staff guidance steering non-material incidents to Item 8.01, and filers decide materiality themselves. A direct EDGAR full-text count finds original Item 1.05 filings rose again, from 8 in 2025 to 15 in 2026 through 18 October; the phrase search slightly undercounts, finding 22 for 2024 where the tracker lists 25.

### Primary telemetry added 19 October: Cloudflare Radar, ransomware.live, EDGAR, EPSS

**Judgment: four independent Cloudflare measures all rose in 2026, and a second leak-site dataset confirms the ransomware surge (high confidence on direction, moderate on size).**

&#91;embedded content: Cloudflare Radar API, weekly series 2023-01-02 to 2026-10-12, averaged by quarter; index series chain-linked across yearly queries; code: fetch\_radar.py\]

- **DDoS.** Network-layer DDoS volume in 2026 Q1–Q3 averaged 2.5 times the 2025 level, peaking in Q2. This matches Cloudflare's published count of attacks over 1 Tbps rising sixfold in Q2.
- **Web attacks.** Mitigated web-attack requests in 2026 Q2–Q3 ran 19% above the 2025 average and are near their 2023–26 high.
- **Malicious email.** The malicious share of email Cloudflare scans was 4–5% through mid-2025, then rose to 12% in 2026 Q1 and 24% in Q2 before easing to 10%. Scam-category messages jumped to 37% of flagged email in 2026 Q1. Cloudflare's email customer mix can shift these shares, so treat the spike's size with caution.
- **Bots.** Automated traffic held at 29–30% of web requests from 2023 to 2025, then rose to 36% in 2026 Q3 and 39% in October. AI crawlers are a steady 17–22% of identified bot traffic, so the growth is broader automation, not only AI crawling.
- **Ransomware, second source.** [ransomware.live](https://www.ransomware.live) counts 2,940 leak-site victims in 2026 Q3 against 1,672 a year earlier (+76%), posted by 107 groups against 77. This agrees with GuidePoint's +75%.
- **Exploitation is not becoming less predictable.** The median [EPSS](https://www.first.org/epss/) score of a KEV flaw the day before CISA listed it rose from 0.001 (2024) to 0.005 (2026), and the share scoring under 1% fell from 77% to 64%. There is no sign of a wave of AI-driven exploitation of obscure, unexpected bugs.

### 3.6 Attack surface and fragmentation (Q5, Q6)

**Judgment: the bug mix is slowly improving at the top of the market while exploitation spreads into the long tail (moderate confidence).**

| Year | KEV added | Memory corruption share | Edge-vendor share | Distinct vendors | Top-5 vendor share | Ransomware-linked |
| --- | --- | --- | --- | --- | --- | --- |
| 2026 (to 16 Oct) | 264 | 15.2% | 22.3% | 101 | 32% | 10%\* |
| 2025 | 245 | 18.4% | 22.0% | 99 | 29% | 13%\* |
| 2024 | 186 | 16.1% | 23.7% | 64 | 38% | 24% |
| 2023 | 187 | 26.2% | 17.1% | 67 | 37% | 23% |

\*CISA updates the ransomware flag months after listing, so recent years are understated.

- Memory-corruption KEVs fell 28% against the 2023–24 mean, consistent with memory-safe code at large vendors, but short of the one-third threshold (C5).
- Exploited vendors rose from 64 to 101 a year. Exploitation is spreading to smaller vendors, not concentrating on a few patched platforms.
- AI infrastructure is now attack surface: four Langflow KEVs in 2026, and 175,000 exposed Ollama servers ([GreyNoise State of the Edge](https://greynoise.io/resources/2026-state-of-the-edge-report), citing SentinelLABS/Censys, B2). Exposed ICS hosts rose 4% to about 134,000 ([Censys](https://censys.com/?p=11187), B2).
- Victims of AI-run campaigns sit in the long tail: 204 of 395 PaperCut victims were in education.

### 3.7 Capability, incidents and impact are three different claims

| Layer | Strongest evidence | What it shows |
| --- | --- | --- |
| Capability | Glasswing partners: 10,000+ high/critical findings in a month; 271 Firefox 150 bugs ([Anthropic](https://www.anthropic.com/research/glasswing-initial-update), B3). GTIG: LLMs find logic flaws that fuzzers miss ([GTIG](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access), B2) | Discovery cost has collapsed |
| Incidents | PaperCut: 395 orgs, 11 in 26 seconds, agents drifting outside the operator's own target rules (GreyNoise, B2). Anthropic's [September 2026 report](https://anthropic.com/threat-intelligence-report-september-2026): six cyber cases with high autonomy, incl. \~200 downstream SaaS customers in one (B2). GTIG: one AI-built zero-day, disrupted before mass use | Attack cost per campaign has fallen; skill no longer signals actor |
| Impact | IC3: 4.3% of losses AI-linked; no leak-site, 8-K or GTIG zero-day dataset attributes outcomes to AI | Measured harm attributable to AI is small and lags capability by 2–3 orders of magnitude |

### 3.8 Scorecard against the pre-registered cleanup indicators

**Judgment: no cleanup is underway by the definition set in Section 1 (high confidence).** None of the five indicators is met, and two are moving the wrong way.

| ID | Threshold | Latest | Status |
| --- | --- | --- | --- |
| C1 | < 15% exploited on or before disclosure | 25% (KEV proxy, fresh entries, 2026 Q3); 23.4% (VulnCheck, 1H 2026) | Not met; improving slowly |
| C2 | ≤ 46 KEV additions a quarter (25% under the 2025 mean of 61) | 100 in 2026 Q3 | Not met; wrong direction |
| C3 | ≤ 70% of 2025 quarterly victims | 2,760 (GRIT) and 2,940 (ransomware.live) vs about 1,600 a year earlier | Not met; wrong direction |
| C4 | KEV exposure half-life ≤ 7 days | Median 88 days (55 days for 2026 flaws); 8% of CVEs halve within 7 days | Not met; improving |
| C5 | Memory-corruption share down ≥ one-third | Down 28% | Not met; closest |

## 4. Analysis of Competing Hypotheses

**Judgment: "permanent arms race" and "fragmentation" are the only hypotheses with no inconsistent evidence; "cleanup" is the most contradicted after "attacker breakout" (moderate confidence).** The two survivors are not exclusive: fragmentation is an arms race whose outcomes diverge by tier. The evidence that separates them (E3, E5, E7) leans toward fragmentation.

### Hypotheses (dominant regime by the forecast date)

- **H1 Cleanup.** All of C1–C3 plus C4 or C5 met for four quarters; AI is net-defensive.
- **H2 Permanent arms race.** Both sides scale; exploitation and harm grow roughly with digital activity; no regime change.
- **H3 Fragmentation.** Large platforms and vendors measurably improve while the long tail (SMBs, education, edge devices, open-source maintainers) worsens.
- **H4 Walled gardens.** Security arrives mainly through consolidation: managed platforms, gated software and agent ecosystems, mandated deadlines; the open long tail is abandoned or regulated out.
- **H5 Attacker breakout.** Defenders cannot absorb AI-driven volume; systemic, multi-sector incidents become routine.

### Matrix

Scores: ++ strongly consistent, + consistent, 0 neutral, − inconsistent, −− strongly inconsistent. Only inconsistencies count against a hypothesis (− = 1, −− = 2).

| Evidence (grade) | H1 Cleanup | H2 Arms race | H3 Fragment. | H4 Walled | H5 Breakout |
| --- | --- | --- | --- | --- | --- |
| E1 Time-to-exploit flat 2023–26 (A1) | 0 | + | 0 | 0 | − |
| E2 Fresh KEV 2026 Q3 above trend (A1) | − | + | + | 0 | + |
| E3 CVE volume ×3; 14% of Glasswing disclosures patched (A2/B3) | − | + | ++ | + | + |
| E4 Leak-site victims +75%, IC3 losses +26% (B3/A2) | −− | + | + | 0 | + |
| E5 AI-run campaigns hit education and SMBs (B2) | − | + | ++ | + | + |
| E6 Memory-corruption KEV share down 28% (A1) | + | 0 | + | + | − |
| E7 Exploited vendors 64 → 101 a year (A1) | − | 0 | ++ | − | + |
| E8 Deadlines 21 → 3 days; CERT-In 12 h (A1/C3) | + | + | 0 | + | 0 |
| E9 Defensive AI wins; AI-found bugs exploited at base rate (B2/B3) | + | + | 0 | + | − |
| E10 Zero-days stay in the 60–100 band (A2) | 0 | ++ | 0 | 0 | − |
| E11 AI-attributable harm about 4% of losses (A3) | 0 | + | 0 | 0 | −− |
| E12 Edge devices 22% of KEV, most same-day listings (A1) | − | + | + | ++ | + |
| **Inconsistency score** | **7** | **0** | **0** | **1** | **6** |

The most diagnostic items are E4 and E7. A sustained fall in leak-site victims would rescue H1; a fall in the number of exploited vendors would move weight from H3 to H4.

### Pre-mortem: it is 2031 and this assessment was wrong. Why?

1. **KEV was the wrong instrument.** CISA lists a few hundred flaws a year, so KEV cannot show volume growth in web apps, libraries and small vendors. If AI exploitation grew mainly there, this report understated attacker gains. *Check:* VulnCheck's broader KEV count against CISA's.
2. **Bug depletion arrived early.** AI swept the major codebases faster than new bugs were written, and 2026 was the CVE peak. Exploitable flaws at large vendors then fell steeply from 2028, and cleanup came to the core sooner than forecast. *Check:* CVE volume per major vendor falling for four quarters.
3. **An open-weights model with Mythos-class cyber skill shipped.** Gated access was the main brake on offensive diffusion; once removed, breakout followed. *Check:* release of such a model.
4. **Harm metrics misled.** Leak-site counts rose because AI made it cheap to extort small, low-value victims, while dollars per victim fell. *Check:* IC3 losses per complaint; insurer loss ratios.
5. **Regulation consolidated the market faster.** Deadlines, liability and the EU Cyber Resilience Act's obligations pushed buyers to managed platforms, so H4 won outright.
6. **Author bias.** As an Anthropic model I may have over-credited lab-run defense or under-weighted lab capability claims (Section 6).

## 5. Forecasts

**Judgment: the thesis is half right. "Painfully" is already true; "cleaned up" is a 15% outcome by 2031, rising to about 37% if walled-garden consolidation counts as a cleanup (low confidence on the long horizon).**

&#91;embedded content: Analyst judgment from Sections 3–4; outcomes are mutually exclusive regimes\]

The shift from 2028 to 2031 rests on two mechanisms: AI bug-sweeping depleting flaws in the largest codebases, and buyers moving to managed platforms under deadline and liability pressure. Both help the core of the internet first, which is why fragmentation and walled gardens together stay above 50% in both years.

### Signposts that would move these numbers

| Signpost | Moves toward | Size of move |
| --- | --- | --- |
| Leak-site victims ≥ 30% below the 2025 mean for two quarters | Cleanup | +10 pts |
| CVE volume at the top-20 vendors falls for four quarters while KEV additions fall | Cleanup, walled gardens | +5 each |
| Shadowserver exposure half-life for KEV edge CVEs ≤ 7 days | Cleanup | +5 |
| An open-weights model with Mythos-class cyber capability is released | Breakout | +10; cleanup −5 |
| An AI-agent breach of one SaaS or cloud provider reaches > 1,000 downstream customers | Breakout | +5 |
| Exploited vendors in KEV fall below 70 a year | Walled gardens | +5; fragmentation −5 |
| Insurers require managed platforms for SMB cover | Walled gardens | +5 |

### Prediction register

Each prediction resolves from a public dataset on or after the date shown; the first falls due Jan 5, 2027. Score with the Brier rule.

| # | Prediction | Resolves | Resolution source | p |
| --- | --- | --- | --- | --- |
| P1 | CISA KEV additions in calendar 2026 are ≥ 320 | 2027-01-05 | KEV JSON, dateAdded | 0.80 |
| P2 | NVD publishes ≥ 100,000 CVEs in calendar 2026 | 2027-01-05 | NVD API totalResults | 0.85 |
| P3 | GuidePoint GRIT full-year 2026 ransomware victims exceed full-year 2025 | 2027-02-28 | GRIT annual report | 0.90 |
| P4 | FBI IC3 2026 report shows losses > $20.9B | 2027-05-31 | IC3 annual report | 0.75 |
| P5 | A new primary vendor or lab report documents an AI-agent campaign with ≥ 100 victim organizations | 2027-06-30 | Vendor or lab publication | 0.80 |
| P6 | Anthropic or a Glasswing partner reports ≥ 50% of disclosed high/critical findings patched | 2027-06-30 | Anthropic publication | 0.55 |
| P7 | Share of fresh KEV entries listed ≤ 7 days after publication, calendar 2027, is 40–60% | 2028-01-10 | analysis.py on KEV | 0.75 |
| P8 | Memory-corruption share of 2027 KEV additions is ≤ 15% | 2028-01-10 | analysis.py on KEV | 0.50 |
| P9 | C1 met: < 15% of fresh KEV listed on or before publication in any 2027 quarter | 2028-01-10 | analysis.py on KEV | 0.07 |
| P10 | Any 2027 quarter has leak-site victims ≥ 30% below the 2025 quarterly mean | 2028-02-28 | GRIT quarterly | 0.08 |

The register is also in the bundle as `predictions.csv`, with blank outcome and Brier columns.

## 6. Where datasets agree, where they conflict, and limitations

### Agreement and conflict

| Question | Agree | Conflict or tension | Resolution |
| --- | --- | --- | --- |
| Is exploitation getting faster? | CISA KEV (this analysis) and VulnCheck: no; zero-day share flat or down | Vendor blogs claim time-to-exploit has "gone negative" | Both are true: it went near zero before 2025 for edge devices; it has not moved since |
| Median time to exploit | — | VulnCheck median 80 days (1H 2026); this analysis 4–7 days | Different populations: VulnCheck counts old CVEs newly exploited; this analysis filters to fresh CVEs |
| Is exploitation volume up? | KEV (+20% vs trend), VulnCheck (+10% half on half), GreyNoise (212 attempts/s) | VulnCheck: KEV-to-CVE ratio fell from 2.7% to 1.4% | Volume up in absolute terms, down per known bug, because AI discovery inflates the denominator |
| Is harm up? | GRIT victims, IC3 losses, Cloudflare >1 Tbps attacks all up | Material 8-K filings halved in 2025, then rebounded in 2026 (8 → 15) | 8-K fall is regulatory (2024 SEC guidance), not a decline in incidents |
| Is AI changing outcomes? | Anthropic, GTIG, GreyNoise: real AI-run intrusions | GTIG's zero-day review attributes none of 2025's 90 zero-days to AI; IC3 attributes 4% of losses | Capability and incidents are ahead of measurable impact; attribution methods lag |
| Did BOD 26-04 change behaviour? | KEV due dates: yes, sharply | Break begins in March, three months before the directive | The policy change preceded its formal issue; outcome effect untested |

### Limitations

- **KEV is a lagging, capacity-limited instrument.** Listing dates are upper bounds on first exploitation, and CISA's staffing and priorities shape them. A faster CISA after BOD 26-04 could mimic faster exploitation.
- **Patch speed is measured only as exposure decay.** It comes from Shadowserver's public dashboard, summed over 14 countries, with indicative unique-IP counts; a halving can reflect scan-coverage changes as well as patching. The CERT-In country test was not run, because it needs one export per country.
- **Denominators are approximate.** NVD quarterly totals include records later rejected and use NVD's own publication date, which can differ from the CVE record by days.
- **Pre-AI baseline is short.** Eight quarters give wide prediction intervals; only 2026 Q3 escapes them. A longer baseline would include the KEV launch backlog.
- **Secondary summaries were used where primary pages would not render** (IC3, Cloudflare, GRIT, 8-K tracker). Each is graded down for that.
- **Leak-site counts measure extortion claims, not breaches**, and are inflated by re-posts and false claims.

### Potential bias as an Anthropic model

I am Claude, built by Anthropic, and several sources here are Anthropic's own: the Glasswing update and the September 2026 threat report. Three biases are plausible.

1. **Self-interest in "AI helps defense".** I may over-weight Glasswing's patch numbers. Mitigation: graded B3, treated as capability rather than impact, and the AI-found-bug exploitation rate came from VulnCheck, not Anthropic.
2. **Self-interest in "AI threat is real, so gated models matter".** Anthropic's threat reports support its case for restricting Mythos-class access. Mitigation: those cases sit in the incident layer only and are not used in any quantitative estimate.
3. **Reluctance to blame AI labs for harm.** Mitigation: the attribution ceiling (20%) is reported prominently, and "attacker breakout" was kept as a hypothesis.

A reader should check the Anthropic-sourced rows in Section 7 first and rerun the code without them; none of the statistical tests in Sections 3.1–3.4 uses them.

## 7. Source register (Admiralty Code)

Reliability: A completely reliable … F cannot be judged. Credibility: 1 confirmed by other sources … 6 cannot be judged. "Read" = the page actually opened for this report.

| Source | Type | Read | Grade | Used for |
| --- | --- | --- | --- | --- |
| [CISA KEV catalog](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json) v2026.10.16 | Primary dataset | Raw JSON | A1 | Exploitation events, deadlines |
| [CVE records, cvelistV5](https://github.com/CVEProject/cvelistV5) | Primary dataset | 1,748 raw records | A1 | Publication dates, credits |
| [NVD API 2.0](https://services.nvd.nist.gov/rest/json/cves/2.0) | Primary dataset | Quarterly totals | A2 | Denominators |
| [VulnCheck State of Exploitation 1H 2026](https://www.vulncheck.com/blog/state-of-exploitation-1h-2026) | Vendor research | Yes | B2 | Cross-check; AI-found bugs |
| [GreyNoise: AI-orchestrated PaperCut campaign](https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf) | Primary incident write-up | Yes | B2 | AI incident evidence |
| [GreyNoise 2026 State of the Edge](https://greynoise.io/resources/2026-state-of-the-edge-report) | Vendor research | Yes | B2 | Scanning volume, exposure |
| [Google GTIG: AI for exploitation and initial access](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access) | Primary threat intel | Yes | B2 | AI incidents, capability |
| [Google GTIG 2025 zero-day review](https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/) | Primary threat intel | Yes | A2 | Zero-day counts |
| [Anthropic threat report, Sept 2026](https://anthropic.com/threat-intelligence-report-september-2026) | Lab disclosure (interested party) | Yes, first 100k chars | B2 | AI incident evidence |
| [Anthropic Glasswing initial update](https://www.anthropic.com/research/glasswing-initial-update) | Lab disclosure (interested party) | Yes | B3 | Capability, patch backlog |
| FBI IC3 2025 report, via [Help Net Security](https://www.helpnetsecurity.com/2026/04/07/online-crime-financial-losses-fbi-report/) | Government report, secondary summary | Summary only | A2 (AI figures A3) | Losses |
| [GuidePoint GRIT Q3 2026](https://www.guidepointsecurity.com/blog/ransomware-insights-q3-2026/) | Vendor leak-site tracking | Yes | B3 | Ransomware victims |
| Cloudflare DDoS report, via [SiliconANGLE](https://siliconangle.com/2026/08/11/cloudflare-says-1-tbps-ddos-attacks-grew-sixfold-second-quarter/) | Telemetry, secondary | Summary only | B2 | DDoS trend |
| [Cherry Hill 8-K tracker](https://www.cherryhilladvisory.com/sec-cybersecurity-disclosure-rule-two-year-review) | Compiled from EDGAR | Yes | C2 | 8-K counts |
| [Tenable BOD 26-04 FAQ](https://www.tenable.com/blog/cisa-bod-26-04-FAQ-vulnerability-remediation-impact); [Inside Government Contracts](https://www.insidegovernmentcontracts.com/2026/06/cisa-releases-binding-operational-directive-on-prioritizing-security-updates-based-on-risk/) | Secondary on a directive (CISA page failed to load) | Yes | B2 | BOD 26-04 dates and tiers |
| [CERT-In CISG-2026-02 listing](https://www.cert-in.org.in/s2cMainServlet?pageid=GUIDLNVIEW02&refcode=CISG-2026-02) | Primary listing; PDF not read | Listing only | A2 | Title, date |
| [The Hacker News on CERT-In](https://thehackernews.com/2026/05/cert-in-mandates-12-hour-patching-for.html) | Press | Yes | C3 | CERT-In timelines |
| [Cybersecurity Dive on NetScaler](https://www.cybersecuritydive.com/news/cisa-citrix-netscaler-customers-patch-new-flaws-disclosed/832741/) | Press citing Shadowserver | Yes | B3 | Exposure at disclosure |
| [Censys ICS exposure](https://censys.com/?p=11187) | Scan data summary | Yes | B2 | Exposure trend |

Added: [Shadowserver public dashboard](https://dashboard.shadowserver.org/help/), time-series export by the user on 19 October 2026 (vulnerability-scan sources, CVE tags, 14 countries). Grade B2: primary scan telemetry, counts indicative by Shadowserver's own note.

Added: [Cloudflare Radar API](https://developers.cloudflare.com/radar/) (A2: primary telemetry, one large provider's view); [ransomware.live](https://www.ransomware.live) v2 monthly victim lists (B2: leak-site claims, agrees with GRIT); [SEC EDGAR full-text search](https://efts.sec.gov/LATEST/search-index?q=%22Material%20Cybersecurity%20Incidents%22&forms=8-K) (A1 source, phrase search a slight undercount); [FIRST EPSS API](https://www.first.org/epss/api) (A2).

## 8. Data appendix

The bundle `ai_cleanup_assessment.zip` reproduces Sections 3.1–3.6 from raw files. Run from its root: `python3 code/fetch_cve.py` (optional refresh), `python3 code/build_table.py`, `python3 code/analysis.py`. Only numpy, scipy, pandas and matplotlib are needed.

| File | Contents |
| --- | --- |
| `data/kev.json` | CISA KEV v2026.10.16, 1,748 entries |
| `data/cve/*.json` | 1,748 CVE JSON 5 records |
| `data/nvd_quarterly_counts.csv` | NVD published-CVE totals, 2022Q1–2026Q3 |
| `data/kev_joined.csv` | One row per KEV entry with dates, credits, SSVC |
| `out/quarterly_exploitation.csv` | Section 3.1 series |
| `out/survival_by_pub_quarter.csv` | KM incidence per 1,000 CVEs at 0/7/30/90 days |
| `out/trend_baseline_excess.csv` | Pre-AI trend, prediction intervals, excess |
| `out/its_remediation_window.csv`, `out/monthly_windows.csv` | Section 3.4 models and data |
| `out/cwe_class_share_by_year.csv`, `out/yearly_summary.csv` | Section 3.6 |
| `predictions.csv` | Prediction register for scoring |

Added 19 October: `data/shadowserver/cve_tags_14countries_2025-01-01_2026-10-18.csv` (dashboard export, 276 CVE tags), `code/exposure_decay.py`, and its outputs `out/exposure_decay_by_cve.csv`, `out/exposure_decay_summary.csv` and `out/exposure_decay_km_curve.csv`.

Also added 19 October: `code/fetch_radar.py` with `data/radar/` (7 weekly series plus raw JSON; needs a Radar read token in CLOUDFLARE\_TOKEN), `code/fetch_edgar_ransomware.py` with `data/edgar/` and `data/ransomware/`, and `code/fetch_epss.py` with `data/epss/`.

To close the open questions, add: one Shadowserver dashboard export per country (CERT-In DiD); EPSS monthly snapshots (does EPSS anticipate AI-era KEVs?); OSV `all.zip` (open-source exploitation outside KEV); an EDGAR export for Item 1.05 and 8.01.

## 9. Glossary

| Term | Meaning |
| --- | --- |
| ACH | Analysis of Competing Hypotheses: scoring evidence against every hypothesis and rejecting the most contradicted |
| Admiralty Code | Two-part grade: source reliability (A–F) and information credibility (1–6) |
| BOD 26-04 | CISA Binding Operational Directive of 10 June 2026 setting risk-tiered remediation deadlines (3 to 60 days) for US federal agencies; replaces BOD 22-01 |
| CERT-In blueprint | India's CISG-2026-02 guidance of 25 May 2026 on AI-assisted exploitation |
| CVE / CNA | Common Vulnerabilities and Exposures identifier / the authority that assigns it |
| DiD | Difference-in-differences: comparing the change in a treated group with the change in a control group |
| EPSS | Exploit Prediction Scoring System, a daily probability of exploitation per CVE |
| Exploitation lag | Days from CVE publication to KEV listing; an upper bound on time-to-exploit |
| Fresh KEV entry | KEV entry listed between 30 days before and 365 days after its CVE was published |
| ITS | Interrupted time series: testing for a level or slope change at an intervention date |
| KEV | CISA's Known Exploited Vulnerabilities catalog |
| Kaplan–Meier | Survival estimator that handles observations not yet ended (censored) |
| Leak site | Website where an extortion group names victims and posts stolen data |
| SSVC | Stakeholder-Specific Vulnerability Categorization, CISA's decision-tree enrichment of CVE records |
| Zero-day | Flaw exploited before or on the day it is disclosed |
