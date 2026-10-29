# Operations: how the study runs without depending on one Claude chat

From the **cutover on Mon 30 Nov 2026**, everything the annual study needs lives in this
repository. A Claude chat is a convenience, not a dependency: any new Claude session, or a
person, can pick up the work from the files and issues below.

## The four kinds of work

| Who | Where it comes from | How it is tracked |
|---|---|---|
| **Author** | `docs/schedule/schedule.yaml` (`owner: author`) | Shared calendar feed; a GitHub issue labelled `owner:author` opens two days before |
| **External reviewer** | `docs/schedule/schedule.yaml` (`owner: reviewer`) | The reviewer's own calendar feed (below); no GitHub issues, since the reviewer is not a repository member. The author and Claude items around each reviewer task open issues as usual |
| **Claude** | `docs/schedule/schedule.yaml` (`owner: claude`) | A GitHub issue labelled `owner:claude` opens on the day; the daily Claude work-queue task picks it up |
| **GitHub (automatic)** | Workflow crons, plus `dispatch:` items in the schedule | Actions tab; dispatched runs leave a closed `owner:github` issue as a record |

The full list, grouped by owner, is `docs/ANNUAL_PLAN.md` (generated; do not edit by hand).

## The schedule is code
- **Source:** `docs/schedule/schedule.yaml`. Edit it, then run
  `python -m snapshot.schedule build`, which rewrites `docs/ANNUAL_PLAN.md`, the calendar
  feeds `docs/schedule/snapshot.ics` and `docs/schedule/reviewer.ics` and the Schedule table in `README.md` (from the
  `milestones:` list, which takes its dates from the items). The Checks workflow fails if you forget.
- **Daily job:** `.github/workflows/schedule.yml` runs at 10:23, 12:07 and 15:37 UTC, because
  GitHub drops scheduled runs at busy times (it skipped the 12:07 run on 25 and 26 Oct 2026).
  As a last safety net the daily Claude work queue (08:32 ET) starts it by hand if no run has
  succeeded that day. It opens each due
  author/Claude issue once (each issue carries a hidden `schedule-uid` marker, so reruns never
  duplicate) and starts any `dispatch:` run that has no cron of its own, such as the 1 Dec dry
  run. If a day is missed, the next run catches up on anything from the previous 6 days.
  Run it by hand from the Actions tab with a date and "dry run" to preview.
- Starting the API-only workflows (no Run button since 29 Oct: Quarterly pull, Research probe,
  Honeypot capture, BigQuery check): `gh api -X POST repos/pagagne/internet-security-snapshot/dispatches
  -f event_type=<research|quarterly-pull|honeypot|bigquery-check> -f 'client_payload[task]=...'`;
  the payload fields are listed at the top of each workflow file. Only when the author asked or
  the schedule says so.
- **Automatic runs with their own cron:** Quarterly pull (1st of each month at 06:00 UTC,
  provisional and final), Rebuild check (10th monthly), Checks (every push).

## The Reviewer's Desk
`site/reviewer/index.html` is the external reviewer's own page: what is due (from the same
schedule as the calendars, via `site/reviewer/tasks.json`), the spot-check draw and worksheets
with an automatic match check (and, for a reviewer who prefers it, a guided check that shows every step of the arithmetic, recorded as "guided"), a guided second-coder round that opens the quarter's answer file (CSV) and saves the completed file to send back, and
the April review steps with a draft template. Progress stays in the reviewer's browser; they
send results by copying or saving them. It goes live with GitHub Pages on 4 Dec 2026; until
then, a private preview is a Claude artifact. Worksheets are listed in
`site/reviewer/worksheets.json`; its `draw_from` list (the headline figures reported that
quarter) is what the reviewer's seeded draw picks from.

## Inquiry log
Questions about how the study would handle an outside event or source go in
`docs/INQUIRIES.md` (question, how the plan handles it, follow-up); they are weighed together
at the March review.

## Sync review
`docs/SYNC_REVIEW.md` is the checklist for keeping the repository, Claude docs, calendars,
scheduled tasks and the Reviewer's Desk in step: weekly until the cutover, then three days
before each provisional report, and on request. Questions for the author are always asked
together, in one list.

## Checking progress
- **Run log:** the Schedule and Rebuild check workflows add a line to
  `reports/log/<YYYY-MM>.md` on the `run-reports` branch after every run (when, result, link to
  the run, and a report file when something happened). The quarterly pull saves its full log,
  manifests and quality reports there too. Anyone can read this branch on GitHub, and a Claude
  session can read it with `git fetch origin run-reports` (Claude sessions cannot download
  Actions logs, only see whether a run passed).
- **Issues:** open `schedule` issues are what is due now; closed ones are what was done, with
  a comment saying how.

## Shared calendar
Subscribe once (one click, while signed in to Google:
[add to Google Calendar](https://calendar.google.com/calendar/render?cid=https%3A%2F%2Fraw.githubusercontent.com%2Fpagagne%2Finternet-security-snapshot%2Fmain%2Fdocs%2Fschedule%2Fsnapshot.ics),
or by hand as below); it then updates itself whenever the schedule changes (Google refreshes
subscribed calendars every few hours to a day):

Google Calendar › **Other calendars** › **+** › **From URL** ›
`https://raw.githubusercontent.com/pagagne/internet-security-snapshot/main/docs/schedule/snapshot.ics`

Every entry's title starts with who is responsible ([Paul], [Reviewer], [Claude] or [GitHub]),
and its description repeats it. `docs/ANNUAL_PLAN.md` has the same list as one table with a
"Who is responsible" column.

**The external reviewer's feed** holds only the reviewer's tasks and the author/Claude items
they depend on (onboarding call, review packet, publication). Send it to the reviewer once they
confirm (1 Mar 2027); it subscribes the same way:
`https://raw.githubusercontent.com/pagagne/internet-security-snapshot/main/docs/schedule/reviewer.ics`
(Google: [add with one click](https://calendar.google.com/calendar/render?cid=https%3A%2F%2Fraw.githubusercontent.com%2Fpagagne%2Finternet-security-snapshot%2Fmain%2Fdocs%2Fschedule%2Freviewer.ics); Outlook and Apple Calendar: "subscribe from web" with the URL).
It names no one: the reviewer's name, email and phone never go in the repository.
The author subscribed on 24 Oct 2026, and the older hand-made "Snapshot: ..." events were
removed from the author's own calendar the same day (all of them are in the feed). Add new
dates to the schedule file, never as hand-made calendar events, so the calendars cannot drift.

## How decisions are put to the author
(Author's preference, 26 Oct 2026.) Questions go together, never spread across messages: as
option cards in chat (two to four options, the recommendation first and marked), and for a
meeting as a decision sheet in `docs/decisions/` (question, options, recommendation, evidence)
linked from the calendar entry. News and ideas the author raises go to `docs/INQUIRIES.md`
the same day, and anything needing a decision is added to the next meeting's sheet.
The author listens to replies with a read-aloud tool (29 Oct): chat replies are written mostly in
plain sentences, with tables, code and long links kept in the documents and PDFs. Option cards
cannot be read aloud, so before each card the same questions and options, with the
recommendation, are sent as a plain message he can listen to.
Every email or form exchange with an outside organisation about the study (data sources,
reviewers, universities) is recorded the day it is sent or received (author, 28 Oct): the full
text in the private Drive folder `correspondence/`, an index in the Claude project
(`claude/correspondence.md`), and a summary without personal contact details in
`docs/PERMISSIONS.md` (permissions) or `docs/INQUIRIES.md` (everything else). The author
forwards or attaches the email; Claude does the filing.
At the end of each working day the session writes a log in `docs/sessions/<week>/` (weekly folders,
Sunday to Saturday, named like `2026-10-25_to_2026-10-31`; what was asked,
decided and done, with the day's workflow runs) and copies it to the Claude project.
When the author is next online (usually the following morning), the session opens by
presenting that report in chat: what was accomplished, what carried over, and what is due
that day (author's request, 27 Oct).

## Private by design
(Decided 27 Oct 2026.) The repository stays public. Three rules keep private material out of it:
1. A source whose `publish` switch is off (`config/sources.yaml`) never appears in a public
   run download, run report or quality report; the quarterly pull moves it to the author's
   private Drive backup (`snapshot.private`, `docs/BACKUP.md`).
2. Personal and third-party details (candidates, contacts, family, private emails) stay in the
   Claude project or Drive; repository documents describe people by role.
3. Embargoed or not-yet-public vulnerability information never enters the repository.

Periodic checks (27 Oct 2026): the privacy scan (`snapshot.privacy`) runs on every push
(Checks), twice a day on `main` and `run-reports` (its own Privacy scan workflow since 29 Oct, with a Run
button; findings open a `privacy` issue),
and in each sync review together with a reading of new logs for what patterns cannot catch.

## How a Claude session picks up work
(In a Claude session GitHub's GraphQL API is blocked, so use `gh api` REST calls rather than
`gh issue`, `gh pr` or `gh workflow run`. The Schedule workflow itself runs on GitHub and is
not affected.)

1. Read this file, then `docs/HANDOVER.md` (repository rules and standing rules).
2. If the Schedule workflow has no successful run today, start it
   (`gh api -X POST repos/pagagne/internet-security-snapshot/actions/workflows/schedule.yml/dispatches -f ref=main`)
   so today's issues exist.
3. List open issues labelled `owner:claude`, oldest first. Each says what to do and points at
   the files involved. Do it, commit (small doc fixes to `main`; code by one pull request at a
   time), comment with what was done, and close the issue.
4. If an item needs the author, comment on the issue and, for anything time-critical, tell the
   author directly. Never guess at a decision listed for the author.
5. New work or changed dates go into `docs/schedule/schedule.yaml` (then `build`), not into a
   chat reminder.

The daily **Claude work-queue** scheduled task (on the author's Claude account) does exactly
this and ends silently when no `owner:claude` issue is open. Until the cutover it only
confirms it can see the queue; the original chat's check-ins handle 26 Oct, 20 Nov and 25 Nov.

## Documents: repository first, artifacts as backup
- The repository is the **source of truth** for every project document. The Claude artifacts
  (the author's Claude artifacts list) are readable, shareable copies and a backup.
- When a document changes, change the repository file and the artifact in the same session.
  `docs/artifacts/README.md` maps each file to its artifact and says which way it is kept in
  step.
- The Hand Check app's answers live in the app's own database; the app's source is
  `apps/hand-check.html`.

## Cutover checklist (30 Nov 2026; issue opens that day)
- [ ] Schedule workflow green for 7 days in a row.
- [x] Author subscribed to the calendar feed (24 Oct 2026).
- [ ] Claude work-queue task live and has confirmed it can see the queue.
- [x] Private Google Drive backup configured and tested (`docs/BACKUP.md`; 27 Oct 2026).
- [ ] This file current.
- [ ] Remaining one-off check-ins in the original chat retired.

## Standing rules
See `docs/HANDOVER.md`. In short: no keys or tokens in chat or issues (GitHub secrets only);
VulnCheck-derived data private until written permission; ransomware.live aggregates only;
no scanning or host-level data; no project links shared publicly before 4 Dec 2026.
