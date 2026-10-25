# Annual plan: every action item, by who does it

Generated from `docs/schedule/schedule.yaml` by `python -m snapshot.schedule build`; do not edit by hand.
The same items are in the calendar feed `docs/schedule/snapshot.ics`, and each author or Claude item
opens a GitHub issue when it falls due (label `schedule`, plus `owner:author` or `owner:claude`).

## Every quarter and every month

| Who | What | When |
|---|---|---|
| Author | Approve the provisional draft | day 2, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 10:00 ET |
| Author | Quarterly hand-check window | day 4, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 (25 days) |
| Author | Hand-check answers due by the 28th | day 25, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 10:00 ET |
| Author | Final-run check and approve the final results | day 2, Feb, May, Aug, Nov, 2027-02 to 2028-02, 10:00 ET |
| Author | Annual review and change window | day 15, Mar, 2027-03 to 2028-03, 11:00 ET |
| External reviewer | Second coder - 20 blinded items | day 29, Jan, Apr, Jul, Oct, 2027-04 to 2028-01 (14 days) |
| Claude | Draft the provisional evaluation; load the hand-check lists | day 1, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 |
| Claude | Send the second coder this quarter's blinded sample | day 29, Jan, Apr, Jul, Oct, 2027-01 to 2028-01 |
| Claude | Summarize provisional-to-final changes; prepare the release | day 1, Feb, May, Aug, Nov, 2027-02 to 2028-02 |
| Claude | Score the second coder's sheet; publish agreement | day 13, Feb, May, Aug, Nov, 2027-05 to 2028-02 |
| GitHub (automatic) | Quarterly pull, provisional run | day 1, Jan, Apr, Jul, Oct, 2027-01 to 2028-01, 06:00 UTC |
| GitHub (automatic) | Rebuild check of the latest frozen bundle | day 10, every month, 2026-11 to 2028-04, 07:17 UTC |
| GitHub (automatic) | Quarterly pull, final run | day 1, Feb, May, Aug, Nov, 2027-02 to 2028-02, 06:00 UTC |

## Author: dated items

| When | What | Details |
|---|---|---|
| Wed 28 Oct 2026, 10:00 ET | Call the UGA Career Center about the reviewer posting | Employer relations, (706) 542-3375. Ask whether an independent researcher can post an unpaid, remote research role on hireUGA (Handshake), and whether it is better listed as an unpaid internship with course credit. Note who you spoke with. |
| Fri 06 Nov 2026 | Create the project email address | For university postings and the reviewer invitation (instead of a personal address). |
| Thu 12 Nov 2026, 10:00 ET | Review research results; decide race fix-date effort | Every flagged race fix date (about 1½ h a quarter; the author's leaning on 24 Oct) or a sample (about 50 min). The CISA-flag preview (zero-day share possibly understated by half) is on the agenda. docs/RESEARCH_PLAN.md. |
| Mon 16 Nov 2026, 10:00 ET | Validation fix dates, then spot-check references | In the Hand Check app, list "Validation: reference cases": record the fix dates BEFORE opening prereg/ground_truth_reference.csv. Then tell Claude. |
| Wed 18 Nov 2026 | Ask Georgia State Career Services about the reviewer posting | Same question as UGA; the Handshake account carries over. |
| Fri 20 Nov 2026, 09:00 ET | Data-permission follow-ups | Claude drafts follow-ups for any of ransomware.live (ticket #3425), VulnCheck (community@vulncheck.com) and Shadowserver (ticket pqaytmyy) that have not replied; you send them. Log in docs/PERMISSIONS.md. Cutoff: the 21 Dec session. |
| Mon 23 Nov 2026, 10:00 ET | Baseline-year hand check, part 1 of 2 | AI-credit spot checks and edge cases, then cohort fix dates. docs/HAND_CHECK.md. |
| Tue 24 Nov 2026, 10:00 ET | Baseline-year hand check, part 2 of 2 | Slot (c) internet-facing checks and fix dates for the 12 baseline months. |
| Wed 25 Nov 2026 | Ask Georgia Tech College of Computing about a research internship posting | Main board (CareerBuzz) does not accept unpaid remote roles; ask the College of Computing Career Center whether an unpaid remote research internship for course credit qualifies. If no, drop Georgia Tech. |
| Wed 02 Dec 2026, 10:00 ET | Hand check on the dry run | AI-credit spot checks, slot (c) checks, fix dates (cohort and race list). First real test of the race list: note anything awkward. Approve or hold the dry-run page. |
| Thu 03 Dec 2026, 10:00 ET | Move the quarterly pull into the container (if the dry run passed) | Claude opens the pull request; you review and merge; then Actions > Quarterly pull > Run workflow (2026Q4, dry-run) to test it before 1 Jan. If the dry run failed, leave it for the 21 Dec session. |
| Fri 04 Dec 2026, 10:00 ET | Landing page, Discussions, Zenodo | Claude builds the GitHub Pages landing page and Discussions welcome post; you switch on Discussions and Pages, and Zenodo archiving (zenodo.org, sign in with GitHub). Project links may be shared publicly from today. |
| Sat 05 Dec 2026 | Register on Handshake and connect the approved schools | Organization: "Internet Security Snapshot (independent research project)", the project email, the GitHub page as website. Approvals arrive during the RV trip. |
| Mon 21 Dec 2026, 10:00 ET | Core-freeze decision session | docs/CORE_FREEZE_DECISIONS.md items 0-21 (confirm 0, 7, 12; decide 1-3, 9-11, 13-21, including the companion label check, X13 and hand-check reliability, the 2028 closing re-run). Any source without a written yes runs without it for the pilot. |
| Tue 29 Dec 2026, 10:00 ET | Freeze the core (core-v1.2) and update OSF | Publish release core-v1.2 on GitHub; file the OSF update (Claude gives you the text). |
| Mon 04 Jan 2027 | Post the reviewer ad; email statistics department coordinators | On each approved board (UGA first); applications close 15 Feb. |
| Tue 12 Jan 2027, 10:00 ET | Line up the external reviewer and second coder | Send the invitation (claude.ai doc "Invitation: Independent Reviewer"); candidates from the 21 Dec shortlist. The second coder can be the same person. Confirm by 1 March. |
| Mon 08 Feb 2027, 10:00 ET | Evaluate the AI-credit rule on pilot data; PHP2Shell case | Outcome goes to the 15 March review. |
| Mon 15 Feb 2027 | Reviewer applications close; schedule calls | Calls with finalists 16-26 Feb, with the three-item fix-date trial. |
| Mon 15 Feb 2027, 10:00 ET | Write the Censys research-access application | In your own words (Censys rejects AI-written requests). Claude can list the facts to cover. |
| Mon 01 Mar 2027 | Confirm the external reviewer | Two weeks before the annual review; review window 3-28 April. Ask for their disclosure of any ties to AI labs (Anthropic included), security vendors or the data providers, how they want to be named (name or initials) and their ORCID. Send them the reviewer calendar feed (docs/OPERATIONS.md). Then tell Claude, so the reviewer items below can start. |
| Thu 04 Mar 2027, 10:00 ET | Onboarding call with the external reviewer | Walk through the repository, the hand-check rules and the second-coder sheet; answer questions; go over the practice round if done. Move the time to suit the reviewer. |
| Thu 15 Apr 2027, 10:00 ET | Optional mid-review check-in with the reviewer | Answer questions; confirm the review will arrive by 28 April or agree a new date. |
| Thu 29 Apr 2027 | Write the response to the external review | Point by point; anything accepted becomes a deviations-log row or an item for the next annual review. The review itself is published unedited. |

## External reviewer: dated items

| When | What | Details |
|---|---|---|
| Tue 02 Mar 2027 to 14 Mar | Getting started - read the overview, plan and statistical review | About 3-4 hours including the call. docs/HOW_IT_WORKS.md (the overview), the registered plan (OSF DOI 10.17605/OSF.IO/3XT82, and prereg/ in the repository), docs/STATISTICAL_REVIEW_2026-10-24.md. Can start in February if you confirm early. |
| Tue 02 Mar 2027 to 14 Mar | Optional - practice round as second coder (pilot quarter) | About 45 minutes, not scored. 20 items from the Q4 2026 pilot with Paul's answers removed: mostly fix dates (open the vendor's advisory, record when the fix was released). |
| Mon 15 Mar 2027, 11:00 ET | Optional - join the 2027 annual review | Video call; the one time each year the scored rules may change. Comments welcome beforehand. |
| Sat 03 Apr 2027 to 28 Apr | Independent review of the Q1 2027 provisional report | About 8-12 hours. Read the provisional Q1 2027 report against the registered plan and the deviations log; check that each headline figure is computed as the plan defines it (read the code, or recompute a few numbers from the data bundle); look at the sample of hand decisions and their written rules. Send a short written review (two to five pages: what holds up, what doesn't, what you'd change) by 28 April. The window can move a week or two if needed; publication is 1 May. |
| Thu 02 Mar 2028 to 14 Mar | Optional - comment on the first annual check | About 1-2 hours. Read the first annual check of the free data against better reference data (drafted 1 March) and comment before the 15 March 2028 annual review. |

## Claude: dated items

| When | What | Details |
|---|---|---|
| Mon 26 Oct 2026 | Continue the research window | docs/RESEARCH_PLAN.md: item 5 (an on/off switch per permissioned source in config), then item 4 (remaining evaluation code: labels T2, T4-T6; X6-X12; NVD root-cause fill; draft evaluation page); consider CISA's active-exploitation assessment date as a research-flag T_exploit candidate; then Plan 1 / Plan 2 research. Report to the author only findings worth knowing. |
| Tue 17 Nov 2026 | Run the validation and report pass/fail | snapshot.validate against prereg/ground_truth_reference.csv (pass = 4 of 5 cases). |
| Fri 20 Nov 2026 | Draft the permission follow-ups and update the log | docs/PERMISSIONS.md; decision item 16 sets the 21 Dec cutoff. |
| Wed 25 Nov 2026 | Race fix-date list ready in the Hand Check app | List builder in snapshot.review, report table and time estimate, alongside snapshot.race.t1_kev_race and X10; read the app artifact before republishing. Tell the author only if something will not be ready for 1-2 Dec. |
| Mon 30 Nov 2026 | Cutover check (study no longer depends on one Claude chat) | Confirm: the Schedule workflow has run green for 7 days; the author has subscribed to the calendar feed; the Claude work-queue scheduled task is live; docs/OPERATIONS.md is current. Then retire any remaining one-off check-ins in the old chat. docs/OPERATIONS.md. |
| Tue 01 Dec 2026 | Read the dry-run quality report; prepare the hand-check lists | Load the review lists (including the race list) into the Hand Check app. |
| Tue 22 Dec 2026 | Prepare the core freeze (core-v1.2) | Deviation rows, LOCKED.yaml checksums, freeze summary and the OSF update text. |
| Wed 03 Feb 2027 | Prepare the 8 Feb session | AI-credit rule evaluation on the pilot's final data (headline vs narrow count, a sample of lab-affiliation-only credits, spot checks) and the PHP2Shell case note docs/cases/php2shell.md. Send the author a heads-up. |
| Tue 02 Mar 2027 | Record the confirmed reviewer | Add the reviewer as a contributor (name or initials as they asked, ORCID) to .zenodo.json and the report template; record their disclosed ties for publication beside the review. Never put their email or phone in the public repository. |
| Tue 02 Mar 2027 | Send the reviewer the practice second-coder sheet (pilot quarter) | python -m snapshot.agreement sample --batch 2026Q4; send the sheet (not the weights file) and the written rules. Unscored practice; score it only to discuss on the onboarding call. |
| Fri 02 Apr 2027 | Send the reviewer the Q1 2027 review packet | Once the provisional Q1 2027 report is approved: links to the report, the registered plan, prereg/DEVIATIONS.md, the data bundle and the exact code commit; the sample of hand decisions with their rules; a short review template (holds up / doesn't / would change). |
| Sat 01 May 2027 | Publish the external review beside the Q1 2027 final report | Review unedited, the author's response, the reviewer's disclosed ties and credit; archived with the release (Zenodo). Send the reviewer the link. |
| Wed 01 Mar 2028 | Draft the first annual check against reference data (2027) | prereg section 13: exposure reference if scan data was obtained by 31 Jan, harm reference always. For the author's approval at the 15 March 2028 review. |
| Sat 01 Apr 2028 | 2027 closing re-run with full follow-up | Re-run all four 2027 quarters once every 2027 cohort CVE has its 90-day follow-up; publish as a completeness addendum to the annual check. Labels unchanged (decision item 21). The author approves. |

## GitHub (automatic): dated items

| When | What | Details |
|---|---|---|
| Tue 01 Dec 2026, 11:00 UTC | Dry run of the quarterly pull (Oct-Nov data) | Started by the Schedule workflow (December has no cron). Unscored. |

