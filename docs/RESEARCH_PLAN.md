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
- Other exposure options: terms of free tiers (GreyNoise, Shodan) for research use; Censys
  application stays 15 Feb.
- Fallback wording for core-v1.2: T1b and T2 "not measured" with the reason; T1(a) under
  option (a) becomes the headline race measure.

## Author's time in this window
Review on 12 Nov (20-30 min). Claude starts any GitHub runs.
