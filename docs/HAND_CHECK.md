# Hand-check procedure

Some items are flagged by code but need a person to confirm them before they count.
Nothing unverified is ever estimated or filled in: an item that is not confirmed is left
out and reported as pending.

## What is checked by hand

1. **AI-credit matches** (T7, cohort category d): CVEs whose credits contain a term from
   `config/ai_credit_terms.yaml`.
2. **Internet-facing status** for cohort CVEs in category (c), "any other product".
3. **Patch dates** (T_patch) for cohort CVEs, confirmed against the vendor's advisory.
4. **Ground-truth reference dates** for the validation cases (done once, before the run).

## How a review works each quarter

1. After the pull, the code writes `review/<quarter>.csv`: one row per item, with the
   evidence (exact credit text, product, vendor link) and a suggested decision.
2. Identical credit texts are grouped, so one decision covers every CVE that uses it.
3. Decisions already made in earlier quarters are applied automatically from
   `review/decisions.csv` and listed as "already decided".
4. The author marks each new row **yes** or **no**, with an optional note, in the Hand Check
   app (below).
5. Only rows marked yes are used. Unreviewed rows are excluded and reported as pending.
6. The review file, decisions, reviewer and date are published in the quarter's bundle.

## The Hand Check app

Hand checks are done in a private web app (source: `apps/hand-check.html`; how to use it:
[`HAND_CHECK_APP.md`](HAND_CHECK_APP.md)), not in a spreadsheet. After each data run, Claude loads that quarter's review list into it. The app
shows one item at a time (AI credits and cohort picks as separate sections), saves every
answer as it is made, tracks time spent, and ends with a report.

How results flow into the study:
1. The author answers items in the app; answers are saved in the app's own database.
2. When the author says the list is done, Claude reads the answers and writes them to
   `review/decisions.csv` in this repository (one row per item: decision, fix date and its
   status, time, note), committed with a dated message. Earlier decisions carry over to
   later quarters automatically.
3. The evaluation uses only `review/decisions.csv`, so every hand decision behind a
   published number is public and reviewable.
4. A CSV copy can also be saved from the app's Report view as a personal backup.

## How the hand check fits the random draw

Each month's pick in every slot comes from a seeded random draw (`config/cohort_rules.yaml`,
`selection`). The review file lists, for slots (c) and (d), the CVE at the top of the
draw order. Mark it yes or no:

- **Yes:** it is the month's pick for that slot.
- **No:** it is recorded as skipped with the reason, and the next CVE in draw order is
  added to the next review file. You never choose which CVE comes next; the draw does.
- A slot stays open until its pick is confirmed, so an unanswered item holds that slot
  (and only that slot) back.

## Automatic yes for clear-cut credits (since 2026-10-22)

Credits where a tool or model name appears in a clear role pattern, such as "using
Codex", "found by Big Sleep" or "Claude Opus 5", are
accepted automatically (`config/ai_credit_auto_accept.yaml`). Lab or company names alone
never qualify (except in a stated collaboration, below), and wording that makes the AI the subject of the flaw ("vulnerability in
Claude", "prompt injection") always goes to the author. A random 10% of automatic yeses
(at least three) still comes to the author as spot checks; a "no" on a spot check
suspends that pattern until it is reviewed. Everything else is checked by hand as below.

**Stated collaboration counts (author's decision, 2026-10-23).** A credit saying the finder
worked "in collaboration with" an AI tool or an AI lab ("in collaboration with Claude and
Anthropic Research", "Trail of Bits in collaboration with OpenAI") counts as AI involvement
and is accepted automatically. Credits do not say what the AI did, and the study does not
try to split that hair: a stated collaboration is taken as involvement. Affiliation alone
("Jane Doe of OpenAI") and bare "with Claude" still go to the author. (History: the pattern
was removed on 22 Oct after a practice spot check and restored, extended to labs, on 23 Oct.)

## Criteria for AI-credit matches

A match counts as **AI-credited** only if the credit names an AI tool, model or agent as
the finder or co-finder of the vulnerability. Examples that count:

- "Found by XBOW", "Google Big Sleep", "Claude Security"
- "Jane Doe using Claude", "in collaboration with Claude and Anthropic Research"
- "Tsinghua University using GLM-5.1 from Z.ai", "Deepseek agent"

Examples that do **not** count:

- A person's name that happens to match a term (e.g. "Claude Bernard").
- A username or handle that matches a term with no sign of an AI tool (e.g. "Qwen (VulDB
  User)").
- A researcher identified only by employer, including AI labs (e.g. "Nicholas Carlini of
  Anthropic", "Amy Burnett | OpenAI"). **Lab-name matches never count on their own**; the
  credit must also say an AI tool or agent took part, or that the work was done in
  collaboration with the lab.
- Human teams with no AI tool named (e.g. "Google Project Zero"; its AI tool Big Sleep is
  matched separately).

When the text is genuinely unclear, the decision is **no**, with a note, so the measure
leans toward undercounting rather than overcounting AI involvement.

## Two versions reported

T7 is reported each quarter under the registered term list (v1.0) and the current list,
with the current list labeled as a deviation. See `prereg/DEVIATIONS.md`.

## T7 as a range

Credits often do not say how a flaw was found, so T7 is reported as a range each quarter
(`src/snapshot/t7.py`), with one denominator, all CVEs published in the quarter:

- **Floor:** credits accepted by a clear published pattern; no judgment involved.
- **Hand-checked:** the floor plus credits the author answered yes to (the registered T7).
- **Ceiling:** every credit mentioning any listed AI term, lab names included.

Q3 2026 (test data, rules of 23 Oct): floor 0.53%, ceiling 0.81% of 36,732 CVEs.
A direction is called only when the floor and the ceiling move the same way (two quarters
running against the median of the previous four); otherwise T7's direction is "unclear".
Borderline calls can move the hand-checked figure within the range but cannot create a
trend on their own. (Direction rule to be confirmed at the 21 December session.)

## Consistency of hand decisions

Each quarter, five credit texts the author decided before are shown again, unmarked, among
the new ones. The share answered the same way both times is published as the consistency
rate (`snapshot.decisions.consistency`). High consistency means the judgment is steady even
where the rules are fuzzy.

## How to read T7: disclosed, not total

T7 counts flaws whose credits *say* an AI tool took part. It depends on the finder
choosing to disclose it. Discoveries made with hosted AI services are often credited
(the lab may share the credit), while discoveries made with models run privately on a
researcher's own machine, such as open-weight models, usually are not. As local models
improve, T7 can lag real AI use, or even fall while use rises. Every report states this
next to the T7 figures, and a change in T7 is described as a change in *disclosed* AI
involvement.

See `docs/EVALUATION_FLOW.md` for where each hand check feeds into the measures.
