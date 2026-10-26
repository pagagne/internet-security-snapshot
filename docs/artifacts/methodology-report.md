# Methodology Report: Quarterly Internet Security Snapshot

Oct 24, 2026 · @Paul

## Summary

The Quarterly Internet Security Snapshot is a free, independent study. It tracks, quarter by quarter, whether internet security is getting better or worse, and how AI is involved. Its central question: **are defenders closing internet-exposed vulnerabilities faster than attackers start exploiting them?**

**Where it stands on 24 October 2026:**

- The research plan is registered on the Open Science Framework (OSF): [DOI 10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82). Changes since then are logged in the repository's deviations file.
- The public code repository is live at [github.com/pagagne/internet-security-snapshot](https://github.com/pagagne/internet-security-snapshot). All seven free sources are collected in test runs; the three that need permission stay switched off for publishing until it arrives.
- The race measure and the AI-credit rule were settled on 23 October (Step 12).
- A statistical review on 24 October added a pinned software environment, date ranges instead of single dates, a check on the labelling rule and a second coder for the hand checks (Step 13).
- All four API keys are stored as GitHub secrets, and permission requests are out to the three data providers whose terms limit publishing.

This report sets out, step by step, how the study got here: the data sources and keys it uses, how each quarterly run works, and what it is expected to deliver.

## Step by step: how we got here

**Step 1: The research report (18–19 October).** We built a ranked review of news and research on AI and internet security. It was refined from 100 articles to 75 and then to 50, expanded internationally to include sources from China and Russia, fact-checked, and stress-tested by an adversarial review. Its thesis was that the internet will be cleaned up, painfully. The review found the thesis held only in a softer form.

**Step 2: From dashboard idea to measurement spec.** A global live dashboard was scoped and judged too large. It was cut to a one-month prototype, then rebuilt as a measurement spec. The spec had pre-registered hypotheses, validated indicators, raw versioned data, a followed group of vulnerabilities (the cohort), and rigorous statistics.

**Step 3: Right-sizing.** The spec went from daily capture to a monthly pull, then to a free quarterly study run by one person with Claude's help. Paid data, honeypots and the live feed were dropped. Every source had to be free and keep its own history.

**Step 4: Reframing the questions.** The cleanup hypotheses were replaced by seven neutral tracking questions about whether things are getting better or worse, with the race between patching and exploitation as the central one. Your expectations became stated predictions. A loose rule labels a direction after two quarters moving the same way.

**Step 5: Refining the cohort and evidence base.** Following the Salesforce article on agentic security, each cohort vulnerability gets a root-cause tag, and a fourth monthly slot was added for a vulnerability credited to an AI tool. Research on the data gaps was summarized as proven, early or speculative. On 21 October 2026, before any cohort was selected, the pick within each slot changed from "first published that month" to a seeded random draw, because the earliest flaw each month would favour vendors that publish early. The change is logged as a deviation from the registered plan.

**Step 6: Adding the annual check.** Each March, the year's free results are compared with reference scan data and published insurance-claims and ransom-payment figures. The comparison is reported, not graded.

**Step 7: Freezing and registering the plan (20 October).** The plan and its three rule files were frozen, checksummed, tagged `prereg-v1.0` on GitHub, and registered on OSF with DOI 10.17605/OSF.IO/3XT82.

**Step 8: Building the repository and first code.** We set up a public GitHub repository with:

- a README, licences, a deviations log and a permissions log;
- collectors for CISA's exploited-vulnerability catalog and for all CVE records, both tested on live data;
- classifiers for AI credits, root cause and product category, with 21 passing tests;
- a scheduled quarterly workflow that can also be run by hand.

**Step 9: Accounts, keys and permissions.** Free accounts were opened with NVD, VulnCheck, Cloudflare and ransomware.live, and their keys were saved as GitHub secrets. Permission requests were sent to Shadowserver, VulnCheck and ransomware.live, and the relevant terms of service were reviewed and logged.

**Step 10: Locking the core and opening an exploratory layer (21–22 October).** The core rules were locked by checksum and released as `core-v1.1`, with GitHub rules that stop tags or the main branch being rewritten. New ideas now go to a separate exploratory layer that never decides a label. It covers attacker-side AI that the core cannot see: a log of AI-run attack campaigns, flaws in AI software, fingerprints of faster attacks, and a log of open-weight model releases. A final core freeze is set for 31 December.

**Step 11: Test runs and hand-check tooling (21–22 October).** Six test runs on Q3 2026 data took collection from failing after 80 minutes to all seven sources in about six minutes, fixing slow NVD downloads, a mis-saved Cloudflare token and an SEC search quirk. Each run now writes a data-quality report with drift checks and saves its log for diagnosis. A private Hand Check app replaced the spreadsheet: it walks the author through AI credits and cohort picks, pre-fills fix dates, and records every answer in a public decisions file.

**Step 12: Settling the race and the AI-credit rule (22–23 October).** A back-test on Q2 and Q3 2026 showed the registered cohort holds only 0.3 to 0.4 attacked flaws a quarter, too few for a race median. The race is now measured on every flaw first added to CISA's attacked-flaws list in the quarter (75 to 100 a quarter): the median days from the fix to the first attack. The share attacked before any fix existed stays exploratory until a year of data shows it is steady, and the registered cohort version is reported alongside for four quarters. For AI credits, the headline counts any credit that mentions an AI tool or frontier AI lab; the registered, narrower count (a tool named in a clear role) is kept as the low end, and a direction is called only when both move the same way. Clear-cut credits are accepted by published rules, so the author checks only spot samples and edge cases. Both changes are logged as deviations.

**Step 13: Statistical review (24 October).** An outside evaluation proposed ten changes. A re-run of the back-test with its central proposal, sampling flaws by their predicted chance of attack (EPSS), gave about 1.4 attacked flaws a quarter instead of the 2.5 to 3.5 claimed, and still no usable race estimate, so it was not adopted. Adopted instead:

- a pinned software environment (a hash-locked package list, a container pinned by digest and a monthly job that recomputes the latest frozen data and checks the results match);
- fix and attack dates stored as ranges, so the zero-day share is reported as a range and the race median as an upper bound;
- a companion test beside every direction label: by simulation, the registered two-quarter rule labels pure noise in about 48% of quarters, the test in about 10%;
- 20 earlier hand decisions re-shown each quarter instead of 5, and a second, independent coder answering 20 items blind;
- a whole-population comparison of AI-credited and other serious flaws (exploratory X13).

A first preview on test data found that CISA's "active exploitation" assessment comes before the attacked-flaws listing for about a third of newly attacked flaws, so the listing-based zero-day share may understate zero-days by about half. It is a preview, to be recomputed on the December dry run. A 2027 closing re-run on 1 April 2028, once every 2027 flaw has its full 90-day follow-up, was added to the plan.

## Data sources

Every source is free and keeps its own history, so each quarter can be rebuilt after it ends.

| Source | What it provides | Feeds | Access | Collector status |
| --- | --- | --- | --- | --- |
| CVE.org records (CVEProject/cvelistV5 on GitHub) | Every published vulnerability: dates, severity, weakness type, affected products, credits | T5 disclosure growth, T7 AI credits, cohort selection | Public, no key | Built and tested (410,719 records) |
| CISA Known Exploited Vulnerabilities (cisagov/kev-data) | US government list of flaws confirmed under attack, with date added | T1 race (every newly listed flaw), T3 time to exploitation, T4 (secondary), agreement check | Public, no key | Built and tested (1,748 entries) |
| CISA Vulnrichment | Severity and weakness type where a CVE record lacks them | Cohort details | Public, no key | Built: read from the CISA section of each CVE record, including the "active exploitation" assessment |
| NVD API 2.0 | Severity, weakness type and product matching | Cohort details (fallback) | Free key: `NVD_API_KEY` | Built (NVD's data via the FKIE mirror on GitHub) |
| FIRST EPSS | Daily probability that each CVE will be exploited | Context; cohort exploit-likelihood over time | Public, no key | Built (daily scores) |
| VulnCheck KEV (community) | Broader exploited-vulnerability list (about 5,600 entries) | T1, T3, agreement check; private use only until permission | Free key: `VULNCHECK_TOKEN` | Not run until permission is given |
| Shadowserver public dashboard | Daily counts of vulnerable systems per CVE; honeypot attack statistics | T1b, T2 exposure; T4 age mix; first-exploitation dates | Public; reuse needs permission | Planned, pending permission |
| Vendor advisories (CSAF, MSRC, PSIRT pages) | Patch release dates | Cohort patch date | Public | Built for fix-date pre-fill (GitHub, Microsoft, Cisco, Palo Alto) |
| Exploit-DB, Metasploit, Nuclei, GitHub | First public exploit code | Cohort exploit-code date | Public | Planned (exploratory X7) |
| Cloudflare Radar | Bot share of web traffic | Context only | Free key: `CLOUDFLARE_TOKEN` | Built |
| ransomware.live | Ransomware leak-site postings | T6a visible harm | Free PRO key: `RANSOMWARE_LIVE_KEY`; aggregate counts only | Built (aggregate counts only); not published until permission is given |
| SEC EDGAR | Material cybersecurity incident filings (Form 8-K, Item 1.05) | T6b visible harm | Public, no key | Built |

**Annual check sources:** historical scan data (Censys research access, or a one-off licence) for exposure, and published annual figures from Coalition, Coveware and Chainalysis for harm.

## Accounts and API keys

All keys were created on 20 October 2026 and stored as GitHub repository secrets. The quarterly workflow reads them at run time, so they never appear in the code, the chat or any published file.

| Service | GitHub secret | What it's for | Scope and notes |
| --- | --- | --- | --- |
| ransomware.live (PRO, free) | `RANSOMWARE_LIVE_KEY` | Posting counts for T6a | 500,000 calls a month; fair-use policy accepted (no raw data published) |
| NVD | `NVD_API_KEY` | Severity and product data at higher rate limits | Raises the limit from about 5 to 50 requests per 30 seconds; may expire if left unused |
| VulnCheck (community) | `VULNCHECK_TOKEN` | VulnCheck KEV, and XDB for exploit-code dates | Service terms accepted; private use only until permission is given |
| Cloudflare | `CLOUDFLARE_TOKEN` | Radar bot-traffic context | Account → Radar → Read only; no IP filter, no expiry |

**Other accounts:** OSF (registration), GitHub (code, runs, website) and, later, Zenodo (archive and DOI for each quarter's data).

**How the keys are kept safe:**

- Each key is stored only as a GitHub secret.
- Keys are never pasted into chat, email or files.
- Each key has the narrowest permission available.
- A key that leaks is revoked and replaced, and the replacement is noted in the permissions log.

## Permissions

Three providers' terms limit or don't address publishing results built from their data, so each was asked in writing on 20 October 2026. Until a provider says yes, nothing derived from its data is published. No answer by the deadline counts as no.

| Provider | How asked | Reference | What we asked | If refused |
| --- | --- | --- | --- | --- |
| Shadowserver | Web contact form | Ticket pqaytmyy | Publish aggregate charts and figures, with credit; how to get the time series | T1b and T2 stay at "baseline building"; T4 uses the weaker KEV measure |
| VulnCheck | community@vulncheck.com | — | Publish derived statistics (agreement scores, lags) labeled "VulnCheck KEV" | Exploitation dates come from CISA KEV and Shadowserver only; ENISA's EU vulnerability database could replace it in the agreement check |
| ransomware.live | Support form | Ticket #3425 | Publish aggregate posting counts, with credit and no victim names | T6a switches to another tracker or to published quarterly counts; T6b is unaffected |

**Terms already accepted:**

- ransomware.live's fair-use policy: no raw data is published, and no polling more often than every 30 minutes.
- VulnCheck's service terms: attribution is required; free data may not be used to train AI models; VulnCheck may list you as a customer.

**Deadlines:** follow-ups go out on 20 November 2026, with a reminder already set. The cutoff is the 21 December 2026 decision session: a source without a written yes by then is left out of the Q4 2026 pilot, and switched on at the next quarter's run if a yes arrives later. Every request and reply is recorded in `docs/PERMISSIONS.md`.

## How each quarterly run works

The same steps run every quarter, automatically, on GitHub's servers.

1. **Start.** At 06:00 UTC on 1 January, April, July and October, the scheduled workflow starts and works out which quarter just ended.
2. **Test the code.** The automated tests run first, in a software environment pinned to exact package versions. If any fail, the run stops before touching data.
3. **Pull each source.** Each collector fetches the quarter's data using its key. Git-based sources are pinned to an exact version (commit); other files are saved as received.
4. **Apply the terms.** Sources that forbid publishing raw data are reduced to aggregate counts during the run, and the raw responses are discarded.
5. **Freeze.** Every saved file gets a SHA-256 checksum, its source version and retrieval time in a manifest. A source that fails is retried for 48 hours, then recorded as a gap, never estimated.
6. **Select the cohort.** The frozen rule picks up to four new vulnerabilities per month, one per slot, by a seeded random draw that anyone can repeat, and tags each by root cause. Internet-facing status (slot c) is checked by hand, and AI-credited picks (slot d) pass automatically when the credit mentions an AI tool or lab; a rejected pick passes to the next flaw in the draw. Fix dates are pre-filled from vendor sources and confirmed by hand, with 20 earlier decisions re-shown unmarked to measure consistency.
7. **Analyze.** The seven tracking questions are computed, with 90% confidence intervals, and compared with the median of the previous four quarters. The race uses every flaw first listed as attacked in the quarter, with ranges for uncertain fix and attack dates. The two-quarter rule sets each label, and a companion test reports whether each label stands out from noise.
8. **Draft and approve.** Claude drafts the evaluation from the code's output only. You review and approve it within two days before anything is published, and do the quarter's hand checks between the 4th and the 28th.
9. **Publish the provisional results.** The evaluation page goes live on GitHub Pages, marked provisional.
10. **Run the final pass a month later.** The workflow repeats on 1 February, May, August and November to catch late listings and corrections. The final page is published, and the frozen data and code are archived on Zenodo with a DOI. On the 10th of each month, a separate job recomputes the latest frozen data inside the pinned environment and fails if any result differs.

Any change from the registered plan goes into `prereg/DEVIATIONS.md` with its date, reason and the results it affects.

## What we hope to get when finished

### Deliverables

- **A quarterly evaluation page** on GitHub Pages: provisional on the 1st, final a month later. It carries a scorecard for all seven questions, cohort timelines, the race, exploitation age, discovery pressure, harm and AI credits.
- **A running archive** that lines the quarters up, so each question's direction can be followed over time.
- **A reproducible data bundle each quarter** on Zenodo, with a DOI. The pinned software environment recomputes every published number from the frozen files, and a monthly check confirms it still does.
- **An annual wrap-up each March** comparing the year's free results with reference scan data and published insurance-claims and ransom-payment figures. The first is due in March 2028, with a closing re-run of all four 2027 quarters on 1 April 2028.
- **Public logs** of every deviation from the plan and every data permission, and an independent reviewer's published review of the first scored quarter.

### What we hope to learn

- **The race (central):** whether repair is catching up with attack. Is the gap between a fix and the first attacks widening, and are vulnerable systems halving before attackers arrive?
- **Patching speed:** whether exposed systems disappear faster after fixes, or linger for months.
- **Exploitation speed:** whether the window between disclosure and attack is still shrinking, and how often attacks start on day zero.
- **Age of attacked flaws:** whether attackers mostly hit old, fixable flaws, which would mean patching is failing, or brand-new ones, which would mean attackers are getting faster.
- **Discovery pressure:** whether vulnerability disclosures keep rising with AI, as you predict.
- **Visible harm:** whether ransomware and reported breaches are rising or falling. The annual check separates real change from the effect of fewer victims paying.
- **AI's role:** how much vulnerability discovery is credited to AI, and whether AI-found flaws differ from others in severity and bug type. Whether they are attacked sooner needs several years of data: in mid-2026 none of about 100 AI-credited serious flaws had yet been listed as attacked.
- **The free system itself:** from the annual check, how well free data tracks reality, and where it falls short.

Together, these answer the report's original question with evidence rather than argument: is the internet's security getting better or worse as AI advances?

## Timeline and limitations

### Timeline

| Date | Milestone |
| --- | --- |
| 1 Apr 2028 | Closing re-run of all four 2027 quarters with full 90-day follow-up |
| Mar 2028 | First annual wrap-up, covering 2027 |
| 1 Apr / 1 May 2027 | Q1 2027, the first scored quarter; outside reviewer's review 3–28 April |
| 15 Mar 2027 | Annual review: the one time each year the scored rules may change |
| 1 Jan / 1 Feb 2027 | Q4 2026 pilot: provisional and final |
| 21 / 29 Dec 2026 | Decision session, then the core freeze (core-v1.2) and an OSF update |
| 15–16 Dec 2026 | Full dry run with all available sources (1 October to 14 December data), unscored, and its hand check |
| 1–2 Dec 2026 | Dry run on October–November data, unscored, and its hand check |
| 23–24 Nov 2026 | Hand check of the baseline year (Q4 2025 to Q3 2026) |
| 20 Nov 2026 | Follow-ups to any data provider that hasn't replied |
| 16 Nov 2026 | Validation against five documented cases, with the author's own fix dates |
| 12 Nov 2026 | Review of the research results; decision on how many race fix dates to check by hand |
| 24 Oct 2026 | Statistical review; pinned environment, date ranges, label check and second coder built |
| 23 Oct 2026 | Race measure and AI-credit rule settled |
| 20 Oct 2026 | Plan registered on OSF; repository, keys and permission requests in place |

### Known limitations

- **Exposure coverage:** free exposure data covers only the vulnerabilities Shadowserver tracks, and depends on its permission.
- **A mostly US view:** the attack list (CISA KEV), NVD and the harm series (SEC, HHS) are US sources. Views from other countries (exploratory X19–X22) are being tested, and each finding states what it covers.
- **What exploitation data can see:** opportunistic, automated attacks are visible; targeted intrusions are not.
- **Attack dates are late:** CISA lists a flaw only after it is attacked and guidance exists, so the zero-day share is a minimum and the race median overstates the days from fix to first attack. Fix and attack dates are carried as ranges to show how much this matters.
- **Small samples:** at most twelve cohort vulnerabilities a quarter, so cohort results are noisy; the race therefore uses every newly attacked flaw instead. The two-quarter rule labels pure noise in about half of quarters, so each label carries a companion test and confidence intervals so readers can judge.
- **AI attribution:** only AI discovery that is credited can be counted. Whether an attack was AI-driven can't be measured from free data, and evidence on that is summarized separately as proven or speculative.
- **Conflict of interest:** Claude writes the code and drafts the evaluations. Anthropic is named in the original report, and about 83% of AI-credited CVEs so far credit Claude. The safeguards are the registered plan, public code, author approval and outside review.
- **One maintainer:** the runs are automated so a busy quarter doesn't stop the study, but approvals still depend on one person.
