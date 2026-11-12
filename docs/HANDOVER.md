# Handover: session 1 to the continuing session (24 Oct 2026) (updated 12 Nov 2026)

> **NEW CHAT? This is not the starting point.** A new Claude chat taking over the study starts
> with **START HERE: NEW CHAT**, the file `START_HERE_NEW_CHAT.md` (private repository
> `pagagne/snapshot-manual`, root; copy in the Claude project as `claude/START-HERE-NEW-CHAT.md`).
> It has the setup steps, the reading order, how the author works, the standing rules, where
> things stand, and the scheduled tasks to recreate (author's request, 11 Nov 2026; procedure in
> `docs/SOP_MANUAL_RUNS.md`, section 7). Read this file after it, for the repository rules below;
> the rest is the 24 Oct handover, kept for the record.

From now on, **one Claude session works on this repository, the author's calendar and the
artifacts below**. This file and the project doc `claude/handover-session-1.md` hold what the
new session needed on 24 Oct. (Then: read this first, then `exploratory/docs/BUILD_PLAN.md`, `docs/RESEARCH_PLAN.md` and
`docs/CORE_FREEZE_DECISIONS.md`. Now superseded by START HERE.)

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
<!-- date:permission-follow-ups-exploratory -->13 Nov<!-- /date --> permission follow-ups · 23-24 Nov baseline hand check · <!-- date:dry-run -->1 Dec<!-- /date --> dry run · 2 Dec dry-run hand
check · 3 Dec move the pull into the container (added by the other session) · <!-- date:landing-page -->4 Dec<!-- /date --> landing page,
Discussions, Zenodo, delete leftover branch · <!-- date:freeze-session -->21 Dec<!-- /date --> decision session · <!-- date:freeze -->29 Dec<!-- /date --> freeze ·
quarterly: 2nd Jan/Apr/Jul/Oct approve draft and open the 4th-28th hand-check window; 25th
reminder; 2nd Feb/May/Aug/Nov final-run check · 12 Jan 2027 line up the external reviewer ·
<!-- date:ai-rule-session -->8 Feb 2027<!-- /date --> AI-credit rule evaluation and PHP2Shell case · Censys application sent 28 Oct 2026, declined 10 Nov (reapply decided 15 March 2027) ·
15 Mar annual review (yearly). Descriptions were updated 24 Oct to the current rules.

## Scheduled check-ins to recreate in the new session
Superseded (11 Nov 2026): the current list, with each task's full message, is section 6 of
`START_HERE_NEW_CHAT.md` in the private repository.

## Decisions made in session 1 (all logged)
- Race (T1a): days from fix to first attack over every flaw first added to CISA KEV in the quarter;
  zero-day share stays exploratory (X10) until a year of data (23 Oct).
- AI credits: headline counts any mention of an AI tool or frontier AI lab; the registered
  tool-named count is kept as the low end; trend only when both agree; re-evaluated 8 Feb 2027 (23 Oct).
- Provisional reports: drafted on the 1st, published after the author's review within two days;
  hand-check window 4th-28th (23 Oct).
- External reviewer for Q1 2027 (decision item 17; confirm by 1 Mar (was 15 Mar; moved 24 Oct), review 3-28 Apr).
- Decided items 0, 7 and 12 only need confirming at the <!-- date:freeze-session -->21 Dec<!-- /date --> session.

## Open for the author
- 12 Nov: every flagged race fix date or a sample (sets the quarterly and baseline workload).
- <!-- date:freeze-session -->21 Dec<!-- /date --> agenda: `docs/CORE_FREEZE_DECISIONS.md` (items 1-22; 22 = the workflow lock, added 25 Oct).

## Standing rules (unchanged)
Never paste keys or tokens into chat (GitHub secrets only); VulnCheck-derived data private until
written permission; ransomware.live aggregates only, no victim names, no polling more often than
every 30 minutes; no scanning or host-level data; the Censys application is written by the author;
research organisations, not individuals; no project links shared publicly before <!-- date:landing-page -->4 Dec<!-- /date -->.
