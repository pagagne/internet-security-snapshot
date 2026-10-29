# Indicator review, I1 to I8 (29 Oct 2026)

Asked by the author on 29 Oct 2026: explain each registered indicator in depth, review each
before the 29 Dec freeze, relate them to TrendAI's "Not only ARTEX" report (`docs/INQUIRIES.md`,
29 Oct), and consider a new indicator. The indicators are defined in
`prereg/PREREGISTRATION.md` section 8 (registered 20 Oct 2026) and explained in
`docs/HOW_IT_WORKS.md`. Nothing here changes the registered plan: recommendations go to the
21 Dec freeze session (`docs/CORE_FREEZE_DECISIONS.md`), and changes after the freeze follow
`docs/CHANGE_POLICY.md`.

## Summary

- **Sound as registered:** I5 (discovery growth) and I8 (AI in discovery, already reworked
  in items 9 and 12-15). I3 (the race) is sound after item 0 (decided 23 Oct).
- **At risk from permissions:** I1, I4 and I6 depend on Shadowserver, and I6 also on
  VulnCheck. Neither has said yes. Without them, under Plan 2 (`docs/RESEARCH_PLAN.md`), I1 is
  read by hand for the few flaws Shadowserver tracks, I4 falls back to its registered secondary
  version (KEV), and I6 cannot be computed as registered. This is the largest open risk for the
  pilot.
- **Known weakness, already on the freeze list:** I2's attack date is CISA's confirmation date,
  which can lag real attacks by days (PHP2Shell: attempts from 17 Oct, KEV 26 Oct). Item 23
  offers an earlier CISA date.
- **Small counts:** I7(b), SEC material-incident filings, had 11 in Q3 2026. Labels on so few
  events will often follow noise; items 2 and 19 address it.
- **Blind spot confirmed by TrendAI:** none of the eight sees AI-run attacks that use no CVE.
  The registered plan says so (section 12); X3 covers it as exploratory.
- **New indicator:** no new labeled indicator before the freeze (it would be untested and
  curated data cannot carry a label). Proposed instead, as item 24: an "AI in attacks" context
  panel reported beside I8 every quarter, never labeled.

## Map: which data feeds each indicator

Drawn at the author's request (29 Oct), **assuming every permission request is granted**
(Shadowserver, VulnCheck, Censys, GreyNoise, CrowdSec).

![Indicators I1 to I8 and the data sources that feed them](diagrams/indicator_sources.png)

*Solid lines: registered sources (pre-registration sections 6 and 8). Dashed grey: exploratory
companions, reported beside the indicator, never replacing it. Green: free and public. Blue:
permission granted. Orange: permission requested, assumed granted here. \* Vulnrichment's first
"active exploitation" date feeds I2 and I3 only if freeze item 23 is adopted. Source:
`docs/diagrams/indicator_sources.dot`.*

| Indicator | Registered sources (all permissions granted) | Exploratory companions |
|---|---|---|
| I1 Exposure half-life | Shadowserver exposure counts; vendor advisories for the fix date | Censys scans (if granted) |
| I2 Disclosure to first attack | CVE.org (publication date); CISA KEV; VulnCheck KEV; Shadowserver honeypots; Vulnrichment "active" date (item 23) | GreyNoise, CrowdSec sightings; national alerts (X19) |
| I3 The race | Vendor advisories (fix date); CISA KEV, VulnCheck KEV, Shadowserver honeypots (attack date); Shadowserver exposure (race part b); CVE.org, NVD, Vulnrichment, EPSS (cohort selection) | - |
| I4 Age of attacked flaws | Shadowserver honeypot statistics; CISA KEV (secondary version) | SANS ISC honeypot (X14); GreyNoise, CrowdSec |
| I5 Growth in new CVEs | CVE.org records | - |
| I6 Agreement between attack sources | CISA KEV; VulnCheck KEV; Shadowserver honeypots | National alerts (X19); EUVD |
| I7 Visible harm | ransomware.live (a); SEC EDGAR (b) | - |
| I8 AI in discovery | CVE.org credits field | - |

Without the pending permissions (Plan 2), the orange sources drop out: I1 is hand-read from
Shadowserver's public dashboard or "not available"; I2 and I3 rest on CISA alone; I4 uses its
KEV version; I6 cannot be computed as registered.

## Each indicator in depth

### I1. Exposure half-life (feeds T2 and T1b)
- **Measures:** for one flaw, the number of days after the fix until the number of vulnerable
  systems seen on the internet falls below half its first count (seven-day average).
- **Data:** Shadowserver's public dashboard, daily vulnerable-instance counts per CVE.
- **Weak spots:** Shadowserver tracks only flaws it chooses, mostly edge devices; a count
  mixes patched, offline and firewalled systems; its method cannot be inspected; at most
  twelve cohort flaws a quarter, few of them tracked.
- **Review:** permission not yet given (asked 20 Oct; follow-up 20 Nov; decision item 16 on
  21 Dec). Plan 2 already provides the fallback: counts read by hand for the tracked flaws,
  with credit, never scraped. Recommendation: confirm at item 16 that without permission
  I1 is reported from hand-read counts or as "not available", never from a substitute source;
  HTTP Archive version shares (12 Nov decision 10) and deps.dev stay exploratory beside it.

### I2. Time from disclosure to first attack (feeds T3)
- **Measures:** days from a flaw's publication (T0) to its first recorded attack, for flaws
  first attacked in the quarter; also the share attacked on or before publication.
- **Data:** CISA KEV additions plus cohort flaws; VulnCheck KEV and Shadowserver as earlier
  dates when permitted.
- **Weak spots:** the KEV date is when CISA confirms an attack, not when it began; targeted
  attacks are rarely seen; free sources lag commercial ones.
- **Review:** PHP2Shell shows the lag (attempts 17 Oct, KEV 26 Oct). Item 23 (CISA
  Vulnrichment's first "active exploitation" date) is the registered-plan answer; X19 (CERT-FR
  and JPCERT/CC alerts, adopted 29 Oct) adds an exploratory comparison. Recommendation:
  decide item 23 on 21 Dec with the 11 Nov evidence; no other change.

### I3. The race (feeds T1)
- **Measures:** days from the fix to the first attack (negative means attacked before a fix
  existed), and whether exposure halved before the first attack.
- **Data:** fix dates (pre-filled automatically, a sample checked by hand) and attack dates
  from I2; the exposure part needs I1.
- **Weak spots:** the registered version on the cohort alone is almost never computable (item
  0); fix dates are uncertain; early private patches (embargoes) are invisible.
- **Review:** item 0 decided (all flaws first attacked in the quarter); interval dates and the
  embargo note are item 20. The "exposure halved first" part (T1b) shares I1's permission
  risk. Recommendation: no change beyond items 0 and 20.

### I4. Age of attacked flaws (feeds T4)
- **Measures:** the share of attacks aimed at flaws more than a year old.
- **Data:** Shadowserver honeypot events with a CVE label; secondary version from KEV
  additions; the two are reported separately and never merged.
- **Weak spots:** honeypots see automated scanning, not careful targeted attacks; labels
  favour well-known flaws; KEV measures confirmation, not attempts.
- **Review:** Shadowserver's honeypot statistics share the permission risk. The SANS Internet
  Storm Center honeypot counts (X14, monthly since 27 Oct) carry CVE labels too.
  Recommendation: report an X14-based age mix as exploratory beside I4 (never replacing it),
  and the KEV version as registered if Shadowserver says no.

### I5. Discovery pressure (feeds T5)
- **Measures:** growth in new CVE records against the same quarter in earlier years
  (rejected records excluded).
- **Data:** CVE.org's own git history (not NVD).
- **Weak spots:** a few large numbering authorities, policy changes and AI scanning campaigns
  cause jumps unrelated to risk.
- **Review:** sound; shown with and without the five largest authorities as registered.
  AI-driven bursts are expected and are what T5 predicts ("Rising"). No change.

### I6. Agreement between attack sources (methods check, never labeled)
- **Measures:** how far CISA KEV, VulnCheck KEV and Shadowserver agree on which flaws are
  attacked, and how late each is.
- **Data:** the three lists, trailing two quarters.
- **Weak spots:** different inclusion rules; VulnCheck is broader than CISA.
- **Review:** needs both VulnCheck and Shadowserver; with neither, there is nothing to compare
  (Plan 2 names EUVD and inthewild.io as free stand-ins for VulnCheck). Recommendation:
  without permission, report I6 as "not available" for the pilot and, as exploratory only,
  agreement between KEV, EUVD and the X19 national alerts (CERT-FR, JPCERT/CC).

### I7. Visible harm (feeds T6)
- **Measures:** (a) ransomware leak-site postings; (b) SEC material-incident filings (Form
  8-K Item 1.05) per 1,000 public companies. Each labeled separately.
- **Data:** ransomware.live (permission granted 27 Oct, aggregates only); SEC EDGAR.
- **Weak spots:** leak sites show only victims who did not pay; SEC covers only US public
  companies and depends on companies' own judgment of materiality; (b) is a small count.
- **Review:** (b) had 11 filings in Q3 2026, so two-quarter labels will often be noise. Item 2
  (add voluntary Item 8.01 disclosures) and item 19 (a significance check beside every label)
  address it. Recommendation: decide both on 21 Dec; no other change.

### I8. AI in discovery (feeds T7)
- **Measures:** the share of new CVEs whose credits name an AI tool or, since 23 Oct, an AI
  lab (headline), with the registered tool-named count kept as the low end.
- **Data:** the credits field of CVE records; versioned term list; spot checks by hand.
- **Weak spots:** credits are optional and inconsistent; uncredited AI use is invisible; names
  can collide.
- **Review:** reworked in items 9 and 12-15. TrendAI cites PHP2Shell as an AI-assisted
  defensive find, which I8 counts. Recommendation: no change beyond those items.

## What the TrendAI report means for the indicators

TrendAI described three AI-using operations against Japan (logged in X3, 29 Oct). They entered
through unprotected admin pages, default passwords and leftover credentials, and named no CVE.
So:
- **I2, I3, I4 and I6** see only attacks on flaws with a CVE that reach a list or a honeypot.
  These attacks had none. CyberStrikeAI also throttled its traffic per target to avoid
  detection, which makes honeypot sightings less likely.
- **I1** measures how fast flaws are patched; a default password is not a flaw that gets a patch.
- **I7** would see these attacks only if a victim appeared on a leak site or, as a US public
  company, filed with the SEC; the victims were mostly small Japanese organisations.
- **I8** measures AI finding flaws, not AI using them.

TrendAI's own conclusion, that AI changed the scale, speed and language of the attacks but not
the way in, matches the plan's stated limit (section 12, "AI attribution") and the pilot
expectations. It is the reason X3 exists, and it argues for showing X3 every quarter, not only
in the annual report.

## A new indicator?

Options weighed:
1. **A labeled "AI-run attacks" indicator** from X3. Not recommended before the freeze: X3 is
   hand-curated from what organisations choose to publish, so a count reflects attention as
   much as activity, and it has no tested baseline.
2. **An "AI in attacks" context panel** (recommended, item 24): reported every quarter beside
   I8, never labeled. Contents: X3 reports in the quarter (all and confirmed only, from the
   new `ai_evidence` field), their entry routes (CVE or not), the AI attack-tool supply if
   decision 12 adopts it on 12 Nov, and X12's downloadable-model curve. This keeps the
   registered indicators untouched while making the blind spot visible each quarter.
3. **Exposure of AI services** (Trend's Case B targeted exposed AI and GPU services). Needs
   internet-scan data; considered again if Censys grants access.

## Proposed for the 21 Dec freeze session

- Item 16 (permissions): record that without Shadowserver I1 is hand-read or "not available",
  I4 uses its registered KEV version, and I6 is "not available"; substitutes appear only as
  exploratory, beside the registered measure.
- Item 24 (new): the "AI in attacks" context panel, reported beside I8, never labeled.
- Exploratory companions: an X14-based age mix beside I4; agreement among KEV, EUVD and the X19
  national alerts beside I6.

## Author's decisions (29 Oct 2026)

- **No substitutes** inside the registered indicators (freeze item 16): without Shadowserver,
  I1 hand-read or "not available", I4 its KEV version, I6 "not available".
- **Companions adopted** as exploratory: X23 (SANS ISC age mix, beside I4) and X24 (agreement
  among CISA KEV, EUVD and the X19 national alerts, beside I6).
- **The registered plan is evaluated after the pilot** for justified changes: Claude's draft
  10 Feb 2027, author's review 17 Feb, changes only at the 15 Mar annual review.
- **The "AI in attacks" panel (item 24):** the author asked for more context before deciding.

