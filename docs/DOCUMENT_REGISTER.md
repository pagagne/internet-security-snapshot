# Critical documents register (updated 16 Nov 2026)

The documents the study depends on: what each is for, who keeps it, where every copy lives,
whether it is a **reference** document (rules and procedures, changed rarely and deliberately) or
a **living record** (changes as the study runs), and when it locks. Built 16 Nov 2026 at the
author's request; kept current at every sync review until the lock. After the pilot, Claude cleans
up this list and checks every cross-reference by 10 Feb 2027; the author approves the lock on
17 Feb 2027 (schedule items `document-cleanup` and `document-lock`). What exactly locks is decided
then (the "Locks" column below is the current proposal).

Copies: **P** = Claude project doc (`claude/...`), **A** = Claude artifact or Claude Doc (links in
the private artifact map, `exploratory/docs/artifacts/README.md`), **D** = Drive. "Private" means
the private repository `pagagne/snapshot-manual`; everything else is in this public repository.

## 1. The registered study (already locked)

| Document | Purpose | Keeper | Copies | Kind | Locks |
|---|---|---|---|---|---|
| `prereg/PREREGISTRATION.md` | The registered plan (OSF DOI 10.17605/OSF.IO/3XT82) | Author | OSF | Reference | Locked since 20 Oct 2026 (`prereg/LOCKED.yaml`) |
| `prereg/LOCKED.yaml` | Checksums of the locked core | Claude | - | Reference | Changes only with a deviation |
| `prereg/DEVIATIONS.md` | Every change to the registered plan | Claude, author approves | - | Living (new entries only) | Entries never edited; locked with the procedures in Feb 2027 |
| `prereg/ground_truth_reference.csv` | Validation answers, recorded in advance | Claude | - | Reference | Locked (written before the run) |

## 2. How the study is run

| Document | Purpose | Keeper | Copies | Kind | Locks |
|---|---|---|---|---|---|
| `docs/schedule/schedule.yaml` | Every dated task by owner; the single source for dates | Claude | Calendar feed, README table | Living | Never (dates move by logged edits) |
| `docs/ANNUAL_PLAN.md` | The schedule as one table (generated) | Generated | P `annual-plan.md` | Living | Never (generated) |
| `docs/OPERATIONS.md` | How the study runs without one chat | Claude | P `operations.md` | Reference | Proposed: 17 Feb 2027 |
| `docs/SOP_MANUAL_RUNS.md` | Running workflows by hand; the one-primary-chat procedure | Claude, author adopts | P `sop-manual-runs.md` | Reference | Adopted 8 Feb 2027; proposed lock 17 Feb |
| `docs/WORKFLOWS.md` | What each workflow does and how critical it is | Claude | P `workflows.md` | Reference | Workflows lock 29 Dec 2026; this page 17 Feb 2027 |
| `docs/SYNC_REVIEW.md` | Checklist that keeps copies in step | Claude | - | Reference | Proposed: 17 Feb 2027 |
| `docs/HANDOVER.md` | Repository rules (24 Oct handover) | Claude | P `handover-session-1.md` | Reference | Proposed: 17 Feb 2027 |
| `docs/HAND_CHECK.md` | Written rules for the hand decisions | Claude, author approves | - | Reference | Proposed: 17 Feb 2027 |
| `docs/CHANGE_POLICY.md` | How anything locked may change | Author | - | Reference | Locked with the core, 29 Dec 2026 |
| `docs/PRIVACY.md` | Private by design | Claude | - | Reference | Proposed: 17 Feb 2027 |
| `docs/DOCUMENT_REGISTER.md` | This register | Claude | - | Reference | Locked last, 17 Feb 2027 |

## 3. Handover and the primary chat (private)

| Document | Purpose | Keeper | Copies | Kind | Locks |
|---|---|---|---|---|---|
| `START_HERE_NEW_CHAT.md` (private root) | Short reference for a new chat: setup, reading order, where things stand, tasks to recreate | Primary chat | P `START-HERE-NEW-CHAT.md` | Living (status section) | Sections 1-4 and 7 proposed for 17 Feb 2027; status stays open |
| `PRIMARY_CHAT.md` (private root) | Names the primary chat | Primary chat | P `PRIMARY-CHAT.md` | Living | Never (changes on promotion) |
| `PROJECT_INSTRUCTIONS.md` (private root) | Source text of the project's custom instructions | Primary chat, author pastes | Project settings | Reference | Proposed: 17 Feb 2027 |
| Project doc `claude/WHATS-DUE.md` | Next two weeks by owner (from the schedule) | Primary chat, each morning | - | Living | Never (generated) |

## 4. Methods and decisions

| Document | Purpose | Keeper | Copies | Kind | Locks |
|---|---|---|---|---|---|
| `docs/HOW_IT_WORKS.md` | Plain-language overview | Claude | A How It Works | Reference | Proposed: 17 Feb 2027 |
| `docs/EVALUATION_FLOW.md` | How the data flows to each measure | Claude | - | Reference | Proposed: 17 Feb 2027 |
| `docs/RESEARCH_PLAN.md` | Research window and its findings | Claude | - | Record | Closed after the pilot; proposed lock 17 Feb 2027 |
| `docs/CORE_FREEZE_DECISIONS.md` | The 21 Dec decisions | Claude, author decides | - | Record | Closed after 21 Dec 2026 |
| `docs/decisions/*.md` | Decision sheets | Claude | - | Record | Each closes when decided |
| `docs/PILOT_EXPECTATIONS.md` | Expectations written before the pilot | Author | P `pilot-expectations.md` | Reference | Fixed record of 26 Oct 2026 |

## 5. Sources and permissions

| Document | Purpose | Keeper | Copies | Kind | Locks |
|---|---|---|---|---|---|
| `docs/PERMISSIONS.md` | Every data permission asked for and given | Claude | - | Living | Never (permissions change) |
| `docs/TERMS_OF_USE.md` | Each source's terms and request limits | Claude | - | Living | Never (terms change; watched weekly) |
| `config/sources.yaml` | Source switches (publish on or off) | Claude, author approves | - | Reference | With the core, 29 Dec 2026 |

## 6. Living records (never locked)

| Document | Purpose | Keeper | Copies |
|---|---|---|---|
| Session logs (private `exploratory/sessions/`) | What was asked, decided and done each day | Primary chat | P `session-logs.md` |
| Correspondence index | Every exchange with an outside organisation | Primary chat | P `correspondence.md`, D `correspondence/` |
| `docs/INQUIRIES.md` | News, ideas and how the plan handles them | Claude | - |
| Private `exploratory/docs/RISK_REVIEW.md` | Safeguards and the watch list | Claude | - |
| Private `exploratory/docs/artifacts/README.md` | Map of files to their Claude copies | Claude | - |
| `docs/cases/*.md` | Case notes | Claude | - |

## 7. The manual

"The Snapshot" (`config/manual.yaml`) assembles every study document into one private manual;
Checks fails if a document in the docs folders is left out of it. Since 16 Nov 2026 its private
edition also carries the three handover files of section 3. This register says which documents
are critical; the manual's contents page is the full index.
