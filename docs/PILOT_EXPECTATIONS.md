# What we expect from the Q4 2026 pilot (written 26 Oct 2026, before any Q4 result)

Recorded at the author's request so the pilot can be compared with what we expected before we
saw it. These are best guesses from the Q2-Q3 2026 previews and what had been reported in
October; they are **not** registered hypotheses and decide nothing. Compared with the results
after the final run (schedule item `pilot-expectations-check`, 3 Feb 2027).

## What the pilot is for
- Prove the machinery: provisional pull on 1 Jan and final on 1 Feb on time with every
  approved source, a clean manifest, the author's review gate, the hand check in about 1½
  hours, and the first Zenodo archive on 1 Feb.
- Find the rough edges before Q1 2027, the first scored quarter.
- No Improving/Worsening verdicts: labels need scored quarters to compare with.

## Best-guess readings
| Measure | Expected | Basis |
|---|---|---|
| T1(a) race: median days from fix to first known attack | a few days to two weeks | previews: Q3 at least 8 days, Q2 at least 15 |
| Zero-day share (X10), KEV dates | about 15-25%, a minimum | previews: 16% (Q2), 23% (Q3) |
| Zero-day share with CISA's "active exploitation" date | toward a third | flag set earlier for about 1 in 6 flaws |
| Flaws newly added to CISA KEV | about 75-100 | Q2 75, Q3 100 |
| AI-credited share of serious flaws (T7) | still rising | trend since 2025 |
| AI-found flaws that get attacked | very few; PHP2Shell may be the first notable one if CISA lists it | 0 of 102 in Q2-Q3 |
| AI-run attack log (X3), Q4 entries | roughly as many as the whole first half of 2026 | about a dozen Q4 cases logged by 26 Oct (Cairn, ARTEX, CERT-In, "Skynet") |
| Open-weight releases (X12) | curve still climbing; gap to the frontier a matter of months | DeepSeek, OpenClaw, Hermes already in attacks |
| SEC Item 1.05 filings (T6b) | around a dozen | Q3 test pull |
| Exposure (T1b, T2) | "not measured" or "baseline building" unless Shadowserver or Censys arrive | permissions pending |
| Web patch adoption (HTTP Archive, PHP2Shell) | a large share of PHP sites still on unfixed or never-fixable versions | author's concern, 26 Oct |

## The story we expect
Attackers are fast and getting faster at the edges; AI-run attacks have moved from rare to
routine; the defender side is the blind spot. If so, the pilot's most useful result is showing
exactly which data would close the gap (Shadowserver or Censys permission).

## What would surprise us
- A median race of zero or below (attacks typically before fixes).
- An AI-found flaw at the centre of a mass-exploitation campaign.
- A quiet quarter in the AI-run attack log.
