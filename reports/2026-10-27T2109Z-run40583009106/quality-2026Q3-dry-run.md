# Data quality: 2026Q3 (dry-run)

## 1. Sources

| Source | Status | Note |
|---|---|---|
| cisa_kev | ok |  |
| cisa_kev | ok | 1760 entries |
| cve_org | ok | 415387 records; raw JSON pinned by commit, not copied |
| nvd | ok | 37369 CVEs published 2026-07-01..2026-09-30; key=yes |
| epss | ok | 118 days 2026-07-01..2026-10-26, step 1d; CVE IDs from 2025 on; 0 day(s) missing |
| sec_edgar | ok | 11 filings |
| sec_edgar | ok | 8024 registrants |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| ransomware_live | ok | aggregate counts only, no victim names; 539 rows |

## 2. CVE records published in the quarter

- Published: **36,952**; rejected in the same window: 130
- With a CVSS score in the CVE record: 93.4%
- With a CWE (weakness) ID: 88.5%; root cause 'other_unknown': 38.7%
- With vendor/product names: 97.2%
- With CISA Vulnrichment (ADP): 90.3%
- CISA exploitation status: none 26,763, poc 6,549, none recorded 3,566, active 74
- Days from publication to CISA scoring: median 0.7, 90th percentile 4.2

## 3. NVD compared with CVE.org

- NVD CVEs published in the window: 37,369; in both: 36,829; CVE.org only: 123; NVD only: 540
- NVD status: Deferred 14,752, Analyzed 13,033, Awaiting Analysis 3,944, Received 3,737, Modified 1,063, Rejected 529, Undergoing Analysis 311
- Share analyzed by NVD, by publication month: 2026-07 48%, 2026-08 30%, 2026-09 30%
- CVE record has no CVSS but NVD does: 330 (NVD could fill these)
- Both scored: 34,254; differ by 1.0 or more: 8.3%; cross the 8.0 line differently: 571
- No product names in CVE record but NVD has CPE products: 58

## 4. CISA KEV dates across sources

- KEV entries: 1,760
- In KEV and NVD with a KEV date: 72; same date: 100.0%
- Quarter CVEs in KEV: 74; marked 'active' by CISA Vulnrichment: 74; in both: 74

## 5. Cohort pools (eligible CVEs per month)

Slot c still needs the internet-facing hand check, slot d the AI-credit check.

| Month | a edge | b web/collab | c other | d AI candidates |
|---|---|---|---|---|
| 2026-07 | 20 | 42 | 2,480 | 7 |
| 2026-08 | 19 | 80 | 3,512 | 41 |
| 2026-09 | 58 | 87 | 3,584 | 33 |

- Eligible CVEs without product names (fall to slot c by default): 266 of 9,882

## 5b. X5 (exploratory): flaws in AI software

- Eligible CVEs affecting AI software: 162 of 9,882 (1.6%)
- Quarter CVEs in KEV affecting AI software: 3 of 74

## 6. AI-credit review load

- Candidates: 297 (0.8% of CVEs); distinct credit texts to review: 90
- Matched only on a lab name (stricter review): 102
- AI-looking credits matching no term (watchlist scan): 132

## 7. EPSS

- Days captured: 118; rows: 11,135,867; file size: 75.1 MB
- Quarter CVEs with a score on the last day: 99.4%

## 9. SEC 8-K Item 1.05

- 11 filings (7 original 8-Ks) against 8,024 registrants: 0.872 per 1,000
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

Compared with the previous run (2026Q3 dry-run).

- No drift flagged.
