# Hand Check app: user guide

The Hand Check app is where the author makes the study's hand decisions each quarter. It
replaces working through a spreadsheet. The criteria for each decision are in
[`HAND_CHECK.md`](HAND_CHECK.md); this guide covers how to use the app.

- **Where:** a private page in the author's Claude account, named "Snapshot Hand Check"
  (claude.ai → Artifacts). Only the author can open it. It works on a phone or a computer.
- **Source code:** [`apps/hand-check.html`](../apps/hand-check.html)
- **When:** the day after each quarterly run, and the baseline-year sessions (23-24 Nov 2026).
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

Question: does this credit say an AI tool took part in finding the flaw?

Two ways to work, switch any time:

- **One at a time:** the credit text, the terms that matched, how many flaws it covers,
  and links to open example CVE records. Answer **Yes**, **No** or **Not sure** (counts
  as no). Keys on a computer: `Y`, `N`, `U`.
- **List by category:** every credit on one screen, in two groups:
  1. *Names an AI tool or AI phrase* (for example "in collaboration with Claude",
     "using Codex"). Usually yes, but read each one.
  2. *Lab or company name only* (for example "Jane Doe of OpenAI"). Usually no: count it
     only if the text also says an AI tool took part.

  Each row has Yes / No / ? buttons. Credits covering the most flaws are listed first.
  **Mark unanswered as Yes/No** answers all remaining rows in a group after you confirm;
  use it only after reading the rows, and change any exception before or after.

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
- **Can't find** if no fix date can be established (for example only a workaround exists);
  add a note.

Dates marked *assumed* came from the CVE publication date, not from an advisory: open the
link before confirming.

**Check online** links on every item: the CVE record (cve.org), the NVD page, a product
search, and the vendor's advisory or patch links from the CVE record. They open in a new
tab.

## 5. Notes, Back and Skip

- **Note:** optional, saved with the answer. Use it for anything unusual.
- **Back:** returns to the previous item to change an answer.
- **Skip for now:** moves on and leaves the item open.

Answers save the moment you tap. Close the page any time; it resumes where you left off,
on any device.

## 6. Report and finishing

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
