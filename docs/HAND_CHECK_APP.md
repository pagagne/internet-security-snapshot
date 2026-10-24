# Hand Check app: user guide

The Hand Check app is where the author makes the study's hand decisions each quarter. It
replaces working through a spreadsheet. The criteria for each decision are in
[`HAND_CHECK.md`](HAND_CHECK.md); this guide covers how to use the app.

- **Where:** a private page in the author's Claude account, named "Snapshot Hand Check"
  (claude.ai → Artifacts). Only the author can open it. It works on a phone or a computer.
- **Source code:** [`apps/hand-check.html`](../apps/hand-check.html). This file is for
  reference only: downloaded and opened from a computer it cannot reach the review lists or
  save answers. Always open the app from claude.ai → Artifacts → Snapshot Hand Check.
- **When:** any time from the 4th to the 28th of the month after each provisional run (for example 4-28 Jan for Q4 2026), and the baseline-year sessions (23-24 Nov 2026). Answers given by the 28th are used in the final report on the 1st.
  Calendar entries carry the steps.

## 1. Before you start

After a data run, Claude loads that quarter's review list into the app. Ask Claude in the
chat if the list you expect is missing. Pick the list from the **List** menu at the top.
Practice lists are labelled "not scored".

## 2. The screen

- **Progress bar and counts** at the top: items done, done per section, time spent so far,
  and an estimate of time left based on your own pace.
- **Sections:** *AI credits*, *Cohort picks* and *Report*. Do them in any order; each
  saves on its own.

## 3. AI credits

Since 23 October 2026, any mention of an AI tool or a frontier AI lab in a credit counts as
AI involvement and is accepted automatically (`HAND_CHECK.md`). Most quarters this section
will therefore be short: it holds only

- **spot checks** (marked): a random sample of automatic yeses, mainly to catch name
  collisions such as a person named Claude. Answer honestly: a "No" suspends the rule that
  accepted it;
- **edge cases**: credits where the AI product may be the thing that had the flaw, and
  credits naming Qihoo 360 (a security company, not an AI lab).

Question for each: does this credit name an AI tool or AI lab as taking part, rather than a
person who shares a name with a tool, or the product that had the flaw? Answer **Yes**,
**No** or **Not sure** (counts as no). Keys on a computer: `Y`, `N`, `U`.

Two ways to work, switch any time: **one at a time** (credit text, matched terms, flaws
covered, links to example CVE records) or **list by category** (all items on one screen,
Yes / No / ? on each row; **Mark unanswered as Yes/No** answers the rest of a group after
you confirm).

Everything accepted automatically is listed under **Accepted automatically** for reference.

Each distinct credit text appears once even if it covers many flaws, and decisions carry
over to later quarters, so later lists only ask about new credit texts.

## 4. Cohort picks

The month's picks from the seeded random draw, one slot at a time.

- **Edge device and Web/collaboration slots:** only the fix date is needed.
- **Other product (slot c):** is the product reachable from the internet in normal use?
- **AI-credited (slot d):** does the credit say an AI tool took part?

For slots c and d, up to three candidates are listed in draw order. Answer **No** and the
app moves to the next candidate; answer **Yes** and the remaining candidates are skipped
and the app asks for the fix date. If all three are no, the slot stays empty.

**Fix date:** the pre-filled date, where it came from, and the advisory links.

- **Confirm date** (`C`) if the link shows the same date.
- **Correct it** (`E`) to pick the right date.
- **Can't find** if a fix exists but its date can't be established; add a note.
- **No fix yet** if the vendor has not released a fix (for example only workarounds, or
  "fix pending" for every version). The check date is recorded, and the flaw comes back for a fix date in later runs until one exists.
  An unfixed flaw is a real result for the race between fixing and exploitation.

Dates marked *assumed* came from the CVE publication date, not from an advisory: open the
link before confirming.

**Check online** links on every item: the CVE record (cve.org), the NVD page, a product
search, and the vendor's advisory or patch links from the CVE record. They open in a new
tab.

## 5. Help me decide

On AI-credit cards and slot c/d candidates, **Help me decide** (in the list view, it opens
that credit in the one-at-a-time view) walks
through the rule as a few yes/no questions and ends with a suggested answer and the reason.
**Use this answer** records it; **Start over** resets. The questions are:

*AI credit:* (1) Does it name an AI tool or model, not just a company? (2) Is the AI only the
thing that had the flaw? If so, does it also say an AI tool helped find it? (3) Does it say
the tool took part in finding, testing or reporting it? (4) If still unclear: answer no.

*Internet-facing (slot c):* (1) Is it a server, appliance, web app or online service?
(2) Is it normally reached over the internet? (3) If meant to be internal, is it commonly
exposed anyway (from your own knowledge or the vendor's documentation)? Otherwise no.

## 6. Notes, Back and Skip

- **Note:** optional. On a card, type it and tap **Save note** (it also saves when you click
  away). In the list view, tap **Add note** under a credit. Notes are kept even if you clear
  the answer, and appear in the Report.
- **Back:** returns to the previous item to change an answer.
- **Skip for now:** moves on and leaves the item open.
- **Clear my answer** (one at a time), or tap a highlighted answer again (list view):
  removes the answer so the item is open again.

Answers save the moment you tap. Close the page any time; it resumes where you left off,
on any device.

## 7. Report and finishing

The **Report** tab shows AI credits counted, each slot's pick and fix date, dates corrected
or unknown, "not sure" answers, notes and total time. Tap any item to change it.
**Save answers as CSV** keeps a personal copy.

When everything is answered, tell Claude in the chat. Claude then:

1. reads the answers from the app;
2. writes them to `review/decisions.csv` in this repository (one row per item: decision,
   fix date and status, time spent, note), in a dated commit;
3. reruns the evaluation, which uses only `review/decisions.csv`.

Every hand decision behind a published number is therefore public and reviewable.

## What the app does not decide

Which flaws qualify, which slot they fall in and which one is drawn are set by the frozen
rules before the list reaches you. The app records only the three judgments above.
