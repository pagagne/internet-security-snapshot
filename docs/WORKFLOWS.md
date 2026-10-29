# The study's workflows

Written 27 Oct 2026 at the author's request, from the explanation given that day; every workflow
was tested the same evening (`docs/WORKFLOW_REVIEW_2026-10-27.md`). The 14 Dec workflow review
(schedule item `workflows-doc`) adds failure handling and the lock list for decision item 22.

A workflow is a script GitHub runs for the study on its own computers: on a timer, when
something changes, or when the author or Claude starts it by hand. There are ten, in
`.github/workflows/`. All times are UTC.

**Run buttons (author's decision, 29 Oct 2026).** Workflows that work only inside the repository
(or with the author's own Drive) have a **Run workflow** button on the Actions page; clicking it
opens a box whose first line says what the workflow does. Workflows that contact anything
outside (data sources, SANS, Google BigQuery) have **no button**, so a stray click can never send
the study's traffic to a source: they run on their timer, or are started through GitHub's API
by the Schedule workflow (dry runs) or by Claude (probes). A test keeps it that way. When each may
be run by hand after the pilot: `docs/SOP_MANUAL_RUNS.md`.

| With a Run button | API only (no button) |
|---|---|
| Checks, Privacy scan, Schedule, Rebuild check, Diagrams, Backup | Quarterly pull, Research probe, Honeypot capture, BigQuery check |

## At a glance

| Workflow | File | Starts | Can change | Secrets | Tested |
|---|---|---|---|---|---|
| Quarterly pull | `quarterly-pull.yml` | 06:00 on 1 Jan/Apr/Jul/Oct (provisional) and 1 Feb/May/Aug/Nov (final); Schedule (dry runs); no button | repository (tags, run-reports) | NVD, Cloudflare, SEC user agent, ransomware.live, VulnCheck, Drive | 27 Oct, run 40583009106 |
| Rebuild check | `rebuild-check.yml` | 07:17 on the 10th of each month; Run button | run-reports | none | 27 Oct, run 40584529355 |
| Schedule | `schedule.yml` | 10:23, 12:07 and 15:37 daily; Run button | issues, run-reports, starts other workflows | none | 27 Oct, run 40583012321 |
| Checks | `checks.yml` | every push and pull request; Run button | nothing (read only) | none | 27 Oct, test push |
| Privacy scan | `privacy.yml` | 11:47 and 21:13 daily; Run button | issues, run-reports | none | 29 Oct |
| Backup | `backup.yml` | 10:17 on the 3rd of each month; Run button | nothing in the repository (writes to Drive) | Drive | 27 Oct, run 40583019078 |
| Research probe | `research.yml` | started by Claude through the API; no button | run-reports | GitHub token | 27 Oct, run 40583022560 |
| Honeypot capture | `honeypot.yml` | 09:43 on the 2nd of each month; no button | run-reports | none | 27 Oct, run 40586462028 |
| Diagrams | `diagrams.yml` | when a diagram source changes; Run button | nothing (read only) | none | 27 Oct |
| BigQuery check | `bigquery-check.yml` | started by Claude through the API; no button | nothing (read only); signs in to Google Cloud without a key | none (keyless sign-in) | 29 Oct |

## 1. Quarterly pull: the heart of the study

**When:** 06:00 on 1 January, April, July and October (the provisional run), and again a month
later (the final run). Dry runs (1 and 15 Dec) are started by the Schedule workflow through
GitHub's API. No Run button: it contacts every data source.

**What it does:**

1. Downloads every switched-on free source for the quarter (`config/sources.yaml`): CVE
   records, CISA's exploited list (KEV), Vulnrichment, NVD, EPSS, SEC breach filings,
   Cloudflare Radar, and ransomware.live (permission granted 27 Oct; counts only).
2. Freezes an exact copy with checksums.
3. Moves anything not yet allowed to be published (VulnCheck, once added, until it gives written
   permission) out of the public copy.
4. Counts any refusals from a source's server (HTTP 403 or 429, "server pushback") so the run
   report shows at once if a source starts treating the study's downloads as unwelcome.
5. Writes a data-quality report and the list for the author's hand check.

**What it produces:** the public bundle (kept on GitHub for 90 days), a tag marking the run, a
run report on the run-reports branch, and the full bundle, including the private part, in the
author's Google Drive folder under `runs/`.

## 2. Rebuild check: proves the numbers can be recomputed

**When:** monthly, and by hand after a pull (Run button).

**What it does:** takes a frozen bundle, builds the study's pinned software environment from
scratch, recomputes everything, and confirms the result matches what was stored. This is the
guarantee that anyone, years later, can reproduce the study's figures. Files kept privately are
skipped. On 27 Oct: "frozen files and recomputed figures match".

## 3. Schedule: the study's calendar, running itself

**When:** three times a day. Claude's daily work queue (8:32 ET) also starts it if it has not run
that day.

**What it does:** reads `docs/schedule/schedule.yaml` and opens a GitHub issue for each item that
falls due, for the author, for Claude, or for a review. On dry-run dates (1 Dec, 15 Dec) it starts
the quarterly pull itself. (Until 29 Oct it also ran the daily privacy scan, now its own
workflow: section 10.)

## 4. Checks: the safety net on every change

**When:** every push to main and every pull request, and by hand (Run button, since 29 Oct).

**What it does:** runs all the tests (122 on 29 Oct). They include the test confirming the locked
pre-registration core has not been altered, and checks that the schedule outputs are current,
the diagrams match their sources, and the privacy scan is clean. A second job builds the pinned
container. Since 27 Oct a ruleset requires both jobs to pass before a change lands on main,
with the author (repository admin) able to bypass it.

## 5. Backup: the private copy in Google Drive

**When:** the 3rd of every month, and by hand (Run button).

**What it does:** saves a complete copy of the repository (every branch and all history) as one
file in the author's Drive folder "Internet-Security-Snapshot-2027", under `repository/`. Started
by hand, it also writes a small test file under `tests/` to prove the connection works. Each
quarterly pull backs up its own data separately, as its last step. Setup: `docs/BACKUP.md`.

## 6. Research probe: the testing bench

**When:** only when Claude starts it through GitHub's API (no Run button: probes contact
outside sources).

**What it does:** runs one small experiment from a fixed list. Examples: how many flaws a vendor's
site gives fix dates for, how far CISA's list lags other lists, patch adoption from deps.dev, or
resource use. Results go to the run-reports branch under `research/`. This is how a new source is
tried before it joins the study.

## 7. Honeypot capture: attack activity from SANS

**When:** the 2nd of each month; monthly by the author's choice, to keep the load on SANS low. No
Run button (it downloads from SANS).

**What it does:** downloads the SANS Internet Storm Center web-honeypot files (about 1 GB) and
reduces them to counts by attack category and by flaw. It then discards the raw files: no IP
addresses and no attacked URLs are kept. About 40 KB of counts are saved to run-reports under
`data/isc-honeypot/`. This is exploratory context (X14) and never decides a result.

## 8. Diagrams: a cross-check for the pictures

**When:** whenever a diagram's Mermaid source changes, and by hand (Run button).

**What it does:** draws the diagram pictures and attaches them to the run as a download for
comparison. It can read the repository but not change it (since 27 Oct). Claude renders and
commits the actual PNGs together with each diagram change.

## 9. BigQuery check: the keyless Google Cloud sign-in

**When:** only when Claude starts it through GitHub's API (added 29 Oct 2026; no Run button:
it contacts Google).

**What it does:** signs in to the author's Google Cloud project **without any stored key**:
GitHub proves to Google that the run comes from this repository (Workload Identity Federation),
and Google returns a pass valid for that run only, for the `snapshot-bq` service account, which
may only run BigQuery queries. It then runs a free dry run against HTTP Archive and one tiny real
query capped at 10 MB. The same sign-in is used by the HTTP Archive and deps.dev work.

## 10. Privacy scan: keeps private things out of the public repository

**When:** twice a day, at 11:47 and 21:13 UTC (07:47 and 17:13 ET), and by hand (Run button).
Its own workflow since 29 Oct 2026 at the author's request; before that it was a step inside
Schedule. Checks also runs the same scan on every change.

**What it does:** reads every file on main and on the run-reports branch and looks for anything
that must never be public: keys, tokens and passwords (Google, GitHub, AWS and similar), private
key files, personal email addresses and phone numbers, and figures from sources not yet cleared
for publishing. A short list of public organisational addresses is allowed. If anything turns
up it opens one `privacy` issue for the author and Claude, giving only the kind of finding and
where it is, never the value itself. It scans the current files, not the old history: the
author decided on 27 Oct to leave the history of run-reports as it was (docs/PERMISSIONS.md).

## How they depend on each other

Added 29 Oct 2026 at the author's request, as the starting point for the 14 Dec lock list.

```
Claude work queue (08:32 ET, outside GitHub)
   └─ starts Schedule if it missed its daily run
Schedule (3x daily)
   ├─ opens the day's issues
   └─ 1 and 15 Dec: starts Quarterly pull (dry runs)
Quarterly pull (1 Jan/Apr/Jul/Oct provisional, a month later final)
   ├─ reads config/sources.yaml + the source keys (GitHub secrets)
   ├─ writes: tag, run report, 90-day bundle, Drive copy
   └─ its bundle feeds -> Rebuild check (the 10th): recomputes and must match
Checks: the gate on every change; nothing reaches main unless it passes
```

Standing alone (no other workflow depends on them): Privacy scan, Backup, Diagrams, Honeypot capture,
Research probe, BigQuery check. Shared by several: the run-reports branch (five workflows write
to it, each retrying if another writes at the same moment), the secrets, and the pinned
Python, actions and packages.

**What each one means to the study.** The author asked (29 Oct) that each workflow's function
be judged by how critical it is to the study; the 14 Dec review confirms or changes this.

| Workflow | Role | If it stopped working |
|---|---|---|
| Quarterly pull | **Core**: collects every quarter's data | No data for that quarter: the study's results stop. |
| Rebuild check | **Core**: proves the figures can be recomputed | Results still produced, but unverified; the reproducibility promise in the plan is broken. |
| Checks | **Core safeguard**: guards the locked plan and every change | Errors and changes to the locked core could reach main unnoticed. |
| Privacy scan | **Core safeguard**: keeps keys, personal details and unpublishable figures out of public view | A leak could stay public unnoticed until the next push (Checks scans every push, but not run-reports). |
| Schedule | **Support**: runs the calendar and the dry runs | Reminders and dry runs stop; the Claude work queue restarts it. The quarterly pulls still run on their own timer. |
| Backup | **Support**: monthly private copy in Drive | One fewer copy; the pull still saves its own data to Drive. |
| Diagrams | **Support**: cross-check of the pictures | None for the results; Checks still verifies the diagrams. |
| Honeypot capture | **Exploratory** (X14) | One exploratory context series pauses; core results unaffected. |
| Research probe | **Exploratory**: tries sources before they join | New sources can't be tested; core results unaffected. |
| BigQuery check | **Exploratory**: confirms the Google sign-in | The HTTP Archive and deps.dev work can't be checked; core results unaffected. |

The pilot (1 Jan provisional, 1 Feb final) needs Schedule -> Quarterly pull -> Rebuild check, with
Checks guarding every change. If any of the other five failed, the pilot would still run.

## How they fit together

Schedule keeps time, and Quarterly pull does the collecting. Rebuild check and Checks confirm
nothing went wrong. Backup and the pull's own backup step keep a private copy in Drive. Research
probe and Honeypot capture feed the exploratory side.

**Not a GitHub workflow:** Claude's daily work queue, a scheduled Claude task at 8:32 ET. It
checks that Schedule ran (and starts it if not) and picks up the items assigned to Claude.

**Also not a workflow:** Dependabot, GitHub's own watchman (switched on 29 Oct). It reads the
study's package list (`requirements.txt`, an exact copy of `requirements.lock`, 61 packages) and
raises an alert if any package gets a known security flaw. It only warns; automatic update
proposals are off, so nothing changes without the author. Turning it on added a tenth entry to the Actions
tab, **Dependency Graph**: GitHub's own built-in job (it has no file in `.github/workflows/`) that
re-reads the package list whenever `requirements.txt` changes; its runs are named "Graph Update:
pip in /". Two repository rules protect main: "protect main" (no deleting or rewriting
history; also on run-reports) and "require checks on main" (the Checks workflow must pass; the
author can bypass it).
