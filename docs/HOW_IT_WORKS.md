# The Internet Security Snapshot: How It Works and What It Will Show

23 October 2026 · Paul Gagne

## Abstract

The Internet Security Snapshot asks one question every quarter: are defenders closing exploitable software flaws faster than attackers start using them, and how is AI changing that race? It answers with free public data only, on a plan registered in advance (OSF, DOI 10.17605/OSF.IO/3XT82, 20 October 2026), so the results cannot be bent to fit a story.

Each quarter an automatic job collects the data and freezes an exact copy. The author hand-checks the few judgments a computer cannot make, and a report follows: a provisional draft on the 1st of January, April, July and October, published once the author has reviewed it (within two days), and a final report one month later. The report tracks seven questions, from how fast newly disclosed flaws are attacked to how often AI tools are credited with finding them.

The first report covers the last quarter of 2026 as a labelled pilot. The first scored quarter is Q1 2027. By the end of 2027 the project will have a year of comparable evidence on the race, and on AI's growing role on both sides of it.

## How the data flows

Every number in the report travels the same path, left to right: free sources, an automatic quarterly pull, a frozen copy, checks, analysis, and publication.

![Architecture: free sources flow through the quarterly pull, frozen bundles, normalize and analysis to four published outputs](diagrams/architecture.svg)

1. **Free sources.** Public records of software flaws (CVE records), CISA's list of flaws known to be attacked, CISA's added analysis (Vulnrichment), daily attack-likelihood scores (EPSS), NVD, vendor advisories, company breach filings with the SEC, and Cloudflare Radar's internet traffic data.
2. **Quarterly pull.** GitHub Actions collects everything at 06:00 UTC on 1 January, April, July and October, and again one month later for the final report.
3. **Frozen bundles.** An exact copy of every input is kept with checksums and archived on Zenodo, so anyone can recompute any number later.
4. **Normalize.** Automatic data checks flag missing fields or sudden changes in a source, then the fixed rules pick which flaws to study.
5. **Analysis.** The author's hand checks are added. Claude drafts the analysis and the author approves it before anything is published.
6. **Publish.** The evaluation page, a quarter-by-quarter archive, timelines for the sampled flaws, and a citable Zenodo bundle of data and code.

**Three sources are placeholders for now.** Shadowserver (internet exposure counts and honeypot attack data), VulnCheck KEV (earlier attack dates) and ransomware.live (leak-site post counts) were asked for permission on 20 October 2026. Follow-ups go out on 20 November, and replies are hoped for by 1 January 2027, before the pilot report. Nothing derived from a source is published until it says yes; a source that says no is dropped and the change is logged publicly.

## What the study looks at: flaws and four tracks

A **flaw** here is a security weakness in a piece of software that has been given a public ID, a CVE number. Thousands of serious flaws are published every quarter: about 4,800 in Q2 2026 and 9,800 in Q3 met the study's rules, and the number is rising. "Serious" means rated 8 or higher out of 10, or "critical" by the vendor. Only a few hundred flaws a year are newly known to be attacked, and the study is built around that imbalance.

The work runs on four separate tracks, each feeding its own part of the report.

![Overview: public data feeds four tracks, which feed the quarterly report](diagrams/overview.png)

| Track | What goes in | Question the report answers | Status |
| --- | --- | --- | --- |
| A. A fair sample of new serious flaws | Up to 12 flaws a quarter, one per group per month: firewalls and VPNs, web and collaboration software, other internet-facing software, flaws credited to an AI tool | Once a fix exists, how fast do exposed systems on the internet get updated? | Waits for internet scan data |
| B. Every flaw attackers started using this quarter | Every flaw added for the first time to CISA's list of attacked flaws, typically 75 to 100 | How soon are flaws attacked, how old are they, and is the fix usually out first? | Reported now; the race measure is decided on 21 December |
| C. Was AI involved in finding the flaw? | The credits line of every new flaw | What share of new flaws were found with AI tools? | Reported now |
| D. Background trends | Count of all new flaws; ransomware leak-site posts; company breach filings | Is flaw discovery rising, and is visible harm rising or falling? | Reported now (leak-site counts once permitted) |

Track A is picked by a fixed random draw that anyone can repeat, so nobody chooses which flaws are studied. Track B takes no sample at all: every newly attacked flaw counts. Each track is explained step by step, with its own diagram, in [EVALUATION_FLOW.md](EVALUATION_FLOW.md).

## Why some checks are done by hand

A few questions need a person reading a vendor's page or a credit line, not a program matching words. The author answers them in a private Hand Check app, about 45 to 50 minutes a quarter, under written rules ([HAND_CHECK.md](HAND_CHECK.md)).

| Hand check | Why a program cannot do it alone |
| --- | --- |
| **Does the pick qualify?** Is an "other" product really reachable from the internet; did an AI tool really take part in finding an AI-credited flaw? | Product names and credit lines are ambiguous: "Claude" in a credit can be a person, a lab or a tool. |
| **When was the fix released?** Confirm or correct a pre-filled date from the vendor's own announcement; mark "No fix yet" or "Can't find". | Vendors often announce a flaw before the fix ships, or fix it quietly weeks earlier. That date decides whether an attack came before or after the fix. |
| **Unclear AI credits** (Yes / No). Clear patterns such as "found using \[tool\]" are counted automatically, with 1 in 10 re-checked. | Wording varies widely; a lab or company name alone never counts as AI, unless the credit says the work was a collaboration with it. |

Two safeguards keep the hand checks honest. Each quarter, five earlier answers are shown again unmarked, and the share answered the same way is reported. The random draw decides which flaws are studied; a hand check can only skip a pick that does not qualify, never choose one.

## The race, and the decision on how to measure it

The race starts when a fix is released. Defenders must install it on their systems; attackers study the fix, build an attack, and look for systems that have not updated. A fix protects no one until it is installed. The race asks who gets there first.

It has two halves. The attacker side is how many days pass between the fix and the first recorded attack (negative when the attack came before any fix, a zero-day). The defender side is how fast exposed systems disappear from the internet once the fix is out. The defender side needs internet scan data (Shadowserver), so the attacker side comes first.

**The measurement problem.** As registered, the attacker side was to be measured on the random sample of Track A. But very few serious flaws are ever attacked: in Q3 2026 only 41 of 9,812 eligible flaws (0.42%) reached CISA's list. A back-test on Q2 and Q3 2026 found the sample averages 0.3 to 0.4 attacked flaws a quarter, too few to compute anything. The decision tree below sets out the choice for the 21 December session.

![T1 decision tree: three questions lead to options (a), (b), (c) or (a+d)](diagrams/t1_decision.png)

| Option | What it does | Q2–Q3 2026 back-test | Trade-off |
| --- | --- | --- | --- |
| **(a) All flaws first attacked in the quarter** | Measures the race on every newly attacked flaw (Track B), 75 to 100 a quarter | 16–23% attacked before a fix existed; at least 8 to 15 days from fix to first attack (typical) | Usable every quarter; covers only flaws that were attacked. The zero-day share is a minimum. |
| **(b) Keep as registered** | Sample only | 0.3–0.4 attacked flaws a quarter | Almost always "no estimate". |
| **(c) Much larger sample** | Same rule, about 2,000 picks a quarter | Not run | Far too much hand work. |
| **(a+d) Add a weighted sample** | (a) for the number; the sample favours flaws predicted likely to be attacked (EPSS), so 2 to 3 attacked flaws a quarter can be followed end to end | Weighted sample alone: zero-day share anywhere from about 3% to 87% | Breaks the registered rule that predictions never pick flaws; pays off only with scan data. |

The figures for (a) count every newly attacked flaw, including older ones, as corrected on 23 October. They are minimums because CISA lists a flaw only once there is guidance for fixing it, which delays the listing of zero-days most. Two free improvements have been identified and are being built in. CISA's "active exploitation" flag marks about 1 in 10 attacked flaws a week or more before the listing. Vendor sources (Microsoft, Cisco, Palo Alto, GitHub) now date the fix for 54 of 175 recent attacked flaws, up from 18. Details: [proposals/T1_OPTIONS.md](../proposals/T1_OPTIONS.md).

## What we hope to show about AI, from now to the end of 2027

AI now works on both sides of the race. Defenders and researchers use it to find flaws; attackers use it to build and run attacks. Over five quarters the study will show whether these trends move together, and how fast. It can show what moved and when; it cannot prove that AI caused a change, and the report will say so.

**Defender side: AI finding flaws (scored).**

- **Share of new flaws found with AI tools,** every quarter, as a low, hand-checked and high range. The author's registered prediction is that it rises. A trend is called only when the low and high figures move the same way.
- **Are AI-found flaws different?** Within the sample, flaws credited to AI are compared with the rest on severity, on how often they allow an attacker to run code, and on how soon they are attacked.
- **Who is finding them:** which AI labs' tools are credited, and new tools appearing before they reach the term list.
- A caution already found: in Q3 2026, about 133 of 139 unclear credits came from organisations with documented AI-discovery programmes. The true AI share is probably above the hand-checked figure, which is why the range is shown.

**Attacker side: AI-assisted attacks (exploratory, clearly labelled, never deciding a label).**

- **Speed in the tail:** the share of newly attacked flaws hit within 1 day and within 7 days of going public, and the share attacked before any fix existed. Faster exploitation is the first place AI-built attacks would show.
- **A log of publicly reported AI-operated attack campaigns:** what they targeted, and whether they used known flaws or bugs that never got a CVE.
- **AI software as a target:** flaws in model servers, agent platforms and AI gateways, and self-hosted AI servers left exposed on the internet.
- **Capable models attackers can run privately:** a log of open-weight model releases, to line up with any change in attack speed.

**How the year builds.** The Q4 2026 pilot (January) gives the first look. Q1 2027 (April) is the first scored quarter. At the March 2027 annual review, an exploratory AI measure that has proved reliable can be promoted into the scored core. By Q3 2027 (November) there are four comparable quarters, enough to see whether AI-credited discovery and the attacker's clock are moving together. The first check against better reference data, covering 2027, follows in March 2028.

## The 2027 calendar

The year runs on a fixed rhythm: each quarter gets a provisional draft on the 1st, published after the author's review within two days, a hand-check window from the 4th to the 28th, and a final report a month later.

![Snapshot calendar 2027: four quarterly cycles plus the Censys application, the annual review, the external review and the side-by-side period](diagrams/calendar_2027.png)

| Date | Event | What it is | Why it is needed |
| --- | --- | --- | --- |
| Fri 1 Jan | Q4 2026 provisional report | The automatic pull for October to December 2026, labelled **pilot** | Tests the whole system on real data before any result is scored |
| 4–28 Jan | Q4 2026 hand-check window | About 45 to 50 minutes in the Hand Check app, at any time in the window | Supplies fix dates and AI-credit decisions no program can make |
| Mon 1 Feb | Q4 2026 final report | Data pulled again, hand checks included | Sources keep updating; a month's wait catches late listings and corrections |
| 15 Feb – 1 Mar | Censys research application | Request for internet scan data, written by the author | Needed for the defender side of the race and the yearly accuracy check |
| Mon 15 Mar | Annual review and change window | The only time the scored rules may change, logged on OSF; external reviewer confirmed by this date | Lets the study fix errors in the open without moving the goalposts mid-year |
| Thu 1 Apr | Q1 2027 provisional report | **The first scored quarter**, the first with Improving / Worsening labels | The point where results start to count |
| 5–28 Apr | Q1 2027 hand-check window | As above | As above |
| 3–28 Apr | External review of Q1 2027 | An independent reviewer checks the first scored report before it is final | Promised in the pre-registration as a safeguard against the author's and Claude's blind spots |
| Sat 1 May | Q1 2027 final report | Data pulled again, hand checks and the reviewer's comments included | Sources keep updating; a month's wait catches late listings and corrections |
| Thu 1 Jul, 5–28 Jul, Sun 1 Aug | Q2 2027 provisional, hand check, final | Second scored quarter | Builds the comparison |
| Fri 1 Oct, 4–28 Oct, Mon 1 Nov | Q3 2027 provisional, hand check, final | Third scored quarter; fourth report of the year | Four comparable quarters: enough to see trends |
| All year | Old and new race measures side by side | Applies only if the race measure changes on 21 December 2026 | A changed rule is shown next to the old one for four quarters, so readers can see what the change did |
| Sat 1 Jan 2028 | Q4 2027 provisional report | Closes the first full year | Followed in March 2028 by the first check against better reference data |

Hand-check windows run from the 4th to the 28th so the author has as much time as possible; answers are needed by the 28th so the final run on the 1st can use them.

## How the rules stay trustworthy

The study's core was registered publicly in advance and is locked: the seven questions, the rules for picking flaws, the list of AI-tool terms and the root-cause groups. An automatic check stops any quiet change, and only the core decides whether a trend is called Improving, Worsening, Rising or Falling. New ideas, including most of the attacker-side AI measures, can be explored at any time in a separate, clearly labelled section that never affects those labels.

The core changes only to fix an error or a measure that has stopped working, and then in the open. The old and new versions are reported side by side for four quarters, the switch happens only at the March review, and every change is logged with its date, recorded on OSF and tagged. All raw data is kept, so a question added later can usually be answered for earlier quarters too. Full details: [CHANGE_POLICY.md](CHANGE_POLICY.md).

The result, by the end of 2027, should be a year of evidence anyone can check: how fast attacks follow fixes, how fast defenders patch where the data allows, and whether AI is speeding up either side.

**Sources:** project repository [pagagne/internet-security-snapshot](https://github.com/pagagne/internet-security-snapshot) (pre-registration, change policy, T1 options paper, research plan); registration [doi.org/10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82); [CISA Known Exploited Vulnerabilities](https://cisa.gov/known-exploited-vulnerabilities).
