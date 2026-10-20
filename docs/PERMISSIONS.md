# Data permissions log

Requests to data providers to confirm that this free, non-commercial project may publish
derived results from their data. Any source that declines is dropped and the change is
logged in `prereg/DEVIATIONS.md`. Replies must arrive before the pilot evaluation
(1 January 2027).

| Source | Asked | Channel | Reference | What was asked | Status | Reply |
|---|---|---|---|---|---|---|
| ransomware.live | 2026-10-20 | Support form ("Other") | Ticket #3425 | Aggregate posting counts only, credited; victim names dropped at capture; no raw data published | Awaiting reply | — |
| VulnCheck KEV (community) | 2026-10-20 | Email to community@vulncheck.com | — | Derived statistics only (agreement scores, median lags), labeled "VulnCheck KEV"; entries not republished | Awaiting reply | — |
| Shadowserver | — | Web contact form ("Dashboard Data/Visualization") | — | Aggregate figures and charts from public dashboard series, credited; no host-level data | Not yet sent | — |

## Terms already accepted

- **ransomware.live Fair Usage Policy** (accepted 2026-10-20 when generating the PRO API
  key): no excessive polling; no relaying third-party queries; no re-serving data as an
  API or feed; one account and key; **no publishing of raw data in any form**; no
  website that mimics ransomware.live. The collector therefore keeps only aggregate
  counts in any saved or published output, including GitHub Actions artifacts.
