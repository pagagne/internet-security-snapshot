# Invitation: Independent Reviewer for the Internet Security Snapshot

> Copy of the Claude doc [Invitation: Independent Reviewer](https://claude.ai/artifact/VJaEuiADo22MGeEGadAGnm) (the editable original). The reviewer's tasks and dates are in `docs/schedule/schedule.yaml` (owner `reviewer`) and the reviewer's calendar feed `docs/schedule/reviewer.ics`. Personal details (the reviewer's name, contact details) are never added here.

24 October 2026 · Paul Gagne

Dear \[Name\],

I'd like to ask you to be the independent reviewer for a research project I'm running through 2027: about 15 to 19 hours over roughly 14 months, more than half of it in April 2027. The job needs someone who reads data and calculations skeptically, cares more about whether a number is right than whether it tells a good story, and has no stake in the outcome. \[One sentence on why you thought of this person.\] No security background is needed.

**The project in one paragraph.** The Internet Security Snapshot asks, every quarter, whether defenders are fixing exploitable software flaws faster than attackers start using them, and how artificial intelligence is changing that race on both sides. It uses only free public data: the public list of software flaws (CVE records), the U.S. government's list of flaws known to be attacked (CISA KEV), daily attack-likelihood scores, and company breach filings. The plan was registered publicly in advance on the Open Science Framework (DOI 10.17605/OSF.IO/3XT82, 20 October 2026), so the results cannot be bent to fit a story. A pilot quarter is reported in January 2027, the first scored quarter in April 2027, and a full year of comparable evidence by early 2028. All code and data are public on GitHub: github.com/pagagne/internet-security-snapshot.

## Why an outside reviewer matters

Without an independent check, the project's central safeguards rest on one person and one AI system checking their own work. Three reasons make your role more than a courtesy:

- **It's a public promise.** The registered plan commits to an external reviewer for the first scored quarter. Readers will look for it, and the plan isn't fully kept without it.
- **There is a conflict of interest to offset.** The code is written and the analysis drafted with Claude, an AI model made by Anthropic, and AI labs, Anthropic included, are part of what the study measures. I approve every release, but an independent statistician-minded reader is the strongest answer to the question "who checked the AI's work?"
- **Some errors are invisible from the inside.** A few judgments can't be automated: when a vendor actually released a fix, whether a product is reachable from the internet, whether a finder's credit means an AI tool took part. I re-check my own past answers each quarter, but that only shows I'm consistent. If I'm consistently wrong, only a second person answering the same items blind can show it.

The timing matters too. 2027 is the first year in which AI tools are widely credited with finding software flaws and are increasingly used in attacks. A careful, checkable record of what changed, and what didn't, will be useful to researchers and policy people for years, but only if it can be trusted. Your review is a large part of what makes it trustworthy.

## The role

The role has two parts. You can say yes to both, or only the first.

**1. Independent review of the first scored quarter (Q1 2027).** The main job, once, in April 2027:

- Read the provisional Q1 2027 report (published 1 April) against the registered plan and the logged deviations.
- Spot-check the headline figures: three drawn at random from the report's headline figures, plus any others you choose. Each will come with a short worksheet that states the plan's definition in plain words, gives the inputs as a spreadsheet and lists the steps from one to the other, so you recompute it in Excel or Google Sheets; no programming is needed (if you read Python, you can follow the code instead). If a spot check doesn't match, we trace it together, and the mismatch and its cause are published with your review. To see exactly what this involves, there is a [sample worksheet for the race measure](https://github.com/pagagne/internet-security-snapshot/tree/main/docs/reviewer/sample-worksheet) on real data (about 20-30 minutes).
- Look at a sample of my hand decisions and their written rules.
- Write a short review (two to five pages is plenty): what holds up, what doesn't, what you'd change. It is published as you write it, beside the final report on 1 May, with my response.

**2. Second coder, each quarter (20 items).** After each quarter's hand check, a seeded sample of 20 of my decisions is sent to you with my answers removed. Most are fix dates: open the vendor's advisory and record when the fix was released, about one to two minutes each. A few ask whether a product is reachable from the internet, or whether a credit line says an AI tool helped find the flaw. You answer in a spreadsheet; written rules cover each case. Your answers never change mine; they measure how often two careful people agree, and the agreement rates are published every quarter.

**Also welcome, never required:** a comment on any statistical method at any time (the project's labelling rule, its handling of uncertain dates, its interval estimates), and a seat at the 15 March 2027 annual review, the one time each year the scored rules may change.

## Time commitment

About 15 to 19 hours over 14 months for the required parts, or up to 25 with everything optional. More than half of it falls in April 2027; the rest comes in pieces of under an hour.

| When | Task | Estimated time | Required? |
| --- | --- | --- | --- |
| 2-14 Mar 2027 (earlier if you confirm early) | Getting started: read the two-page overview, the registered plan and the October 2026 statistical review; a one-hour call with me | 3 to 4 hours | Yes |
| 2-14 Mar 2027 | Practice round as second coder on the pilot quarter (Q4 2026), not scored | 45 minutes | Optional |
| 15 Mar 2027 | Annual review session (video call) | 1 to 1.5 hours | Optional |
| 3 to 28 Apr 2027 | Independent review of the Q1 2027 provisional report, code and hand decisions; written review | 8 to 12 hours | Yes |
| 29 Apr - 12 May 2027 | Second coder, Q1 2027: 20 items | 45 minutes | Yes |
| 29 Jul - 11 Aug 2027 | Second coder, Q2 2027: 20 items | 45 minutes | Yes |
| 29 Oct - 11 Nov 2027 | Second coder, Q3 2027: 20 items | 45 minutes | Yes |
| 29 Jan - 11 Feb 2028 | Second coder, Q4 2027: 20 items | 45 minutes | Yes |
| 2-14 Mar 2028 | Read the first annual check of the free data against better reference data, and comment | 1 to 2 hours | Optional |

Each second-coder round has a two-week window and can be done in one sitting, at any time of day. The April review window can shift by a week or two if your schedule needs it; the published date is 1 May.

## What you'd need

- Comfort with spreadsheets and careful arithmetic. Reading Python helps but is not needed: every figure you check will come with a spreadsheet worksheet.
- A free GitHub account, to leave comments and download the quarterly data bundles (reading the code needs no account).
- A spreadsheet program (Excel, Google Sheets or similar) for the worksheets and the second-coder rounds.
- No cybersecurity background. Everything the role touches is explained in the project's documents, and I'll walk you through it on our first call.

The study uses only public data. You won't handle anything confidential or personal.

## What you get

- **Credit.** You're named as the independent reviewer in the Q1 2027 report and in every quarterly report that uses your second-coder answers. You're also listed as a contributor on the archived, citable releases (Zenodo; with your ORCID if you have one). Your written review is a citable document in its own right.
- **A real dataset and a real design problem.** Pre-registered, quarterly, open, with genuine statistical questions: rare events, censored and uncertain dates, small samples, a labelling rule that has to resist noise. If anything here sparks a paper or a talk of your own, you're welcome to it.
- **Influence.** Your comments go into the open record, and the March review is where well-argued changes get made.
- A volunteer role: I can't offer pay; the return is the credit, the experience and the record above.

## Independence and conflicts of interest

- Your review is published as you write it, with my response beside it. I won't edit it, and you're free to disagree with me in public.
- Your second-coder answers are published under your name, or your initials if you prefer, and never change my own answers.
- You can step away at any time; the project will just note that the review role ended on that date.
- Please tell me about any ties to AI labs (Anthropic included), cybersecurity vendors, or the data providers. A tie doesn't rule you out; it gets disclosed beside your review, just as the project discloses its own.

## Next steps

1. If you're interested, or want to know more first, reply to this message or call me. A no is completely fine. If your employer has rules on outside activities (government and many university employers do), please check them before agreeing; the review would be done in your personal capacity.
2. We set up a one-hour call in January or February. I'll send the overview beforehand and answer anything you want to ask about the study or the commitment.
3. If it still suits you after the call, I'll ask for your confirmation by 1 March 2027, so you can be named before the 15 March annual review.

Thank you for considering it. Having someone like you look hard at this work would make it stronger.

Paul Gagne

[Phone or email\]
