# Root-cause map: findings and proposal (for decision item 1, 21 Dec 2026)

Analysis of the 36,732 CVEs published in Q3 2026 (test data, 2026-10-22).

## Findings

1. **"Other/unknown" is 38.6% of all CVEs and 29.2% of cohort-eligible CVEs** under the
   registered map (v1.0).
2. **Missing CWE is not the main cause.** 11.6% of CVE records carry no CWE. Filling from
   NVD, which the registered source order already allows (CVE record, Vulnrichment, NVD),
   lowers that only to 10.7%. NVD fill is an implementation step, not a rule change, and will
   be built into the evaluation.
3. **Unmapped CWEs are the main cause: 27.4% of CVEs** have a CWE the map does not cover.
   The most common: CWE-200 information exposure (828), CWE-400 resource consumption (624),
   CWE-20 input validation (623), CWE-269 privilege management (609), CWE-770 resource
   allocation (520), CWE-362 race condition (244), CWE-295 certificate validation (174),
   CWE-347 signature verification (171), CWE-601 open redirect (164).

## Proposal: map v1.1 (`proposals/root_cause_map_v1.1.yaml`)

- Add common CWEs to existing classes (for example type confusion to memory safety, XXE and
  request smuggling to injection, privilege management to access control, open redirect to
  request forgery).
- Add five classes: cryptography and verification, resource exhaustion, information
  exposure, race conditions, and unspecific input validation (CWE-20 kept separate because
  it says little about the actual flaw).

Effect on Q3 2026:

| | v1.0 (registered) | v1.1 (proposed) |
|---|---|---|
| Other/unknown, all CVEs | 38.1% | 19.4% |
| Other/unknown, eligible CVEs | 29.2% | 13.9% |
| Of which no CWE at all | 10.7% | 10.7% |

Eligible CVEs under v1.1: access control 29%, injection 18%, memory safety 17%,
other/unknown 14%, path/file 6%, others 1-3% each.

## How to decide

- **Adopt v1.1** before the freeze: logged deviation, new checksum, core-v1.2. The
  root-cause tag is descriptive and used only in analysis, never for selection, so the
  change affects no label.
- **Or keep v1.0** and report v1.1 alongside as exploratory.

Either way the remaining 10.7% (no CWE from any source) stays "unknown".
