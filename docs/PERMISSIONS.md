# Data permissions log

Requests to data providers to confirm that this free, non-commercial project may publish
derived results from their data. Any source that declines is dropped and the change is
logged in `prereg/DEVIATIONS.md`. A source without a written yes by the 21 December 2026 decision session runs
without it for the Q4 2026 pilot (decision item 16); a later yes is switched on at the next quarter's run.

The switches are in `config/sources.yaml` (permission, collect, publish per source). When a
status below changes, change the matching switch in the same commit; a test checks the two agree.

| Source | Asked | Channel | Reference | What was asked | Status | Reply |
|---|---|---|---|---|---|---|
| ransomware.live | 2026-10-20 | Support form ("Other") | Ticket #3425 | Aggregate posting counts only, credited; victim names dropped at capture; no raw data published | **Granted** 2026-10-27 (Julien, 06:16 UTC) on seven conditions, below; publishing switched on the same day (author) | Conditions accepted in the author's reply of 2026-10-28 (12:32 UTC); full thread in the private correspondence record |
| VulnCheck KEV (community) | 2026-10-20 | Email to community@vulncheck.com | — | Derived statistics only (agreement scores, median lags), labeled "VulnCheck KEV"; entries not republished | Awaiting reply | — |
| Shadowserver | 2026-10-20 | Web contact form ("Dashboard Data/Visualization") | Ticket pqaytmyy | Aggregate figures and charts from public dashboard series, credited; no host-level data; asked about export/API for researchers | Awaiting reply (auto-acknowledged; volunteer team, may be slow). Follow up by reply to contact@shadowserver.org with "[Ticket #pqaytmyy]" in the subject if no answer by 20 Nov 2026 | — |

## ransomware.live conditions (ticket #3425, 27 Oct 2026)
Authorized for this non-commercial research use on these conditions, which the study meets:
1. **Access** only through the dedicated api-pro endpoint with a personal token (free). The
   collector has no fallback to any other endpoint and records a gap without the token.
2. **Fair usage:** no excessive polling or abusive request volumes. Three requests a pull, 5 s
   apart; the study's own rule of no more than one call every 30 minutes; server pushback logged.
3. **Attribution:** ransomware.live named as the source on any page, dashboard, interface,
   report, publication or deliverable using its data (quality report, README, evaluation page,
   status page, Zenodo archive).
4. **No SLA or warranty;** data to be independently verified before critical decisions.
5. **No continuity guarantee:** the service may change or stop without notice (a gap is
   recorded; Plan 2 covers running without it).
6. **No publishing of raw data** in any form (API, file or otherwise): only counts by month,
   group, country and sector are kept; victim records never reach disk.
7. **No cloning** of the ransomware.live website's look, layout or branding.

## Exposure note (27 Oct 2026)
Found in the public/private review of 27 Oct: before ransomware.live had replied, three monthly
aggregate totals from the 22 Oct test run (postings for Jul-Sep 2026, no victim names) were
written into the public run report on the `run-reports` branch, the public run download and the
public data-quality notice. Fixed the same day: the manifest note carries no figures, the
quality report withholds them, and non-publishable sources are moved out of every public output
and kept only in the author's private Drive backup (`snapshot.private`). The figures were also
removed from the current files of the six 22 Oct run reports on `run-reports`; the branch
history was left as it is (author's decision); this note records it. A privacy scan now checks
`main` and `run-reports` every day. Later the same day it emerged that ransomware.live's written
yes had arrived at 06:16 UTC, before the clean-up, so the figures were in fact permitted; the
clean-up stands as the template for sources still awaiting permission.

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

**Points for the 20 Nov Shadowserver follow-up** (reply to contact@shadowserver.org with
"[Ticket #pqaytmyy]" in the subject; Claude drafts, the author sends):
- Recap: free, non-commercial, pre-registered study (OSF DOI 10.17605/OSF.IO/3XT82); aggregate
  country- and CVE-level figures only, credited; no host-level data, nothing resold.
- The specific ask: may the study download the public dashboard series for a short list of
  named CVEs (about 12-100 a quarter) once a quarter, by a script or an API key, and publish
  derived figures (exposure half-life, share still exposed) with credit?
- The fallback, stated openly: if automated access isn't possible, the study would read those
  few series by hand from the public dashboard each quarter and cite them; does that fit the
  dashboard's terms?
- Attribution: ask for their preferred credit wording.
- Timing: decisions are fixed on 21 Dec 2026; a later yes is switched on the next quarter.

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

## Terms read for the global sources (28 Oct 2026)
- **CERT-FR (ANSSI):** site content under the Licence ouverte / open licence (Etalab), unless
  stated otherwise; commercial exploitation needs ANSSI's prior leave; no framing of pages; no
  logos (cyber.gouv.fr legal notice). The study uses alert titles, CVE IDs and dates, credited.
- **JPCERT/CC, APNIC Labs, RIPEstat, UK ICO, OAIC, ENISA:** terms still to read (by 11 Nov).
- **PDPC (Singapore):** its site answered the workflow with a bot check (HTTP 202, empty page);
  not to be worked around.

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
