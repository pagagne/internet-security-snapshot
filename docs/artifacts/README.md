# Project documents: repository copies and their Claude artifacts

The repository is the source of truth. Each Claude artifact is a shareable copy and a backup.
When one changes, change the other in the same session (`docs/OPERATIONS.md`).

| Repository file | Claude artifact | Kept in step how |
|---|---|---|
| `docs/HOW_IT_WORKS.md` | [How It Works and What It Will Show](https://claude.ai/artifact/CZcDzwVzYSvCjqDLCjgFwe) | Edit both |
| `docs/artifacts/methodology-report.md` | [Methodology Report](https://claude.ai/artifact/RQ1pS1mmZZoSL24SFDX7Fq) | Edited in the doc; re-export here |
| `docs/artifacts/technical-spec.md` | [Prototype Technical Spec](https://claude.ai/artifact/7xFEbdxzh7eet3vbGjJvdG) | Edited in the doc; re-export here |
| `docs/artifacts/statistical-review-2026-10-24.md`, `...-review-points.md` (and `docs/STATISTICAL_REVIEW_2026-10-24.md`) | [Statistical Review of EVAL-2026-ISS-01](https://claude.ai/artifact/Jvtt3BWPFJeVvHb5pUmfSA) | Fixed record of 24 Oct |
| `docs/artifacts/listening-version.md` | [Listening Version](https://claude.ai/artifact/DF97QSNCnCpLDMc3a6Vcz3) | Fixed record of 20 Oct |
| `docs/artifacts/october-assessment-*.md` | [Is AI Cleaning Up the Internet?](https://claude.ai/artifact/MW5YmRTzi4VZpqmYhAibMG) | Fixed record (reconciled in `docs/RECONCILIATION_2026-10.md`) |
| `docs/artifacts/combined-report-2026.md` | [Combined Report](https://claude.ai/artifact/FFMzZZivpEHetjQefrQGgL) | Fixed record of 18 Oct |
| `docs/ANNUAL_PLAN.md` | Annual Plan (backup page) | Regenerated from `docs/schedule/schedule.yaml`; republish the backup after changes |
| `apps/hand-check.html` | [Snapshot Hand Check app](https://claude.ai/artifact/C5bsQdxdWcrM9tNTJfY5CB) | Edit the file, `read` the artifact, republish; answers stay in the app's database |

Not in the repository (the repository is public): the reviewer invitation letter, which is a
personal letter. It is kept as a Claude artifact only.

Exports were made on 24 Oct 2026 and checked for keys, tokens and private data before commit.
