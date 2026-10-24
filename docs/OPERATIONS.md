# Operations: how the study runs without depending on one Claude chat

From the **cutover on Mon 30 Nov 2026**, everything the annual study needs lives in this
repository. A Claude chat is a convenience, not a dependency: any new Claude session, or a
person, can pick up the work from the files and issues below.

## The three kinds of work

| Who | Where it comes from | How it is tracked |
|---|---|---|
| **Author** | `docs/schedule/schedule.yaml` (`owner: author`) | Shared calendar feed; a GitHub issue labelled `owner:author` opens two days before |
| **Claude** | `docs/schedule/schedule.yaml` (`owner: claude`) | A GitHub issue labelled `owner:claude` opens on the day; the daily Claude work-queue task picks it up |
| **GitHub (automatic)** | Workflow crons, plus `dispatch:` items in the schedule | Actions tab; dispatched runs leave a closed `owner:github` issue as a record |

The full list, grouped by owner, is `docs/ANNUAL_PLAN.md` (generated; do not edit by hand).

## The schedule is code
- **Source:** `docs/schedule/schedule.yaml`. Edit it, then run
  `python -m snapshot.schedule build`, which rewrites `docs/ANNUAL_PLAN.md` and the calendar
  feed `docs/schedule/snapshot.ics`. The Checks workflow fails if you forget.
- **Daily job:** `.github/workflows/schedule.yml` runs at 12:07 UTC. It opens each due
  author/Claude issue once (each issue carries a hidden `schedule-uid` marker, so reruns never
  duplicate) and starts any `dispatch:` run that has no cron of its own, such as the 1 Dec dry
  run. If a day is missed, the next run catches up on anything from the previous 6 days.
  Run it by hand from the Actions tab with a date and "dry run" to preview.
- **Automatic runs with their own cron:** Quarterly pull (1st of each month at 06:00 UTC,
  provisional and final), Rebuild check (10th monthly), Checks (every push).

## Shared calendar
Subscribe once; it then updates itself whenever the schedule changes (Google refreshes
subscribed calendars every few hours to a day):

Google Calendar › **Other calendars** › **+** › **From URL** ›
`https://raw.githubusercontent.com/pagagne/internet-security-snapshot/main/docs/schedule/snapshot.ics`

Every entry says who does it (Author, Claude or GitHub) in its description and category.
The older hand-made "Snapshot: ..." events in the author's own calendar can be deleted after
subscribing; the feed has them all.

## How a Claude session picks up work
1. Read this file, then `docs/HANDOVER.md` (repository rules and standing rules).
2. List open issues labelled `owner:claude`, oldest first. Each says what to do and points at
   the files involved. Do it, commit (small doc fixes to `main`; code by one pull request at a
   time), comment with what was done, and close the issue.
3. If an item needs the author, comment on the issue and, for anything time-critical, tell the
   author directly. Never guess at a decision listed for the author.
4. New work or changed dates go into `docs/schedule/schedule.yaml` (then `build`), not into a
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
- [ ] Author subscribed to the calendar feed.
- [ ] Claude work-queue task live and has confirmed it can see the queue.
- [ ] This file current.
- [ ] Remaining one-off check-ins in the original chat retired.

## Standing rules
See `docs/HANDOVER.md`. In short: no keys or tokens in chat or issues (GitHub secrets only);
VulnCheck-derived data private until written permission; ransomware.live aggregates only;
no scanning or host-level data; no project links shared publicly before 4 Dec 2026.
