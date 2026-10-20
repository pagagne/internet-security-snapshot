# Internet Security Snapshot

An unfunded, quarterly measurement of the internet's security status, built to test
whether the internet is being "cleaned up" faster than it is being attacked.

Each quarter, an automated job pulls free, versioned public data (CVE, CISA KEV,
Vulnrichment, EPSS, Shadowserver, SEC EDGAR, ransomware.live and others), freezes it,
and tests five pre-registered hypotheses. A provisional evaluation is published on the
1st of January, April, July and October; the final one follows a month later.

- **Pre-registration:** [`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md)
  (draft; frozen on OSF by 31 October 2026)
- **Deviations log:** [`prereg/DEVIATIONS.md`](prereg/DEVIATIONS.md)
- **Cohort rules:** [`config/cohort_rules.yaml`](config/cohort_rules.yaml)

## Schedule

| Date | Milestone |
|---|---|
| 31 Oct 2026 | Pre-registration frozen on OSF |
| 1 Dec 2026 | Dry run on Oct–Nov 2026 data (unscored) |
| 1 Jan / 1 Feb 2027 | Q4 2026 pilot: provisional / final |
| 1 Apr / 1 May 2027 | Q1 2027, first confirmatory quarter: provisional / final |

## Principles

- Free data and free infrastructure only; nothing is estimated to fill a gap.
- Rates with stated denominators, not raw counts.
- Raw inputs frozen with checksums; every published number reproducible with one command.
- All five hypotheses reported every quarter, whatever the result.
- No scanning, no exploitation, no host-level data, no victim names.

## AI involvement and conflict of interest

Code and draft evaluations are written with Claude, an AI model made by Anthropic.
Anthropic is named in the report this study tests. Safeguards: the frozen
pre-registration, public code, the author's approval of every release, and an external
reviewer for the first confirmatory quarter.

## Licence

Code: MIT (see `LICENSE`). Documentation and the study's own derived data: CC BY 4.0.
Third-party data keeps its own terms; see the licensing table in the spec.
