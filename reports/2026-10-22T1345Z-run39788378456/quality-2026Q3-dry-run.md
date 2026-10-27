# Data quality: 2026Q3 (dry-run)

## 1. Sources

| Source | Status | Note |
|---|---|---|
| cisa_kev | ok |  |
| cisa_kev | ok | 1754 entries |
| cve_org | ok | 413101 records; raw JSON pinned by commit, not copied |
| nvd | ok | 37369 CVEs published 2026-07-01..2026-09-30; key=yes |
| epss | ok | 113 days 2026-07-01..2026-10-21, step 1d; CVE IDs from 2025 on; 0 day(s) missing |
| sec_edgar | ok | 11 filings |
| sec_edgar | ok | 8029 registrants |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| cloudflare_radar | ok |  |
| ransomware_live | ok | aggregate counts only, no victim names; monthly totals withheld until ransomware.live permits publication (scrubbed 27 Oct 2026): 17 hits, 17 read, forms {'8-K': 13, '8-K/A': 4}, with Item 1.05: 11
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

No previous run to compare with; field checks only.

- No drift flagged.
