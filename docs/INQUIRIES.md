# Inquiry log

Questions raised about how the study would handle something seen outside it: a news story, a
report, a new data source. Each entry records the question, how the registered plan handles
it, what the free data recorded against what happened, and any follow-up. Entries are not
rule changes: they are weighed together at the March review (`docs/CHANGE_POLICY.md`).
Started 25 Oct 2026 at the author's request.

| Date | Raised by | Question | How the plan handles it | Follow-up |
|---|---|---|---|---|
| 2026-10-25 | Author | How would the PHP2Shell story (The Next Web, 25 Oct) be picked up? | T7: headline count yes (OpenAI credited), narrow count no, though GPT-5.6 Sol and Gemini 4 Argon were used. T1(a): only if CISA lists it in Q4; free data dates the first attack after the fix although an attempt came 4 days before; X10 a minimum. Cohort: only if drawn. T1b/T2: needs scan data. | Points in `docs/cases/php2shell.md`; case note by 3 Feb 2027; review 8 Feb 2027. Led to the 25 Oct brainstorm (`docs/RESEARCH_PLAN.md`). |
| 2026-10-26 | Author | Should CCRI (the author's alma mater) be approached for the independent reviewer? | Good fit for the second coder (NSA CAE in Cyber Defense); weaker for the statistical review. | Outreach 9 Nov (docs/reviewer/ccri-outreach.md); second-coder summary docs/reviewer/SECOND_CODER.md. |
| 2026-10-25 | Author | Can we widen the pool of scan and attack-timing sources, and improve the process? | Brainstorm doc; all additions exploratory. | Adopted items scheduled; see `docs/RESEARCH_PLAN.md`, "Brainstorm of 25 Oct". |
| 2026-10-26 | Author | Will AI-run attacks that are reported only in scattered articles be missed, and should the planned year-end web search be quarterly? | X3 logged only what AI labs, vendors and agencies report. Now a fixed quarterly sweep (10 searches and about 20 fixed pages, including SANS ISC diaries, vendor research blogs, AI-security trackers and news sites for leads, listed in the X3 entry of `config/exploratory.yaml`), every candidate kept in `exploratory/ai_attack_sweeps.csv` with the reason, kept ones checked by the author in the hand-check window. Incidents nobody reports stay invisible: counts are a lower bound. | First sweep 2 Jan 2027 (Q4 2026); the four sweeps compared at the March 2028 review. |
