# Workflow review, 27 Oct 2026 (security and function)

Asked by the author. Every workflow in `.github/workflows/` was read, linted (actionlint with
shellcheck: clean apart from three information notes on fixed file names), and the changed ones
were run on GitHub from the pull-request branch. Input for `docs/WORKFLOWS.md` (14 Dec) and the
workflow lock (decision item 22).

## Fixed (pull request #26)
| Finding | Risk | Fix |
|---|---|---|
| Run inputs pasted straight into shell scripts (quarterly pull, research, schedule, rebuild check) | Script injection by anyone able to start a run (today only the author and the workflows themselves) | Inputs passed as environment variables and checked against a pattern |
| Backup of each pull relied on a `workflow_run` chain | Runs started by the Schedule workflow's token may not trigger it, so dry runs could go un-backed-up | Each quarterly pull backs up its own full bundle and private part as its last step |
| Private split would make the rebuild check fail (manifest lists files no longer in the public bundle) | Monthly rebuild check failing every month | Manifests mark `kept_privately`; the rebuild check skips them (tested: passes) |
| Three daily Schedule timers can arrive together when GitHub runs late | Two runs racing to open the same issue twice | One Schedule run at a time (concurrency group); the same for the quarterly pull |
| Run-report and honeypot pushes had no retry | A clash with another run's push loses the report | Retry with rebase, as the research workflow already did |
| Jobs without time limits (Checks, Schedule, Diagrams) | A hung job holds a runner for 6 hours | 20-30 minute limits |
| Backup test listed every Drive file in the public log | File names of private backups visible | Top-level folder names only |
| `RCLONE_CONF` not in the run-report scrub list | None today (never printed); belt and braces | Added |

## Tested on GitHub (27 Oct, branch runs)
- Quarterly pull (Q3 2026, KEV and ransomware.live): passed; ransomware.live moved out of the
  public bundle, manifest marked, no figures in the public run report or quality report; the
  backup step warned that Drive is not set up yet.
- Rebuild check on that bundle: passed ("frozen files match").
- Schedule, dry run for 15 Dec: lists the full dry run and its three items, as planned.
- Research probe and Backup: passed (Backup: "not configured" until the author's token).

## Confirmed sound
- Every action pinned by commit SHA; Python packages installed with hashes; runner image pinned.
- Each workflow sets its own minimal permissions; secrets only where used; GitHub masks them
  in logs; pull requests from forks get no secrets and read-only access.
- Rulesets: `main` cannot be deleted or force-pushed; `prereg-*`, `core-*` and `snapshot-*` tags
  cannot be moved or deleted, but new tags can be created (the 1 Jan provisional tag will work).
- Secret scanning and push protection are on.

## Still open (for the author or later work)
1. **Locked-core guard only warns.** CODEOWNERS has no effect without a "require code owner
   review" rule, and a direct push to `main` is not blocked by a failing Checks run. Option: a
   ruleset requiring the Checks status on `main`, with the author and the workflows as bypass.
   Decided 27 Oct (author): added now as a separate ruleset "require checks on main" (jobs
   `test` and `container`) with the repository admin as bypass, so direct pushes continue and
   the Diagrams PNG push falls back to its artifact. Whether to drop the bypass is reviewed at
   the workflow lock (21 Dec).
2. **`run-reports` branch unprotected** (author adding it to "protect main", 27 Oct). Add it to the "protect main" ruleset (deletion and
   force push blocked); every workflow already pushes fast-forward only. One-minute settings
   change for the author.
3. **Dependabot alerts are off** (author turning alerts on, 27 Oct; no automatic updates). Turning on alerts (not automatic updates) warns of a
   vulnerable pinned package. Settings change for the author.
4. **Schedule starting the quarterly pull is untested end to end** (first real case: the
   1 Dec dry run). The 1 Dec Claude item checks it started and starts it by hand if not.
5. **Diagrams installs the Mermaid renderer from npm** with write access to `main`; low risk
   (pinned version), could be pinned by lockfile.
6. **Not built yet:** the Pages workflow (by 27 Nov) and the Zenodo release (by 31 Dec).
7. Done 27 Oct: the architecture diagram shows the private Drive backup.
