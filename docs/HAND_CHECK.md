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
4. The author marks each new row **yes** or **no**, with an optional note. Rows can be
   edited in GitHub's web editor, or the answers given to Claude to record.
5. Only rows marked yes are used. Unreviewed rows are excluded and reported as pending.
6. The review file, decisions, reviewer and date are published in the quarter's bundle.

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
  credit must also say an AI tool or agent took part.
- Human teams with no AI tool named (e.g. "Google Project Zero"; its AI tool Big Sleep is
  matched separately).

When the text is genuinely unclear, the decision is **no**, with a note, so the measure
leans toward undercounting rather than overcounting AI involvement.

## Two versions reported

T7 is reported each quarter under the registered term list (v1.0) and the expanded list
(v1.1), with v1.1 labeled as a deviation. See `prereg/DEVIATIONS.md`.
