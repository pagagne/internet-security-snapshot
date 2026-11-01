# Data quality: 2026Q3 (dry-run)

## 1. Sources

| Source | Status | Note |
|---|---|---|
| cisa_kev | ok |  |
| cisa_kev | ok | 1766 entries |
| cve_org | ok | 417673 records; raw JSON pinned by commit, not copied |
| nvd | ok | 37369 CVEs published 2026-07-01..2026-09-30; key=yes |
| epss | ok | 123 days 2026-07-01..2026-10-31, step 1d; CVE IDs from 2025 on; 0 day(s) missing |
| sec_edgar | ok | 11 filings |
| sec_edgar | ok | 8017 registrants |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| ransomware_live | ok | aggregate counts only, no victim names; 539 rows |

Server pushback: none (no 429 or 403 replies from any source).

## 2. CVE records published in the quarter

- Published: **36,951**; rejected in the same window: 131
- With a CVSS score in the CVE record: 93.4%
- With a CWE (weakness) ID: 88.5%; root cause 'other_unknown': 38.7%
- With vendor/product names: 97.2%
- With CISA Vulnrichment (ADP): 90.3%
- CISA exploitation status: none 26,760, poc 6,550, none recorded 3,566, active 75
- Days from publication to CISA scoring: median 0.7, 90th percentile 4.2

## 2b. Published-count cross-check (I5)

CVE records published in this quarter and the same quarter of earlier years: our count from the CVE List against NVD's own count for the same dates (rejected records excluded). A difference over 5% is flagged; dates can differ by a day between the two.

| Year | Our count | NVD count | Difference |
|---|---|---|---|
| 2023 | 6,921 | 6,930 | -0.1% |
| 2024 | 8,522 | 8,523 | -0.0% |
| 2025 | 11,722 | 11,725 | -0.0% |
| 2026 | 36,951 | 36,959 | -0.0% |

- Counts agree within tolerance.

## 3. NVD compared with CVE.org

- NVD CVEs published in the window: 37,369; in both: 36,828; CVE.org only: 123; NVD only: 541
- NVD status: Deferred 14,751, Analyzed 13,096, Awaiting Analysis 3,910, Received 3,737, Modified 1,090, Rejected 530, Undergoing Analysis 255
- Share analyzed by NVD, by publication month: 2026-07 49%, 2026-08 30%, 2026-09 30%
- CVE record has no CVSS but NVD does: 380 (NVD could fill these)
- Both scored: 34,253; differ by 1.0 or more: 8.3%; cross the 8.0 line differently: 572
- No product names in CVE record but NVD has CPE products: 59

## 4. CISA KEV dates across sources

- KEV entries: 1,766
- In KEV and NVD with a KEV date: 74; same date: 100.0%
- Quarter CVEs in KEV: 75; marked 'active' by CISA Vulnrichment: 75; in both: 75

## 5. Cohort pools (eligible CVEs per month)

Slot c still needs the internet-facing hand check, slot d the AI-credit check.

| Month | a edge | b web/collab | c other | d AI candidates |
|---|---|---|---|---|
| 2026-07 | 20 | 42 | 2,480 | 7 |
| 2026-08 | 19 | 80 | 3,512 | 41 |
| 2026-09 | 58 | 87 | 3,583 | 33 |

- Eligible CVEs without product names (fall to slot c by default): 266 of 9,881

## 5b. X5 (exploratory): flaws in AI software

- Eligible CVEs affecting AI software: 162 of 9,881 (1.6%)
- Quarter CVEs in KEV affecting AI software: 3 of 75

## 6. AI-credit review load

- Candidates: 297 (0.8% of CVEs); distinct credit texts to review: 90
- Matched only on a lab name (stricter review): 102
- AI-looking credits matching no term (watchlist scan): 132

## 7. EPSS

- Days captured: 123; rows: 11,759,037; file size: 79.8 MB
- Quarter CVEs with a score on the last day: 99.4%

## 8. Ransomware leak-site counts (aggregates)

_Source: ransomware.live (https://www.ransomware.live), used with permission; aggregate counts only._

- 2026-07: 952 postings, 62 groups; unknown country 4.0%, unknown sector 5.6%
- 2026-08: 1,143 postings, 85 groups; unknown country 8.2%, unknown sector 9.5%
- 2026-09: 846 postings, 78 groups; unknown country 10.2%, unknown sector 10.9%

## 9. SEC 8-K Item 1.05

- 11 filings (7 original 8-Ks) against 8,017 registrants: 0.873 per 1,000
- Search "Item 1.05" [8-K]: 17 hits, 17 read, forms {'8-K': 13, '8-K/A': 4}, with Item 1.05: 11
- Search "Item 1.05" [8-K/A]: 4 hits, 4 read, forms {'8-K/A': 4}, with Item 1.05: 4
- Search "Material Cybersecurity Incidents" [8-K]: 11 hits, 11 read, forms {'8-K/A': 4, '8-K': 7}, with Item 1.05: 10
- Search "Material Cybersecurity Incidents" [8-K/A]: 4 hits, 4 read, forms {'8-K/A': 4}, with Item 1.05: 4

## 10. Cloudflare Radar

- ai_bots_by_user_agent_timeseries: ok
- attacks_layer3_timeseries: ok
- attacks_layer7_by_vertical: ok
- attacks_layer7_timeseries: ok
- http_bot_class_timeseries: ok

## 11. Drift checks

Compared with the previous run (2026Q3 final).

- No drift flagged.
