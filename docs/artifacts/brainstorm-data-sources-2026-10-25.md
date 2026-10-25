# Brainstorm: Data Sources and Process

25 October 2026 · Paul Gagne

## Purpose and ground rules

The study's weakest points are the defender side of the race (exposure, T1b and T2) and the date of the first attack, both now resting on sources that may never say yes (Shadowserver, VulnCheck). This brainstorm looks for more free sources and ways to tighten the process before the 29 Dec lock. Nothing here changes a rule; anything adopted goes through the 21 Dec decisions or, after the lock, the March review.

Every idea has to pass the standing rules:

- **Free, or free for research:** no paid licence except the once-a-year scan data already budgeted.
- **Aggregates only:** counts and shares, never lists of hosts, IP addresses or victims.
- **No scanning of our own** and no host-level data, even when a source offers it.
- **Research organisations, not individuals,** as data sources.
- **Terms checked and logged** in `docs/PERMISSIONS.md` before anything is published.

## Internet exposure data (T1b, T2)

The best addition is HTTP Archive, which needs no permission, and the best lever is applying to Censys in November instead of February. Shadowserver stays first choice but may never answer.

| Source | What it would give | Cost and terms | Fit | Idea |
| --- | --- | --- | --- | --- |
| [Shadowserver dashboard](https://dashboard.shadowserver.org/help/) | Daily counts of vulnerable web apps by CVE, vendor or product; honeypot attack counts mapped to CISA KEV; time series | Free dashboard; publishing terms asked 20 Oct, no reply yet | Best for T1b and T2 | Keep; follow up 20 Nov as planned |
| [Censys research access](https://docs.censys.com/docs/research-access-to-censys-data) | Daily internet-wide scans with about five years of history; data may lag a week or a month | Free for non-commercial research that is published and cites Censys; independent researchers can apply; you pay BigQuery compute (1 TB of queries a month is free); requests written with AI tools are rejected | Strong for T2 and the annual check; history allows a baseline | Apply in November, written by you, not 15 Feb |
| [HTTP Archive](https://github.com/HTTPArchive/httparchive.org/blob/master/docs/gettingstarted_bigquery.md) | Monthly crawl of millions of websites with detected software (Wappalyzer), public on BigQuery | Free (1 TB of queries a month); public research dataset; no permission needed | Proxy for how fast websites move to fixed versions of web software (PHP, CMSs, libraries); websites only | Test whether version numbers are recorded; if so, an exploratory measure |
| WordPress.org plugin statistics | Share of active installs on each plugin version | Free public endpoint | Patch adoption for WordPress plugin flaws (some reach KEV and slot b) | Verify the endpoint; exploratory |
| [Shodan academic upgrade](https://help.shodan.io/the-basics/academic-upgrade) | 100 queries a month, no website downloads | Needs a university email address | You don't qualify as an independent researcher, and results are host-level | Skip |
| Commercial search engines (Netlas, ONYPHE, LeakIX, FOFA, ZoomEye) | Host lists with small free quotas | Terms generally bar redistribution; host-level | Conflicts with the aggregates-only rule | Skip |

None of these replaces Shadowserver for counts by CVE. HTTP Archive measures websites, not devices: it can't see VPN gateways or firewalls, the most-attacked slot.

## Attack timing: earlier than CISA's list

Free honeypot data already exists without Shadowserver: the SANS Internet Storm Center publishes daily web-honeypot URLs with first-seen dates. With it, PHP2Shell's 17 Oct attempt could be dated from public data. Attempts are not confirmed attacks, so these dates would sit beside the scored date as an exploratory "first attempt seen", never replace it before a March review.

| Source | What it would give | Cost and terms | Idea |
| --- | --- | --- | --- |
| CISA KEV plus CISA's "active exploitation" flag | Already used; the flag predates the listing for 23 of 57 and 30 of 91 flaws (Q2, Q3 2026) | Free, public | Keep (decided) |
| [SANS ISC / DShield web honeypot](https://isc.sans.edu/feeds_doc.html) | Daily list of every URL its honeypots saw, with first- and last-seen dates; a categorised file links URLs to vulnerabilities | Free; attribution required; no reselling; the site shows a non-commercial licence, which fits; at most one download an hour | Collect daily from now; map URLs to CVEs; exploratory first-attempt date |
| [ENISA EU Vulnerability Database](https://github.com/cku-heise/euvd-api-doc) | A second government list of exploited flaws, with an "exploited since" field | Free, no key reported | Compare with KEV for listing lag; check what "exploited since" means first |
| [Google Project Zero "0day In the Wild"](https://securityaffairs.com/85668/security/google-project-zero-days.html) | Public sheet of zero-days seen in attacks, with discovery and patch dates | Free, public | Cross-check X10's zero-day share against an independent list; confirm it is still maintained |
| [inthewild.io database](https://github.com/gmatuz/inthewilddb) | Dated exploitation reports per CVE, updated hourly | Free, Apache 2.0 licence | Triangulate first-report dates; check freshness |
| GreyNoise research access | Tags per CVE with first-seen scanning and attack activity | Free on application for research that is shared | Apply after the DShield test, if it adds coverage |
| [CrowdSec CVE tracker](https://docs.crowdsec.net/u/tracker_api/intro) | Per-CVE exploitation phase and timelines from a large sensor network | API key by request; terms not checked | Ask whether research use and aggregate publication are allowed |
| Exploit-DB, Metasploit, Nuclei | Date public exploit code appeared (X7) | Free, public | Already planned under Plan 2 |

## Fix dates and patch adoption

The biggest hand-check saving is in Linux and other open-source projects whose fixes are dated in public code history. Patch adoption has two free proxies for open-source packages, but none for appliances.

**Fix dates** (88 of 175 recent attacked flaws still fall back to "assumed = publication date"):

- **Linux kernel:** kernel CVE records name the fixing commits and fixed versions; commit and release dates would date most kernel fixes without a hand check.
- **Linux distribution trackers** (Debian, Ubuntu): free, machine-readable "fixed in" dates; a second date for open-source flaws already covered by GitHub.
- **More vendors' machine-readable advisories (CSAF):** Siemens, Red Hat, SUSE and others publish them like Cisco does; each one added cuts the assumed list. Fortinet still has no feed we know of.
- **Revision histories:** keep flagging "fix released later" wording (Cisco, Palo Alto) for hand checks; extend it to every CSAF vendor added.

**Patch adoption** (how fast users move to the fixed version):

| Source | What it would give | Cost and terms | Idea |
| --- | --- | --- | --- |
| [deps.dev on BigQuery](https://docs.deps.dev/bigquery/) | Every version of npm, PyPI, Maven, Go and Cargo packages, with who depends on which version and when | Free public dataset, CC-BY 4.0 | Share of dependents on the fixed version, 30 and 90 days after the fix (Plan 2 idea, now concrete) |
| PyPI download statistics on BigQuery | Downloads by package version | Free public dataset | Same, measured by downloads |
| HTTP Archive, WordPress.org | Version shares on websites and WordPress sites (section above) | Free | Same, for web software |

These cover open-source software only. Appliances (VPNs, firewalls), the most-attacked slot, stay dependent on scan data.

## AI involvement and harm (T7, T6)

For AI credits, the labs' own public lists of flaws their tools found are the strongest free cross-check: they tell us when a credit line hides an AI tool, as with PHP2Shell. For harm, the US health-breach register is a free, official second series.

**AI involvement (T7)**

- **Labs' published lists:** Google keeps a public list of flaws its Big Sleep tool found ([issue tracker](https://issuetracker.google.com/issues?q=componentid:1836411&s=type:desc&s=issue_id:desc)); OpenAI's funded audits ("Patch the Planet") and similar programmes publish findings too. Matching their CVEs against our credit counts would measure how much the credit field misses. Exploratory, never scored.
- **Advisory text, not just the credit field:** vendor and finder write-ups (PHP's advisory, Calif, Wiz) name the tools used. A yearly hand-read sample of advisories for the AI-credited and lab-affiliated flaws would size the gap.
- **Finders that are AI companies:** a short, dated list of AI-native research firms (for example XBOW) beside the lab list, reviewed each March, so credits from them are recognised.

**Harm (T6)**

- **US health-breach register (HHS OCR):** every breach affecting 500 or more people, with dates, a "hacking/IT incident" type and the number of people affected ([field summary](https://www.accountablehq.com/post/hhs-ocr-breach-portal-search-reported-hipaa-data-breaches)). Official, free, aggregates only. A second harm series beside the SEC filings, for one sector.
- **State breach notices** (for example Maine's register): free, but fragmented by state; lower priority.
- **ransomware.live:** still waiting for permission; aggregates only once it comes.

## Process improvements

The most important process change is capturing daily sources every day: honeypot files and other changing lists cannot be pulled back later, unlike CVE records. The rest tighten what 24-25 Oct showed: drift between documents, a dropped run, and evidence that arrives as news.

1. **Capture daily sources daily.** The quarterly pull rebuilds the past from sources that keep history. DShield files, EUVD's list and similar change daily and keep little history, so a small daily collector must save aggregates (counts per URL category, first-seen dates) from the start, or the baseline is lost.
2. **An inquiry log.** Each outside story you raise (like PHP2Shell) gets a short entry: the question, how the plan handles it, what free data recorded against what happened, and any follow-up. Entries feed the March review, so ideas are weighed together, not adopted one by one.
3. **Watch cases chosen by a rule.** To avoid picking only cases that make a point, choose them by fixed criteria (for example, every flaw with CVSS 9 or more that national CERTs warned about in the quarter), at most two a quarter.
4. **"Earliest evidence" beside the scored date.** Report the first-attack date from every source (KEV, CISA's flag, EUVD, honeypots, exploitation reports) and the gap between the earliest and KEV each quarter. That measures KEV's lag directly; the scored date stays as registered until a March review.
5. **Register additions before looking.** Every new exploratory measure gets a dated entry in `config/exploratory.yaml` before its first result is seen.
6. **Source health in the quality report.** For each source: last successful pull, rows against the previous run, and a GitHub issue when a source fails, as the schedule job now does for dropped runs.
7. **Permission fallbacks written down.** For each pending source, name the free substitute from this brainstorm (Shadowserver → DShield plus HTTP Archive; VulnCheck → EUVD plus inthewild.io), so a refusal is a settings change, not a redesign.
8. **Hand-check minutes recorded.** Log time per item in the Hand Check app, so the sample-or-all decision rests on measured time.

## Shortlist before the 29 Dec lock

New collectors are data workflows, so anything adopted must be built and tested by 14 Dec to be locked on 29 Dec. All additions below are exploratory: they are reported, never scored, until a March review.

| When | Item | Effort | Value | Who |
| --- | --- | --- | --- | --- |
| From early Nov | Daily DShield web-honeypot capture (aggregates only), with first-seen dates mapped to CVEs | Low | High: honeypot dates without permission | Claude |
| Nov | Censys research application, moved from 15 Feb | 1 hour | High: scan data with five years of history | You (it must be written without AI tools) |
| Nov | HTTP Archive test: are version numbers recorded? If yes, a patch-adoption measure for web software | Low | Medium | Claude |
| Nov | Linux kernel and distribution fix dates | Medium | High: fewer assumed fix dates, fewer hand checks | Claude |
| Nov | Back-test of KEV's lag on Q2-Q3 2026 against EUVD, Project Zero's sheet and inthewild.io | Low | Medium: sizes the zero-day undercount | Claude |
| Nov | Inquiry log started, PHP2Shell as the first entry | Low | Medium | Claude |
| Dec | deps.dev patch-adoption prototype for open-source flaws | Medium | Medium (Plan 2) | Claude |
| By 3 Feb | AI labs' lists against our credit counts (Big Sleep first), for the 8 Feb session | Low | Medium | Claude |
| After the lock | GreyNoise research access; CrowdSec terms; HHS OCR harm series | Low each | Medium | You apply; Claude builds |

Skipped: Shodan (needs a university email; host-level) and commercial search engines (redistribution barred; host-level).

## Decisions (25 Oct 2026)

1. **Shortlist:** every item adopted, all exploratory, now in the schedule: honeypot capture from 2 Nov; KEV-lag back-test and Linux fix dates 9 Nov; HTTP Archive test 16 Nov; deps.dev prototype 7 Dec; AI labs' lists 25 Jan; GreyNoise and CrowdSec requests 11 Jan; HHS OCR series 18 Jan.
2. **Censys:** application moved to Tue 17 Nov 2026, written by you.
3. **Inquiry log:** started (`docs/INQUIRIES.md`), PHP2Shell first.
4. **Watch cases:** chosen by rule from Q1 2027: CVSS 9.0 or more plus a national CERT alert, at most two a quarter by the seeded draw.

## What the probes found (25 Oct, same day)

Tested on GitHub against the 246 flaws CISA added in Jan-Sep 2026. Two sources work well, three disappoint, and one changes the AI-credit picture.

| Source | Result | Verdict |
| --- | --- | --- |
| Linux kernel commits | 5 of 8 kernel flaws dated from fixing commits, a median 22 days before the CVE was published | Build into the pre-fill (2 Nov) |
| Outside AI-found lists | Of 5 outside AI-found CVEs: headline count caught 3, narrow 0; 2 (Microsoft, Apple) have empty credit fields because those vendors credit finders only in their own advisories | Key point for 8 Feb |
| Project Zero sheet | Current; 24 of its zero-days are in the window; discovery dates mostly unknown | Zero-day check X15 (decided 25 Oct) |
| SANS ISC honeypot | Capture works (10.2 million URLs, 241 CVEs), but only 2 of the 246 flaws appear, and first-seen dates belong to URLs, not flaws | Context only, captured monthly (decided 25 Oct); about 40 KB saved per capture |
| ENISA EUVD | Mirrors CISA's list; earlier for 10 of 246, by a median 4.5 days | Dropped (decided 25 Oct) |
| inthewild.io | No exploitation reports since Dec 2024 | Dropped (decided 25 Oct) |
| HHS OCR | Portal reachable; export form not yet triggered | Retry 2 Nov |
| WordPress.org statistics | Version shares per plugin, today only | Capture weekly with the HTTP Archive test |

Correction to the ground rules above: the honeypot files keep first-seen dates back to 2012, so waiting does not lose them; a weekly capture is enough.

## Sources

Pages opened on 25 Oct 2026: [Censys research access](https://docs.censys.com/docs/research-access-to-censys-data) · [Shodan academic upgrade](https://help.shodan.io/the-basics/academic-upgrade) · [GreyNoise Community](https://www.greynoise.io/plans/community) · [HTTP Archive on BigQuery](https://github.com/HTTPArchive/httparchive.org/blob/master/docs/gettingstarted_bigquery.md) · [Shadowserver dashboard help](https://dashboard.shadowserver.org/help/) · [EUVD API notes](https://github.com/cku-heise/euvd-api-doc) · [Project Zero 0day In the Wild](https://securityaffairs.com/85668/security/google-project-zero-days.html) · [SANS ISC feeds](https://isc.sans.edu/feeds_doc.html) · [inthewild.io database](https://github.com/gmatuz/inthewilddb) · [CrowdSec CVE tracker](https://docs.crowdsec.net/u/tracker_api/intro) · [deps.dev BigQuery](https://docs.deps.dev/bigquery/) · [Big Sleep list](https://www.techradar.com/pro/security/googles-new-ai-powered-bug-hunting-tool-finds-major-issues-in-open-source-software) · [HHS OCR breach portal fields](https://www.accountablehq.com/post/hhs-ocr-breach-portal-search-reported-hipaa-data-breaches). Not verified: the WordPress.org version-statistics endpoint (not reachable from here) and whether HTTP Archive records version numbers.
