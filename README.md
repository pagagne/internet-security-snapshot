# Internet Security Snapshot

An unfunded, quarterly measurement of whether internet security is getting better or
worse, and how AI is involved. The central question: are defenders closing
internet-exposed vulnerabilities faster than attackers start exploiting them?

Each quarter, an automated job pulls free, versioned public data (CVE, CISA KEV,
Vulnrichment, EPSS, Shadowserver, SEC EDGAR, ransomware.live and others), freezes it,
and reports seven pre-registered tracking questions. A provisional evaluation is published on the
1st of January, April, July and October; the final one follows a month later.

- **Pre-registration:** [`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md)
  (v1.0, tag `prereg-v1.0`), registered on OSF on 20 October 2026:
  [doi.org/10.17605/OSF.IO/3XT82](https://doi.org/10.17605/OSF.IO/3XT82)
  (project: [osf.io/3smuq](https://osf.io/3smuq))
- **Deviations log:** [`prereg/DEVIATIONS.md`](prereg/DEVIATIONS.md)
- **Change policy:** [`docs/CHANGE_POLICY.md`](docs/CHANGE_POLICY.md): a locked core
  (baseline `core-v1.1`, checksums in `prereg/LOCKED.yaml`) and an exploratory add-on
  layer (`config/exploratory.yaml`) that never decides a label
- **Hand checks:** criteria in [`docs/HAND_CHECK.md`](docs/HAND_CHECK.md); the author works
  through them in the Hand Check app ([user guide](docs/HAND_CHECK_APP.md))
- **Cohort rules:** [`config/cohort_rules.yaml`](config/cohort_rules.yaml),
  [`config/ai_credit_terms.yaml`](config/ai_credit_terms.yaml),
  [`config/root_cause_map.yaml`](config/root_cause_map.yaml)

## Schedule

| Date | Milestone |
|---|---|
| 20 Oct 2026 | Pre-registration registered on OSF (DOI 10.17605/OSF.IO/3XT82) |
| 1 Dec 2026 | Dry run on Oct–Nov 2026 data (unscored; started by hand) |
| 4 Dec 2026 | Public landing page (GitHub Pages) and Discussions opened; project links shared from here on |
| 21 Dec 2026 | Core-freeze decision session (docs/CORE_FREEZE_DECISIONS.md) |
| by 31 Dec 2026 | Final core freeze: tag core-v1.2, OSF update |
| 1 Jan / 1 Feb 2027 | Q4 2026 pilot: provisional / final |
| Feb 2027 | Censys research-access application (written by the author) |
| 15 Mar 2027, then yearly | Annual review and change window; annual check of free numbers from March 2028 |
| 1 Apr / 1 May 2027 | Q1 2027, first confirmatory quarter: provisional / final |

## Principles

- Free data and free infrastructure only; nothing is estimated to fill a gap.
- Rates with stated denominators, not raw counts.
- Raw inputs frozen with checksums; every published number reproducible with one command.
- All seven tracking questions reported every quarter, whatever the result.
- No scanning, no exploitation, no host-level data, no victim names.

## AI involvement and conflict of interest

Code and draft evaluations are written with Claude, an AI model made by Anthropic.
Anthropic is named in the report this study grew from. Safeguards: the frozen
pre-registration, public code, the author's approval of every release, and an external
reviewer for the first confirmatory quarter.

## Licence

Code: MIT (see `LICENSE`). Documentation and the study's own derived data: CC BY 4.0.
Third-party data keeps its own terms; see the licensing table in the spec.
