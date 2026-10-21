# Data permissions log

Requests to data providers to confirm that this free, non-commercial project may publish
derived results from their data. Any source that declines is dropped and the change is
logged in `prereg/DEVIATIONS.md`. Replies must arrive before the pilot evaluation
(1 January 2027).

| Source | Asked | Channel | Reference | What was asked | Status | Reply |
|---|---|---|---|---|---|---|
| ransomware.live | 2026-10-20 | Support form ("Other") | Ticket #3425 | Aggregate posting counts only, credited; victim names dropped at capture; no raw data published | Awaiting reply | — |
| VulnCheck KEV (community) | 2026-10-20 | Email to community@vulncheck.com | — | Derived statistics only (agreement scores, median lags), labeled "VulnCheck KEV"; entries not republished | Awaiting reply | — |
| Shadowserver | 2026-10-20 | Web contact form ("Dashboard Data/Visualization") | Ticket pqaytmyy | Aggregate figures and charts from public dashboard series, credited; no host-level data; asked about export/API for researchers | Awaiting reply (auto-acknowledged; volunteer team, may be slow). Follow up by reply to contact@shadowserver.org with "[Ticket #pqaytmyy]" in the subject if no answer by 20 Nov 2026 | — |

## Terms already accepted

- **ransomware.live Fair Usage Policy** (accepted 2026-10-20 when generating the PRO API
  key): no excessive polling; no relaying third-party queries; no re-serving data as an
  API or feed; one account and key; **no publishing of raw data in any form**; no
  website that mimics ransomware.live. The collector therefore keeps only aggregate
  counts in any saved or published output, including GitHub Actions artifacts.
- **VulnCheck Service Terms** (revised 6 July 2026; accepted 2026-10-20 on community
  sign-up). Relevant points: free offerings require a prominent attribution notice on
  any output that uses the data; free-tier data may not be used to train or fine-tune AI
  models; VulnCheck may name the user as a customer in marketing; and Section 6 says
  "Customer may not make the Services Data available for free or under an open source
  or similar license" and bars derivative works. Whether derived statistics (agreement
  scores, median lags) count as Services Data is unclear, so **nothing derived from
  VulnCheck is published until VulnCheck confirms in writing**. Until then VulnCheck KEV
  and XDB are used privately only; published T1/T3 dates and the I6 agreement check use
  CISA KEV and Shadowserver. If VulnCheck declines, the change is logged in
  `prereg/DEVIATIONS.md`.

## Keys saved as GitHub repository secrets

`RANSOMWARE_LIVE_KEY`, `NVD_API_KEY`, `VULNCHECK_TOKEN`, `CLOUDFLARE_TOKEN` (all added
2026-10-20). `SEC_USER_AGENT` (the SEC requires a User-Agent with the requester's name and
contact email, e.g. "Name name@example.com"; it is sent only to sec.gov). The Cloudflare token is limited to Account → Radar → Read, with no IP filter
and no expiry.
