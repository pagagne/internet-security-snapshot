# Build plan to the December dry run

| By | Item | Status |
|---|---|---|
| 15 Nov | Reference dates for five validation cases (`prereg/ground_truth_reference.csv`) | done 2026-10-22 |
| 20 Nov | Cohort draw over real data; `review/baseline.csv` and quarterly review files; `review/decisions.csv` carry-over | builder done (`snapshot.review`); carry-over to do |
| 20 Nov | Drift checks in the quality report: expected fields present per source, counts compared with the previous run (from the `run-reports` branch), sharp changes flagged | done 2026-10-22 |
| 20 Nov | Pre-filled fix dates in review lists (GitHub releases, advisories, commits; else marked as assumed) | built 2026-10-22; first live test pending |
| 30 Nov | Evaluation code: T1-T7 labels, bootstrap intervals, exploratory X1-X12. Built 2026-10-22: events (`snapshot.events`), validation (`snapshot.validate`), T1(a)/T3 (`snapshot.race`), T7 range and programme-evidence figure (`snapshot.t7`), consistency rate | in progress |
| 30 Nov | Draft evaluation page for the dry run | to do |
| 30 Nov | Root cause: fill missing CWEs from Vulnrichment then NVD (registered source order) in the evaluation | to do |
| 20 Nov | Picks recorded "no fix yet" return to the review list for a fix date in later runs (within the 90-day follow-up) | done 2026-10-22 |
| 16 Nov | Validation batch in the Hand Check app: the author records fix dates for the reference CVEs before opening the reference file | to do |

Author checkpoints: 16 Nov reference-date spot check, 23-24 Nov baseline-year hand check (two sessions),
1 Dec dry run, 2 Dec dry-run hand check, 4 Dec landing page.
