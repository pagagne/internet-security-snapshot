# Internet Security Snapshot

## Mission

The Internet Security Snapshot is a study of the internet's security through the year 2027.
Every quarter it asks one question: are defenders closing internet-exposed software flaws
faster than attackers start exploiting them, and how is AI changing that race?

It answers with free public data only, on a plan registered in advance (OSF, DOI
[10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82), 20 October 2026), so the results
cannot be bent to fit a story. The sources are public records of software flaws (CVE), CISA's
list of flaws known to be attacked (KEV) and its added analysis (Vulnrichment), NVD, daily
exploitation-likelihood scores (EPSS), vendor fix dates, company breach filings with the SEC and
Cloudflare Radar's internet traffic data. ransomware.live joined with written permission on 27 October 2026; Shadowserver, VulnCheck and
Censys join only once each grants permission or access.

Each quarter an automatic job freezes an exact copy of the data, the author hand-checks what a
computer cannot judge, and seven pre-registered questions are reported: a provisional evaluation
on the 1st of January, April, July and October, and a final one a month later. Q4 2026 is a
labelled pilot; Q1 2027 is the first scored quarter.

## Key documents

- **How it works (plain-language overview with diagrams):** [`docs/HOW_IT_WORKS.md`](docs/HOW_IT_WORKS.md)
- **Pre-registration:** [`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md)
  (v1.0, tag `prereg-v1.0`), registered on OSF on 20 October 2026:
  [doi.org/10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82)
  (project: [osf.io/3smuq](https://osf.io/3smuq))
- **Deviations log:** [`prereg/DEVIATIONS.md`](prereg/DEVIATIONS.md)
- **Change policy:** [`docs/CHANGE_POLICY.md`](docs/CHANGE_POLICY.md): a locked core
  (baseline `core-v1.1`, checksums in `prereg/LOCKED.yaml`) and an exploratory add-on
  layer (`config/exploratory.yaml`) that never decides a label
- **Hand checks:** criteria in [`docs/HAND_CHECK.md`](docs/HAND_CHECK.md); the author works
  through them in the Hand Check app ([user guide](docs/HAND_CHECK_APP.md))
- **Cohort rules:** [`config/cohort_rules.yaml`](config/cohort_rules.yaml),
  [`config/ai_credit_terms.yaml`](config/ai_credit_terms.yaml),
  [`config/root_cause_map.yaml`](config/root_cause_map.yaml)

## Data sources

Status as of 26 Oct 2026. Terms, requests and replies are logged in
[`docs/PERMISSIONS.md`](docs/PERMISSIONS.md); this table is updated with it. "Core" sources feed
the pre-registered measures; "exploratory" ones are reported separately and never decide a label
([`config/exploratory.yaml`](config/exploratory.yaml)).

### In use: free and public (ransomware.live with written permission)

| Source | What it gives the study | Role |
|---|---|---|
| CVE.org records (CVEProject/cvelistV5) | New flaws (T5), finder credits for AI involvement (T7), cohort dates and bug types | Core |
| CISA Known Exploited Vulnerabilities (KEV) | First-attack dates for the race (T1a), time to exploitation (T3), age of exploited flaws (T4) | Core |
| CISA Vulnrichment | CISA's "active exploitation" flag; bug type and severity where the CVE record lacks them | Core |
| NVD API 2.0 | Severity, bug type and product matching (fallback) | Core |
| FIRST EPSS | Daily exploitation-likelihood scores | Context |
| SEC EDGAR | Breach filings, 8-K Item 1.05 (T6b) | Core |
| Cloudflare Radar | Internet-wide attack and traffic trends | Context |
| Vendor advisories and GitHub/OSV (Microsoft, Cisco, Palo Alto, GitHub advisories) | Fix dates for the race | Core |
| Exploit-DB, Metasploit, Nuclei, GitHub | Dates public exploit code appeared | Core (cohort), exploratory (X7) |
| Linux kernel commits | Fix dates for Linux flaws (being added, Nov 2026) | Core (fix-date pre-fill) |
| Google Project Zero "0day In the Wild" | Independent check of the zero-day share | Exploratory (X15) |
| SANS Internet Storm Center web honeypot | Attack activity by category, monthly, aggregates only | Exploratory, context (X14) |
| deps.dev and OSV | Patch adoption for open-source packages (in testing) | Exploratory (X16) |
| HTTP Archive and WordPress.org statistics | Patch adoption on websites (in testing) | Exploratory |
| HHS OCR breach register | Health-sector hacking breaches (in testing) | Exploratory (X17) |
| [ransomware.live](https://www.ransomware.live) (with permission, 27 Oct 2026) | Ransomware leak-site postings, aggregate counts only, credited (T6a) | Core |

### Awaiting permission or access

| Source | What it would give the study | Request | Status |
|---|---|---|---|
| Shadowserver | Exposure series (T1b, T2) and honeypot attack statistics (T1, T3, T4) | Asked 20 Oct 2026 | Awaiting reply; follow-up 20 Nov |
| VulnCheck KEV (community) | Earlier exploitation dates (T1, T3); agreement checks | Asked 20 Oct 2026 | Awaiting written permission; used privately only until then |
| Censys | Internet exposure counts (T1b, T2) and the annual check | Application 28 Oct 2026 | To send |

Each source above has an on/off switch in [`config/sources.yaml`](config/sources.yaml); nothing derived
from one is published until its permission is granted.

### Being tested: views beyond the US (added 26 Oct 2026)

| Source | What it would give the study | Role |
|---|---|---|
| CERT-FR, JPCERT/CC, BSI, KrCERT/CC alerts | Other countries' active-exploitation alerts, compared with CISA KEV | Exploratory (X19) |
| APNIC Labs and RIPE NCC | DNSSEC validation and RPKI route checking by country | Exploratory (X20) |
| Cloudflare Radar and ransomware.live by region | Attack, bot and ransomware trends by world region | Exploratory (X21) |
| UK ICO, OAIC, PDPC, ENISA | Data-breach notifications outside the US | Exploratory (X22) |
| Quarterly web sweep, nine languages | AI-run attack reports outside the usual channels | Exploratory (X3) |
| GreyNoise | Attack activity by CVE | Request 27 Oct 2026 | To send |
| CrowdSec | Exploitation timelines by CVE | Question 27 Oct 2026 | To send |

A source without a written yes by the 21 Dec 2026 decision session runs without it for the
Q4 2026 pilot; a later yes is switched on at the next quarter's run. Gaps are never filled by
estimation.

## Schedule

<!-- schedule:begin -->
<!-- Generated from docs/schedule/schedule.yaml (milestones); edit there, then run python -m snapshot.schedule build. -->
| Date | Milestone |
|---|---|
| 20 Oct 2026 | Pre-registration registered on OSF (DOI 10.17605/OSF.IO/3XT82) |
| 28 Oct 2026 | Censys research-access application sent (written by the author) |
| 30 Nov 2026 | Cutover - the repository's schedule runs the study (docs/OPERATIONS.md) |
| 1 Dec 2026 | Dry run on Oct-Nov 2026 data (unscored; started by the Schedule workflow) |
| 4 Dec 2026 | Public landing page (GitHub Pages) and Discussions opened; project links shared from here on |
| 15 Dec 2026 | Full dry run with all available sources (1 Oct-14 Dec data; unscored) |
| 21 Dec 2026 | Core-freeze decision session (docs/CORE_FREEZE_DECISIONS.md) |
| 29 Dec 2026 | Final core freeze: tag core-v1.2, OSF update |
| 1 Jan / 1 Feb 2027 | Q4 2026 pilot: provisional / final |
| 1 Mar 2027 | External reviewer confirmed (decision item 17) |
| 15 Mar 2027, then yearly | Annual review and change window; annual check of free numbers from March 2028 |
| 1 Apr / 1 May 2027 | Q1 2027, first scored (confirmatory) quarter: provisional / final, with the external review published beside the final |
| 3-28 Apr 2027 | Independent external review of the Q1 2027 provisional report |
| 1 Feb 2028 | Q4 2027 final: last quarter of the first year |
| 1 Apr 2028 | 2027 closing re-run with full follow-up |
<!-- schedule:end -->

## Principles

- Free data and free infrastructure only; nothing is estimated to fill a gap.
- Rates with stated denominators, not raw counts.
- Raw inputs frozen with checksums; every published number reproducible with one command.
- All seven tracking questions reported every quarter, whatever the result.
- No scanning, no exploitation, no host-level data, no victim names.
- Private by design: data a provider has not yet allowed us to publish, and personal details,
  never appear in this repository or its public run outputs. They are kept in a private backup
  ([`docs/BACKUP.md`](docs/BACKUP.md)); a scan on every change and every day checks this
  ([`docs/OPERATIONS.md`](docs/OPERATIONS.md), "Private by design").

## AI involvement and conflict of interest

Code and draft evaluations are written with Claude, an AI model made by Anthropic.
Anthropic is named in the report this study grew from. Safeguards: the frozen
pre-registration, public code, the author's approval of every release, and an external
reviewer for the first confirmatory quarter.

## Licence

Code: MIT (see `LICENSE`). Documentation and the study's own derived data: CC BY 4.0.
Third-party data keeps its own terms; see [`docs/PERMISSIONS.md`](docs/PERMISSIONS.md).
