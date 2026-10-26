# Sync review: keeping everything in step

A repeatable check that the repository, the Claude docs, the calendars, the scheduled tasks
and the Reviewer's Desk all say the same thing. First run 24 Oct 2026 at the author's request.
Scheduled weekly until the 30 Nov 2026 cutover, then three days before each provisional report
(`sync-review` and `sync-review-quarterly` in `docs/schedule/schedule.yaml`), and on request.

Many checks already run on every push (Checks workflow): tests, schedule outputs (plan, both
calendar feeds, README table, the Desk's task list), diagram review stamps, the reviewer feed
matching the full feed, and the Desk's copy of the sample inputs. The review covers what those
cannot see.

## Pass 1: the repository
1. `git log` since the last review: list every change; anything not on main (open PRs, branches
   left to delete).
2. `pytest -q`, `python -m snapshot.schedule check`, `python -m snapshot.diagrams check`: all clean.
   For a diagram warning, compare the diagram with the files it depends on, fix, redraw
   (Diagrams workflow) and re-stamp.
3. Search the docs for statements that may have gone stale: dates that differ from
   `docs/ANNUAL_PLAN.md`, "by hand", "goes public", "not yet", "to do" items that are done,
   names of files or tasks that no longer exist.
4. Overlaps and gaps in `docs/schedule/schedule.yaml`: two items doing the same job, an item
   that depends on something not yet in place (for example a task for someone not yet
   confirmed), a decision that needs an author item.

## Pass 2: sync between places
5. Claude docs against their repository copies (map: `docs/artifacts/README.md`): export each
   doc as markdown and diff it with its copy. Differences other than repo-internal links are
   fixed in both places.
6. Pictures in the Claude docs that were drawn from repository diagrams: replace any that were
   redrawn since.
7. The author's Google Calendar: subscribed to the feed; no hand-made "Snapshot:" events added
   since (any found are moved into the schedule and removed, with the author's agreement).
8. Scheduled tasks (Claude account): the work queue is enabled and its prompt matches
   `docs/OPERATIONS.md`; one-off check-ins are still needed, and none duplicate a schedule item
   after the cutover.
9. GitHub issues: open `schedule` issues match what is due; done work is closed with a comment.
10. The README's data-source tables match `docs/PERMISSIONS.md` (status of every request) and the
    switches in `config/sources.yaml` (a test checks the switches against PERMISSIONS.md).
11. Claude project docs (`claude/operations.md`, `claude/annual-plan.md`,
    `claude/handover-session-1.md`): re-upload any whose repository file changed.

## Pass 3: things that run on their own
12. Workflow runs since the last review (Actions API and `reports/log/` on the `run-reports`
    branch): every scheduled run happened and passed; any failure explained.
13. The next automatic events (the next dispatched run, the next cron run): their inputs,
    permissions and dates are right.
14. The Reviewer's Desk: open it in a browser, exercise each tab, check the task list and the
    worksheets list; republish the private preview if `site/reviewer/` changed.

## Findings
Send the author one message with four lists, each item one short descriptive line:
- **Confirmed**: checked and correct.
- **Fixed**: what was wrong, where, and what it says now.
- **Conflicts resolved**: where two sources disagreed, which one was kept and why.
- **Still for you**: anything only the author can do, with a date where there is one.

Any questions for the author are asked together, at the end, in one list (or one question
card), never spread across messages.
