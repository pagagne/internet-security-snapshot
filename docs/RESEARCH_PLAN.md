# Research window, 23 Oct - 15 Nov 2026: improving the project under two plans

Review with the author: Thu 12 Nov, 10:00 (calendar). Next fixed date: 16 Nov validation.
Permission follow-ups: 20 Nov. If still no reply then, Plan 2 is the default for the
21 Dec decisions. Nothing here changes the locked core; results feed decision items.

## Either way (first)
1. **Fix dates for exploited flaws (option a).** Finding 2026-10-22: the GitHub-based pre-fill
   can date only 16 of 148 CVEs added to KEV in Q2-Q3 2026 (11%); the rest are commercial
   vendors (Microsoft 27, Cisco 14, Adobe, Fortinet, Citrix, ...) and would fall back to
   "assumed = publication date". Research free machine-readable vendor sources: CSAF
   advisory feeds (initial release dates), Microsoft's security update API, NVD references
   tagged "Patch"/"Vendor Advisory". Then rerun the T1 back-test with real dates and measure
   pre-fill coverage and accuracy.
2. **Compare with published studies** (Mandiant/Google time-to-exploit, VulnCheck and Cyentia
   exploitation reports, KEV analyses). Large gaps point to method problems before the freeze.
3. **CISA "active exploitation" flag** (Vulnrichment SSVC, already collected): does it date
   exploitation earlier or more often than KEV listing?
4. **Remaining evaluation code**: labels T2, T4-T6; exploratory X6-X12; NVD root-cause fill;
   first draft of the evaluation page.
5. **One switch per permissioned source** (Shadowserver, VulnCheck, ransomware.live) in config,
   so either plan is a settings change.

## Plan 1: permissions approved
- Shadowserver: data formats; how many cohort picks it tracks (coverage decides whether T1b/T2
  are usable); exposure half-life (T2) and "exposure halved before attack" (T1b) code tested
  on made-up data; honeypot data as primary T4 source and earlier T_exploit; revisit (a+d).
- VulnCheck: how much earlier than CISA its exploitation dates are; private-only route until
  written permission.
- ransomware.live: confirm current aggregate-only use; any extra aggregates allowed.
- Update the validation for the new sources; deviations log entry.

## Plan 2: no reply or refused
- Attack dates from free sources: CISA KEV + CISA active-exploitation flag; public exploit code
  (Exploit-DB, Metasploit, Nuclei) as an earlier "attack possible" date (exploratory X7).
- Patch speed without exposure scans: for open-source flaws, share of downloads/dependents on
  the fixed version over time (npm, PyPI, deps.dev). Feasibility research.
- Other exposure options: see the 25 Oct brainstorm (below). Censys application moved to
  17 Nov 2026 (author's decision, 25 Oct); Shodan's academic tier needs a university email.
- Free substitutes if a permission is refused: Shadowserver -> SANS ISC honeypot data plus
  HTTP Archive and deps.dev for patch adoption; VulnCheck -> EUVD plus inthewild.io.
- Fallback wording for core-v1.2: T1b and T2 "not measured" with the reason; T1(a) under
  option (a) becomes the headline race measure.

## Author's time in this window
Review on 12 Nov (20-30 min). Claude starts any GitHub runs.

## Findings so far

### Item 1: fix dates for exploited flaws (2026-10-23)
Probe run on GitHub Actions over all 175 CVEs added to CISA KEV in Apr-Sep 2026
(`src/snapshot/research/fixdate_probe.py`; results on the run-reports branch under
`research/2026-10-23T1315Z-fixdate_probe/`).

| Tier | CVEs | Note |
|---|---|---|
| GitHub links (current pre-fill) | 18 | open-source; fix 0-37 days *before* CVE publication in 14 of 18 |
| + Microsoft Update Guide API, Cisco CSAF, Palo Alto JSON | 54 in total | vendor date = CVE publication in 31 of 36 |
| + CNA datePublic (disclosure date, not a fix date) | 33 more | earlier than publication in 22 of 58 |
| Publication date assumed | 88 | Linux, Adobe, Fortinet (no machine-readable feed found), Google, Check Point, SonicWall, Oracle, Citrix, ... plus 6 Microsoft CVEs from 2008-2012 |

- For big vendors the vendor date equals CVE publication, so "assumed = publication" is
  usually right *as a disclosure date*. The risk is different: the fix sometimes ships after
  the advisory. Revision histories show it (Cisco 3 of 13: "Updated fixed release
  information"; Palo Alto 2 of 2: "Updated the Fix release timeline"). Those cases decide the
  zero-day share, so they must always be hand-checked.
- Built: `fixdates.prefill_exploited()` (GitHub, Microsoft, Cisco, Palo Alto, datePublic,
  assumed) returning a needs-hand-check flag for fix-later signals, commit-only dates,
  datePublic and assumed dates. Not wired into the measures; option (a) would use it.
- Implication for option (a): hand-check effort is not "about 15 random"; it is every flagged
  case (about 120 of 175 per half-year, mostly quick "fix available at advisory? yes"
  checks) or a random sample of flagged cases. To settle on 12 Nov.
  Author's leaning (24 Oct): the extra time is fine, so check every flagged case (about 1½ h
  a quarter rather than about 50 min); confirm on 12 Nov. Checking every case also narrows
  the fix-date ranges the race now reports (`snapshot.events`), so the zero-day range shrinks.

### Item 2: comparison with published studies (2026-10-23)
- VulnCheck, 1H 2026 (495 newly exploited CVEs, 79 sources): 23.4% exploited on or before CVE
  publication; median publication-to-exploitation 80 days. Our option (a) preview: 21-25%
  zero-day share - close.
- Google/Mandiant, 2023 (138 exploited CVEs, incident-response evidence): 70% zero-days,
  average time-to-exploit 5 days (47 without removing outliers). Much higher zero-day share:
  their evidence sees attacks before public listing, ours (KEV) cannot. Our zero-day share is
  a lower bound and must be labelled so.
- **Bias found in our own preview:** it used only CVEs with records in the 2025-2026 data, so
  older CVEs first exploited in the quarter were dropped (Q2: 18 of 75; Q3: 9 of 100). With
  them counted (as at least 'published before 2025'), the median rises from 8 to at least 15
  days (Q2) and 5 to at least 8 days (Q3), and the zero-day share falls from 21% to 16% (Q2)
  and 25% to 23% (Q3). Option (a) must fetch records for every KEV addition, whatever its
  age (the probe already does).
- CISA lists a CVE in KEV only once there is clear remediation guidance (one of its three
  criteria), so KEV dates can lag exploitation most for flaws with no fix yet - exactly the
  zero-days. Another reason the KEV-based zero-day share is a lower bound.

### Item 3: CISA "active exploitation" flag (2026-10-23)
- In 2025-2026 CVE records, the flag is "active" for exactly the 372 CVEs in KEV and for no
  others, so it adds no new exploited flaws.
- But it is often set earlier: for 60 of 372 the latest assessment saying "active" predates
  the KEV listing by 2+ days, for 36 by a week or more (median 35 days), for 22 by a month or
  more (up to 326 days). The flag does not wait for remediation guidance.
- Proposal for decision item 0 / T_exploit: T_exploit = earliest of KEV date and the date of
  the first "active" assessment (from the vulnrichment repository's history; the current
  record only gives the latest assessment date, which is an upper bound). Free, already
  collected, no permission needed - works under Plan 1 and Plan 2.

### From the reconciliation with the October assessment (2026-10-23)
See `docs/RECONCILIATION_2026-10.md`. Added to this window:
- OSV as a fix-date source for open-source flaws (probe alongside item 1).
- Policy-deadline dates (CISA BOD 26-04, CERT-In CISG-2026-02) as exploratory context.
- Every timing figure names its population (recent CVEs vs all newly exploited flaws).

## Brainstorm of 25 Oct: more free sources and process
Claude doc "Brainstorm: Data Sources and Process" (copy: `docs/artifacts/brainstorm-data-sources-2026-10-25.md`).
Adopted by the author on 25 Oct, all exploratory (registered before first look, never scored
until a March review), scheduled in `docs/schedule/schedule.yaml`: daily SANS ISC honeypot
capture (from 2 Nov); KEV-lag back-test against EUVD, Project Zero's sheet and inthewild.io,
and Linux kernel/distribution fix dates (9 Nov); HTTP Archive version test (16 Nov); Censys
application (17 Nov, by the author); deps.dev patch-adoption prototype (7 Dec); AI labs'
lists against our credit counts (25 Jan); GreyNoise and CrowdSec requests (11 Jan); HHS OCR
harm series (18 Jan). Also an inquiry log (`docs/INQUIRIES.md`) and watch cases chosen by rule.

## Pilot watch cases
Real cases to follow through the Q4 2026 pilot, to see how the study's rules and free
sources handle them.

**How cases are chosen (from Q1 2027; author's decision, 25 Oct 2026):** every flaw published
in the quarter with CVSS 9.0 or more that at least one national CERT (CISA, NCSC UK, CERT-EU,
BSI, ANSSI, CERT-In) issued an alert or advisory for; if more than two qualify, two by the
seeded draw. Chosen on the 6th of the month after the quarter (`watch-case-pick`). PHP2Shell,
chosen before the rule, meets it (CVSS 9.2; CERT-EU and NCSC advised).

- **PHP2Shell, CVE-2026-109618 and CVE-2026-109619** (PHP, CVSS 9.2, published and fixed
  21 Oct 2026). Amazon's MadPot honeypots logged an exploit attempt on 17 Oct, four days
  before disclosure, after details leaked around the embargo
  ([Implicator](https://www.implicator.ai/amazon-logged-a-php2shell-exploit-attempt-four-days-before-disclosure/),
  citing the AWS Security Blog). As of 23 Oct: not in CISA KEV; CISA's exploitation flag
  "none" (21 Oct); CISA, Huntress and the PHP Foundation report no confirmed working
  exploitation.
  - *AI credit:* credits are "Ryan at Calif.io", "Wiz", "OpenAI" and PHP developers; OpenAI
    says frontier AI found the flaws. Counted in the T7 headline (OpenAI is mentioned), not in
    the narrow count (no tool named): a live example of why both numbers are kept.
  - *Race:* if CISA lists it later, our first-attack date will be the listing date, after the
    fix, while Amazon saw an attempt before it. Shows why the zero-day share is a minimum and
    what honeypot data (Shadowserver, Plan 1) would add. An attempt is not a confirmed
    exploitation, which is also why KEV waits.
  - *Cohort:* eligible for October (slot c, "other product", if PHP is judged internet-facing);
    only drawn if the seeded draw picks it.
  - *Follow-up:* reviewed with the author on 8 Feb 2027, after the pilot's final report (same
    session as the AI-credit rule evaluation). Claude writes the case note to
    `docs/cases/php2shell.md` by 3 Feb (points collected so far are already in that file): what each step recorded, and anything to change before
    the first scored quarter.

