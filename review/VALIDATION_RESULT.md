# Validation result, 17 Nov 2026

Pre-registration Section 11: the study's pipeline is run on five documented reference cases. Pass: for at least
4 of 5 cases, the fix date (T_patch) and the CISA listing date (T_kev) match exactly, and the first-exploitation
date (T_exploit) is within one day of the documented date or later and explained by free-source coverage.

**Result: PASS, 4 of 5 cases** (`python -m snapshot.validate`, schedule item validation-run, issue #69).

Inputs: the author's blind fix dates (`review/validation-decisions.csv`, 16 Nov 2026, made in the Hand Check app
without seeing the reference file); CISA's KEV catalog version 2026.11.13; the reference file
`prereg/ground_truth_reference.csv` (recorded 22 Oct 2026). Row by row: `review/validation-result-2026-11-17.csv`.

- Case 1, PAN-OS GlobalProtect (CVE-2024-3400): pass. Fix 14 Apr 2024 and KEV 12 Apr 2024 match; first exploitation
  seen 17 days after the documented date (Volexity's incident response, a source the study does not have).
- Case 2, Langflow (CVE-2025-3248): pass. Fix 31 Mar 2025 and KEV 5 May 2025 match; exploitation 25 days after the
  documented honeypot date.
- Cases 3a and 3b, PaperCut (CVE-2026-81578, CVE-2026-82078): pass. Fix 27 Aug 2026 and KEV 31 Aug 2026 match;
  exploitation 5 days after the documented date.
- Case 4, Zammad (CVE-2026-102489, CVE-2026-102490): **fail**, on the fix date only. The author dated both to the
  5 Oct 2026 advisory; the reference has 23 Sep 2026 (the 7.2.0 release) for the first and no confirmed fix for the
  second. KEV (2 Oct 2026) matches.

Two caveats, stated so the pass is not over-read:

1. The exploitation check is weak for now. T_exploit is the earliest of CISA KEV, VulnCheck KEV and Shadowserver,
   but VulnCheck is collected only from the 1 Dec 2026 dry run and Shadowserver has not answered, so today
   T_exploit equals the KEV date for every case. All five exploitation checks pass only through the
   "later, explained by free-source coverage" clause. The check should be re-run after the 1 Dec dry run,
   when VulnCheck dates are in (expected to move some dates earlier).
2. The Zammad miss is what led to the two fix-date rules added to `docs/HAND_CHECK.md` on 16 Nov 2026 (the
   release of the first fixed version, not the advisory; upgrade advice without a stated fix is "no fix yet").
   The validation answers are not redone under the new rules: they were given before the author saw the
   reference, and redoing them after would not be blind.
