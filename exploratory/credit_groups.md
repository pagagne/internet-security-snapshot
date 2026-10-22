# Who is behind the unclear AI credits? (Q3 2026, researched 2026-10-22)

The hand check judges each credit by its wording. Many credits name an AI lab, an AI
security company or a partnership without saying how the flaw was found. This note groups
those unclear credits (139 CVEs in Q3 2026 that mention an AI term but were not accepted
automatically) by the organization behind them, and records what each has said publicly
about how it finds flaws. It researches organizations and programs only, never the
individual researchers named in credits. It does not change any hand-check answer.

| Group (CVEs in Q3 2026) | Example credit wording | What the organization says publicly | Evidence that AI is used for discovery |
|---|---|---|---|
| OpenAI researchers and "OpenAI Codex Security" (81) | "Amy Burnett of OpenAI", "Chris Jarrett-Davies of the OpenAI Codex Security Team" | OpenAI runs Codex Security, an AI agent that finds and validates vulnerabilities (research preview 6 Mar 2026, formerly Aardvark), and the Patch the Planet programme (22 Jun 2026) in which researchers use GPT-5.5-Cyber and Codex Security on open source; OpenAI researchers report confirmed flaws (e.g. 34 in FreeBSD). | **Strong at programme level**; individual credits rarely say so |
| Partners "in collaboration with OpenAI" (5): Trail of Bits, IBM | "Filipe Casal of Trail of Bits in collaboration with OpenAI" | Trail of Bits leads Patch the Planet using OpenAI models, with human review of every finding before it reaches maintainers. IBM is not named in the programme page. | **Strong** for Trail of Bits; unknown for IBM |
| Anthropic and partners (41): Ada Logics, Calif.io, Anthropic researchers, Anthropic OSS program | "Claude and Ada Logics", "Calif.io in collaboration with Anthropic", "Ben Morris (Anthropic)", "Anthropic OSS program" | Anthropic's Frontier Red Team uses Claude to find vulnerabilities in open source and discloses them through a coordinated-disclosure programme; six partner firms (Ada Logics, Anvil, Calif.io, Doyensec, Ophion Security, Trail of Bits) triage and notify maintainers. The OSS Scanner (opened 8 Oct 2026) scans enrolled projects with Claude models. | **Strong at programme level**. Conflict of interest: Anthropic |
| Z.ai Security (3) | "Z.ai Security (Z.ai)" | Z.ai publishes a disclosure ledger (cvd.z.ai) of vulnerabilities found with its GLM models; Red Hat and FreeBSD advisories credit Z.ai / GLM. Claimed totals are largely unauditable (53 of 2,436 entries public). | **Moderate to strong** |
| Xint / Theori (3) | "Yonghwa Lee, Xint from Theori" | Xint Code is Theori's LLM-based code-analysis product (commercial since 17 Mar 2026). "Xint" is the tool itself. | **Strong**: the credit names the tool |
| DepthFirst AI, XBOW, BugBunny.ai (3) | "Zheng Yu (DepthFirst AI)", "fedek-xbow" | Companies whose products are AI vulnerability finders. | **Weak per credit**: affiliation only |
| Other (3) | | | Unknown |

## What this suggests

About 133 of the 139 unclear CVEs come from organizations that publicly run AI-driven
vulnerability discovery programmes in this period. That supports the view that most of
them were found with AI help. It does not prove it for any single CVE: these programmes
also involve human research and human review, and a researcher at an AI lab can still
find a bug by hand.

In numbers (Q3 2026): floor 158 CVEs (0.43%), ceiling 297 (0.81%). Counting credits from
organizations with documented AI-discovery programmes would put an evidence-based estimate
near 291 (0.79%), close to the ceiling.

## Proposed use (decision item 15)

Add a fourth T7 figure, **programme-evidence estimate**: the floor plus credits from
organizations with a dated, public AI-discovery programme active at the time, listed in a
versioned file with a source for each. It would be reported alongside floor, hand-checked
and ceiling, never replace them, and would not decide T7's direction.

Sources: OpenAI, *Patch the Planet* (openai.com/blog/patch-the-planet); AI Business,
*OpenAI launches Codex Security* (Mar 2026); Anthropic Frontier Red Team, *zero-days* (Feb
2026) and CVD dashboard (red.anthropic.com/2026/cvd/about); BetaNews on Anthropic's OSS
Scanner (Oct 2026); SiliconANGLE on Theori's Xint Code (Mar 2026); Codersera on GLM-5.3
cyber claims (2026).
