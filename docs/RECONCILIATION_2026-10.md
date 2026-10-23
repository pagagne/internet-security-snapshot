# Reconciliation with the October 2026 assessment "Is AI Cleaning Up the Internet?"

The one-off assessment (another Claude session, around 19 Oct 2026; its own document and
`ai_cleanup_assessment.zip` bundle) and this project ask the same question. The assessment is
a single snapshot with forecasts; the Snapshot repeats a narrower, pre-registered measurement
every quarter. This file records where they agree, where they differ, and what the Snapshot
takes from it. Compared 2026-10-23 from the assessment's summary as pasted by the author.

## Findings compared

| Topic | Assessment | Snapshot data (Q2-Q3 2026 test runs) | Verdict |
|---|---|---|---|
| Speed of attack | Not accelerating since 2023; about half of newly exploited flaws listed within a week; median 3-4 days | Recent CVEs only: median 5 days (Q3), 8 (Q2); 53% within 7 days (Q3). Counting older CVEs first exploited in the quarter: at least 8 and 15 days | Agree for recent CVEs. The Snapshot's corrected figure (all newly exploited flaws) is slower; say which population a number describes |
| Volume of flaws | NVD published 3.1 times as many CVEs in Q3 2026 as a year earlier | CVE.org records published: 36,732 in Q3 2026 vs 10,659 in Q3 2025 (3.4 times; this extract holds 2025-26 IDs only, which slightly understates 2025) | Agree: discovery volume roughly tripled. Snapshot T5 reports it with CVE.org, rejected records excluded |
| Harm | Ransomware leak-site victims +75% year on year (Q3 2026); IC3 losses +26% (2025) | ransomware.live Q3 2026: 962 / 1,059 / 831 posts (Jul / Aug / Sep); year-earlier months not yet pulled | Not comparable yet. The baseline backfill gives the year-on-year figure; publication waits for ransomware.live's permission |
| Patch speed | Not measured (Shadowserver, Censys/Shodan blocked); BOD 26-04 test shows only that deadlines changed (cut began March, three months before the directive) | Not measured either: T1(b)/T2 wait for Shadowserver; Censys application Feb 2027 | Same gap, same fix (Plan 1). Shadowserver's per-country exposure series named most valuable by both |
| Data access | EPSS, OSV, Shadowserver, Censys/Shodan, Cloudflare Radar, EDGAR full-text blocked from the workspace | EPSS, Cloudflare Radar (token) and EDGAR (searched per form) collected in GitHub Actions | Snapshot closes three of the six gaps; OSV is new to the Snapshot (below) |
| AI's share | AI mostly flooded the supply of known bugs; forecast cleanup 5% by 2028, 15% by 2031 | T7 reports the AI-credited share as a low/hand/high range; no forecasts | Consistent in spirit. The Snapshot does not forecast; its yearly trend can test the assessment's view over 2027 |

## What the Snapshot takes from the assessment (added to `docs/RESEARCH_PLAN.md`)
1. **OSV as a fix-date source** for open-source flaws (fixed versions and dates), alongside GitHub advisories.
2. **Policy deadlines as exploratory context:** CISA BOD 26-04 and CERT-In CISG-2026-02 dates logged in the exploratory layer, so a change in patch or attack timing can be read against them. Not a scored measure.
3. **State which population every timing figure covers** (recent CVEs vs all newly exploited flaws), since the two give different medians.
4. **The assessment's thresholds as a reference point:** its five "cleanup" tests map onto Snapshot questions (speed: T3, T1; volume: T5; harm: T6; patch speed: T1b, T2; AI share: T7, X3). The Snapshot's year-end 2027 summary can report how each moved, without adopting the assessment's thresholds as labels.

## Not taken
- Forecast probabilities and the competing-hypotheses matrix: outside a measurement study.
- Secondary-source figures the assessment graded down (IC3, Cloudflare summary, 8-K tracker): the Snapshot uses primary data only.
