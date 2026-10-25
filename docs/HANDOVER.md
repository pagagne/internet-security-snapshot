# Handover: session 1 to the continuing session (24 Oct 2026)

> **Since 24 Oct:** day-to-day work is driven from the repository. Start with
> `docs/OPERATIONS.md` (how any session picks up work) and `docs/ANNUAL_PLAN.md` (every action
> item by owner). Dates below are kept for the record; `docs/schedule/schedule.yaml` is current.

From now on, **one Claude session works on this repository, the author's calendar and the
artifacts below**. This file and the project doc `claude/handover-session-1.md` hold what the
new session needs. Read this first, then `docs/BUILD_PLAN.md`, `docs/RESEARCH_PLAN.md` and
`docs/CORE_FREEZE_DECISIONS.md`.

## Repository
- `main` is the only working branch (plus `run-reports` for run logs). Push to `main` directly or
  via pull requests the author merges. Avoid side branches: this workspace's GitHub proxy can
  push them but cannot delete them.
- Workflows: Checks (tests, locked-core guard, stale-diagram warning), Quarterly pull,
  Diagrams (redraws PNGs from `docs/diagrams/*.mmd`), Research probe, plus the pinned-container
  checks added 24 Oct.
- After editing a diagram source or any file it depends on: review it, then run
  `python -m snapshot.diagrams stamp <name>` (`docs/diagrams/sources.json`). The architecture
  diagram is drawn by `tools/architecture_svg.py`, not Mermaid.
- Locked core: `prereg/LOCKED.yaml` (includes `config/ai_credit_auto_accept.yaml` since 23 Oct).
  Any change needs a dated row in `prereg/DEVIATIONS.md` and a new checksum.
- Test data used in session 1 (CVE, KEV, EPSS extracts) lived in that session's scratch space and
  is gone; re-pull through the workflows when needed.

## Artifacts (all private to the author)
| Artifact | Link | Notes |
|---|---|---|
| Snapshot Hand Check (app) | https://claude.ai/artifact/C5bsQdxdWcrM9tNTJfY5CB | Source `apps/hand-check.html` (version 14). Answers live in the app's own database. A new session must `read` the artifact before republishing it. |
| The Internet Security Snapshot: How It Works and What It Will Show (Claude Doc) | https://claude.ai/artifact/CZcDzwVzYSvCjqDLCjgFwe | Same text as `docs/HOW_IT_WORKS.md`; keep both in step. PDF built from the markdown with pandoc and headless Chromium. |
| Methodology Report | https://claude.ai/artifact/RQ1pS1mmZZoSL24SFDX7Fq | Steps 10-11 updated 22 Oct; not updated since. |
| Prototype Technical Spec | https://claude.ai/artifact/7xFEbdxzh7eet3vbGjJvdG | "Changes since registration" section from 22 Oct; not updated since. |
| Quarterly Internet Security Snapshot: Listening Version | https://claude.ai/artifact/DF97QSNCnCpLDMc3a6Vcz3 | 20 Oct. |
| Is AI Cleaning Up the Internet? (the October assessment) | https://claude.ai/artifact/MW5YmRTzi4VZpqmYhAibMG | Reconciled in `docs/RECONCILIATION_2026-10.md`. |
| AI and the Internet's Security Posture: Combined Report | https://claude.ai/artifact/FFMzZZivpEHetjQefrQGgL | Not updated since 18 Oct. |

## Calendar (as of the handover; superseded)

> Since 24 Oct the calendar is the subscribed feed generated from `docs/schedule/schedule.yaml`;
> the hand-made events listed below were removed. Kept for the record.

12 Nov research review (includes the decision on race hand-check effort) · 16 Nov validation ·
20 Nov permission follow-ups · 23-24 Nov baseline hand check · 1 Dec dry run · 2 Dec dry-run hand
check · 3 Dec move the pull into the container (added by the other session) · 4 Dec landing page,
Discussions, Zenodo, delete leftover branch · 21 Dec decision session · 29 Dec freeze ·
quarterly: 2nd Jan/Apr/Jul/Oct approve draft and open the 4th-28th hand-check window; 25th
reminder; 2nd Feb/May/Aug/Nov final-run check · 12 Jan 2027 line up the external reviewer ·
8 Feb 2027 AI-credit rule evaluation and PHP2Shell case · 15 Feb Censys application ·
15 Mar annual review (yearly). Descriptions were updated 24 Oct to the current rules.

## Scheduled check-ins to recreate in the new session
Session 1's check-ins fired into session 1 and were removed when it was retired. Recreate them
(one-off messages to the new session):

| When (UTC) | What |
|---|---|
| 2026-10-26 13:00 | Continue the research window (`docs/RESEARCH_PLAN.md`): item 5 (an on/off switch per permissioned source in config), then item 4 (remaining evaluation code: labels T2, T4-T6; X6-X12; NVD root-cause fill; draft evaluation page); consider the CISA active-exploitation first-assessment date as a research-flag T_exploit candidate; then Plan 1 / Plan 2 research. Message the author only for findings worth knowing. |
| 2026-11-20 14:00 | Permission follow-ups: read `docs/PERMISSIONS.md`; ask which of ransomware.live (ticket #3425), VulnCheck (community@vulncheck.com) and Shadowserver ([Ticket #pqaytmyy], contact@shadowserver.org) replied; draft polite follow-ups; update the log. Cutoff is the 21 Dec session (decision item 16). |
| 2026-11-25 14:00 | Before the dry run: the Hand Check app's "Race: newly attacked flaw" fix-date list (list builder in `snapshot.review`, report table, time estimate) built, tested and published, alongside `snapshot.race.t1_kev_race` and X10. Tell the author only if something will not be ready for 1-2 Dec. |
| 2027-02-03 14:00 | Prepare the 8 Feb session: AI-credit rule evaluation on the pilot's final data (headline vs narrow count, sample of lab-affiliation-only credits, spot checks) and the PHP2Shell case note `docs/cases/php2shell.md` (watch case in `docs/RESEARCH_PLAN.md`); send the author a heads-up. |

## Decisions made in session 1 (all logged)
- Race (T1a): days from fix to first attack over every flaw first added to CISA KEV in the quarter;
  zero-day share stays exploratory (X10) until a year of data (23 Oct).
- AI credits: headline counts any mention of an AI tool or frontier AI lab; the registered
  tool-named count is kept as the low end; trend only when both agree; re-evaluated 8 Feb 2027 (23 Oct).
- Provisional reports: drafted on the 1st, published after the author's review within two days;
  hand-check window 4th-28th (23 Oct).
- External reviewer for Q1 2027 (decision item 17; confirm by 15 Mar, review 3-28 Apr).
- Decided items 0, 7 and 12 only need confirming at the 21 Dec session.

## Open for the author
- 12 Nov: every flagged race fix date or a sample (sets the quarterly and baseline workload).
- 21 Dec agenda: `docs/CORE_FREEZE_DECISIONS.md` (items 1-22; 22 = the workflow lock, added 25 Oct).

## Standing rules (unchanged)
Never paste keys or tokens into chat (GitHub secrets only); VulnCheck-derived data private until
written permission; ransomware.live aggregates only, no victim names, no polling more often than
every 30 minutes; no scanning or host-level data; the Censys application is written by the author;
research organisations, not individuals; no project links shared publicly before 4 Dec.
