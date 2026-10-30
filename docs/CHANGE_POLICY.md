# Change policy: locked core and add-on layer

The study keeps a stable baseline while still learning new things by keeping two layers apart.

## 1. Locked core (baseline `core-v1.1`)

The seven tracking questions, the cohort rule (`config/cohort_rules.yaml`), the AI-credit
term list (`config/ai_credit_terms.yaml`), the automatic-yes rules for clear-cut AI credits
(`config/ai_credit_auto_accept.yaml`) and the root-cause map
(`config/root_cause_map.yaml`), together with the frozen pre-registration. These are
computed the same way every quarter and alone decide the Improving/Worsening and
Rising/Falling labels.

The baseline includes the rule changes logged in `prereg/DEVIATIONS.md` on 20–21 October
2026 (AI-credit term list v1.1 and v1.2, the seeded random draw, plus two clarifications),
all made before any result or cohort existed. Git tag `core-v1.1` marks it.

**Until the core freeze (31 December 2026)** the core can still change, because no quarter
has been scored yet: each change is logged in `prereg/DEVIATIONS.md` on the day it is made
(for example the automatic yes for clear-cut AI credits and the T7 range, 22 October), and
the open questions are settled at the 21 December decision session
(`docs/CORE_FREEZE_DECISIONS.md`). The freeze tags `core-v1.2` and files an update on OSF.
From then on the rules in section 4 apply.

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

## 7. Sources that change during the year

Added 30 Oct 2026 (author's decision, after JPCERT/CC's terms page warned that its addresses may
change). Sources are watched every week by the Source watch workflow (`config/source_watch.yaml`:
every core and companion data address and every source's terms page), so a change is usually
found weeks before a pull needs it. Each change found is handled in one of three ways, written
in the session log the day it is handled and in `prereg/DEVIATIONS.md` once the core is frozen:

1. **Moved, same data.** The address changed but the data did not (same fields, same counting,
   same terms). Update the address in the collector and in `config/source_watch.yaml`, log the
   date with both addresses, and confirm the next dry run or pull reads it. The series carries
   on unchanged. This is a bug-fix-level change (section 4, last paragraph).
2. **Changed format, method or terms.** The source still exists but its fields, its counting
   or its terms changed (a new or renamed column, a new definition, a narrower licence). The
   figures from the first affected quarter onward are flagged **exploratory** in the quarterly
   report until the next review (September or March) decides, with the side-by-side comparison
   of section 4, whether the series is still comparable. A terms change that withdraws
   permission stops collection at once (`config/sources.yaml`), whatever the review date.
3. **Gone.** The source has stopped publishing or can no longer be reached for a whole pull
   window. The series is marked **broken** from that quarter, and every report says so plainly.
   No other source is ever put in its place under the same name (decision item 16, no
   substitutes); a replacement can only start as a new exploratory measure (section 2) and
   reach the core at a March review.

Terms pages are copied, dated, to `source-watch/terms/` on the run-reports branch and saved in
the Internet Archive whenever their wording changes, so the terms in force when the data was
used can always be shown.

