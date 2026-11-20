# Build-out record (updated 19 Nov 2026)

The author's request of 19 Nov 2026: a record, in the manual, of every question or prompt put to
the author while the study is being built, with Claude's answer or recommendation and the
solution agreed. Only the chosen option is kept; options that were not chosen are left out.
Exploratory figures, contact details, people's names (beyond organisations) and private data are
left out, because this document is public. The full working notes stay in the private session
logs; how each decision was carried out is in the schedule (`docs/schedule/schedule.yaml`) and
the inquiry log (`docs/INQUIRIES.md`).

## 19 November 2026

### Morning: decisions moved up from the 23 November review

1. **Tool-sweep labels and search rules, and the AI-attack log's outside leads.**
   Claude's recommendation: purpose-first labels; a second security term required for SOC 2
   matches; new search terms with copies of known tools counted once; new searches plus an
   outside index as a quarterly coverage check; count attack-log cases per named group when a
   report describes that group's own activity; work the October-November leads before the pilot.
   Agreed: all of the above, except that every outside lead (not only October-November) is worked
   before the pilot. The sweep rules are applied on 21 Nov; the leads are worked by 18 Dec.

2. **Ray / ShadowRay (CVE-2023-48022).** The author asked what it is. Claude explained it.
   Agreed: added as a reference case (`docs/cases/ray-shadowray.md`) for the 8 Feb 2027 review,
   outside the watch-case rule because it was published in 2023.

3. **The cutover.** The author asked what it involves. Claude explained the steps, purpose and
   signs of success. Agreed: the cutover check stays on 23 Nov.

4. **AI infrastructure as a target (proposed X29).** Claude proposed a measure of attacks on AI
   servers and the shared systems AI stacks run on, after checking it could be measured.
   Agreed at first: adopt it, add AI products to the Censys request, and write a note to
   GreyNoise asking to read its AI-product tags. Later the same morning Claude pointed out that
   it overlapped X5 and X11. Agreed: fold it into X5, X11 and the AI-attack log; X29 retired
   as merged.

5. **Internet-facing AI areas not yet covered.** The author asked what else was missing.
   Claude found five areas. Agreed: AI software supply chain becomes X30; floods of
   AI-generated vulnerability reports become X31; AI-written security fixes are probed first;
   indirect prompt injection is context only; leaked AI-provider keys become a new entry route
   in the AI-attack log.

### GreyNoise

6. **The note to GreyNoise about AI-product tags.** Claude drafted it (mail drafting was not
   available, so the text was given in the chat). Agreed: the author sent it.

7. **When to test the AI-tag reading.** Claude proposed waiting for GreyNoise's reply.
   Agreed: a test the next day, giving GreyNoise a day to answer.

8. **GreyNoise replied positively.** Agreed: proceed; the scheduled test was replaced by a test
   run that day. The test showed the 90-day view lists every day for every tag, so the earlier
   reading of "active days" was wrong; Claude corrected the collector to read GreyNoise's
   90-day totals.

9. **Confirmation run of the corrected collector.** Agreed ("let's run it now"): run at once.
   It worked as expected, with no IP addresses collected.

### Other morning items

10. **X26, how much people hand over to AI.** Claude ran a probe and asked which signals to
    keep. Agreed: keep the four signals (GitHub agent pull requests, Cloudflare Radar's
    user-action share, OpenRouter's agent share, and the news log); an outside economic index
    as dated context only; no separate AI-browser signal; a human-approval column in the
    AI-attack log and the news log.

11. **The baseline-year review list.** The full list was larger than two sessions could hold.
    Claude asked how to handle it. Agreed: keep every flagged race date and finish in December,
    in five sessions (23 and 24 Nov; 9, 14 and 18 Dec), with calendar reminders 30 minutes
    before each.

12. **AI-written security fixes.** After the probe, Claude asked how to use it. Agreed: context
    only, beside X26, repeated once a year.

13. **A public commit that briefly carried an exploratory count.** It was removed within minutes;
    Claude asked whether to rewrite the public history. Agreed: leave the history as it is; the
    privacy scan now blocks a push instead of only reporting.

14. **Open questions for the author.** The author asked whether any were left. Claude listed
    them; all were answered above.

### Afternoon: mail and outside advisories

15. **Three emails in the project inbox.** Claude reviewed them: a news-site account welcome, a
    newsletter already handled the day before, and a vendor marketing email. Agreed: nothing to
    apply. A GitHub app permission request was left to the author as an account setting.

16. **The joint advisory on SafePay ransomware (AA26-293A).** The author asked whether the
    study had it. Claude: not before; its flaws are old ones already on CISA's list, and it does
    not mention AI. Agreed: recorded in the news log as context only.

17. **The FBI flash on North Korea's "FaceStealer" scheme.** The author asked whether the study
    had it. Claude: already among the outside leads, not yet in the AI-attack log; recommended
    entering it now. Agreed: leave it for the 18 Dec lead review; a news-log entry records the
    decision.

18. **The FBI's 2024 public notice on generative-AI fraud.** Claude: not held, by design (a
    trend warning, not a campaign, and before the log's period); offered a background entry.
    Agreed: leave it out.

### Afternoon: building ahead of schedule

19. **What to work on next.** Claude recommended the APNIC Labs collector (X20). The author
    asked why APNIC might limit automated reading and what its terms require. Claude: no
    evidence of a limit; the site had not been tested; APNIC publishes no terms for this data,
    and its written permission asks for credit and figures shown as published. Agreed: test the
    site first, then build the collector. The site allowed automated reading, and the collector
    was built.

20. **The row-count check (risk R9).** Agreed ("proceed"): built, comparing each source with
    its last four quarters.

21. **The credits block.** Agreed ("proceed"): one list of every source's credit, printed on
    every report, its PDF, the README and `docs/CREDITS.md`.

### Afternoon: checking the work before the website

22. **Evaluate the day's work and its logic before the website.** Claude found one design flaw
    (the APNIC figures did not match the quarter), two gaps (credits incomplete; the row-count
    check not wired to anything and its threshold never confirmed) and a process slip (an
    unapproved edit to the public README). Agreed: hold the website; make all four fixes.

23. **Which period the APNIC figures cover.** Agreed: the whole quarter, the 90 days ending on
    its last day (for RPKI, APNIC's nearest published window, 112 days, noted with each figure).

24. **What holds a release.** Agreed: zero rows, or fewer than half the average of the last
    four quarters.

25. **What a hold does.** Agreed: it opens a GitHub issue for the author, and publishing waits
    until the issue is closed.

26. **The README edit and the out-of-date sources table.** Agreed: keep the correction, refresh
    the table, and show the changes to the author first. The author approved them, and they
    were published.

27. **The website plan.** The author asked for a list of what the website build includes.
    Claude listed it. Agreed: as listed.

28. **The diagrams.** The author asked for every diagram to be checked before the website.
    Agreed: all fourteen checked; four updated, the rest confirmed current.

29. **The website, the cutover and going live.** The author asked how they connect. Claude:
    the website does not change the cutover, but after the cutover the daily work queue could
    start the website build on its own, and the planned Publish results workflow would not
    refresh the website. Agreed: both items are done only by the primary chat, and Publish
    results also refreshes the website. The website build waits until 17:00, when the author's
    usage renews.

30. **A build-out section in the manual.** Agreed: this document, in the manual's records part,
    not in the operating procedures.

31. **Changing the model or starting a new chat.** The author asked whether a new chat could use
    a newer model. Claude: yes, and the model can also be changed within a chat; a new chat
    becomes primary only when the author says so. Agreed: keep this chat as the primary on an
    upgraded model; schedule the new-chat test for after the pilot.

32. **An independent, adversarial review of the study.** Agreed: around 3 Feb 2027, after the
    pilot's final report, Claude Fable 5.1 reviews the whole study in a new chat outside the
    project, given only the public repository, with past-chat search and memory switched off.
    It covers the method, the race measure, hand-check reliability, dependence on sources,
    statistics, and a privacy reading of every public document for anything from private
    conversations or correspondence. The author decides what to act on; changes to the
    registered core wait for the 15 Mar 2027 review.

### Evening

33. **The README's Mission section, shown word for word on the website, was out of date.**
    Claude drafted an update. Agreed: as drafted. VulnCheck is listed with the collected data
    (from the 1 December test run), two sources are still pending (Shadowserver), the
    international views are marked exploratory with every agency the study uses, and GreyNoise
    and the SANS Internet Storm Center are named as context.

34. **An old open task, "Continue the research window".** The window ended on 15 Nov.
    Agreed: closed as done.

35. **When to approve the pilot-timeline layout on the run-health page.** Agreed: on 23 Nov,
    as planned; the draft label stays until then.

36. **A step-by-step guide for the website.** Agreed: `docs/WEBSITE.md` covers switching the site
    on (4 Dec), approving the draft sections, and how a results publish flows from January.

37. **May a successor approve reports if the author cannot?** Claude recommended a limited,
    written delegation. Agreed: no delegation; results wait for the author, while the runs
    and frozen data continue.

38. **When to name the successor and grant access.** Agreed: at the 28 Nov account check,
    together with two-factor sign-in and recovery codes.

39. **The details written today for each exploratory measure belong in the manual.** Agreed:
    `docs/EXPLORATORY_MEASURES.md`, built from `config/exploratory.yaml` (one section per
    measure: question, status with its dated note, sources and method), kept in Appendix A for
    now, beside this record, and checked so it can never fall behind the file. The manual's main
    parts are then built up from the build-out records.

40. **The privacy scan flagged three lines in the new exploratory measures document.** They were
    method text already public in `config/exploratory.yaml` (source names such as "Unit 42", the
    fixed list of 57 protocols, a 100-star checking threshold, a sample of up to 100), not study
    results; the push had gone out because the scan did not yet read files before they were
    added. Agreed: mark those three lines as reviewed, tied to their exact wording, so any change
    is checked again. The scan now also reads new files before they are added.

41. **Where is the step-by-step guide for the independent review?** It existed only in three
    schedule entries. Agreed: a guide, `docs/INDEPENDENT_REVIEW.md`, in Part VI of the manual:
    the choices made, the author's eight steps on 3 Feb 2027, what Claude does after, and what
    the brief asks the critic to do.

