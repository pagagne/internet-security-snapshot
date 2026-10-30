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
5. **HHS breach list download** (X17, since 29 Oct 2026): once a quarter, download the public
   CSV from the HHS OCR breach portal (ocrportal.hhs.gov/ocr/breach) and give it to Claude,
   who keeps only the quarterly counts.

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

## What counts as AI involvement (author's rule, since 2026-10-23)

**Any mention of an AI tool or a frontier AI lab in the credits counts**, whatever the
wording: "using Codex", "found by Big Sleep", "Claude Opus 5", "in collaboration with Claude
and Anthropic Research", "Trail of Bits in collaboration with OpenAI", "Amy Burnett of
OpenAI", "Alex Matrosov with Claude, Anthropic". The reasoning: people credited from an AI
company can be taken to be using AI, and credits rarely say how a flaw was found, so
judging each wording adds work without adding information. These credits are counted
automatically (`config/ai_credit_auto_accept.yaml`, v1.3).

Still sent to the author:
- Name collisions: a person or handle that happens to match a term ("Claude Bernard",
  "Qwen (VulDB User)").
- Wording that makes the AI the subject of the flaw ("vulnerability in Claude", "prompt
  injection").
- Qihoo 360, a security company rather than an AI lab, whose credits usually name human
  researchers.

A random 10% of automatic yeses (at least three) still comes to the author as spot checks,
mainly to catch name collisions; a "no" on a spot check suspends the rule that accepted it
until it is reviewed.

**The narrower count is kept alongside.** Credits that name an AI *tool* in a clear role
("using", "found by", a model name with its version, "in collaboration with" a tool) are
also counted separately, with lab names ignored. This is the measure as registered, and it
is the low end of the T7 range (below). The gap between the two shows how much of the
headline rests on lab affiliation; for example, if AI labs hire more security researchers,
the headline rises even if AI use does not.

History: automatic yes for clear patterns adopted 22 Oct; "in collaboration with" removed
22 Oct after a practice spot check; restored and extended to labs 23 Oct; any mention of a
tool or lab 23 Oct. All logged in `prereg/DEVIATIONS.md`. The rule is re-evaluated on the
Q4 2026 pilot data in February 2027, before the 15 March review.

## Criteria for the remaining hand decisions

The few credits that still reach the author are name collisions and edge cases. Count a
credit as AI involvement if it names an AI tool, model or agent, or a frontier AI lab, in
any role other than as the thing that had the flaw. Do **not** count:

- A person's name or handle that happens to match a term ("Claude Bernard", "Qwen (VulDB
  User)").
- Credits where the AI product is the subject of the flaw, with no sign an AI tool helped
  find it.
- Security companies that are not AI labs (Qihoo 360, Google Project Zero as a human team;
  its AI tool Big Sleep is matched separately).

When the text is genuinely unclear, the decision is **no**, with a note.

## Two versions reported

T7 is reported each quarter under the registered term list (v1.0) and the current list,
with the current list labeled as a deviation. See `prereg/DEVIATIONS.md`.

## T7 as a range

Credits often do not say how a flaw was found, so T7 is reported as a range each quarter
(`src/snapshot/t7.py`), with one denominator, all CVEs published in the quarter:

- **Low end (AI tool named):** credits naming an AI tool in a clear role, lab names
  ignored; the measure as registered; no judgment involved.
- **Headline (AI tool or lab mentioned):** any mention of an AI tool or frontier AI lab,
  plus any credits the author answered yes to.
- **Ceiling:** every credit mentioning any listed AI term; equals the headline except for
  name collisions and other credits the author rejected.

Q3 2026 (test data, rules of 23 Oct): low end 0.43%, headline 0.81% of 36,732 CVEs.
A direction is called only when the low end and the headline move the same way (two quarters
running against the median of the previous four); otherwise T7's direction is "unclear".
Borderline calls can move the hand-checked figure within the range but cannot create a
trend on their own. (Direction rule to be confirmed at the 21 December session.)

## Consistency of hand decisions

Each quarter, 20 earlier author decisions are shown again, unmarked, among the new ones:
AI-credit texts, fix dates and slot (c) internet-facing calls, drawn by a seeded sample
(`snapshot.decisions.retest_items`). Fix-date items show the pre-fill the author saw the first
time, never the earlier answer. A re-shown answer is recorded with `retest=True` and never
replaces the original decision. Consistency is published per kind
(`snapshot.decisions.consistency_by_kind`): the same yes/no answer for credits and slot (c),
and for fix dates the same status with dates within one day. Each rate carries its one-sided
90% lower bound: if all 20 match, consistency is at least 89% (with 5 it was only 63%; five
items were used until 24 Oct 2026). About 8 extra minutes a quarter.

## Second coder

Consistency cannot reveal a bias the author applies the same way every time; a second,
independent coder can. Each quarter, after the author's hand check, `snapshot.agreement`
draws 20 of the author's decisions (up to half from uncertain cases: marked unsure, fix date
corrected, unknown or "no fix yet", pre-fill assumed or flagged), writes them without the
author's answers for the second coder, and keeps the sampling weights in a separate file the
coder does not see. The coder answers in that file, or in the Hand Check app as a batch whose
metadata names them; their answers go to `review/second_coder.csv`, never to
`review/decisions.csv`. Reported: raw agreement, Cohen's kappa, Gwet's AC1 and agreement on
Yes and No for the yes/no checks, and the share of fix dates within one day with the median
difference, weighted back to the whole batch. Pooled over the year for the March review.
Nothing here decides a label. The second coder is lined up with the external reviewer
(decision item 17).

## How to read T7: disclosed, not total

T7 counts flaws whose credits *say* an AI tool took part. It depends on the finder
choosing to disclose it. Discoveries made with hosted AI services are often credited
(the lab may share the credit), while discoveries made with models run privately on a
researcher's own machine, such as open-weight models, usually are not. As local models
improve, T7 can lag real AI use, or even fall while use rises. Every report states this
next to the T7 figures, and a change in T7 is described as a change in *disclosed* AI
involvement.

See `docs/EVALUATION_FLOW.md` for where each hand check feeds into the measures.

## Time per quarter (estimate, 24 Oct 2026)

From the practice round (about 30-60 seconds per item) and the rules as of 24 Oct:

| Part | Items | Time |
|---|---|---|
| Approve the provisional draft (1st-3rd) | 1 | 20-30 min |
| AI credits: spot checks and edge cases | about 10-15 | 5-8 min |
| Cohort: fix dates and slot c checks | about 12 picks + 3-6 candidates | 15-20 min |
| Race: flagged fix dates of newly attacked flaws | about 60 (or a sample of about 15-20) | about 60 min (or 15-20 min) |
| Re-shown items (consistency) | 20 | about 8 min |
| HHS breach list download (X17) | 1 file | about 5 min |
| **Hand-check window total** | | **about 1½ hours, or about 50 minutes with a race sample** |
| Final-run check (2nd of the following month) | new rows only | 15-30 min |

Whether every flagged race fix date is checked or a sample is decided on 12 Nov 2026. The
same choice applies to the baseline year (four quarters of newly attacked flaws, roughly
200-250 flagged dates if all are checked), which the race labels compare against.

