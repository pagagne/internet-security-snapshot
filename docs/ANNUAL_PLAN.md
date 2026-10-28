# Annual plan: every action item, by who does it

Generated from `docs/schedule/schedule.yaml` by `python -m snapshot.schedule build`; do not edit by hand.
The same items are in the calendar feeds `docs/schedule/snapshot.ics` (everything) and
`docs/schedule/reviewer.ics` (the external reviewer's items), and each author or Claude item
opens a GitHub issue when it falls due (label `schedule`, plus `owner:author` or `owner:claude`).

## Every quarter and every month

| Who | What | When |
|---|---|---|
| Author | Approve the provisional draft | day 2, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 10:00 ET |
| Author | Quarterly hand-check window | day 4, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 (25 days) |
| Author | Hand-check answers due by the 28th | day 25, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 10:00 ET |
| Author | Confirm whether scan data was obtained for the annual check | day 31, Jan, 2028-01 to 2030-01 |
| Author | Final-run check and approve the final results | day 2, Feb, May, Aug, Nov, 2027-02 to 2028-02, 10:00 ET |
| Author | Annual review and change window | day 15, Mar, 2027-03 to 2030-03, 11:00 ET |
| External reviewer | Second coder - 20 blinded items | day 29, Jan, Apr, Jul, Oct, 2027-04 to 2028-01 (14 days) |
| Claude | Draft the provisional evaluation; load the hand-check lists | day 1, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 |
| Claude | Quarterly web sweep for AI-run attack reports (X3) | day 2, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 |
| Claude | Copy the Drive backup's inventory and small private data into the Claude project | day 4, every month, 2026-11 to 2027-12 |
| Claude | Choose this quarter's watch cases by the rule | day 6, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 |
| Claude | Send the second coder this quarter's blinded sample | day 29, Jan, Apr, Jul, Oct, 2027-04 to 2028-01 |
| Claude | Summarize provisional-to-final changes; prepare the release | day 1, Feb, May, Aug, Nov, 2027-02 to 2028-02 |
| Claude | Score the second coder's answer file; publish agreement | day 13, Feb, May, Aug, Nov, 2027-05 to 2028-02 |
| Claude | Draft the annual check against reference data (previous year) | day 1, Mar, 2029-03 to 2030-03 |
| Claude | Sync review before the provisional report (three passes; findings to the author) | day 28, Mar, Jun, Sep, Dec, 2026-12 to 2027-12 |
| GitHub (automatic) | Quarterly pull, provisional run | day 1, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 06:00 UTC |
| GitHub (automatic) | Rebuild check of the latest frozen bundle | day 10, every month, 2026-11 to 2028-04, 07:17 UTC |
| GitHub (automatic) | Quarterly pull, final run | day 1, Feb, May, Aug, Nov, 2027-02 to 2028-02, 06:00 UTC |

## Calendar: every dated item in order

The same list as the calendar feeds, one row per occurrence (repeating items included).

| When | Who is responsible | What |
|---|---|---|
| Sun 25 Oct 2026 | Claude | Patch-adoption prototype from deps.dev (open-source flaws) - snapshot run |
| Sun 25 Oct 2026 | Claude | Monthly honeypot capture (SANS ISC), aggregates only - built |
| Sun 25 Oct 2026 | Claude | Linux kernel fix dates - probe run |
| Sun 25 Oct 2026 | Claude | Back-test KEV's lag against EUVD, Project Zero's sheet and inthewild.io - first run |
| Sun 25 Oct 2026 | Claude | Sync review (three passes; findings to the author) |
| Mon 26 Oct 2026 | Claude | Draft the CCRI outreach email and the second-coder role summary - done |
| Mon 26 Oct 2026 | Claude | Continue the research window |
| Tue 27 Oct 2026 | Claude | Probe the global sources (X19-X22) and translate the sweep searches |
| Tue 27 Oct 2026, 10:00 ET | Paul | Send the GreyNoise research request and the CrowdSec question |
| Wed 28 Oct 2026, 10:00 ET | Paul | Call the UGA Career Center about the reviewer posting - done |
| Wed 28 Oct 2026, 14:00 ET | Paul | Write and send the Censys research-access application - sent 28 Oct |
| Thu 29 Oct 2026, 10:00 ET | Paul | Set up BigQuery in the Google Cloud project (HTTP Archive, deps.dev history); turn on Dependabot alerts |
| Mon 02 Nov 2026 | Claude | HHS OCR health-breach series - second attempt at the export |
| Mon 02 Nov 2026 | Claude | HTTP Archive test - are software versions recorded? (after the BigQuery project) |
| Mon 02 Nov 2026 | Claude | Add kernel commit dates (and more CSAF vendors) to the fix-date pre-fill |
| Mon 02 Nov 2026 | Claude | Sync review (three passes; findings to the author) |
| Wed 04 Nov 2026 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Thu 05 Nov 2026 | Claude | Recheck the trial AI-attack sweep's open items |
| Fri 06 Nov 2026 | Paul | Create the project email address |
| Mon 09 Nov 2026 | Claude | Sync review (three passes; findings to the author) |
| Mon 09 Nov 2026, 10:00 ET | Paul | Email CCRI's cybersecurity program director (alumni route, second coder) |
| Mon 09 Nov 2026, 11:00 ET | Paul | Check the 15 AI-attack entries from the trial sweep |
| Tue 10 Nov 2026, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 10 Nov 2026, 10:00 ET | Paul | Email SANS asking them to suggest a reviewer (former-employer route) |
| Wed 11 Nov 2026 | Claude | Restore test of the Drive backup |
| Wed 11 Nov 2026 | Claude | Fill in the 12 Nov decision sheet with the probe and trial results |
| Thu 12 Nov 2026, 10:00 ET | Paul | Research review - exceptions only (8 of 11 approved conditionally on 27 Oct; 1, 2, 9 decided) |
| Mon 16 Nov 2026 | Claude | Sync review (three passes; findings to the author) |
| Mon 16 Nov 2026, 10:00 ET | Paul | Validation fix dates, then spot-check references |
| Tue 17 Nov 2026 | Claude | Run the validation and report pass/fail |
| Wed 18 Nov 2026 | Paul | Ask Georgia State Career Services about the reviewer posting |
| Fri 20 Nov 2026 | Claude | Draft the permission follow-ups and update the log |
| Fri 20 Nov 2026, 09:00 ET | Paul | Data-permission follow-ups |
| Mon 23 Nov 2026 | Claude | Sync review (three passes; findings to the author) |
| Mon 23 Nov 2026, 10:00 ET | Paul | Baseline-year hand check, part 1 of 2 |
| Tue 24 Nov 2026, 10:00 ET | Paul | Baseline-year hand check, part 2 of 2 |
| Wed 25 Nov 2026 | Paul | Ask Georgia Tech College of Computing about a research internship posting |
| Wed 25 Nov 2026 | Claude | Race fix-date list ready in the Hand Check app |
| Fri 27 Nov 2026 | Claude | Build the project website and its publishing workflow (ready for 4 Dec) |
| Mon 30 Nov 2026 | Claude | Cutover check (study no longer depends on one Claude chat) |
| Mon 30 Nov 2026 | Claude | Sync review (three passes; findings to the author) |
| Tue 01 Dec 2026 | Claude | Read the dry-run quality report; prepare the hand-check lists |
| Tue 01 Dec 2026, 11:00 UTC | GitHub | Dry run of the quarterly pull (Oct-Nov data) |
| Wed 02 Dec 2026, 10:00 ET | Paul | Hand check on the dry run |
| Thu 03 Dec 2026, 10:00 ET | Paul | Move the quarterly pull into the container (if the dry run passed) |
| Fri 04 Dec 2026 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Fri 04 Dec 2026, 10:00 ET | Paul | Landing page, Discussions, Zenodo |
| Sat 05 Dec 2026 | Paul | Register on Handshake and connect the approved schools - started early, 28 Oct |
| Thu 10 Dec 2026, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Fri 11 Dec 2026 | Claude | Get every available source ready for the full dry run |
| Mon 14 Dec 2026 | Claude | Document and test every GitHub workflow; draft the lock list |
| Tue 15 Dec 2026 | Claude | Review the full dry run; findings for the 21 Dec session |
| Tue 15 Dec 2026, 11:00 UTC | GitHub | Full dry run with all available sources (1 Oct-14 Dec data) |
| Wed 16 Dec 2026, 10:00 ET | Paul | Hand check on the full dry run; read the findings |
| Fri 18 Dec 2026, 10:00 ET | Paul | Review the workflow page and the lock list |
| Mon 21 Dec 2026, 10:00 ET | Paul | Core-freeze decision session |
| Tue 22 Dec 2026 | Claude | Prepare the core freeze (core-v1.2) |
| Mon 28 Dec 2026 | Claude | Sync review before the provisional report (three passes; findings to the author) |
| Tue 29 Dec 2026, 10:00 ET | Paul | Freeze the core (core-v1.2) and update OSF |
| Fri 01 Jan 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Fri 01 Jan 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sat 02 Jan 2027 | Claude | Quarterly web sweep for AI-run attack reports (X3) |
| Sat 02 Jan 2027, 10:00 ET | Paul | Approve the provisional draft |
| Mon 04 Jan 2027 to 28 Jan | Paul | Quarterly hand-check window |
| Mon 04 Jan 2027 | Paul | Post the reviewer ad; email statistics department coordinators |
| Mon 04 Jan 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Wed 06 Jan 2027 | Claude | Choose this quarter's watch cases by the rule |
| Sun 10 Jan 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 12 Jan 2027, 10:00 ET | Paul | Line up the external reviewer and second coder |
| Wed 20 Jan 2027 | Claude | Build the figure worksheets for the reviewer's spot check |
| Mon 25 Jan 2027 | Claude | Outside AI-found CVE lists against our AI-credit counts, on pilot data |
| Mon 25 Jan 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Mon 01 Feb 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Mon 01 Feb 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Tue 02 Feb 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Wed 03 Feb 2027 | Claude | Prepare the 8 Feb session |
| Wed 03 Feb 2027 | Claude | Compare the pilot with what we expected (docs/PILOT_EXPECTATIONS.md) |
| Thu 04 Feb 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Mon 08 Feb 2027, 10:00 ET | Paul | Evaluate the AI-credit rule on pilot data; PHP2Shell case |
| Wed 10 Feb 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 15 Feb 2027 | Paul | Reviewer applications close; schedule calls |
| Mon 01 Mar 2027 | Paul | Confirm the external reviewer |
| Tue 02 Mar 2027 to 14 Mar | Reviewer | Getting started - read the overview, plan and statistical review |
| Tue 02 Mar 2027 to 14 Mar | Reviewer | Optional - practice round as second coder (pilot quarter) |
| Tue 02 Mar 2027 | Claude | Record the confirmed reviewer |
| Tue 02 Mar 2027 | Claude | Send the reviewer the practice second-coder answer file (pilot quarter) |
| Thu 04 Mar 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Thu 04 Mar 2027, 10:00 ET | Paul | Onboarding call with the external reviewer |
| Wed 10 Mar 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 15 Mar 2027, 11:00 ET | Paul | Annual review and change window |
| Mon 15 Mar 2027, 11:00 ET | Reviewer | Optional - join the 2027 annual review |
| Sun 28 Mar 2027 | Claude | Sync review before the provisional report (three passes; findings to the author) |
| Thu 01 Apr 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Thu 01 Apr 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Fri 02 Apr 2027 | Claude | Quarterly web sweep for AI-run attack reports (X3) |
| Fri 02 Apr 2027 | Claude | Send the reviewer the Q1 2027 review packet |
| Fri 02 Apr 2027, 10:00 ET | Paul | Approve the provisional draft |
| Sat 03 Apr 2027 to 28 Apr | Reviewer | Independent review of the Q1 2027 provisional report |
| Sun 04 Apr 2027 to 28 Apr | Paul | Quarterly hand-check window |
| Sun 04 Apr 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Tue 06 Apr 2027 | Claude | Choose this quarter's watch cases by the rule |
| Sat 10 Apr 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Thu 15 Apr 2027, 10:00 ET | Paul | Optional mid-review check-in with the reviewer |
| Sun 25 Apr 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Thu 29 Apr 2027 | Paul | Write the response to the external review |
| Thu 29 Apr 2027 to 12 May | Reviewer | Second coder - 20 blinded items |
| Thu 29 Apr 2027 | Claude | Send the second coder this quarter's blinded sample |
| Sat 01 May 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Sat 01 May 2027 | Claude | Publish the external review beside the Q1 2027 final report |
| Sat 01 May 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Sun 02 May 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Tue 04 May 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Mon 10 May 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Thu 13 May 2027 | Claude | Score the second coder's answer file; publish agreement |
| Fri 04 Jun 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Thu 10 Jun 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 28 Jun 2027 | Claude | Sync review before the provisional report (three passes; findings to the author) |
| Thu 01 Jul 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Thu 01 Jul 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Fri 02 Jul 2027 | Claude | Quarterly web sweep for AI-run attack reports (X3) |
| Fri 02 Jul 2027, 10:00 ET | Paul | Approve the provisional draft |
| Sun 04 Jul 2027 to 28 Jul | Paul | Quarterly hand-check window |
| Sun 04 Jul 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Tue 06 Jul 2027 | Claude | Choose this quarter's watch cases by the rule |
| Sat 10 Jul 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sun 25 Jul 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Thu 29 Jul 2027 to 11 Aug | Reviewer | Second coder - 20 blinded items |
| Thu 29 Jul 2027 | Claude | Send the second coder this quarter's blinded sample |
| Sun 01 Aug 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Sun 01 Aug 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Mon 02 Aug 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Wed 04 Aug 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Tue 10 Aug 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Fri 13 Aug 2027 | Claude | Score the second coder's answer file; publish agreement |
| Sat 04 Sep 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Fri 10 Sep 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 28 Sep 2027 | Claude | Sync review before the provisional report (three passes; findings to the author) |
| Fri 01 Oct 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Fri 01 Oct 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sat 02 Oct 2027 | Claude | Quarterly web sweep for AI-run attack reports (X3) |
| Sat 02 Oct 2027, 10:00 ET | Paul | Approve the provisional draft |
| Mon 04 Oct 2027 to 28 Oct | Paul | Quarterly hand-check window |
| Mon 04 Oct 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Wed 06 Oct 2027 | Claude | Choose this quarter's watch cases by the rule |
| Sun 10 Oct 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 25 Oct 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Fri 29 Oct 2027 to 11 Nov | Reviewer | Second coder - 20 blinded items |
| Fri 29 Oct 2027 | Claude | Send the second coder this quarter's blinded sample |
| Mon 01 Nov 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Mon 01 Nov 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Tue 02 Nov 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Thu 04 Nov 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Wed 10 Nov 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sat 13 Nov 2027 | Claude | Score the second coder's answer file; publish agreement |
| Sat 04 Dec 2027 | Claude | Copy the Drive backup's inventory and small private data into the Claude project |
| Fri 10 Dec 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 28 Dec 2027 | Claude | Sync review before the provisional report (three passes; findings to the author) |
| Sat 01 Jan 2028 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Sat 01 Jan 2028, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sun 02 Jan 2028 | Claude | Quarterly web sweep for AI-run attack reports (X3) |
| Sun 02 Jan 2028, 10:00 ET | Paul | Approve the provisional draft |
| Tue 04 Jan 2028 to 28 Jan | Paul | Quarterly hand-check window |
| Thu 06 Jan 2028 | Claude | Choose this quarter's watch cases by the rule |
| Mon 10 Jan 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 25 Jan 2028, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Sat 29 Jan 2028 to 11 Feb | Reviewer | Second coder - 20 blinded items |
| Sat 29 Jan 2028 | Claude | Send the second coder this quarter's blinded sample |
| Mon 31 Jan 2028 | Paul | Confirm whether scan data was obtained for the annual check |
| Tue 01 Feb 2028 | Claude | Summarize provisional-to-final changes; prepare the release |
| Tue 01 Feb 2028, 06:00 UTC | GitHub | Quarterly pull, final run |
| Wed 02 Feb 2028, 10:00 ET | Paul | Final-run check and approve the final results |
| Thu 10 Feb 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sun 13 Feb 2028 | Claude | Score the second coder's answer file; publish agreement |
| Wed 01 Mar 2028 | Claude | Draft the first annual check against reference data (2027) |
| Thu 02 Mar 2028 to 14 Mar | Reviewer | Optional - comment on the first annual check |
| Fri 10 Mar 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Wed 15 Mar 2028, 11:00 ET | Paul | Annual review and change window |
| Sat 01 Apr 2028 | Claude | 2027 closing re-run with full follow-up |
| Mon 03 Apr 2028, 10:00 ET | Paul | Approve the 2027 closing re-run addendum |
| Mon 10 Apr 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Wed 31 Jan 2029 | Paul | Confirm whether scan data was obtained for the annual check |
| Thu 01 Mar 2029 | Claude | Draft the annual check against reference data (previous year) |
| Thu 15 Mar 2029, 11:00 ET | Paul | Annual review and change window |
| Thu 31 Jan 2030 | Paul | Confirm whether scan data was obtained for the annual check |
| Fri 01 Mar 2030 | Claude | Draft the annual check against reference data (previous year) |
| Fri 15 Mar 2030, 11:00 ET | Paul | Annual review and change window |

## Author: dated items

| When | What | Details |
|---|---|---|
| Tue 27 Oct 2026, 10:00 ET | Send the GreyNoise research request and the CrowdSec question | Drafts from Claude (chat, 25 Oct). GreyNoise: research (VIP) access for work that is shared publicly. CrowdSec: whether research use and publishing aggregates are allowed. Use the project email if it exists by then. Claude logs both in docs/PERMISSIONS.md. |
| Wed 28 Oct 2026, 10:00 ET | Call the UGA Career Center about the reviewer posting - done | Done 28 Oct (author, before 9:00): the call went well; an independent researcher can register on Handshake; the Career Center could not say whether an unpaid internship with course credit is the better listing, so the role is listed as Experiential Learning. Original: Employer relations, (706) 542-3375. Ask whether an independent researcher can post an unpaid, remote research role on hireUGA (Handshake), and whether it is better listed as an unpaid internship with course credit. Note who you spoke with. |
| Wed 28 Oct 2026, 14:00 ET | Write and send the Censys research-access application - sent 28 Oct | Moved from 15 Feb 2027 (17 Nov, then 28 Oct at the author's choice). In your own words: Censys rejects requests written with AI tools, and the standing rules say you write it. It is an email to research-access-request@censys.com (no web form) covering: a 3-4 sentence project description with the research question and where results are published; your background (public profile or past work); how Censys helps and which access (BigQuery; delayed data is fine); how recent the data must be; confirmation of non-commercial use and citing Censys; agreement to the terms; your Censys username (make an account first). Guide: Claude doc "Censys Research Access: Application Guide". Log it in docs/PERMISSIONS.md (Claude can do the log). Access to choose: option 3 on their page, additional API endpoints and Censys credits (counts by software version or CVE without host data; enough credits for weekly counts on about 80-100 flaws a quarter, a few hundred count queries a month). Not raw Parquet downloads (too large; host data). Platform UI optional. Two things to ask: (1) can count queries be run as of past dates, back to late 2025, for a baseline year? (2) is BigQuery access also available? It would run in the Google Cloud project set up on 29 Oct. |
| Thu 29 Oct 2026, 10:00 ET | Set up BigQuery in the Google Cloud project (HTTP Archive, deps.dev history); turn on Dependabot alerts | First, one minute in GitHub (step 3 of the 27 Oct settings PDF): Settings > Advanced Security > Dependabot alerts > Enable (dependency graph on; security and version updates left off); tell Claude, who checks it. The project "internet-security-snapshot" already exists (made 27 Oct for the Drive backup's client ID). console.cloud.google.com, that project: enable the BigQuery API; no billing needed (the BigQuery sandbox includes 1 TB of queries a month); if you ever link billing, add a budget alert at $1; IAM > Service accounts > create "snapshot-bq" with the role BigQuery Job User; Keys > Add key > JSON; in GitHub > Settings > Secrets and variables > Actions, add GCP_SA_KEY (paste the whole file) and GCP_PROJECT (the project ID). Never paste the key into chat. Delete the downloaded file afterwards. |
| Fri 06 Nov 2026 | Create the project email address | For university postings and the reviewer invitation (instead of a personal address). |
| Mon 09 Nov 2026, 10:00 ET | Email CCRI's cybersecurity program director (alumni route, second coder) | Rewrite docs/reviewer/ccri-outreach.md in your own words and send it to the program director, with docs/reviewer/SECOND_CODER.md. Mainly for the second coder; also asks about CCRI graduates now in a bachelor's programme for the full review. Disclose your alumni tie if a CCRI candidate is chosen (the invitation's conflict-of-interest section). Tell Claude, who logs it. |
| Mon 09 Nov 2026, 11:00 ET | Check the 15 AI-attack entries from the trial sweep | exploratory/ai_attack_campaigns.csv, the 15 rows marked "awaiting author check" (tables in exploratory/sweep-trial-2026.md): keep or exclude each; two questions there (Shai-Hulud: X3 or X5? keep the single-source Brazil case?). |
| Tue 10 Nov 2026, 10:00 ET | Email SANS asking them to suggest a reviewer (former-employer route) | Write from docs/reviewer/sans-outreach.md (facts to cover; your own words) and send to the SANS Technology Institute or another SANS contact that reaches the right people, with the invitation letter. Main ask: the independent reviewer (confirmed by 1 Mar 2027); optional: a second coder. Disclose that you worked at SANS and that the study uses Internet Storm Center data; ask for someone you did not work with. Tell Claude, who logs it. |
| Thu 12 Nov 2026, 10:00 ET | Research review - exceptions only (8 of 11 approved conditionally on 27 Oct; 1, 2, 9 decided) | Since 27 Oct: #1, #2 and #9 decided; #3-8, #10, #11 approved on their stated conditions, so only those whose evidence fails a condition come back as option cards. Original list: Decision sheet: docs/decisions/2026-11-12-research-review.md (each question with options and a recommendation; Claude also asks them in chat as option cards that morning). 1 race fix-date effort (rec. every flagged case); 2 CISA active-exploitation date (rec. exploratory now, core proposal on 21 Dec); 3 X19 other countries' attack alerts; 4 X20 DNSSEC and RPKI by country; 5 X21 regional splits; 6 X22 breach counts outside the US; 7 X12 release-curve sources; 8 X12 capable bar (rec. coding and security, separately); 9 AI-attack sweep searches after the trial; 10 HTTP Archive web patch adoption, PHP2Shell first; 11 X16 and X17. For information: KEV lag, kernel fix dates, honeypot, AI-list check, Gemini/Irregular, PHP2Shell patch flow. |
| Mon 16 Nov 2026, 10:00 ET | Validation fix dates, then spot-check references | In the Hand Check app, list "Validation: reference cases": record the fix dates BEFORE opening prereg/ground_truth_reference.csv. Then tell Claude. |
| Wed 18 Nov 2026 | Ask Georgia State Career Services about the reviewer posting | Same question as UGA; the Handshake account carries over. |
| Fri 20 Nov 2026, 09:00 ET | Data-permission follow-ups | Claude drafts follow-ups for VulnCheck (community@vulncheck.com) and Shadowserver (ticket pqaytmyy) if they have not replied (ransomware.live granted 27 Oct); you send them. Log in docs/PERMISSIONS.md. Cutoff: the 21 Dec session. |
| Mon 23 Nov 2026, 10:00 ET | Baseline-year hand check, part 1 of 2 | AI-credit spot checks and edge cases, then cohort fix dates. docs/HAND_CHECK.md. |
| Tue 24 Nov 2026, 10:00 ET | Baseline-year hand check, part 2 of 2 | Slot (c) internet-facing checks and fix dates for the 12 baseline months. |
| Wed 25 Nov 2026 | Ask Georgia Tech College of Computing about a research internship posting | Main board (CareerBuzz) does not accept unpaid remote roles; ask the College of Computing Career Center whether an unpaid remote research internship for course credit qualifies. If no, drop Georgia Tech. |
| Wed 02 Dec 2026, 10:00 ET | Hand check on the dry run | AI-credit spot checks, slot (c) checks, fix dates (cohort and race list). First real test of the race list: note anything awkward. Approve or hold the dry-run page. |
| Thu 03 Dec 2026, 10:00 ET | Move the quarterly pull into the container (if the dry run passed) | Claude opens the pull request; you review and merge; then Actions > Quarterly pull > Run workflow (2026Q4, dry-run) to test it before 1 Jan. If the dry run failed, leave it for the 21 Dec session. |
| Fri 04 Dec 2026, 10:00 ET | Landing page, Discussions, Zenodo | Claude has built the landing page, the publishing workflow (27 Nov) and the Discussions welcome post. You: Settings > Pages > Source: GitHub Actions, then run the Pages workflow once from the Actions tab; switch on Discussions; and Zenodo archiving (zenodo.org, sign in with GitHub). Project links may be shared publicly from today. |
| Sat 05 Dec 2026 | Register on Handshake and connect the approved schools - started early, 28 Oct | Organization: "Internet Security Snapshot (independent research project)", the project email, the GitHub page as website. Approvals arrive during the RV trip. Started 28 Oct; schools requested: UGA, Georgia State, Georgia Tech, Clemson, University of South Carolina, College of Charleston, The Citadel, Emory, MIT. Posting saved as a draft (docs/reviewer/HANDSHAKE_POSTING.md), live 4 Jan - 15 Feb 2027. |
| Wed 16 Dec 2026, 10:00 ET | Hand check on the full dry run; read the findings | A shorter pass than 2 Dec (only items new since then), then Claude's findings. Anything to fix goes in before the 29 Dec freeze; anything to decide goes to the 21 Dec session. |
| Fri 18 Dec 2026, 10:00 ET | Review the workflow page and the lock list | docs/WORKFLOWS.md and the draft lock list (decision item 22), for the 21 Dec session. |
| Mon 21 Dec 2026, 10:00 ET | Core-freeze decision session | docs/CORE_FREEZE_DECISIONS.md items 0-22 (confirm 0, 7, 12; decide 1-3, 9-11, 13-22, including the companion label check, X13 and hand-check reliability, the 2028 closing re-run, and the workflow lock), with the findings of the 15 Dec full dry run. Any source without a written yes runs without it for the pilot. Added 26 Oct: item 16, the Shadowserver hand-read fallback for the pilot (rec. yes if no permission); item 20, the early-patch (embargo) note on fix dates (rec. yes); the CISA active-exploitation date as T_exploit (12 Nov decision 2); item 8, fixing the sweep's searches and the X12 capable bar and the adopted X19-X22 before the freeze. Claude asks these as option cards with recommendations, as on 12 Nov. |
| Tue 29 Dec 2026, 10:00 ET | Freeze the core (core-v1.2) and update OSF | Publish release core-v1.2 on GitHub (scored rules and the locked workflows); file the OSF update (Claude gives you the text). |
| Mon 04 Jan 2027 | Post the reviewer ad; email statistics department coordinators | On each approved board (UGA first); applications close 15 Feb. The UGA posting is already written and saved in Handshake as a draft (28 Oct; text in docs/reviewer/HANDSHAKE_POSTING.md): check the links work (the site opens 4 Dec) and set it live today. |
| Tue 12 Jan 2027, 10:00 ET | Line up the external reviewer and second coder | Send the invitation (docs/reviewer/INVITATION.md; edit the claude.ai doc "Invitation: Independent Reviewer") with the sample spot-check worksheet (docs/reviewer/sample-worksheet); candidates from the 21 Dec shortlist, including any CCRI candidates (second coder; outreach 9 Nov). The second coder can be the same person. Confirm by 1 March. |
| Mon 08 Feb 2027, 10:00 ET | Evaluate the AI-credit rule on pilot data; PHP2Shell case | Outcome goes to the 15 March review. |
| Mon 15 Feb 2027 | Reviewer applications close; schedule calls | Calls with finalists 16-26 Feb, with the three-item fix-date trial. |
| Mon 01 Mar 2027 | Confirm the external reviewer | Two weeks before the annual review; review window 3-28 April. Ask for their disclosure of any ties to AI labs (Anthropic included), security vendors or the data providers, how they want to be named (name or initials) and their ORCID. Send them the Reviewer's Desk link (site/reviewer/, it includes the calendar feed; docs/OPERATIONS.md). Then tell Claude, so the reviewer items below can start. |
| Thu 04 Mar 2027, 10:00 ET | Onboarding call with the external reviewer | Walk through the repository, the hand-check rules and the second-coder answer file in the Reviewer's Desk; answer questions; go over the practice round if done. Move the time to suit the reviewer. |
| Thu 15 Apr 2027, 10:00 ET | Optional mid-review check-in with the reviewer | Answer questions; confirm the review will arrive by 28 April or agree a new date. |
| Thu 29 Apr 2027 | Write the response to the external review | Point by point; anything accepted becomes a deviations-log row or an item for the next annual review. The review itself is published unedited. |
| Mon 03 Apr 2028, 10:00 ET | Approve the 2027 closing re-run addendum | Read Claude's summary of what changed against each 2027 quarter's final report (scored labels do not change; decision item 21) and approve publishing it as an addendum to the annual check, with its Zenodo archive. |

## External reviewer: dated items

| When | What | Details |
|---|---|---|
| Tue 02 Mar 2027 to 14 Mar | Getting started - read the overview, plan and statistical review | About 3-4 hours including the call. docs/HOW_IT_WORKS.md (the overview), the registered plan (https://doi.org/10.17605/OSF.IO/3XT82, and prereg/ in the repository), docs/STATISTICAL_REVIEW_2026-10-24.md. Can start in February if you confirm early. |
| Tue 02 Mar 2027 to 14 Mar | Optional - practice round as second coder (pilot quarter) | About 45 minutes, not scored. 20 items from the Q4 2026 pilot with Paul's answers removed: mostly fix dates (open the vendor's advisory, record when the fix was released). |
| Mon 15 Mar 2027, 11:00 ET | Optional - join the 2027 annual review | Video call; the one time each year the scored rules may change. Comments welcome beforehand. |
| Sat 03 Apr 2027 to 28 Apr | Independent review of the Q1 2027 provisional report | About 8-12 hours. Read the provisional Q1 2027 report against the registered plan and the deviations log; spot-check three headline figures drawn at random (from a seed you choose) plus any you pick, recomputing each from its worksheet in a spreadsheet (no programming needed); look at the sample of hand decisions and their written rules. Send a short written review (two to five pages: what holds up, what doesn't, what you'd change) by 28 April. The window can move a week or two if needed; publication is 1 May. |
| Thu 02 Mar 2028 to 14 Mar | Optional - comment on the first annual check | About 1-2 hours. Read the first annual check of the free data against better reference data (drafted 1 March) and comment before the 15 March 2028 annual review. |

## Claude: dated items

| When | What | Details |
|---|---|---|
| Sun 25 Oct 2026 | Patch-adoption prototype from deps.dev (open-source flaws) - snapshot run | Research probe depsdev_adoption, 25 Oct: today's share of dependents on affected versions for attacked open-source flaws (deps.dev free API). History over time needs deps.dev's BigQuery tables (httparchive-test, after the BigQuery project). |
| Sun 25 Oct 2026 | Monthly honeypot capture (SANS ISC), aggregates only - built | Built and first run 25 Oct (exploratory X14, context only; .github/workflows/honeypot.yml, 2nd of each month; data/isc-honeypot/ on run-reports, about 40 KB a capture). First capture: 10.2 million URLs, 304 attack categories, 241 CVEs. |
| Sun 25 Oct 2026 | Linux kernel fix dates - probe run | Probe 25 Oct: 5 of 8 kernel flaws added to KEV in Jan-Sep 2026 are dated from fixing commits, a median 22 days before CVE publication (the 3 others are older Red Hat records without commits). Follow-up: kernel-fixdates-prefill. |
| Sun 25 Oct 2026 | Back-test KEV's lag against EUVD, Project Zero's sheet and inthewild.io - first run | Research probe kev_lag (KEV additions Jan-Sep 2026), first runs 25 Oct; results and their limits go to the 12 Nov research review. |
| Sun 25 Oct 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Mon 26 Oct 2026 | Draft the CCRI outreach email and the second-coder role summary - done | docs/reviewer/ccri-outreach.md (draft for the author to rewrite) and docs/reviewer/SECOND_CODER.md (one-page role summary). Author's decision, 26 Oct: approach CCRI (the author's alma mater; NSA CAE in Cyber Defense) mainly for the second coder. |
| Mon 26 Oct 2026 | Continue the research window | docs/RESEARCH_PLAN.md: item 5 (an on/off switch per permissioned source in config), then item 4 (remaining evaluation code: labels T2, T4-T6; X6-X12; NVD root-cause fill; draft evaluation page); consider CISA's active-exploitation assessment date as a research-flag T_exploit candidate; then Plan 1 / Plan 2 research. Report to the author only findings worth knowing. |
| Tue 27 Oct 2026 | Probe the global sources (X19-X22) and translate the sweep searches | Author's request of 26 Oct (docs/INQUIRIES.md). Quick tests through the Research probe workflow: can each national alert feed (CERT-FR, JPCERT/CC, BSI, KrCERT/CC) be read and dated, what do APNIC Labs and RIPE NCC publish per country, can Radar and ransomware.live be split by region, and what the breach regulators publish. Terms of use read for each and logged in docs/PERMISSIONS.md. Translate the X3 sweep searches into the eight languages and fix them in config/exploratory.yaml. Findings go to the 12 Nov research review; any source that holds up becomes active before the 29 Dec freeze. Also the X12 amendment of 26 Oct (open-weight release rate): Hugging Face Hub API by lab, Epoch AI's model database, and candidate benchmarks for the "capable" bar. |
| Mon 02 Nov 2026 | HHS OCR health-breach series - second attempt at the export | Probe 25 Oct: the portal answers, but its CSV export is a form the probe did not trigger. Second attempt with the form's real fields; if it still fails, the public research copies of the same register are checked for terms. Quarterly counts of "hacking/IT incident" breaches of 500+ people; aggregates only, beside T6. |
| Mon 02 Nov 2026 | HTTP Archive test - are software versions recorded? (after the BigQuery project) | One small BigQuery query within the free tier, with a per-query byte cap. If versions are recorded, propose an exploratory patch-adoption measure for web software (share of sites on the fixed version, 30 and 90 days after the fix). WordPress.org version statistics work (probe 25 Oct: version shares per plugin, today only), so they need weekly capture to build history. Also deps.dev's BigQuery history for the patch-adoption prototype. First test case: PHP2Shell (fixed 21 Oct 2026; author's concern of 26 Oct that many servers will stay unpatched): from the X-Powered-By PHP versions in the September, October and November crawls, the share of PHP-reporting sites on a fixed release, and the share on releases that will never get a fix (PHP 5.4-7.3). Sites that hide their version are not counted. |
| Mon 02 Nov 2026 | Add kernel commit dates (and more CSAF vendors) to the fix-date pre-fill | snapshot.fixdates.prefill_exploited: fixing commits from kernel CVE records dated through the GitHub mirrors; Debian/Ubuntu trackers as a cross-check; CSAF feeds of further vendors (Siemens, Red Hat, SUSE) where they cover attacked flaws. Measure the drop in "assumed" dates on the 175-flaw probe. Code change by pull request, before the 14 Dec review. |
| Mon 02 Nov 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Thu 05 Nov 2026 | Recheck the trial AI-attack sweep's open items | The trial itself ran early, on 26 Oct, at the author's request (exploratory/sweep-trial-2026.md; 15 kept after the China and Russia retry, log 13 -> 28). Read the primary reports behind the kept entries (Sysdig, GTIG, CrowdStrike, GMO) and the 8 "recheck" rows in exploratory/ai_attack_sweeps.csv; correct the log; final list of proposed search changes for decision 9 on 12 Nov. |
| Mon 09 Nov 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Wed 11 Nov 2026 | Restore test of the Drive backup | The backup was set up and tested on 27 Oct (own Google client ID; connection test and a 7 MB repository copy arrived in the Drive folder). Now restore: clone the newest repository bundle and confirm it matches main; after the 1 Dec dry run, check its bundle and private part arrived. Add the Backup workflow to docs/WORKFLOWS.md and the lock list. |
| Wed 11 Nov 2026 | Fill in the 12 Nov decision sheet with the probe and trial results | docs/decisions/2026-11-12-research-review.md: the Evidence line under each decision (27 Oct global probes, 2 Nov tests, 5 Nov trial sweep); change a recommendation only if the evidence says so, and say why. Since 27 Oct: apply each conditionally approved item (#3-8, #10, #11) whose evidence meets its condition, and list the exceptions for 12 Nov. On 12 Nov before 10:00, ask the same decisions in chat as option cards with the recommendation first. |
| Mon 16 Nov 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Tue 17 Nov 2026 | Run the validation and report pass/fail | snapshot.validate against prereg/ground_truth_reference.csv (pass = 4 of 5 cases). |
| Fri 20 Nov 2026 | Draft the permission follow-ups and update the log | docs/PERMISSIONS.md (request texts as sent, and the points for the Shadowserver follow-up, including the hand-read fallback); decision item 16 sets the 21 Dec cutoff. |
| Mon 23 Nov 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Wed 25 Nov 2026 | Race fix-date list ready in the Hand Check app | List builder in snapshot.review, report table and time estimate, alongside snapshot.race.t1_kev_race and X10; read the app artifact before republishing. Tell the author only if something will not be ready for 1-2 Dec. |
| Fri 27 Nov 2026 | Build the project website and its publishing workflow (ready for 4 Dec) | site/index.html (landing page: what the study is, links to the plan, reports and the Reviewer's Desk at site/reviewer/) and .github/workflows/pages.yml (publishes the site/ folder with GitHub's official Pages actions, pinned by commit, on pushes to main that touch site/ and by hand). Test the pages locally; the workflow is switched on by the author on 4 Dec (Settings > Pages > Source: GitHub Actions). Address: https://pagagne.github.io/internet-security-snapshot/ ; the Desk at .../reviewer/. Plus the run-health status page (decided 27 Oct; mock-up approved first, Claude Design artifact "Run-Health Dashboard Mock-up"): a build step reads the run-reports branch and renders last run, next pull, quarter stage, source health with pushback and permission state, rebuild verdict, integrity checks, evaluations list and recent runs. Health only, no findings or counts (those follow the author's review on the evaluation page); covered by the daily privacy scan. Rebuilt after every workflow run. |
| Mon 30 Nov 2026 | Cutover check (study no longer depends on one Claude chat) | Confirm: the Schedule workflow has run green for 7 days; the author has subscribed to the calendar feed; the Claude work-queue scheduled task is live; docs/OPERATIONS.md is current. Then retire any remaining one-off check-ins in the old chat. docs/OPERATIONS.md. |
| Mon 30 Nov 2026 | Sync review (three passes; findings to the author) | docs/SYNC_REVIEW.md: repository, sync between repository, Claude docs, calendars and scheduled tasks, and everything that runs on its own. Findings to the author as Confirmed / Fixed / Conflicts resolved / Still for you. Weekly until the 30 Nov cutover. |
| Tue 01 Dec 2026 | Read the dry-run quality report; prepare the hand-check lists | First check that the Schedule workflow really started the quarterly pull (first end-to-end test, docs/WORKFLOW_REVIEW_2026-10-27.md item 4); if not, start it by hand. Then load the review lists (including the race list) into the Hand Check app. |
| Fri 11 Dec 2026 | Get every available source ready for the full dry run | Author's request of 26 Oct: a second dry run before the pilot using all available data. By 14 Dec every source in use is collected by the quarterly pull or by its own workflow, with the exploratory ones adopted so far (honeypot series, Project Zero, kernel fix dates, deps.dev, HHS, and the global sources adopted on 12 Nov); config/sources.yaml switched on for any permission granted by then. Check the evaluation steps run end to end (labels, draft page, hand-check lists, reviewer worksheets). Note anything not ready in the run's issue, so its absence is a known gap rather than a surprise. |
| Mon 14 Dec 2026 | Document and test every GitHub workflow; draft the lock list | docs/WORKFLOWS.md (written 27 Oct in plain language; extend it from docs/WORKFLOW_REVIEW_2026-10-27.md): for each workflow, what starts it, its permissions and secrets, inputs and outputs, what happens on failure and who notices, and its latest successful run (link). Run any workflow without a successful run since its last change (rebuild check on the dry run's bundle; quarterly pull inside the container; the daily honeypot collector). Draft the lock list for decision item 22: data workflows (quarterly pull, rebuild check, daily collectors, Dockerfile) locked like the core; support workflows (Checks, Schedule, Diagrams, Research, Pages, Backup) under a change log. |
| Tue 15 Dec 2026 | Review the full dry run; findings for the 21 Dec session | Quality report, gaps per source, the exploratory collectors' outputs and the full evaluation (labels, draft page, review lists, worksheets). Compare with the 1 Dec dry run. Load the hand-check lists into the Hand Check app; write the findings as one list for the author with anything that needs a decision on 21 Dec. |
| Tue 22 Dec 2026 | Prepare the core freeze (core-v1.2) | Deviation rows, LOCKED.yaml checksums (including the workflows locked under decision item 22), freeze summary and the OSF update text. |
| Wed 20 Jan 2027 | Build the figure worksheets for the reviewer's spot check | Extend the sample (docs/reviewer/sample-worksheet, snapshot.worksheet race-sample) to a worksheet per headline figure (T1-T7), generated with every release: the plan's definition in plain words, the inputs as a CSV a spreadsheet opens, the steps from inputs to figure, and the published value to match, listed in site/reviewer/worksheets.json for the Reviewer's Desk (whose seeded draw picks three). Test on the Q4 2026 pilot (provisional 1 Jan) so a worksheet can be tried in the practice round. Check that each worksheet can be followed in a spreadsheet with no code. |
| Mon 25 Jan 2027 | Outside AI-found CVE lists against our AI-credit counts, on pilot data | Prototype 25 Oct (research probe ai_lists): of 5 outside AI-found CVEs with records, the headline rule caught 3, the narrow 0, and 2 (Microsoft, Apple) have empty credit fields: those vendors credit finders only in their own advisories. For 8 Feb: rerun on the pilot, and test vendor acknowledgments (Microsoft's update guide, Apple's security notes) as an exploratory source for T7. |
| Wed 03 Feb 2027 | Prepare the 8 Feb session | AI-credit rule evaluation on the pilot's final data (headline vs narrow count, a sample of lab-affiliation-only credits, spot checks) and the PHP2Shell case note docs/cases/php2shell.md. Send the author a heads-up. |
| Wed 03 Feb 2027 | Compare the pilot with what we expected (docs/PILOT_EXPECTATIONS.md) | After the Q4 2026 final run: put each reading next to the expectation written on 26 Oct 2026, mark hits and surprises in one short table, and add it to the pilot report's notes for the author. Nothing in the comparison changes a rule. |
| Tue 02 Mar 2027 | Record the confirmed reviewer | Add the reviewer as a contributor (name or initials as they asked, ORCID) to .zenodo.json and the report template; record their disclosed ties for publication beside the review. Never put their email or phone in the public repository. |
| Tue 02 Mar 2027 | Send the reviewer the practice second-coder answer file (pilot quarter) | Claude emails the reviewer a small answer file (CSV) with 20 items from the pilot quarter, Paul's answers removed. Open it in the Reviewer's Desk (Second coder tab), work through the items with the written rules shown there, then save the completed file and send it back. Practice only, not scored; discussed on the onboarding call. (Claude: python -m snapshot.agreement sample --batch 2026Q4; never send the weights file.) |
| Fri 02 Apr 2027 | Send the reviewer the Q1 2027 review packet | Once the provisional Q1 2027 report is approved: links to the report, the registered plan, prereg/DEVIATIONS.md, the data bundle and the exact code commit; the worksheet for every headline figure; the sample of hand decisions with their rules; a short review template (holds up / doesn't / would change). Before sending, list in site/reviewer/worksheets.json ("draw_from") the headline figures actually reported this quarter and add their worksheets; the reviewer draws three on the Reviewer's Desk with a seed of their own (anyone can repeat it). Never choose the figures. |
| Sat 01 May 2027 | Publish the external review beside the Q1 2027 final report | Review unedited, the author's response, the reviewer's disclosed ties and credit; archived with the release (Zenodo). Send the reviewer the link. |
| Wed 01 Mar 2028 | Draft the first annual check against reference data (2027) | prereg section 13: exposure reference if scan data was obtained by 31 Jan, harm reference always. For the author's approval at the 15 March 2028 review. |
| Sat 01 Apr 2028 | 2027 closing re-run with full follow-up | Re-run all four 2027 quarters once every 2027 cohort CVE has its 90-day follow-up; publish as a completeness addendum to the annual check. Labels unchanged (decision item 21). The author approves. |

## GitHub (automatic): dated items

| When | What | Details |
|---|---|---|
| Tue 01 Dec 2026, 11:00 UTC | Dry run of the quarterly pull (Oct-Nov data) | Started by the Schedule workflow (December has no cron). Unscored. |
| Tue 15 Dec 2026, 11:00 UTC | Full dry run with all available sources (1 Oct-14 Dec data) | Started by the Schedule workflow. Second dry run, the closest test of the 1 Jan pilot: every source switched on in config/sources.yaml, in the container if container-pull is done. Unscored; nothing published. |

