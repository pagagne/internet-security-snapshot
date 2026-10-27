# Decision sheet: research review, Thu 12 Nov 2026, 10:00 ET

One page per decision: the question, the options, and a recommendation (marked ★). The author's
leaning on 26 Oct was to approve the recommendations unless the evidence says otherwise. Claude
fills in the **Evidence** lines by 11 Nov from the probes (27 Oct global probes, 2 Nov tests,
5 Nov trial sweep) and, on the morning of 12 Nov, asks the same questions in chat as option
cards. Anything decided here that touches the core is confirmed at the 21 Dec freeze session.

**Decided early, 27 Oct 2026 (author, option cards):**
- #1 **A**, every flagged fix date checked each quarter (about 1½ hours).
- #2 **A**, CISA's "active exploitation" date reported beside the KEV-based figures as
  exploratory from the pilot; proposed for the core at the 21 Dec session (CORE_FREEZE item 23).
- #9 **B**, the sweep keeps the list as written on 26 Oct (including the Chinese and Russian
  sites added that day); the trial's other proposed changes are not adopted. The 9 Nov check of
  the 15 trial entries still stands.
- #3-8, #10, #11 **approved on their stated conditions (★)**: Claude applies each once its
  test meets the condition, records the evidence here, and brings back on 12 Nov only those
  that fail or need a choice the condition does not settle.

**Quick list (11 decisions; since 27 Oct only exceptions remain for 12 Nov)**

| # | Decision | ★ Recommendation |
|---|---|---|
| 1 | Race fix-date effort | Check every flagged fix date |
| 2 | CISA "active exploitation" date as an attack date | Report it beside KEV, exploratory; propose for the core on 21 Dec |
| 3 | X19 other countries' attack alerts | Adopt every agency whose data and terms hold up |
| 4 | X20 DNSSEC and RPKI by country | Adopt |
| 5 | X21 regional splits | Adopt; ransomware figures only once permitted |
| 6 | X22 other countries' breach counts | Adopt the regulators that publish regularly; the rest at the March review |
| 7 | X12 open-weight release curve: sources | Adopt Hugging Face by lab, checked against Epoch AI |
| 8 | X12 "capable" bar | Two bars, reported separately: coding and security |
| 9 | AI-attack sweep: searches and pages | Adopt the trial's proposed changes, then fix the list |
| 10 | Web patch adoption (HTTP Archive, PHP2Shell first) | Adopt as exploratory if versions are recorded |
| 11 | Open-source patch adoption (X16) and health-sector breaches (X17) | Adopt whichever ran cleanly; retry the other once |

For information (no decision): KEV's lag against other sources, Linux kernel fix dates in the
pre-fill (2 Nov), honeypot first-seen dates (context only, decided 25 Oct), the AI-list check
(empty credit fields at Microsoft and Apple; for 8 Feb), the Gemini/Irregular entry (X3), and
the PHP2Shell case (patch-information flow; early-patch note goes to 21 Dec, item 20).

---

## 1. Race fix-date effort
How many flagged fix dates in the race list does the author check each quarter?
- **A ★ Every flagged case** (about 1½ hours a quarter). Narrows the fix-date ranges, so the
  zero-day share's range shrinks. The author's leaning on 24 Oct.
- B A random sample of flagged cases (about 50 minutes); wider ranges.

Evidence: about 120 of 175 flagged per half-year, mostly quick "fix available at the advisory?"
checks (`docs/RESEARCH_PLAN.md`, item 1).

## 2. CISA "active exploitation" date as an attack date
CISA's flag is set before the KEV listing for about 1 in 6 newly attacked flaws (median 35
days earlier; a preview suggests the zero-day share is understated by up to half). Use it?
- **A ★ Report it beside the KEV-based figures as exploratory now, and propose it for the core
  at the 21 Dec session** (T_exploit = the earlier of the two dates). Free, already collected.
- B Adopt it into the core straight away (on 21 Dec without an exploratory quarter).
- C Leave it out; KEV dates only.

Evidence: `docs/RESEARCH_PLAN.md`, item 3. To add by 11 Nov: whether the first "active" date
can be read from the repository history (today only the latest is known).

## 3. X19: other countries' attack alerts against KEV
Which of CERT-FR, JPCERT/CC, BSI and KrCERT/CC to add?
- **A ★ Every agency whose alerts can be read and dated and whose terms allow it.**
- B Only the two easiest (fewest gaps), the others at the March review.
- C None for now.

Evidence (27 Oct probe): _to fill_.

## 4. X20: DNSSEC validation and RPKI route checking by country
- **A ★ Adopt** (APNIC Labs and RIPE NCC, quarterly, by region with a world figure).
- B Adopt one of the two measures only.
- C Not now.

Evidence: _to fill_.

## 5. X21: regional splits of Cloudflare Radar and ransomware.live
- **A ★ Adopt;** ransomware.live regional figures published only once permission is granted
  (`config/sources.yaml`).
- B Radar only.
- C Not now.

Evidence: _to fill_.

## 6. X22: breach notifications outside the US
UK ICO, Australia's OAIC, Singapore's PDPC, ENISA.
- **A ★ Adopt those that publish regularly in a usable form; the rest at the March review.**
- B Adopt all four now.
- C Defer all to the March review.

Evidence: _to fill_ (publication frequency and format of each).

## 7. X12: open-weight release curve, sources
- **A ★ Hugging Face Hub by a fixed list of major labs (base and instruct releases only),
  checked against Epoch AI's model database; history from January 2023.**
- B Epoch AI only (curated, fewer models, slower to update).
- C Hugging Face only.

Evidence: _to fill_ (lab list proposed for approval, counts per quarter since 2023).

## 8. X12: the "capable" bar
A model counts as capable when it reaches a fixed score on a public benchmark.
- **A ★ Two bars, reported separately: a coding benchmark (longest history, most models
  scored) and a security benchmark (closer to attack work, fewer models scored).**
- B Coding benchmark only.
- C Security benchmark only.

Evidence: _to fill_ (candidate benchmarks, threshold, how many open models clear each).

## 9. AI-attack sweep: searches and pages
- **A ★ Adopt the trial's proposed changes, then fix the list for 2027.**
- B Keep the list as written on 26 Oct.
- C Change it in another way (say how).

Evidence (trial run early, 26 Oct, on Jul-Oct 2026; `exploratory/sweep-trial-2026.md`): 50
candidates, 15 kept (log 13 -> 28, awaiting your check), 11 of them found first or only outside
English; Chinese and Russian work only when searched on those countries' own security sites. Proposed changes: add a named watch list of offensive agent frameworks (ARTEX, Cairn,
Hexstrike, Strix, OpenClaw, Hermes, Manus) and an "AI penetration tool used by attackers"
search; move the prompt-injection and MCP searches to X5; add GMO, CrowdStrike, Sysdig,
Cybernews and Trend Micro pages; replace Chinese and Russian searches with fixed native-language
pages, searched by site. About 2 h for the trial; 3-4 h a quarter for the full sweep.

## 10. Web patch adoption from HTTP Archive (PHP2Shell first)
- **A ★ Adopt as exploratory if the crawl records PHP versions:** share of PHP-reporting sites
  on a fixed release, and on releases that will never be fixed, 30 and 90 days after a fix.
- B Run PHP2Shell as a one-off case study only.
- C Not now.

Evidence (2 Nov test, needs the author's Google Cloud project): _to fill_.

## 11. X16 open-source patch adoption and X17 health-sector breaches
- **A ★ Adopt whichever has run cleanly; retry the other once before 11 Dec.**
- B Adopt both regardless.
- C Defer both to the March review.

Evidence (2 Nov lighter deps.dev run, HHS retry): _to fill_.
