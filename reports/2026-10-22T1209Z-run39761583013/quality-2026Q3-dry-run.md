# Data quality: 2026Q3 (dry-run)

## 1. Sources

| Source | Status | Note |
|---|---|---|
| cisa_kev | ok |  |
| cisa_kev | ok | 1754 entries |
| cve_org | ok | 413044 records; raw JSON pinned by commit, not copied |
| nvd | ok | 37369 CVEs published 2026-07-01..2026-09-30; key=yes |
| epss | ok | 113 days 2026-07-01..2026-10-21, step 1d; CVE IDs from 2025 on; 0 day(s) missing |
| sec_edgar | ok | 4 filings |
| sec_edgar | ok | 8029 registrants |
| radar | gap | RuntimeError: Cloudflare Radar rejected CLOUDFLARE_TOKEN: line 1 (length 64): HTTP 400 ['9106:Authentication failed (status: 400)']; line 2  |
| ransomware_live | ok | aggregate counts only, no victim names; monthly totals withheld (scrubbed 27 Oct 2026) |

## 2. CVE records published in the quarter

- Published: **36,953**; rejected in the same window: 129
- With a CVSS score in the CVE record: 93.4%
- With a CWE (weakness) ID: 88.5%; root cause 'other_unknown': 38.7%
- With vendor/product names: 97.2%
- With CISA Vulnrichment (ADP): 90.3%
- CISA exploitation status: none 26,765, poc 6,549, none recorded 3,566, active 73
- Days from publication to CISA scoring: median 0.7, 90th percentile 4.2

## 3. NVD compared with CVE.org

- NVD CVEs published in the window: 37,369; in both: 36,830; CVE.org only: 123; NVD only: 539
- NVD status: Deferred 14,753, Analyzed 12,919, Awaiting Analysis 3,938, Received 3,737, Modified 1,060, Rejected 528, Undergoing Analysis 434
- Share analyzed by NVD, by publication month: 2026-07 48%, 2026-08 30%, 2026-09 30%
- CVE record has no CVSS but NVD does: 303 (NVD could fill these)
- Both scored: 34,255; differ by 1.0 or more: 8.3%; cross the 8.0 line differently: 571
- No product names in CVE record but NVD has CPE products: 58

## 4. CISA KEV dates across sources

- KEV entries: 1,754
- In KEV and NVD with a KEV date: 72; same date: 100.0%
- Quarter CVEs in KEV: 73; marked 'active' by CISA Vulnrichment: 73; in both: 73

## 5. Cohort pools (eligible CVEs per month)

Slot c still needs the internet-facing hand check, slot d the AI-credit check.

| Month | a edge | b web/collab | c other | d AI candidates |
|---|---|---|---|---|
| 2026-07 | 20 | 42 | 2,480 | 7 |
| 2026-08 | 19 | 80 | 3,513 | 41 |
| 2026-09 | 58 | 86 | 3,584 | 33 |

- Eligible CVEs without product names (fall to slot c by default): 266 of 9,882

## 6. AI-credit review load

- Candidates: 297 (0.8% of CVEs); distinct credit texts to review: 90
- Matched only on a lab name (stricter review): 102
- AI-looking credits matching no term (watchlist scan): 132

## 7. EPSS

- Days captured: 113; rows: 10,524,936; file size: 71.2 MB
- Quarter CVEs with a score on the last day: 99.4%

## 8. Ransomware leak-site counts (aggregates)

- Figures withheld until ransomware.live permits publication (scrubbed 27 Oct 2026).

## 9. SEC 8-K Item 1.05

- 4 filings (0 original 8-Ks) against 8,029 registrants: 0.0 per 1,000
