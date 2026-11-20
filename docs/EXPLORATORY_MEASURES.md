# Exploratory measures X1 to X31 (updated 19 Nov 2026)

Built from `config/exploratory.yaml` by `python -m snapshot.explodoc build`; do not edit by hand. Exploratory measures are reported beside the registered core and never decide a label (docs/RESEARCH_PLAN.md). Each section gives the question, its status with the dated note beside it, the sources and the method as decided; no figures appear here.

| Measure | Name | Status |
|---|---|---|
| [X1](#x1) | AI-credited share by lab family | active |
| [X2](#x2) | Watchlist matches | active |
| [X3](#x3) | AI-operated attack campaigns (curated log) | active |
| [X4](#x4) | Automated and AI traffic against websites (Cloudflare Radar) | active |
| [X5](#x5) | Flaws in AI software | active |
| [X6](#x6) | Speed in the tail | planned |
| [X7](#x7) | Patch to public exploit code | planned |
| [X8](#x8) | Breadth of exploitation | planned |
| [X9](#x9) | Bug types being exploited | planned |
| [X10](#x10) | Exploited before a fix existed | planned |
| [X11](#x11) | Exposed and hijacked AI servers | planned |
| [X12](#x12) | Open-weight model release log | active |
| [X13](#x13) | AI-credited versus other serious flaws, whole population | planned |
| [X14](#x14) | Honeypot attack activity by category (SANS ISC), context only | active |
| [X15](#x15) | Zero-day check against Project Zero's list | planned |
| [X16](#x16) | Patch adoption for open-source flaws (deps.dev) | planned |
| [X17](#x17) | Health-sector hacking breaches (HHS OCR) | active |
| [X18](#x18) | Outside AI-found lists against the AI-credit counts | planned |
| [X19](#x19) | National exploitation alerts against CISA KEV | active |
| [X20](#x20) | Internet routing and naming hygiene by country (APNIC Labs) | active |
| [X21](#x21) | Regional splits of attack, bot and ransomware series | active |
| [X22](#x22) | Breach notifications outside the US | active |
| [X23](#x23) | Age of attacked flaws seen by the SANS ISC honeypots (companion to I4) | planned |
| [X24](#x24) | Agreement between free exploitation signals (companion to I6) | planned |
| [X25](#x25) | Supply of AI security tools on GitHub (how they use AI; offensive, defensive and dual-use) | active |
| [X26](#x26) | How much people hand over to AI (autonomy given to AI models and apps) | planned |
| [X27](#x27) | Web patch adoption (HTTP Archive server versions) | planned |
| [X28](#x28) | Age of attacked flaws seen by GreyNoise sensors (companion to I4) | planned |
| [X29](#x29) | AI infrastructure as a target (merged into X5, X11 and X3 the same day) | merged |
| [X30](#x30) | AI software supply chain (malicious packages, models and agent skills) | planned |
| [X31](#x31) | AI-generated reports and the defenders' capacity to fix | planned |

## X1

**AI-credited share by lab family**

*Question.* Which labs' tools are credited with finding vulnerabilities, and how is that mix shifting?

*Status.* active.

*Added* 2026-10-21. *Sources:* cve. *Decides a label:* no.

## X2

**Watchlist matches**

*Question.* How many credits name tools on the newcomer watchlist that are not yet in the term list?

*Status.* active.

*Added* 2026-10-21. *Sources:* cve. *Decides a label:* no.

## X3

**AI-operated attack campaigns (curated log)**

*Question.* How often are attacks run by AI agents or AI tooling publicly reported, what do they target, and do they use known flaws or bugs that never get a CVE?

*Status.* active.

*Added* 2026-10-21. *Sources:* curated. *Decides a label:* no.

*Method.* Hand-curated from public reports. A campaign is logged when a security firm, government agency or AI lab reports attackers using AI agents or AI tooling in intrusions. Counted per quarter by date reported, with entry vector and whether a second independent source confirms it. When a campaign names CVEs, the quarter also reports how many of its KEV additions are linked to an AI-run campaign. Victim names are never recorded. Reporting volume reflects attention as well as activity, so counts are read as a lower bound. Amended 2026-10-26 (author's decision): a separate category, ai_role "evaluation_escape", for an AI model under evaluation (a red-team or capture-the-flag test) that reached real systems with no attacker directing it. Such events are logged and reported beside the campaigns, with the same fields, but never added to the campaign count. First case: Gemini in Irregular's May 2026 test (reported 14 Aug 2026). Amended 2026-10-29 (author's decision, after TrendAI's "Not only ARTEX" report): each row records ai_evidence, "confirmed" when the reporter shows attacker-side proof of AI use (platform logs, prompts, AI-written plans) or "assessed" when it is judged from style or indirect signs; rows logged before then are "unrated" until the author's check. Counts are reported for all rows and for confirmed rows alone. Every CVE ID recorded in the campaign and sweep logs is checked against CVE.org (snapshot.cvecheck, Research task cve_check) when rows are added and at each sweep, because AI tools invent identifiers. Amended 2026-10-29 (author's decision, review item 13, option B): each row also records attack_method (a fixed list in src/snapshot/x3catalogue.py: autonomous_intrusion, agent_recon, credential_harvest, ai_planned_human_led, ai_written_tooling, ai_system_hijack, compute_theft, ai_social_engineering, evaluation_escape, other) and found_via (author, quarterly_sweep, trial_sweep, claude_research). The catalogue of attack methods and the register of resources (exploratory/ai_attack_catalogue.md) are generated from the log; a test keeps them current. Amended 2026-10-29 (author's decision, widening the search): three more channels, each a found_via value. (1) feed_screen: a monthly workflow (Feed screen, the 5th) reads the feeds in config/feeds.yaml (about 60: vendor research, governments and CERTs, AI labs and incident databases, news for leads, and sources in Chinese, Japanese, Korean, Russian, German, French and Portuguese) and lists items naming both an AI term and an attack term. (2) newsletter: security newsletters sent to the project address, read by Claude weekly (Saturdays, from 14 Nov 2026; twice a month before); amended 2026-11-01 (author): newsletters are research only, never shown, and a case first spotted in a newsletter is not entered in the log. (3) conference: a twice-yearly scan of major conferences' talk lists. All candidates are confirmed by the author in the hand-check window; counts stay a lower bound, and each channel's start date is reported so growth from wider looking is not read as growth in attacks.

*Report sources.* Threat-intelligence reports on AI misuse from AI labs (Anthropic, OpenAI, Google GTIG); Anthropic is a conflict of interest and is labeled as such, Security vendor and researcher disclosures (e.g. NorForge for Cairn; GreyNoise for the PaperCut agent campaign), Government advisories (CISA, NCSC, ACSC, JPCERT), MITRE ATLAS case studies and the AI Incident Database, LLM-agent honeypot research (e.g. Palisade Research's honeypot), as context, AI evaluation firms' and labs' incident disclosures (e.g. Irregular; Google), for evaluation_escape

*Sweep.* when: the 2nd of Jan/Apr/Jul/Oct, for the quarter just ended (schedule item ai-incident-sweep); by: Claude runs the searches; the author validates each candidate in the hand-check window; log: exploratory/ai_attack_sweeps.csv; window: reports dated in the quarter; earlier incidents first reported in it count in it; queries: AI agent cyberattack intrusion, attackers used AI agent to exploit vulnerability, LLM generated exploit used in the wild, autonomous AI hacking campaign, AI-assisted ransomware attack, threat actors misuse Claude OR Gemini OR ChatGPT OR Copilot report, MCP server OR AI agent compromised attack, prompt injection attack in the wild data stolen, AI coding assistant supply chain attack, AI model escaped sandbox OR evaluation environment; languages: en, zh, ja, ko, ru, es, pt, de, fr; queries_translated: config/sweep_queries.yaml; also_check: AI-lab threat reports (Anthropic, OpenAI, Google GTIG, Microsoft), Government advisories mentioning AI (CISA, NCSC, ACSC, JPCERT, CERT-EU, ENISA), MITRE ATLAS case studies and AI Incident Database entries added in the quarter, SANS Internet Storm Center handler diaries, Vendor research blogs (Mandiant, Palo Alto Unit 42, Cisco Talos, Microsoft Threat Intelligence, CrowdStrike, ESET, Kaspersky Securelist, Check Point Research, Sophos X-Ops, Huntress), AI-security trackers (OWASP GenAI Security Project incidents, AIAAIC repository), AI evaluation firms' and labs' incident disclosures (e.g. Irregular), for evaluation_escape, News sites, for leads only (The Record, BleepingComputer, SecurityWeek, Dark Reading), {'Research blogs outside the US and Europe (added 2026-10-26)': 'AhnLab ASEC (Korea), Qi An Xin and Qihoo 360 (China), Trend Micro and JPCERT/CC (Japan)'}, {'Chinese security sites (added 2026-10-26 after the trial)': 'FreeBuf, Anquanke, Security Insight (secrss.com), 4hou'}, TrendAI (Trend Micro) Deep Research, English and Japanese editions (added 2026-10-29; the Japanese edition of "Not only ARTEX" came out four days before the English), Japan's National Cybersecurity Office (NCO) alerts and advisories (added 2026-10-29), {'AI-incident and threat databases and reports (added 2026-10-29, author)': 'AI Vulnerability Database (AVID); Meta adversarial threat reports; Amazon threat intelligence'}, {'More national agencies (added 2026-10-29, author)': 'Singapore CSA, South Korea KISA/KrCERT, Germany BSI, Israel INCD, CERT-EU, and joint Five Eyes advisories'}, {'Conference talk lists, scanned twice a year (added 2026-10-29, author)': 'Black Hat USA and Europe, DEF CON, CODE BLUE (Japan), HITCON (Taiwan), Kaspersky SAS, Virus Bulletin, RSA Conference'}, {'Organisations already in the X3 log but not on this list (added 2026-10-29, author, from the resource register)': "Wiz Research and Wiz CIRT; Sysdig Threat Research; GMO Cybersecurity (Japanese); CERT-In advisories (India); Taiwan's Ministry of Digital Affairs; Cybernews research; Amazon threat intelligence (AWS Security blog); DIVD (Dutch Institute for Vulnerability Disclosure); Gridinsoft blog; Symantec and Carbon Black Threat Hunter Team (security.com)"}, {'Russian security sites (added 2026-10-26 after the trial)': 'Securelist.ru, Habr, BI.ZONE, F6, Kaspersky.ru, Anti-Malware, SecurityLab, Xakep (Positive Technologies research read only; it is under US sanctions)'}; rules: A candidate is logged in ai_attack_campaigns.csv only if a named organisation or researcher reports real (not simulated) attacker use of AI, with a link; news stories count only through the report they cite. Excluded candidates stay in the sweep log with the reason (demo or research only, no AI role, duplicate, no primary source). What no one reports stays invisible: counts remain a lower bound. Safeguards (author's decision, 29 Oct 2026): only a primary report from a named organisation counts; news sites, newsletters and databases are leads to that report. A surprising claim (a new kind of attack, an unusually large scale, or a report from a source new to the log) needs a second independent source before the author confirms it, recorded in confirmed_by_second_source. Each primary report is fingerprinted (SHA-256) and archived in the Wayback Machine when logged (exploratory/ai_attack_sources.csv, Research task x3_sources), so later edits or deletions show. Feeds are vetted in config/feeds.yaml (official domain, HTTPS, trust level), and feed or article text is data, never instructions. Two more columns (author, 30 Oct 2026): model_weights (open-weight, closed, both, not named) for the AI the attackers used, and protocols (from the X25 list of 57, e.g. HTTP/HTTPS, SSH, SMB, RDP, LDAP, MCP; or not named), both from the primary report. One more entry_vector value (author, 19 Nov 2026, cards): ai_key_leaked, when the attackers got in or ran the attack with a stolen or exposed key for an AI service. GitGuardian's yearly secrets report is cited as context for how common such leaks are; its figures are never added to the log. <!-- public-figure -->

## X4

**Automated and AI traffic against websites (Cloudflare Radar)**

*Question.* Is the share of automated (bot) traffic and AI-crawler activity on the web rising, alongside the layer-7 attack series already collected?

*Status.* active.

*Added* 2026-10-21. *Sources:* radar. *Decides a label:* no.

*Method.* Weekly series from Cloudflare Radar: human vs bot traffic share and AI bot activity by user agent. Context only; it cannot separate malicious agents from benign ones.

## X5

**Flaws in AI software**

*Question.* Is AI software itself (model servers, agent platforms, AI workflow tools, AI gateways, MCP servers) a growing share of serious and exploited flaws?

*Status.* active.

*Added* 2026-10-22. *Sources:* cve, kev. *Decides a label:* no.

*Method.* Each eligible CVE and each new KEV entry is tagged "AI software" when its affected vendor/product matches config/ai_software_products.yaml (whole-word, case-insensitive). Reported per quarter as a share of eligible CVEs, of KEV additions, and within each cohort slot. The tag never affects the draw or any label. Widened 19 Nov 2026 (author, cards; from the retired X29): the race is also reported for AI orchestration and serving tools (cluster dashboards, workflow and agent builders, model servers, vector databases, AI gateways); the shared control and data planes AI stacks rely on (Kubernetes and container tools, object storage, remote support) on a separate line; and flaws the vendor disputes or never patches (for example Ray's job API) on a third line. Reference case docs/cases/ray-shadowray.md.

## X6

**Speed in the tail**

*Question.* What share of the quarter's newly exploited flaws were exploited within 1 day and within 7 days of public disclosure?

*Status.* planned.

*Added* 2026-10-22. *Sources:* cve, kev. *Decides a label:* no.

*Method.* For KEV additions in the quarter, days from CVE publication to the KEV date (and to earlier exploitation evidence where recorded). Reported as shares at 1 and 7 days.

## X7

**Patch to public exploit code**

*Question.* How quickly does public exploit code appear on GitHub after a fix?

*Status.* planned.

*Added* 2026-10-22. *Sources:* poc_in_github. *Decides a label:* no.

*Method.* For cohort CVEs and KEV additions, days from the vendor fix to the first public proof-of-concept repository indexed by PoC-in-GitHub. Indexed repositories are not all working exploits; reported as an upper-bound timing signal.

## X8

**Breadth of exploitation**

*Question.* Are attackers exploiting more different vendors and products, including ones never exploited before?

*Status.* planned.

*Added* 2026-10-22. *Sources:* kev. *Decides a label:* no.

*Method.* Per quarter, distinct vendors and products among KEV additions, and how many appear in KEV for the first time.

## X9

**Bug types being exploited**

*Question.* Are exploited flaws shifting toward logic, authentication and access-control bugs relative to memory-safety bugs?

*Status.* planned.

*Added* 2026-10-22. *Sources:* kev, cve, nvd. *Decides a label:* no.

*Method.* Root-cause class (config/root_cause_map.yaml, with NVD CWEs filling gaps) for KEV additions per quarter. Depends on the root-cause map decision at the freeze session.

## X10

**Exploited before a fix existed**

*Question.* How often does exploitation start before a fix is available (zero-day share)?

*Status.* planned.

*Added* 2026-10-22. *Sources:* kev, cve, nvd. *Decides a label:* no.

*Method.* Share of KEV additions whose first exploitation evidence precedes the vendor fix date. Fix dates come from the cohort hand check for cohort CVEs and from vendor advisory references otherwise; unknown dates are reported as unknown, never guessed.

*Note.* Kept exploratory by the author's decision of 2026-10-23 (decision items 0 and 7); promotion candidate at the 15 March 2027 review once a year of data shows it is steady.

## X11

**Exposed and hijacked AI servers**

*Question.* Are self-hosted AI servers (e.g. Ollama, LLM gateways) increasingly exposed and attacked?

*Status.* planned.

*Added* 2026-10-22. *Sources:* curated, shadowserver. *Decides a label:* no.

*Method.* Logged from public honeypot reports and, if available, Shadowserver exposure series for AI services. Context only. Widened 19 Nov 2026 (author, cards; from the retired X29): the weekly GreyNoise sweep's AI-product tags (cluster, workflow, model-serving, vector-database and gateway products, shared planes kept separate) give a probing series; exposure totals for the same products come from Censys or Shadowserver only if access is granted. Aggregates only, no host-level data.

## X12

**Open-weight model release log**

*Question.* When do capable models that attackers can run privately become available?

*Status.* active.

*Added* 2026-10-22. *Sources:* curated. *Decides a label:* no.

*Method.* Dated log of open-weight model releases with strong coding or security ability (name, lab, country, licence, size, runs on a laptop). Used only as a timeline for reading changes in other measures.

*Amended 2026-10-26.* Author's request: measure how fast capable open-weight models are being released worldwide, automatically. Added, if the 27 Oct probe shows the data holds up: (1) a monthly capture of new model repositories from a fixed list of major labs on the Hugging Face Hub (public API: model name, lab, creation date, size; base and instruct releases only, community fine-tunes excluded), each lab tagged with its country; (2) Epoch AI's public model database (release date, country, open weights) as an independent check; (3) a capability bar fixed before the 29 Dec freeze: a model counts as "capable" when it scores at or above a set threshold on a public coding or security benchmark. Reported each quarter: releases and capable releases per quarter by country/region, the cumulative curve and its doubling time, and the gap in months between the best open-weight model and the best closed model on the same benchmark. History backfilled to January 2023 (author's choice, 26 Oct), so the curve and its doubling time are known before the first 2027 report. Measures supply only: who downloads these models and what they do with them cannot be seen; changes are read next to the attack-speed fingerprints (X6-X11), never as cause.

*Decided 2026-11-12.* Research review, decisions 7 and 8 (author, after the evidence run runs/research/2026-11-12T1221Z-x12_evidence, private). Releases: counted from the Hugging Face Hub for a fixed list of 25 major labs, text models only (pipeline text-generation), derivatives dropped (quantized copies, adapters, embedding, reward and guard models) and near-duplicate versions of one model grouped as a single release; Epoch AI's database checks only quarters more than six months old (it runs about two quarters behind). Capable bar: a coding bar now, Terminal-Bench (agents working in a command line) at 30% or above, from Epoch AI's benchmark data (204 models scored since June 2025, 33 of them open-weight; 12 open models clear 30%); a security bar is added once a public security benchmark scores enough open-weight models (Epoch's data has none; search by 14 Dec).

## X13

**AI-credited versus other serious flaws, whole population**

*Question.* Do flaws credited to AI tools differ from other serious flaws in severity, bug type and how soon they reach CISA KEV?

*Status.* planned.

*Added* 2026-10-24. *Sources:* cve, kev, nvd. *Decides a label:* no.

*Method.* Population: every CVE meeting the cohort eligibility rule (prereg 7.1 items 2 and 3: critical or CVSS >= 8.0, published on the 1st to 25th) in the quarter, backfilled for Q4 2025 to Q3 2026. Groups: AI-credited under the narrow (registered, tool named in a clear role) and headline (any mention) definitions, each reported. (1) Every quarter: CVSS, share allowing remote code execution and root-cause mix, AI-credited versus other, with 90% intervals. (2) Pooled over all quarters to date: Kaplan-Meier time from publication to first KEV listing, censored at 90 days or the evaluation date, with the event count in each group; while the AI-credited group has fewer than 10 events, only the count and an exact 95% upper bound on its 90-day listing rate are reported (Q2-Q3 2026: 0 of 102). (3) From 20 events: Cox model with product slot, vendor type, CVSS and root cause, proportional hazards checked with Schoenfeld residuals. Descriptive only: AI tools search different code than attackers target, so no difference is read as an effect of AI.

*Note.* Defined on 2026-10-24, before any result is computed (docs/STATISTICAL_REVIEW_2026-10-24.md, point 9). Replaces the 12-flaw cohort as the evidence for the registered secondary comparison of AI-credited and other CVEs; the registered cohort comparison is still reported.

## X14

**Honeypot attack activity by category (SANS ISC), context only**

*Question.* Which kinds of web attacks do honeypots see each quarter, and which named CVEs?

*Status.* active.

*Added* 2026-10-25. *Sources:* isc_honeypot. *Decides a label:* no.

*Method.* Monthly capture of the SANS Internet Storm Center web-honeypot files as aggregates (src/snapshot/collect/isc_honeypot.py): requests and URLs per attack category, and per CVE named in a URL or category. Context only (author's decision, 25 Oct 2026): not used as a first-attack date, because the probe found only 2 of 246 KEV additions in the data and first-seen dates belong to URLs, not flaws. Credit: SANS Technology Institute, Internet Storm Center.

## X15

**Zero-day check against Project Zero's list**

*Question.* Of the zero-days Google Project Zero lists, how many does the study's free data also class as zero-days?

*Status.* planned.

*Added* 2026-10-25. *Sources:* kev, p0_itw. *Decides a label:* no.

*Method.* Each quarter: KEV additions that appear in Project Zero's public "0day In the Wild" sheet (24 of 246 in Jan-Sep 2026), and the share of them that X10 classes as exploited on or before the fix. A low share shows how far the free data understates zero-days. ENISA EUVD and inthewild.io were tested as earlier-attack sources on 25 Oct and dropped (EUVD mirrors KEV; inthewild.io has no reports after Dec 2024).

## X16

**Patch adoption for open-source flaws (deps.dev)**

*Question.* How fast do dependent packages move off affected versions of attacked open-source flaws?

*Status.* planned.

*Added* 2026-10-25. *Sources:* osv, depsdev. *Decides a label:* no.

*Method.* For KEV additions that OSV maps to npm, PyPI, Maven, Go or Cargo packages: share of dependents on affected versions 30 and 90 days after the fix (deps.dev BigQuery history; a today-only snapshot from the free API until then). Open-source software only.

## X17

**Health-sector hacking breaches (HHS OCR)**

*Question.* Is reported hacking harm in US health care rising or falling?

*Status.* active: author's decision 29 Oct 2026 (research review #11 decided early): hand download.

*Added* 2026-10-25. *Sources:* hhs_ocr. *Decides a label:* no.

*Method.* Quarterly count of "Hacking/IT Incident" breaches affecting 500 or more people, and people affected, from the public HHS OCR register. Entity names are never stored. The portal cannot be read by a script (29 Oct probe: the list and its export appear only after browsing in), so the author downloads the public CSV by hand once a quarter in the hand-check window (about 5 minutes) and drops it into the chat; Claude reduces it to the two counts at once and keeps only those, never the file.

## X18

**Outside AI-found lists against the AI-credit counts**

*Question.* How many flaws that outside lists attribute to AI tools do the headline and narrow counts catch?

*Status.* planned.

*Added* 2026-10-25. *Sources:* cve, curated. *Decides a label:* no.

*Method.* A dated, hand-entered list of CVEs that labs or verified trackers attribute to AI tools, each with its source; share caught by the headline and narrow T7 rules, and share with empty credit fields (vendors that credit only in their own advisories). Read with the list's own selection bias in mind.

## X19

**National exploitation alerts against CISA KEV**

*Question.* Do other national cyber agencies flag attacked flaws that CISA's list misses, or flag them earlier?

*Status.* active: 29 Oct: CERT-FR and JPCERT/CC (terms read); BSI and KrCERT/CC not adopted.

*Added* 2026-10-26. *Sources:* national_alerts, kev. *Decides a label:* no.

*Method.* Each quarter: CVEs named in active-exploitation alerts from CERT-FR (France), JPCERT/CC (Japan), BSI (Germany) and KrCERT/CC (Korea), each with its alert date. Reported: how many each agency flagged, the share also in CISA KEV, the share flagged before KEV listed them (and by how many days), and those never in KEV. An earlier alert date is also a candidate T_exploit date (snapshot.events other_exploit), compared side by side with KEV-only dates; it does not replace them in the core.

*Agencies 2026 10 28.* Research review #3 (approved on its condition 27 Oct): CERT-FR adopted 28 Oct (alert feed readable and dated; Licence ouverte). JPCERT/CC adopted 29 Oct: its terms allow quoting with source, document and URL (courtesy email to its PR office, sent by the author). BSI WID and KrCERT/CC not adopted: their feeds carry advisories and vendor notices, not exploitation alerts with an attack date. Collector to build before the 14 Dec review.

## X20

**Internet routing and naming hygiene by country (APNIC Labs)**

*Question.* Are the internet's basic protections (DNSSEC validation, RPKI route checking) spreading, country by country and region by region?

*Status.* active: 19 Nov 2026: collector built and tested (snapshot.collect.apnic: the DNSSEC world map for the quarter and APNIC's per-country RPKI series; raw kept private). 29 Oct: APNIC Labs only (RIPEstat terms forbid redistribution); written leave 1 Nov 2026 (ticket 00177078: credit APNIC Labs, figures as published).

*Added* 2026-10-26. *Sources:* apnic_labs. *Decides a label:* no.

*Method.* Quarterly, for the whole quarter (author, 19 Nov 2026), APNIC Labs' public per-country figures as published: share of users behind resolvers that validate DNSSEC (the 90 days ending on the quarter's last day; full and partial), and share of users whose networks drop RPKI-invalid routes (I-ROV filtering; APNIC's 112-day window ending on the quarter's last day, the published window nearest to 90 days), with samples and APNIC's weights. RPKI route coverage (ROAs) is not in APNIC's tables and is not measured (RIPE NCC dropped 29 Oct). Reported by region with a world figure weighted by users. A measure of the internet's own health, independent of any government's list.

## X21

**Regional splits of attack, bot and ransomware series**

*Question.* Do the attack and harm trends differ by world region?

*Status.* active: 29 Oct: Radar by continent and ransomware.live by country both hold up.

*Added* 2026-10-26. *Sources:* radar, ransomware. *Decides a label:* no.

*Method.* Cloudflare Radar layer-7 attack and bot-traffic series by region, and ransomware.live monthly posting counts by victim country grouped into regions (aggregates only, as the standing rules require; ransomware.live figures published only once permission is granted, config/sources.yaml). Shadowserver per-country series are added if approved.

## X22

**Breach notifications outside the US**

*Question.* Is reported breach harm rising outside the US too?

*Status.* active: 29 Oct: UK ICO and OAIC; PDPC and ENISA at the March review.

*Added* 2026-10-26. *Sources:* uk_ico, oaic, enisa, sg_pdpc. *Decides a label:* no.

*Method.* Published counts of reported data breaches from the UK ICO, Australia's OAIC (twice a year), Singapore's PDPC and ENISA's EU reports, shown next to HHS OCR (X17) and SEC Item 1.05. Each regulator's rules on what must be reported differ, so each series is read as its own trend, never added together. Lower priority: after X19-X21.

## X23

**Age of attacked flaws seen by the SANS ISC honeypots (companion to I4)**

*Question.* What share of the CVE-labelled honeypot activity SANS ISC sees targets flaws more than 12 months old?

*Status.* planned: author's decision 29 Oct (indicator review); first value with the Q4 2026 pilot.

*Added* 2026-10-29. *Sources:* isc_honeypot, cve. *Decides a label:* no.

*Method.* From the monthly X14 aggregates: requests per CVE named in the quarter, each CVE aged from its CVE.org publication date; share older than 12 months, computed as I4 is. Reported beside I4 (Shadowserver honeypots, or its registered KEV version) and never merged with it or used in its place. Honeypots see automated scanning only; CVE names come from URLs.

## X24

**Agreement between free exploitation signals (companion to I6)**

*Question.* How far do CISA KEV, the EU Vulnerability Database's exploited flag and the national alerts of X19 agree on which flaws are attacked, and how late is each?

*Status.* planned: author's decision 29 Oct (indicator review); first value with the Q4 2026 pilot.

*Added* 2026-10-29. *Sources:* kev, euvd, certfr, jpcert. *Decides a label:* no.

*Method.* Same method as I6 (pairwise and multi-rater agreement, and each source's median lag behind the earliest signal), on CVEs with any signal in the trailing two quarters, using only free sources. Reported beside I6 and never in its place: I6 as registered needs VulnCheck and Shadowserver. What EUVD's "exploited since" date means is checked first (KEV-lag back-test, 9 Nov).

## X25

**Supply of AI security tools on GitHub (how they use AI; offensive, defensive and dual-use)**

*Question.* How many open-source security tools on GitHub use AI, and do they rely on hosted closed models or on open-weight models run locally; what do they do (offensive security, defensive security, dual-use, worked out from tool types); how fast does each group grow, which AI does each build on, and how many offensive-security tools mention safeguards? (Reworded 31 Oct 2026, author's decision, from "attack and defence tools"; labels describe what a tool does, not who uses it or why.)

*Status.* active: author's decision 30 Oct 2026 (12 Nov review item 12, decided early, as a hand-run sweep).

*Added* 2026-10-30. *Sources:* github_search. *Decides a label:* no.

*Method.* Defence tools added the same day (author, 30 Oct 2026): fixed defensive queries beside the offensive ones. Since 31 Oct 2026 (author) every repository is labelled first by how it uses AI (hosted closed model, open-weight or local, both, none named), then by tool types, from which its group follows (offensive security, defensive security, dual-use, unclassified), first from its own words, then checked by Claude for every tool with 100+ stars and confirmed by the author; the two sides are compared by trend, since the query lists differ. Run by hand only, never on a timer (Research task github_tools): a baseline in late October 2026, then at the start of 2027, mid-2027 and the end of 2027. Fixed queries (config/github_tool_queries.yaml) over GitHub's public search; per repository: maker (person or organisation), creation date, stars, forks, licence, the AI models or agent frameworks named, and for the most-starred whether the README mentions a scope or authorisation safeguard. No code is downloaded or run. Claude sorts each sweep (dropping tools that test AI models themselves, copies and unrelated hits) and the author confirms the register, exploratory/ai_attack_tools.csv. Read as supply, never as use: never scored, never counted as an attack, reported beside X3 and X12. Each sweep gives the creation-month curve from the start; repeated sweeps add growth in stars and forks. The January 2027 sweep is part of the pilot (author, 30 Oct 2026). Every sweep is kept as exploratory/ai_tool_sweeps/<date>.csv and catalogued with three charts in exploratory/ai_tool_landscape.md (snapshot.x25report), which is part of The Snapshot. <!-- public-figure -->

*Decided 2026-11-19.* Author's decisions, applied by Claude on 19 Nov 2026: labels purpose first (offensive when a tool's own name or description states attacking as its purpose, unless a defensive purpose is stated too, which makes it dual-use); "SOC 1/2/3" counts as a security term only beside another one; new relevance terms (Kali Linux, bug bounty, password cracking, nmap, Wazuh, security alert triage unless about fraud or anti-money laundering); every HexStrike and PentAGI copy counted once, as one line with its number of copies; new searches for agent skills, Claude Code plugins, bug hunters and red-team agents; an outside index of offensive AI agent harnesses (MIT, credited) as a quarterly coverage check, never as counts.

## X26

**How much people hand over to AI (autonomy given to AI models and apps)**

*Question.* How many everyday internet tasks are people handing from themselves to AI, in which kinds of task, and how much control do they keep; does handing over more control, or holding some back, go with better or worse security? (Author, 6 Nov 2026; no view taken on whether handing over is good or bad.)

*Status.* planned: author's decision 6 Nov 2026: for the final 2027 report, even if partly from news reports; probe 19 Nov.

*Added* 2026-11-06. *Sources:* github_search, cloudflare_radar, openrouter, anthropic_econ_index, curated. *Decides a label:* no.

*Method.* No single public measure exists, so several free signals are read side by side, quarter by quarter through 2027, and reported together in the final 2027 report (never scored). (1) Software work: the share of public GitHub pull requests opened by AI coding agents, and the share of those merged with no human change (GitHub's public search; exact for agents that open pull requests under their own accounts, estimated for the rest; checked against a third-party tracker, amplifying.ai). (2) Web tasks: Cloudflare Radar's AI traffic by purpose, especially fetches made on a user's behalf (free API; same source as X4). (3) Conversations: the Anthropic Economic Index share of conversations where the user hands over a whole task rather than working with the model (open data; Claude only, and a conflict of interest because Claude does the study's analysis, so reported with that note and never alone). (4) News and surveys: dated reports of people or organisations handing tasks to AI agents, by task category (shopping, email, payments, coding, IT and security operations), logged like X3 from the monthly feed screen and the author's reading. Security link, descriptive only: the X3 and X5 logs record whether each case's report mentions a human approval step (yes, no, not stated), so the final report can show whether incidents with agents acting on their own differ from those where people kept a check. Data terms, access and a first test count are checked in the 19 Nov probe. Author's decisions 19 Nov 2026 (cards, after the probe; findings private in exploratory/docs/x26-probe-2026-11-19.md): four signals kept, read quarterly with the pull from the Q1 2027 report and reported together in the final 2027 report: (1) GitHub pull requests by AI coding agents, the exact count from agents' own app accounts as the main figure and the count from agents' default branch names as a marked estimate, with a sample of up to 100 merged pull requests per exact agent checked for commits by anyone else; (2) Cloudflare Radar's "user action" share of AI-bot traffic (each reading dated, because Cloudflare relabels purpose history); (3) OpenRouter's task classification (agent share), a reading saved each quarter because it is a rolling window, one platform's customers only; (4) the news log. The Anthropic Economic Index is dated context only, never a figure on its own (conflict of interest). AI browsers get no separate signal (no free reliable count; their web fetches fall in Radar's user-action share; cases go in the news log). The human-approval column goes in the X3 log (back-filled) and the news log, not X5, which is a tag on CVEs with no case reports. <!-- public-figure -->

## X27

**Web patch adoption (HTTP Archive server versions)**

*Question.* After a fix ships for a flaw in widely used web server software, how quickly do the sites that announce their version move to a fixed release, and how many stay on releases that will never get an upstream fix?

*Status.* planned: 12 Nov research review, decision 10: condition met (29 Oct test found versions recorded); first case PHP2Shell.

*Added* 2026-11-12. *Sources:* httparchive. *Decides a label:* no.

*Method.* Monthly, the share of HTTP Archive pages that report a version of the affected software (PHP first) on a fixed release, and on a release line with no upstream fix, 30 and 90 days after the fix. Covers only servers that announce their version (about one in five PHP pages in the 29 Oct test), reported as that subset. Distribution backports keep the old version number, so shares on unfixed versions are an upper bound on unpatched sites, and "never fixed" means "no upstream fix". Exploratory, never scored. Test run: run-reports research/2026-10-29T2336Z-httparchive_versions; case notes docs/cases/php2shell.md.

## X28

**Age of attacked flaws seen by GreyNoise sensors (companion to I4)**

*Question.* Of the CVE-tagged attack traffic GreyNoise sees in the quarter, what share targets flaws more than 12 months old, and which of the quarter's newly exploited flaws did its sensors see, and when first?

*Status.* planned: collector built 18 Nov 2026 (greynoise.yml); first quarterly run 2 Jan 2027; weekly sweep agreed by GreyNoise and switched on 18 Nov 2026.

*Added* 2026-11-17. *Sources:* greynoise, cve, kev. *Decides a label:* no.

*Method.* Quarterly (author's decision, 18 Nov 2026, option B): each CVE's earliest GreyNoise tag creation date (the "GreyNoise detection date", not proof of first attack) and, for the quarter's KEV additions, threat IP counts for the last 1, 10 and 30 days and last seen (counts only; IP addresses are never collected). Weekly, once GreyNoise agrees: the same lookup for every tagged CVE, kept six months, giving the first week each flaw showed activity (the tag activity call returns only the last 24 hours, so history is built up by the study). Each CVE aged from its CVE.org publication date; share older than 12 months, computed as I4 is, reported beside I4 and X23 and never merged with them. For the quarter's newly exploited flaws (Track B), the first day GreyNoise saw activity is recorded beside the KEV and VulnCheck dates as a cross-check. With 90 days of history this covers the age measure (author's rule, 16 Nov 2026: under four months, age only); GreyNoise agreed on 18 Nov 2026 to a private six-month rolling copy of daily tag counts and the weekly sweep. Corrected 19 Nov 2026 after the first test run: the API's 90-day view (days=90) gives one total per tag for the period, not the days a tag was active, so first-attack dates come from the weekly sweep (the first sweep showing activity in the previous ten days), not from the 90-day view. Sensors see automated scanning only. Exploratory, never scored. Credit: "Data provided by GreyNoise".

## X29

**AI infrastructure as a target (merged into X5, X11 and X3 the same day)**

*Question.* Retired number. Adopted 19 Nov 2026 and folded the same morning into X5, X11 and the X3 log, which already covered most of it (author, cards); kept so the number is never reused.

*Status.* merged.

*Added* 2026-11-19. *Sources:* . *Decides a label:* no.

*Method.* See X5 (exploited AI-stack flaws, race times, shared control and data planes, disputed flaws), X11 (GreyNoise AI-product tags; exposure totals from Censys or Shadowserver if granted) and X3 (the "way in" field). Proposal privately in exploratory/docs/x29-ai-infrastructure-proposal.md.

## X30

**AI software supply chain (malicious packages, models and agent skills)**

*Question.* How many malicious packages aimed at AI developers and AI libraries reach public registries each quarter, and how often are poisoned models or agent skills found on AI hubs?

*Status.* planned: author's decision 19 Nov 2026 (cards); built by 28 Nov.

*Added* 2026-11-19. *Sources:* osv_malicious, curated. *Decides a label:* no.

*Method.* Author's decision, 19 Nov 2026. Per quarter, the malicious-package records (OSV MAL-) published for npm and PyPI whose package name, description or dependencies name an AI library, provider or brand on a dated list (for example openai, anthropic, langchain, llama, transformers, huggingface, mcp), including names that imitate them and names AI coding assistants are known to invent ("slopsquatting"), counted beside all malicious records so the AI share is visible. A dated log of poisoned models, datasets and agent skills on AI hubs, entered only from primary reports. Only what has been caught and reported is counted, which is stated with every figure. Exploratory, never scored.

## X31

**AI-generated reports and the defenders' capacity to fix**

*Question.* Are AI-generated vulnerability reports overwhelming the people who fix flaws, and does that go with slower fixes for open-source flaws?

*Status.* planned: author's decision 19 Nov 2026 (cards); built by 28 Nov.

*Added* 2026-11-19. *Sources:* cve, osv, curated. *Decides a label:* no.

*Method.* Author's decision, 19 Nov 2026. Per quarter: CVE records rejected or disputed (from the CVE List already pulled), as a count and a share; a dated log of disclosure channels closed, paused or restructured because of report volume (bug bounties, vendor and open-source programmes), from primary statements; and a test of whether time from disclosure to fix for open-source flaws lengthens as the log grows (descriptive, no causal claim). Rejected CVEs have other causes too, so the count is read as a signal, never proof. Exploratory, never scored.
