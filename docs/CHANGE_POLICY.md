# Change policy: locked core and add-on layer

The study keeps a stable baseline while still learning new things by keeping two layers apart.

## 1. Locked core (baseline `core-v1.1`)

The seven tracking questions, the cohort rule (`config/cohort_rules.yaml`), the AI-credit
term list (`config/ai_credit_terms.yaml`) and the root-cause map
(`config/root_cause_map.yaml`), together with the frozen pre-registration. These are
computed the same way every quarter and alone decide the Improving/Worsening and
Rising/Falling labels.

The baseline includes the four changes logged in `prereg/DEVIATIONS.md` on 20–21 October
2026, all made before any result or cohort existed. Git tag `core-v1.1` marks it.

Checksums of the locked files are in `prereg/LOCKED.yaml`. `tests/test_locks.py` runs on
every push and fails if a locked file changes without its checksum and a dated deviation
row being updated, so no core change can happen quietly.

## 2. Add-on (exploratory) layer

New measures, breakdowns and data sources go in `config/exploratory.yaml`, each with a
dated entry. They appear in a separate "Exploratory" section of the quarterly report, are
clearly labeled, and never decide a label or change the cohort (`feeds_labels: false`,
enforced by a test). They can be added at any time.

## 3. Raw data is kept

Every quarterly pull freezes the full raw inputs with checksums. A question added later
can usually be answered for earlier quarters from those bundles, so starting late does not
lose history. Where a source only keeps aggregates (ransomware.live), only the aggregates
exist to go back to.

## 4. Changing the core

A core change is made only when it fixes an error or a measure has stopped working. Then:

1. **Run both side by side.** Report the old and new versions together for four quarters
   (the length of the comparison window), as is already done for the AI-credit term list.
2. **Switch at the annual review.** Changes to the core, and promotion of an exploratory
   measure into the core, happen only at the March annual review.
3. **Log it.** Add a dated row to `prereg/DEVIATIONS.md`, update `prereg/LOCKED.yaml`,
   file an update on the OSF registration, and tag the new baseline (`core-v1.2`, …).

Bug fixes that change no rule (for example a parsing error) can be made at any time, but
are still logged as deviations if they change any published number.

## 5. Tags

- `prereg-v1.0`: the registered plan.
- `core-v1.1`, `core-v1.2`, …: each locked baseline.
- `snapshot-<quarter>-<provisional|final>`: the exact code and config used for each
  quarterly run, created by the quarterly workflow. Tags are never moved or deleted.

## 6. Run reports

Each quarterly or manual run saves its log, manifest and data quality report to the
`run-reports` branch (secret values scrubbed, no data bundle), so problems can be diagnosed
without signing in to GitHub. The data bundles themselves stay as run artifacts and are
archived on Zenodo with each final release.
