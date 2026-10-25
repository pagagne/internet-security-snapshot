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

## Calendar: every dated item in order

The same list as the calendar feeds, one row per occurrence (repeating items included).

| When | Who is responsible | What |
|---|---|---|
| Mon 26 Oct 2026 | Claude | Continue the research window |
| Wed 28 Oct 2026, 10:00 ET | Paul | Call the UGA Career Center about the reviewer posting |
| Fri 06 Nov 2026 | Paul | Create the project email address |
| Tue 10 Nov 2026, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Thu 12 Nov 2026, 10:00 ET | Paul | Review research results; decide race fix-date effort |
| Mon 16 Nov 2026, 10:00 ET | Paul | Validation fix dates, then spot-check references |
| Tue 17 Nov 2026 | Claude | Run the validation and report pass/fail |
| Wed 18 Nov 2026 | Paul | Ask Georgia State Career Services about the reviewer posting |
| Fri 20 Nov 2026 | Claude | Draft the permission follow-ups and update the log |
| Fri 20 Nov 2026, 09:00 ET | Paul | Data-permission follow-ups |
| Mon 23 Nov 2026, 10:00 ET | Paul | Baseline-year hand check, part 1 of 2 |
| Tue 24 Nov 2026, 10:00 ET | Paul | Baseline-year hand check, part 2 of 2 |
| Wed 25 Nov 2026 | Paul | Ask Georgia Tech College of Computing about a research internship posting |
| Wed 25 Nov 2026 | Claude | Race fix-date list ready in the Hand Check app |
| Mon 30 Nov 2026 | Claude | Cutover check (study no longer depends on one Claude chat) |
| Tue 01 Dec 2026 | Claude | Read the dry-run quality report; prepare the hand-check lists |
| Tue 01 Dec 2026, 11:00 UTC | GitHub | Dry run of the quarterly pull (Oct-Nov data) |
| Wed 02 Dec 2026, 10:00 ET | Paul | Hand check on the dry run |
| Thu 03 Dec 2026, 10:00 ET | Paul | Move the quarterly pull into the container (if the dry run passed) |
| Fri 04 Dec 2026, 10:00 ET | Paul | Landing page, Discussions, Zenodo |
| Sat 05 Dec 2026 | Paul | Register on Handshake and connect the approved schools |
| Thu 10 Dec 2026, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 21 Dec 2026, 10:00 ET | Paul | Core-freeze decision session |
| Tue 22 Dec 2026 | Claude | Prepare the core freeze (core-v1.2) |
| Tue 29 Dec 2026, 10:00 ET | Paul | Freeze the core (core-v1.2) and update OSF |
| Fri 01 Jan 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Fri 01 Jan 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sat 02 Jan 2027, 10:00 ET | Paul | Approve the provisional draft |
| Mon 04 Jan 2027 to 28 Jan | Paul | Quarterly hand-check window |
| Mon 04 Jan 2027 | Paul | Post the reviewer ad; email statistics department coordinators |
| Sun 10 Jan 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 12 Jan 2027, 10:00 ET | Paul | Line up the external reviewer and second coder |
| Wed 20 Jan 2027 | Claude | Build the figure worksheets for the reviewer's spot check |
| Mon 25 Jan 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Fri 29 Jan 2027 | Claude | Send the second coder this quarter's blinded sample |
| Mon 01 Feb 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Mon 01 Feb 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Tue 02 Feb 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Wed 03 Feb 2027 | Claude | Prepare the 8 Feb session |
| Mon 08 Feb 2027, 10:00 ET | Paul | Evaluate the AI-credit rule on pilot data; PHP2Shell case |
| Wed 10 Feb 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 15 Feb 2027 | Paul | Reviewer applications close; schedule calls |
| Mon 15 Feb 2027, 10:00 ET | Paul | Write the Censys research-access application |
| Mon 01 Mar 2027 | Paul | Confirm the external reviewer |
| Tue 02 Mar 2027 to 14 Mar | Reviewer | Getting started - read the overview, plan and statistical review |
| Tue 02 Mar 2027 to 14 Mar | Reviewer | Optional - practice round as second coder (pilot quarter) |
| Tue 02 Mar 2027 | Claude | Record the confirmed reviewer |
| Tue 02 Mar 2027 | Claude | Send the reviewer the practice second-coder sheet (pilot quarter) |
| Thu 04 Mar 2027, 10:00 ET | Paul | Onboarding call with the external reviewer |
| Wed 10 Mar 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 15 Mar 2027, 11:00 ET | Paul | Annual review and change window |
| Mon 15 Mar 2027, 11:00 ET | Reviewer | Optional - join the 2027 annual review |
| Thu 01 Apr 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Thu 01 Apr 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Fri 02 Apr 2027 | Claude | Send the reviewer the Q1 2027 review packet |
| Fri 02 Apr 2027, 10:00 ET | Paul | Approve the provisional draft |
| Sat 03 Apr 2027 to 28 Apr | Reviewer | Independent review of the Q1 2027 provisional report |
| Sun 04 Apr 2027 to 28 Apr | Paul | Quarterly hand-check window |
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
| Mon 10 May 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Thu 13 May 2027 | Claude | Score the second coder's sheet; publish agreement |
| Thu 10 Jun 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Thu 01 Jul 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Thu 01 Jul 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Fri 02 Jul 2027, 10:00 ET | Paul | Approve the provisional draft |
| Sun 04 Jul 2027 to 28 Jul | Paul | Quarterly hand-check window |
| Sat 10 Jul 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sun 25 Jul 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Thu 29 Jul 2027 to 11 Aug | Reviewer | Second coder - 20 blinded items |
| Thu 29 Jul 2027 | Claude | Send the second coder this quarter's blinded sample |
| Sun 01 Aug 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Sun 01 Aug 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Mon 02 Aug 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Tue 10 Aug 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Fri 13 Aug 2027 | Claude | Score the second coder's sheet; publish agreement |
| Fri 10 Sep 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Fri 01 Oct 2027 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Fri 01 Oct 2027, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sat 02 Oct 2027, 10:00 ET | Paul | Approve the provisional draft |
| Mon 04 Oct 2027 to 28 Oct | Paul | Quarterly hand-check window |
| Sun 10 Oct 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Mon 25 Oct 2027, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Fri 29 Oct 2027 to 11 Nov | Reviewer | Second coder - 20 blinded items |
| Fri 29 Oct 2027 | Claude | Send the second coder this quarter's blinded sample |
| Mon 01 Nov 2027 | Claude | Summarize provisional-to-final changes; prepare the release |
| Mon 01 Nov 2027, 06:00 UTC | GitHub | Quarterly pull, final run |
| Tue 02 Nov 2027, 10:00 ET | Paul | Final-run check and approve the final results |
| Wed 10 Nov 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sat 13 Nov 2027 | Claude | Score the second coder's sheet; publish agreement |
| Fri 10 Dec 2027, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sat 01 Jan 2028 | Claude | Draft the provisional evaluation; load the hand-check lists |
| Sat 01 Jan 2028, 06:00 UTC | GitHub | Quarterly pull, provisional run |
| Sun 02 Jan 2028, 10:00 ET | Paul | Approve the provisional draft |
| Tue 04 Jan 2028 to 28 Jan | Paul | Quarterly hand-check window |
| Mon 10 Jan 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Tue 25 Jan 2028, 10:00 ET | Paul | Hand-check answers due by the 28th |
| Sat 29 Jan 2028 to 11 Feb | Reviewer | Second coder - 20 blinded items |
| Sat 29 Jan 2028 | Claude | Send the second coder this quarter's blinded sample |
| Tue 01 Feb 2028 | Claude | Summarize provisional-to-final changes; prepare the release |
| Tue 01 Feb 2028, 06:00 UTC | GitHub | Quarterly pull, final run |
| Wed 02 Feb 2028, 10:00 ET | Paul | Final-run check and approve the final results |
| Thu 10 Feb 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Sun 13 Feb 2028 | Claude | Score the second coder's sheet; publish agreement |
| Wed 01 Mar 2028 | Claude | Draft the first annual check against reference data (2027) |
| Thu 02 Mar 2028 to 14 Mar | Reviewer | Optional - comment on the first annual check |
| Fri 10 Mar 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |
| Wed 15 Mar 2028, 11:00 ET | Paul | Annual review and change window |
| Sat 01 Apr 2028 | Claude | 2027 closing re-run with full follow-up |
| Mon 10 Apr 2028, 07:17 UTC | GitHub | Rebuild check of the latest frozen bundle |

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
| Tue 12 Jan 2027, 10:00 ET | Line up the external reviewer and second coder | Send the invitation (docs/reviewer/INVITATION.md; edit the claude.ai doc "Invitation: Independent Reviewer"); candidates from the 21 Dec shortlist. The second coder can be the same person. Confirm by 1 March. |
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
| Sat 03 Apr 2027 to 28 Apr | Independent review of the Q1 2027 provisional report | About 8-12 hours. Read the provisional Q1 2027 report against the registered plan and the deviations log; spot-check three headline figures drawn at random (from a seed you choose) plus any you pick, recomputing each from its worksheet in a spreadsheet (no programming needed); look at the sample of hand decisions and their written rules. Send a short written review (two to five pages: what holds up, what doesn't, what you'd change) by 28 April. The window can move a week or two if needed; publication is 1 May. |
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
| Wed 20 Jan 2027 | Build the figure worksheets for the reviewer's spot check | A worksheet per headline figure (T1-T7), generated with every release: the plan's definition in plain words, the inputs as a CSV a spreadsheet opens, the steps from inputs to figure, and the published value to match. Plus a seeded draw that picks three figures from a seed the reviewer gives. Test on the Q4 2026 pilot (provisional 1 Jan) so a worksheet can be tried in the practice round. Check that each worksheet can be followed in a spreadsheet with no code. |
| Wed 03 Feb 2027 | Prepare the 8 Feb session | AI-credit rule evaluation on the pilot's final data (headline vs narrow count, a sample of lab-affiliation-only credits, spot checks) and the PHP2Shell case note docs/cases/php2shell.md. Send the author a heads-up. |
| Tue 02 Mar 2027 | Record the confirmed reviewer | Add the reviewer as a contributor (name or initials as they asked, ORCID) to .zenodo.json and the report template; record their disclosed ties for publication beside the review. Never put their email or phone in the public repository. |
| Tue 02 Mar 2027 | Send the reviewer the practice second-coder sheet (pilot quarter) | python -m snapshot.agreement sample --batch 2026Q4; send the sheet (not the weights file) and the written rules. Unscored practice; score it only to discuss on the onboarding call. |
| Fri 02 Apr 2027 | Send the reviewer the Q1 2027 review packet | Once the provisional Q1 2027 report is approved: links to the report, the registered plan, prereg/DEVIATIONS.md, the data bundle and the exact code commit; the worksheet for every headline figure; the sample of hand decisions with their rules; a short review template (holds up / doesn't / would change). Ask the reviewer for a seed number and run the spot-check draw with it (three figures); send them the result. Never choose the figures. |
| Sat 01 May 2027 | Publish the external review beside the Q1 2027 final report | Review unedited, the author's response, the reviewer's disclosed ties and credit; archived with the release (Zenodo). Send the reviewer the link. |
| Wed 01 Mar 2028 | Draft the first annual check against reference data (2027) | prereg section 13: exposure reference if scan data was obtained by 31 Jan, harm reference always. For the author's approval at the 15 March 2028 review. |
| Sat 01 Apr 2028 | 2027 closing re-run with full follow-up | Re-run all four 2027 quarters once every 2027 cohort CVE has its 90-day follow-up; publish as a completeness addendum to the annual check. Labels unchanged (decision item 21). The author approves. |

## GitHub (automatic): dated items

| When | What | Details |
|---|---|---|
| Tue 01 Dec 2026, 11:00 UTC | Dry run of the quarterly pull (Oct-Nov data) | Started by the Schedule workflow (December has no cron). Unscored. |

