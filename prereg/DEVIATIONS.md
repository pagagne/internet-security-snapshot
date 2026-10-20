# Deviations from the pre-registration

Every change made after the pre-registration is frozen is recorded here: the date, what
changed, why, and which results it affects. The frozen original is never edited.

| Date | Section | Change | Reason | Results affected |
|---|---|---|---|---|
| 2026-10-20 | 8 (AI-credit matching) | Implementation note, not a rule change: "whole word" matching treats hyphens and punctuation as word boundaries, so "GPT-5" matches the term "GPT". The term list itself is unchanged. | The first test run's code treated hyphens as part of a word and would have missed credits such as "GPT-5.4-Cyber". Found while testing the collector on live data; no quarterly result had been computed. | T7 (I8), cohort category (d): six more candidate matches across all CVEs to date, each still subject to the hand check |
