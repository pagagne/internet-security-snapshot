# Data permissions log

Requests to data providers to confirm that this free, non-commercial project may publish
derived results from their data. Any source that declines is dropped and the change is
logged in `prereg/DEVIATIONS.md`. A source without a written yes by the 21 December 2026 decision session runs
without it for the Q4 2026 pilot (decision item 16); a later yes is switched on at the next quarter's run.

The switches are in `config/sources.yaml` (permission, collect, publish per source). When a
status below changes, change the matching switch in the same commit; a test checks the two agree.

| Source | Asked | Channel | Reference | What was asked | Status | Reply |
|---|---|---|---|---|---|---|
| ransomware.live | 2026-10-20 | Support form ("Other") | Ticket #3425 | Aggregate posting counts only, credited; victim names dropped at capture; no raw data published | Awaiting reply | — |
| VulnCheck KEV (community) | 2026-10-20 | Email to community@vulncheck.com | — | Derived statistics only (agreement scores, median lags), labeled "VulnCheck KEV"; entries not republished | Awaiting reply | — |
| Shadowserver | 2026-10-20 | Web contact form ("Dashboard Data/Visualization") | Ticket pqaytmyy | Aggregate figures and charts from public dashboard series, credited; no host-level data; asked about export/API for researchers | Awaiting reply (auto-acknowledged; volunteer team, may be slow). Follow up by reply to contact@shadowserver.org with "[Ticket #pqaytmyy]" in the subject if no answer by 20 Nov 2026 | — |

## Request texts as sent (20 Oct 2026)
Kept so follow-ups can quote them exactly. Copied 26 Oct from the author's sent mail and the
ransomware.live ticket page; contact details removed.

**VulnCheck** (email to community@vulncheck.com, 20 Oct 2026 18:12 UTC; subject "Derived
statistics from VulnCheck KEV in a non-commercial research project"; no reply as of 26 Oct):

> Hello,
>
> I'm setting up a free, non-commercial, pre-registered research project that tracks how
> quickly vulnerabilities are exploited compared with how quickly they are patched:
> https://github.com/pagagne/internet-security-snapshot.
>
> I plan to use VulnCheck KEV through a community account. I'd publish only derived
> statistics: agreement scores between VulnCheck KEV, CISA KEV, and Shadowserver, and median
> reporting lags. I'd label every chart and table "VulnCheck KEV," as your attribution notice
> requires. I would not republish the entries themselves.
>
> Could you confirm that publishing these derived statistics is fine under the community
> terms? If you need anything else from me, please let me know.
>
> Thank you,
>
> Paul A. Gagne

**ransomware.live** (support ticket #3425, category Other, 20 Oct 2026 18:29; title
"Permission for non-commercial research use of aggregate counts"; still open with no reply as
of 26 Oct, although the confirmation promised one within 2 business days):

> Hello,
>
> I run a free, non-commercial research project that tracks visible ransomware harm each
> quarter: https://github.com/pagagne/internet-security-snapshot. The research plan is
> pre-registered on OSF.
>
> I've registered for a free PRO API key and would like to use it to collect posting counts
> by date, group, sector and country, once per quarter. I would publish only aggregate counts,
> credited to ransomware.live, and drop victim names when collecting so they are never stored
> or published.
>
> Could you confirm this use is acceptable under your terms for a non-commercial research
> project?
>
> Thank you,

**Shadowserver** (web contact form, topic "Dashboard Data/Visualization", ticket pqaytmyy):
text not kept; no copy in the author's mail. What was asked is in the table above.

## Requests planned (25 Oct 2026 brainstorm)

| Source | When | Channel | What will be asked | Status |
|---|---|---|---|---|
| Censys research access | 28 Oct 2026 | Censys research-access request (written by the author, no AI tools, as Censys requires) | Free research access (BigQuery, delayed data) for published, non-commercial results that cite Censys | To send |
| GreyNoise research (VIP) access | 27 Oct 2026 | GreyNoise research programme form | Research access for an open, published study; aggregates only | To send |
| CrowdSec CVE tracker | 27 Oct 2026 | Email to the CrowdSec team | Whether research use and publishing aggregate figures are allowed, and an API key | To send |

## Free sources used without a request (terms read 25 Oct 2026)

| Source | Terms that matter | How the project complies |
|---|---|---|
| SANS Internet Storm Center web-honeypot files | Attribution required ("SANS Technology Institute, Internet Storm Center, https://isc.sans.edu"); no reselling; the site carries a non-commercial licence; at most one download an hour | One download a month; aggregates only (no URLs, no IP addresses); credited on every output |
| ENISA EU Vulnerability Database | Public EU service | Dropped 25 Oct: its exploited list mirrors KEV |
| Google Project Zero "0day In the Wild" sheet | Public community resource | Zero-day check (X15); cited |
| deps.dev | Generated data under CC-BY 4.0 | Aggregates; credited |
| OSV and GitHub advisories | Public; OSV data CC-BY 4.0 | Version lists only; credited |
| WordPress.org plugin statistics | Public API | Version shares only |
| inthewild.io | Apache 2.0 | Dropped 25 Oct: no exploitation reports after Dec 2024 |

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
