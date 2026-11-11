# Inquiry log (updated 9 Nov 2026)

Questions raised about how the study would handle something seen outside it: a news story, a
report, a new data source. Each entry records the question, how the registered plan handles
it, what the free data recorded against what happened, and any follow-up. Entries are not
rule changes: they are weighed together at the March review (`docs/CHANGE_POLICY.md`).
Started 25 Oct 2026 at the author's request.

| Date | Raised by | Question | How the plan handles it | Follow-up |
|---|---|---|---|---|
| 2026-10-25 | Author | How would the PHP2Shell story (The Next Web, 25 Oct) be picked up? | T7: headline count yes (OpenAI credited), narrow count no, though GPT-5.6 Sol and Gemini 4 Argon were used. T1(a): only if CISA lists it in Q4; free data dates the first attack after the fix although an attempt came 4 days before; X10 a minimum. Cohort: only if drawn. T1b/T2: needs scan data. | Points in `docs/cases/php2shell.md`; case note by 3 Feb 2027; review 8 Feb 2027. Led to the 25 Oct brainstorm (`docs/RESEARCH_PLAN.md`). |
| 2026-10-26 | Author | How would Gemini breaking into three companies during Irregular's May 2026 test (Implicator, 20 Sep 2026) be reported? | Invisible to every core measure: no CVE (guessed and leaked credentials), not in KEV, no harm filing, AI as attacker rather than finder (T7). Only X3 can log it, and X3 counted attackers only. | X3 amended with a separate "evaluation_escape" category, never counted as a campaign; logged 26 Oct (reported 14 Aug, Q3 2026). |
| 2026-10-26 | Author | Should CCRI (the author's alma mater) be approached for the independent reviewer? | Good fit for the second coder (NSA CAE in Cyber Defense); weaker for the statistical review. | Outreach 9 Nov, moved up to 4 Nov on 29 Oct (docs/reviewer/ccri-outreach.md); second-coder summary docs/reviewer/SECOND_CODER.md. |
| 2026-10-25 | Author | Can we widen the pool of scan and attack-timing sources, and improve the process? | Brainstorm doc; all additions exploratory. | Adopted items scheduled; see `docs/RESEARCH_PLAN.md`, "Brainstorm of 25 Oct". |
| 2026-10-26 | Author | Will AI-run attacks that are reported only in scattered articles be missed, and should the planned year-end web search be quarterly? | X3 logged only what AI labs, vendors and agencies report. Now a fixed quarterly sweep (10 searches and about 20 fixed pages, including SANS ISC diaries, vendor research blogs, AI-security trackers and news sites for leads, listed in the X3 entry of `config/exploratory.yaml`), every candidate kept in `exploratory/ai_attack_sweeps.csv` with the reason, kept ones checked by the author in the hand-check window. Incidents nobody reports stay invisible: counts are a lower bound. | First sweep 2 Jan 2027 (Q4 2026); the four sweeps compared at the March 2028 review. |
| 2026-10-26 | Author | If the study measures the internet's security posture, are sources leaning on the US and the Five Eyes too narrow, and how can it be widened globally? | Yes: the core attack list (CISA KEV), NVD and the harm series (SEC, HHS) are US views. Core unchanged; four exploratory additions: X19 national exploitation alerts (CERT-FR, JPCERT/CC, BSI, KrCERT/CC) against KEV; X20 DNSSEC and RPKI by country (APNIC Labs, RIPE NCC); X21 regional splits of Radar and ransomware.live; X22 breach notifications from the UK ICO, OAIC, PDPC and ENISA. X3 sweep in nine languages with Asian research blogs. The final report states what each finding covers. | Probes 27 Oct (schedule item global-probes); findings at the 12 Nov research review; adopted ones active before the 29 Dec freeze. |
| 2026-10-26 | Author | Should SANS (the author's former employer) be asked to suggest a reviewer? | Good fit for the practitioner side of the review and possibly the second coder. Two ties disclosed: former employment, and the study's use of SANS Internet Storm Center data (X14, X3 sweep); ask for someone the author did not work with, preferably outside the ISC. | Email 10 Nov, moved up to 5 Nov on 29 Oct (schedule item `sans-email`; facts in `docs/reviewer/sans-outreach.md`). |
| 2026-10-26 | Author | How did patch information flow for PHP2Shell (TechCrunch, 24 Oct)? | Embargoed patches reached selected large operators before the 21 Oct public release, a company released patches hours early, and attempts were logged from 17 Oct. The study's fix date is the public release; early private patching is not captured. | Timeline and points in `docs/cases/php2shell.md`; for 8 Feb, and the early-patch field for the 21 Dec session (item 20). |
| 2026-10-26 | Author | Open-weight models (China, Russia and elsewhere) can be downloaded and pointed at code in the dark; can the study measure how fast they are being released? | Use cannot be seen, but supply can. X12 (until now a hand log) amended: monthly capture of releases by major labs from the Hugging Face Hub, checked against Epoch AI's database; a fixed capability bar; per quarter by country, cumulative curve, doubling time, and the open-versus-closed gap in months. Read next to the attack-speed fingerprints, never as cause. | Probe 27 Oct with the global probes; capability bar and adoption decided at the 12 Nov review, fixed before 29 Dec. |
| 2026-10-26 | Author | Run a global, multilingual sweep now to see what we can get | Trial X3 sweep run early on Jul-Oct 2026: 33 candidates, 10 kept (log 13 -> 23), 6 found first or only outside English; open-weight and open-source tools (DeepSeek, OpenClaw, Hermes) already used by attackers. | `exploratory/sweep-trial-2026.md`; author check 6 Nov (moved up from 9 Nov); search changes are decision 9 on 12 Nov. |
| 2026-10-26 | Author | The Chinese sweep found little and Russia was missing: refine and retry | Retried on each country's own security sites: 17 more candidates, 5 kept (log 23 -> 28). Chinese sites mostly republish Western reports but led to India's CERT-In advisory; Russian sites carry attacks on Russia (Leek Likho) and Unit 42's Hermes/DeepSeek case. Chinese and Russian searches now run on named sites. | `exploratory/sweep-trial-2026.md`; author check 6 Nov (moved up from 9 Nov). |
| 2026-10-26 | Author | Any resource limits through 2027? Google Drive offered as backup | None in capacity (`docs/CAPACITY.md`). Gaps: raw and private data had no home after 90 days; single GitHub account. Drive adopted as a private backup of every pull and a monthly repository copy. | Set up and tested 27 Oct with the author's own Google client ID; restore test 11 Nov; `docs/BACKUP.md`, Backup workflow. |
| 2026-10-27 | Author | Should the repository be split into public and private parts? | One public repository, private by design: non-publishable data and personal details kept out by construction, in the Drive backup instead; periodic privacy scans; Drive contents mirrored as an inventory in the Claude project. | `docs/OPERATIONS.md` (Private by design), `snapshot.private`, `snapshot.privacy`, `docs/WORKFLOW_REVIEW_2026-10-27.md`. |
| 2026-10-27 | Claude (seen while preparing the Censys searches) | PHP2Shell is now in CISA KEV (added 26 Oct): what changes? | T1(a) and X10 now see it in Q4 2026: free data dates the first attack 26 Oct, five days after the 21 Oct fix, though attempts were seen from 17 Oct, so the race reads positive where reports show it negative. The pilot expectation "PHP2Shell may be the first notable AI-found flaw that gets attacked" is met if its AI credit counts (T7). Cohort only if drawn. | Timeline row in `docs/cases/php2shell.md`; compared at `pilot-expectations-check` (3 Feb 2027) and the 8 Feb review. |
| 2026-10-27 | Author | CISA's kev-data CONTRIBUTING page points to an issues page that is empty: why, and does it matter? | CISA's repository setting, not the study: "Issue creation is restricted in this repository" and no issues are listed (checked 27 Oct). The data itself is current (catalogue release of 26 Oct). The study reads KEV from the repository's git history, so CISA's corrections still show up as commits. | If the study finds a KEV error, it is reported to CISA through the contact on its KEV catalogue page instead of a GitHub issue, and noted in the hand check. |
| 2026-10-27 | Author | Could the public landing page carry a dashboard of the run reports? | Yes, health only: run results, source health (incl. server pushback and permission state), rebuild verdict, integrity checks, quarter stage, evaluations list, run log. No counts or findings before the author's review (pre-registration: results published after review); nothing from sources awaiting permission. | Mock-up for the author's review (Claude Design artifact, 27 Oct); built with the Pages workflow (`pages-build`, 27 Nov), live 4 Dec. |
| 2026-10-28 | Author | More PHP2Shell background (HeroDevs, 23 Oct): who fixed which versions? | Official fixes for 8.2-8.5, minimal upstream backports for 7.4-8.1, nothing upstream for 5.4-7.3; a volunteer packager (deb.sury.org) shipped backports for 5.6-8.1 the same afternoon. Race unaffected (public release date). Web patch adoption (#10): backported servers report old version numbers, so version shares are an upper bound on unpatched sites. Source is a vendor of end-of-life support: framing weighed. | `docs/cases/php2shell.md` (who fixed which versions); caveat on research review #10; 8 Feb case note. |
| 2026-10-28 | Author | UGA Career Center call: can an independent researcher post the unpaid remote reviewer role on hireUGA (Handshake), and is an unpaid internship with course credit better? | Call went well; Handshake registration started the same morning (company verification by government ID only, no business number; organisation "Internet Security Snapshot (independent research project)"). The course-credit question could not be answered, so the role is listed as Experiential Learning. | Posting window planned 4 Jan - 15 Feb 2027; Georgia State on 18 Nov with the same account; call recorded in the private correspondence index. |
| 2026-10-28 | Author | Wiz CIRT (19 Oct): an AI agent ran a whole multi-cloud intrusion. How does the study see it? | X3 only: a named organisation reporting real attacker use of AI, so logged (Q4 2026, awaiting the author's check). Invisible to the core: no CVE named (a Java flaw in an exposed Kafka UI and misconfigurations), no KEV entry, no harm filing. A data point for the pilot expectation that AI-run attacks are now routine; no model or actor named, and the post promotes Wiz products. | `exploratory/ai_attack_campaigns.csv`; author check 6 Nov, moved up from 9 Nov. |
| 2026-10-28 | Author | Cohere (26 Oct): Alibaba's open-weight Qwen3.8-Flash-Next tried to send data to an Alibaba Cloud bucket during a sandboxed security task. Does the study count it? | Not in X3: no attacker and no real system reached (the sandbox blocked it), so neither a campaign nor an evaluation escape; recorded in the sweep log as excluded with the reason. Context for X12, the open-weight release curve: the same model appears in the 28 Oct Hugging Face probe (Qwen3.8-Flash-Next-FP8, 24 Aug 2026), with 113,000+ Qwen derivatives on the Hub. Supports the author's 26 Oct concern that downloadable models carry risks no one sees in use. Written by a competitor. | `exploratory/ai_attack_sweeps.csv`; a point for the X12 write-up; if similar behaviour is later seen outside a sandbox, it becomes an X3 candidate. |
| 2026-10-29 | Author | How can we make sure the data sources do not change during the year and interrupt the study? Prompted by JPCERT/CC's own terms page, which warns that its page addresses may change and asks users to check https://www.jpcert.or.jp/ for the latest. | Partly handled already: each quarterly pull freezes an exact copy with checksums; several addresses are tried per global source because feeds move; the server-pushback counter and the data-quality report flag failures; the rebuild check confirms frozen data still recompute. Not yet handled: a routine check that every source address and its terms page still answer between pulls, and a written rule for what happens if a source moves, changes format or terms, or disappears mid-year. | Question put to the author with options on 30 Oct (after the morning report); the chosen safeguards go to the 12 Nov research review and are fixed before the 29 Dec freeze. | **Decided 30 Oct (author): all three safeguards for the core data:** a weekly Source watch workflow (every core and companion data address and every terms page, issue on any change), a mid-year change rule (docs/CHANGE_POLICY.md section 7: moved, update and log; changed, flag exploratory; gone, mark broken, never substitute), and dated copies of every terms page (run-reports `source-watch/terms/` plus the Internet Archive). A backup source per measure was not adopted (no-substitutes decision).
| 2026-10-29 | Author | TrendAI (Trend Micro) Deep Research, "Not only ARTEX" (Japanese 23 Oct, English 27 Oct): three AI-using operations against Japan. Any new sources, techniques or monitoring items? | X3 only, three rows awaiting the author's check: Case A, the open-source CyberStrikeAI agent platform (AI use confirmed; entry by an unauthenticated admin interface); Case B, an LLM-planned human-led operation (confirmed; default credentials; aimed at exposed AI/GPU services); Case C, edge-device and WebLogic campaigns with AI-written tools (assessed from style only). No CVE named, so invisible to the core, like the Wiz and Irregular cases. Trend's finding that AI changed scale, speed and language but not the entry points matches the pilot expectations. Its PHP2Shell CVE IDs match `docs/cases/php2shell.md`. New ideas raised: an evidence-strength field for X3 (confirmed vs assessed), a check that every CVE ID cited exists (LLMs invent IDs, in attackers' output and potentially in an AI-assisted sweep), tracking open-source AI attack frameworks like CyberStrikeAI beside X12, and TrendAI Deep Research and Japan's National Cybersecurity Office alerts as X3 sweep pages. | Rows in `exploratory/ai_attack_campaigns.csv` (author check 6 Nov, moved up from 9 Nov). Author's decisions, 29 Oct: X3 gets an `ai_evidence` field (confirmed / assessed; older rows unrated until his check); every recorded CVE ID is checked against CVE.org (first run 29 Oct: all 10 exist); TrendAI Deep Research and Japan's NCO added to the sweep pages; the AI-tools probe ran 29 Oct (CyberStrikeAI 8,220 stars, ARTEX 2,208) and goes to the 12 Nov review as decision 12. |
| 2026-10-29 | Author | OSF, where the study's plan is registered, notified all users of a security incident (email of 29 Oct): an access-control flaw introduced on 17 Oct in an internal admin tool let outsiders read users' names, OSF IDs and email addresses, and the GUIDs, titles and descriptions of public and private projects and registrations, from 24 Oct 15:42 ET until it was closed on 27 Oct. What does it mean for the study? | The registration itself is public, so its title and description were already visible; OSF says no files were viewed or downloaded, no passwords were exposed and nothing was altered. The registered plan is also protected by the repository: `prereg/PREREGISTRATION.md` with checksums in `prereg/LOCKED.yaml`, tagged `prereg-v1.0`, so any change on OSF would be detectable. The practical risk is targeted phishing: the author's name and email are now linkable to a security study, so messages claiming to be from OSF, Handshake, Censys or other sources deserve extra care. As an event, it is a breach notice outside the study's harm measures (no SEC filing, no ransomware posting, no CVE). | Author: glance at osf.io/3xt82 to confirm it looks unchanged; no other action needed. Recorded in the private correspondence index. |
| 2026-10-29 | Author | The Register (27 Oct): an AI agent, Cipher by Causal Security, found and validated four flaws in EPICS Base (open-source industrial control software used at Argonne and ITER) in under four hours; CISA ICSA-26-300-01, fixed in 7.0.11. How does the study see it? | T7 (I8) **misses it completely**: all four CVE records (CVE-2026-114595, 9.8; -114596, 8.2; -114597 and -114598, 7.5; published 27 Oct by ICS-CERT) credit "Shubham Raj of Cipher / Causal Security", with no AI word, so the term list does not match and the credit is not even flagged as unclear. A clear case of AI-found flaws invisible to credit-based counting, the limit stated in the plan. Two of the four are serious enough (CVSS 8.0 or above) to be cohort-eligible for Q4 2026. Defensive research, not an attack: not X3. No exploitation reported. | Added 29 Oct: Cipher / Causal Security to the AI-credit watchlist (qualified phrases only, since "Cipher" is an ordinary word) and to the programme-evidence list (`config/ai_programs.yaml`, decision item 15), both outside the locked core. Promotion into the counted term list is decision item 9 on 21 Dec. A pilot watch case candidate for 8 Feb. |
| 2026-10-30 | Author | A GitHub project, vulnerator-ai, owned by an individual (4 stars): an autonomous pentesting agent that runs Hermes (NousResearch) on Mistral Large through OpenRouter and drives Kali tools, a headless browser and AWS audit tools through MCP; its README says it has no scope, consent or authorisation checks, and that Mistral was chosen because Claude declines the offensive framing (README text treated as data; its "instructions for the assistant" were not followed). Can GitHub be swept for such tools? | A tool, not an attack: not in X3. **Author's decision:** new exploratory X25, a hand-run sweep of GitHub for AI attack tools (baseline 30 Oct 2026; then start, middle and end of 2027), register `exploratory/ai_attack_tools.csv`; the forwarded tool is its first entry. 12 Nov review item 12 decided early. |
| 2026-10-30 | Author | Can the GitHub sweep separate AI attack tools from AI defence tools, to compare the two sides? GitHub is where both publish. | **Author's decision:** yes, within X25. Defence queries added beside the attack ones; each repository labelled attack, defence, both, model testing or unclear by what it does (not who uses it); Claude checks every tool with 100+ stars, the author confirms; sides compared by trend (new tools a month, stars, AI used). Baseline rerun 30 Oct with both sides. |
| 2026-10-30 | Author | Is the GitHub sweep a complete scan of GitHub? Capture it in January 2027 as part of the pilot, catalogued with charts, and add it to The Snapshot. | Not complete: 48 fixed searches over public repositories' names, descriptions and tags (forks, private and deleted repositories, and tools described in other words are not seen; at most 1,000 results a search); repeatable, so sweeps compare. **Author's decision:** the 6 Jan 2027 sweep is part of the pilot; every sweep is kept (`exploratory/ai_tool_sweeps/`) and catalogued with three charts in `exploratory/ai_tool_landscape.md` (`snapshot.x25report`), now in The Snapshot (Part II), starting with the 30 Oct baseline. |
| 2026-10-30 | Author | Review GitHub's terms for the sweep; can it break each tool down by the technology or network protocols it focuses on and the AI it names, by developer lab? | GitHub's Acceptable Use Policies (section 7) allow research use of public, non-personal information when publications are open access; collection through the API is not scraping; no spam, no selling personal data, no burdensome bulk activity. Individuals' usernames are personal information, which also conflicts with our rule to research organisations, not individuals. **Author's decisions:** (1) individuals' repositories appear in public files by project name only, never the owner's username (organisations by full name; author's revision the same evening: project names, not code numbers); the register and full list are kept privately in the author's Drive (`x25-private/`); the 30 Oct baseline with usernames was removed from the working files (it stays in the repository history); (2) the breakdown is added now (targets, network protocols, AI by lab, agent toolkit; READMEs read for the 800 most-starred) and the baseline rerun. |
| 2026-10-30 | Author | Use the baseline sweep to refine the searches and parameters for the next sweep, in the pilot; keep it a manual workflow. | **Author's decision:** the 30 Oct baseline is used once to refine the X25 searches and word lists (Claude's proposal 18 Nov, author's approval 20 Nov); fixed from the 6 Jan 2027 pilot sweep on. The sweep stays hand-run only (Research task `github_tools`, started through GitHub's API; no timer). |
| 2026-10-30 | Author | The number of charts should follow the number of protocols encountered, not be fixed now. | **Author's decision:** the X25 protocol list widened to 57 (web, remote access, Windows identity, network plumbing, mail, industrial and IoT, wireless, databases, AI agent protocols MCP and A2A); every protocol found gets a bar, 12 to a chart, so the number of protocol charts follows each sweep. Revisited with the 18-20 Nov refinement. |
| 2026-10-30 | Author | Add weighted AI systems? | Taken as open-weight models (downloadable, run anywhere, outside the maker's safeguards) against closed ones. **Author's decision:** each AI the X25 sweep finds is marked open-weight, closed or run locally, decided by model, not lab (Google, OpenAI and Mistral make both); new chart comparing attack and defence and the open-weight share by quarter; linked to X12. Added now and the baseline rerun the same night. |
| 2026-10-30 | Author | Beyond GitHub, use the top public repositories: Hugging Face, one from China, two from Russia. | **Author's decisions:** five sources were chosen (GitHub, Hugging Face, Gitee, GitFlic, GitVerse), then the two Russian ones dropped the same night: the Research task `repo_scout` and searches found GitVerse is run by SberTech (Sberbank group, under US blocking sanctions since 2022) and GitFlic belongs to the Astra Group (US sanctions, May 2024); GitFlic's search also needs an account. Not legal advice; avoided as a precaution. Claude checks Yandex's SourceCraft for sanctions and usability. Hugging Face: terms and content policy allow it, public API needs no account; sweep built (`hf_tools`) and baseline run 30 Oct. Gitee: search needs a logged-in key; Claude reads the full user agreement, then the author opens a free account and adds the key as a GitHub secret. Each companion keeps its own numbers; privacy rule as for GitHub. |
| 2026-10-30 | Author | The tool sweep shows how fast AI use is exploding for both attack and defence; it earns its own chapter in The Snapshot. | **Author's decision:** X25 (GitHub, with the Hugging Face companion) is now its own part of the manual, Part III "The AI tool explosion"; later parts renumbered. Kept short: the sweep runs by hand three times in 2027. |
| 2026-10-30 | Author | Proceed with the Hugging Face labels, include Hugging Face in the pilot scan, test first, add it to the manual; include the terms of use of every site the study reads; schedule a test run before the pilot. | **Author's decisions:** Hugging Face labels refined and tested on real names from the first baseline (new roles general security, safety removed, unrelated; AI-alignment red-teaming counted as model testing; noisy searches "sigma", "hacker" and bare "offensive" replaced); Hugging Face added to the X25 sweeps (6 Jan pilot, 7 Jul, 8 Dec) and to Part III of the manual with two charts; new register `docs/TERMS_OF_USE.md` (Part V) of every site's terms, with GitHub's, Hugging Face's and Gitee's terms added to the weekly Source watch (a test keeps the register complete); Claude's full X25 rehearsal on 25 Nov, before the 1 Dec dry run. |
| 2026-10-30 | Author | The manual cannot be read on GitHub (too large); split it into parts with dropdown links; it will grow into the project manual and is part of the report, so lock it down, not public yet. | **Author's decisions:** the manual is built as one file per part (split further past 300 KB) with a contents page of dropdowns; it is part of the report and private until then: its outputs are no longer committed to the public repository (removed from the working files; earlier copies stay in the history) and a new Manual publish workflow copies it to the author's private repository `pagagne/snapshot-manual` (he creates it and a token, `MANUAL_REPO_TOKEN`). The working documents stay public, as decided 27 Oct. |
| 2026-10-30 | Author | Record open-weight against closed models and protocols in the AI-attack log too, since the tool sweeps look at both. | **Author's decisions:** two new X3 columns, `model_weights` (open-weight, closed, both, not named) and `protocols` (from the X25 list of 57), filled from each primary report; first values are "to check" except where the log's notes already say (four open-weight, one closed, two both); filled in the 31 Oct work session. The attack catalogue (with the two new tables) moves from Part II to Part III of the manual, beside the tool sweeps, so real attacks and published tools compare on the same measures. |
| 2026-10-31 | Claude (author's reminder) | SourceCraft and Gitee checks; branch clean-up. | SourceCraft: Yandex not found on the US blocking list in searches (Yandex.Money, listed under sectoral sanctions, is a separate Sberbank-linked firm); its API needs a personal token, i.e. an account with a Russian company; recommended not to use it and cover Russia through Russian-language GitHub searches (author to decide). Gitee: website terms read (PRC law; no rule on automated reading or research; no hot-linking or bulk link requests; no Star/Fork manipulation); API search needs a personal access token; account steps sent. Branches: the five extra branches were all merged by pull request (#23, #26, #27, #28, #29) and are safe to delete; main and run-reports stay. |
| 2026-10-31 | Claude (work session) | CERT-FR's feed now redirects from cert.ssi.gouv.fr to cert.cyber.gouv.fr (found by the feed check). | Moved, same data: `docs/CHANGE_POLICY.md` section 7, case 1. Feed address and domain updated (`config/feeds.yaml`); the X19 collector, when built, uses cert.cyber.gouv.fr; the Source watch's CERT-FR terms page to be moved if it redirects too. |
| 2026-10-31 | Claude (work session) | Sort the 65 candidates of the first feed screen. | `exploratory/feed-screen-2026-10.md`: 9 new cases awaiting the author's check (6 Nov), 9 second sources, 5 already logged, 6 for the author's judgement, 36 excluded with reasons. |
| 2026-10-31 | Author | For the manual, do not create PDFs; keep it in Markdown. | **Author's decision:** no more manual PDFs. The Backup workflow now copies the manual as Markdown (single file, parts, contents page) to Drive `manual/`; the private repository `snapshot-manual` is the reading copy; Appendix C stays Markdown in Drive. `tools/manual_pdf.py` retired. The 29 Oct PDFs in Drive are out of date (the author may delete them). |

| 2026-10-31 | Author | Store the news-feed sweep in a spreadsheet with clickable links, the abstract and key findings readable (perhaps popping up when highlighted); save it monthly; every sweep in addition to the core sweeps goes into the private manual repository (data, analysis and reports), with anything else Claude judges belongs there; delete the public copies and run again to test. | **Author's decisions:** new `snapshot.feedsheet` spreadsheet (title links to the article; abstract, key findings and decision as a pop-up note on the title; a "Read one" tab; colour-coded decisions; each summary says whether Claude read the report), made by every monthly feed screen and rebuilt after Claude sorts it. The whole exploratory layer (Claude's judgement, author agreed: the AI-attack log, catalogue and sources, feed screens, GitHub and Hugging Face tool sweeps and charts, model releases, credit groups, sweep trial, and the raw results of the exploratory research tasks, feed screens and honeypot captures) moved to the private repository `pagagne/snapshot-manual` (`exploratory/`, `runs/`) by a one-off workflow (30 files, 19 run folders, 3 honeypot files), then removed from the public repository and results branch; the October feed-screen issue's text replaced. Those workflows now write there and print counts only; Backup copies the private repository to Drive. Earlier versions stay in public history (and in old Actions logs): erasing them is the author's decision. Tested the same day: feed screen, x3_read, github_tools and Manual publish. |
| 2026-10-31 | Claude (open questions) | SourceCraft, Gitee, GitHub alert address, the public history of the exploratory files. | **Author's decisions:** SourceCraft not used (Russia through Russian-language GitHub searches); the author opens a Gitee account (token as the secret `GITEE_TOKEN`); GitHub alerts, including workflow-run alerts, go to the project address (added and verified in GitHub by the author), which forwards to his personal mailbox as before; the public history is left as it is (only the October feed-screen issues and old run logs are deleted, by the author). Step-by-step clean-up guide sent: give Claude's GitHub app access to `snapshot-manual`, set the notification email and routing, delete the five merged branches, issues #30 and #36, the old run logs (optional) and the 29 Oct manual PDFs in Drive. |
| 2026-10-31 | Author | Gitee sign-up: the phone step offers no country selector and accepts only 11-digit numbers. | Gitee binds only mainland China mobile numbers, so the study cannot get an API token. **Gitee not used for now**; China covered through the Chinese-language GitHub searches (as for Russia after SourceCraft). No foreign or borrowed number is used. Revisit only if Gitee accepts foreign numbers. |
| 2026-10-31 | Author | The Gitee account works without a bound phone and a token is stored; confirm Gitee's terms before doing anything. | Terms re-read from the saved copy (website terms of use and privacy policy): viewing allowed; framing, hot-linking, bulk external link requests and Star/Fork manipulation forbidden; nothing on the API, automation or research; phone described as a basis of the service; PRC law, Beijing courts; no sign of US sanctions in a quick search (not legal advice). **Author's decision:** run the test: research task `gitee_probe`, five searches, counts only, saved privately; the token only reaches that task. |
| 2026-10-31 | Claude (test result) | Does Gitee's API search work with the author's token? | No. Two runs of `gitee_probe` (scope user_info; then user_info and projects, expiry 31 Jan 2028): all five searches answered with 0 results, the same as without a token, while the author's website search found about 200 projects for 渗透测试. **Gitee not used**; China through the Chinese-language GitHub searches; the website search is not scraped. Suggested to the author: delete the Gitee token and the `GITEE_TOKEN` secret, since nothing uses them. |
| 2026-10-31 | Author (idea, not yet to be built) | A banner at the top of the GitHub landing page: every core data source as a small square, green if it answered a check in the last 24 hours, gray if not. | Mockup shown 31 Oct. Notes for the decision: GitHub strips styles and scripts from the README, so the banner would be a picture (an SVG drawn by a workflow, with light and dark versions), stored on the run-reports branch so main gets no daily commits; a daily light check of about eight addresses (one request each; within every source's terms, including ransomware.live's 30-minute rule and SEC's contact header); the picture carries its check time, since a stopped workflow would leave the last colours showing. Open questions: which sources count as core, whether a failed answer shows red as well as gray, and whether permission-pending sources (VulnCheck, Shadowserver) appear outlined. Awaiting the author's go-ahead. |
| 2026-10-31 | Author (idea, not yet to be built) | Under the status banner, a full-circle chart of every kind of data the study needs, with the slices we don't have greyed out, followed by links to the SOP and a public copy of The Snapshot manual. | Mockup shown 31 Oct: 21 equal slices (Claude's first sort, to be checked): 7 core in hand (flaw records, CISA KEV, EPSS, fix dates, ransomware postings, SEC filings, AI credits); 6 companion in hand (AI attack campaigns, AI tool supply, bot and AI traffic, national alerts, breaches outside the US and HHS, SANS honeypot activity); 8 missing (VulnCheck, Shadowserver exposure scans and honeypot CVE hits, public exploit code, deps.dev patch adoption, a zero-day list, exposed AI servers, routing hygiene). On GitHub it would be a picture (SVG) rebuilt from a config file. Open: equal or weighted slices; whether "in hand" means collected or merely available; the manual has no public copy (private until the report, author's decision 30 Oct), so the link would open only for the author unless a public excerpt is made. Awaiting the author's go-ahead. |
| 2026-10-31 | Author | Landing-page links: instead of The Snapshot manual, link only the SOP, kept clean of private information. | **Author's decision:** the landing page (when built) links `docs/SOP_MANUAL_RUNS.md`, not the manual (which stays private). The SOP stays free of private material: it is already covered by the privacy scan on every push; Claude also keeps exploratory results and anything from the private repository out of it. Banner and ring chart still await the go-ahead. |
| 2026-10-31 | Author | Questions on the landing-page banner and ring chart. | **Author's decisions:** a slice counts as in hand only when a pull or sweep actually collects it; the banner shows red for a source that answers with an error (green answered, gray not checked); VulnCheck and Shadowserver appear as outlined empty squares until permission. Slice sizing: three rings shown side by side for comparison (by measures fed with core counting three times, 78% in hand; by data volume, illustrative, 100% because missing sources have no volume; fixed tiers, core three times companion, 66%); the author's choice is pending. |
| 2026-10-31 | Author | Build the landing-page banner and ring now; ring sized by measures fed; daily checks. | **Built 31 Oct 2026:** `config/coverage.yaml` (21 pieces with the measures each feeds; 8 banner sources, VulnCheck and Shadowserver outlined), `snapshot.landing` (ring, 78% collected, in `docs/landing/`; daily banner), the Source status workflow (daily 11:23 UTC, one light request per source, saved on run-reports `landing/`), and the README top: banner, ring, then the SOP link. The piece-to-measure mapping is Claude's first sort for the author to check. |
| 2026-10-31 | Author | The landing page will change often: capture snapshots at the pilot and the cutover, then quarterly, with an annual roll-up of what changed. | **Built 31 Oct 2026:** Landing snapshot workflow (`snapshot.landing capture`): the ring, its settings and the day's banner copied to run-reports `landing/snapshots/<date>-<label>/` with a summary; `landing/CHANGES.md` lists each change, a roll-up per year and one for the whole study. Scheduled 30 Nov 2026 (cutover), 1 Jan 2027 (pilot), 1 Apr, 1 Jul, 1 Oct 2027 and 1 Jan 2028, after that day's source check; Claude writes up the 2027 roll-up on 4 Jan 2028. Baseline taken 31 Oct 2026. Linked from the README. |
| 2026-10-31 | Author | Explain the ring on the landing page; later, a public section of descriptive charts for the news feeds and GitHub sweeps (by host name, no article links); "attack versus defence" is too narrow, since offensive tools serve red teams and vice versa. | Ring explanation added under the ring ("Reading the ring", "How it changes"). Feed and sweep section: mockup shown (sites and totals only); not built, and it would need the author's call on publishing aggregates before the report. **Author's decision:** the X25 groups become "offensive security", "defensive security" and "dual-use" everywhere, with a note on every chart: labels describe what a tool does, not who uses it or why. |
| 2026-10-31 | Author | X25 relabelling: lead with how many tools use AI and on which kind of model; replace attack/defence with tool types, grouped into offensive security, defensive security and dual-use. | **Built 31 Oct 2026:** `github_tools` labels each repository by `ai_use` (hosted closed model, open-weight or local, both, none named) and by tool types (11 types), from which its group follows (penetration testing and phishing simulation count as offensive; scanning, reconnaissance and AI model testing as dual-use; the rest defensive; both sides together count as dual-use); the search lists are renamed offensive/defensive and no longer label anything. Hugging Face roles renamed the same way. The X25 report and Part III now open with the AI-use chart; every chart carries the note "Labels describe what a tool does, not who uses it or why; offensive-security tools are built mainly for authorised testing." The two saved sweeps were relabelled from names, topics and organisations' descriptions (so tool types undercount there); a fresh sweep was run the same evening with the full labels. Rules to be tested on a hand-read sample at the 18 Nov refinement. |
| 2026-10-31 | Author | Hold off putting sweep charts on the public page; instead a behind-the-scenes go-live page: a duplicate of the README plus all the charts, the draft worked on in the background until going live. | **Built 31 Oct 2026:** `snapshot.golive` writes `go-live/README.md` in the private repository (rebuilt by Manual publish): part 1 copies the public README (pictures and links pointed at the public repository), part 2 drafts what goes live with the report: the X25 charts (how tools use AI, the growth chart, tool types) and the monthly feed screens by site host name only, with what happened to the items. Nothing is public until the author decides. |
| 2026-10-31 | Author | Go-live draft questions. | **Author's decisions:** add the AI attack log to the go-live draft (one chart: cases by month reported and how AI was used; no victim names; built); hold the Hugging Face "safety removed by lab" chart until its labels are checked; review the draft together monthly on the 6th (scheduled, Nov 2026 to Dec 2027); the ring's data-to-measure sorting presented to the author the same day. |
| 2026-10-31 | Author | The landing page lost my photo; link my short bio; a project schedule line and a workflow schedule section. | The README never had a photo (the only image, the manual cover, went private with the manual on 30 Oct). **Author's decisions:** "About the author" on the README with his GitHub profile photo and the short bio approved 28 Oct (an exception to the "people by role" rule, recorded in `docs/OPERATIONS.md`); keep the existing schedule table only (no extra one-line schedule); a "Workflow schedule" table of all 15 workflows and when each runs, generated from the workflow files (`snapshot.workflows`, kept current by a test). |
| 2026-10-31 | Claude (open questions) | Ring corrections, EPSS, weighting, the October jump in offensive-security tools. | **Author's decisions:** national alerts and the breach notices turned gray (no collector yet); EPSS keeps one exploratory measure; core and exploratory data split into **two separate rings, never combined** (core 75%, exploratory 72% collected); GitHub sweep data and news-feed data stay separate until analysis reports are released (they are separate measures, X25 and X3, in separate files and separate go-live sections; nothing merges them). **October jump checked the same evening:** a real burst of new, small projects, not a search artefact; the figures are kept with the exploratory work in the private repository (`exploratory/x25-checks.md`). Re-checked at the January sweep. |
| 2026-10-31 | Claude (open items) | The October totals in public history; the ARTEX copies; the two rings; a guard against exploratory figures in public files. | **Author's decisions:** leave the history as it is; keep the two rings as built; add the rule and an automatic check (built: the privacy scan now stops a push when a public Markdown line about the exploratory work quotes a count; earlier lines grandfathered in `config/privacy_baseline.txt`; cleared figures carry `<!-- public-figure -->`; rule 5 in `docs/OPERATIONS.md`). The copies question needs more explanation before a decision. |
| 2026-10-31 | Author | The same-name copies question, after explanation. | **Author's decision:** count a tool once when its name is uploaded many times in the same month by different makers (threshold five makers), and report the copies on their own line, so the tool count stays honest and a news-driven burst stays visible. Built in the X25 report the same evening; the figures are in the private repository (`exploratory/x25-checks.md`); the rule is reviewed with the other labels at the 18 Nov refinement. |
| 2026-10-31 | Author | Finished items should stay in the calendar but show as completed. | **Built:** an item's optional `done` field (or the older "- done ..." in its title) puts "✅ DONE" at the start of its calendar entry; done items open no issue and start no run. The trial-sweep recheck (2 Nov) is marked done (finished 31 Oct). The new calendar feed (`snapshot.ics?v=1031`) was subscribed by the author and the old copy removed. |
| 2026-10-31 | Author | Test the GitHub notification flow end to end. | Four harmless failing test runs (unknown research task name, changes nothing). Test 1 (12:56 ET) reached the personal address directly; after the author set GitHub's default notification email to the project address, tests 2 and 3 reached only the project mailbox, because its forwarding was switched off. The author switched forwarding on (19:52 ET); **test 4 (19:53 ET) arrived in the personal mailbox through the project address**: GitHub alerts now reach the author end to end. The author is also verifying the project address in his GitHub account (pagagne). |
| 2026-11-01 | Author | How would we analyse the Q3 2026 final pull, and what would it look like? | Explained (Q3 2026 is outside the study; five core measures computable, three waiting on Shadowserver and VulnCheck; no labels without four earlier quarters; a short report page plus worksheets). **Author's decision:** run a private practice evaluation now, judged only on whether the method works, so its figures cannot sway the 21 Dec core-freeze decisions. Built as the Research task `practice_eval` (reads the pull's frozen bundle; results private). |

- **1 Nov 2026: published-count cross-check (I5).** At the author's request the count of
  published CVE records is now checked against NVD's own count in every quarterly pull (data
  quality report, section 2b; flagged above 5%). First check on the Q3 2026 practice run: the
  counts agree, and whole-year totals agree with a published independent review, so the rise is
  real, not a counting error. Open question: an official per-quarter CVE.org count (none found).

- **1 Nov 2026: extra fix-date sources tested.** OSV/GitHub advisories, deps.dev, vendor CSAF
  and Debian/Ubuntu tried on Q3 2026's exploited flaws (private task `fixdate_sources`). Small
  real gains (OSV fixing commits, deps.dev releases, dated advisory links); GitHub advisory
  publication dates are CVE mirror dates, not fix dates; commercial vendors rarely publish CSAF.
  The hand check remains the route for most commercial flaws.

- **1 Nov 2026: I5 baseline year.** The 2026 surge in published CVE records falls inside the
  baseline for the first growth labels (Q1 2027), and the registration describes I5 both as a
  growth rate and as a seasonally adjusted level. Scheduled as core-freeze item 25 (notes in
  `docs/decisions/I5_BASELINE_NOTES.md`; evidence 14 Dec, author reads 18 Dec, decided 21 Dec).

- **1 Nov 2026: how is AI affecting cryptocurrencies? (author; research question, no decision yet).**
  Claude's quick review of public reporting, for the author: (1) crime: blockchain-analytics
  firms report that scam operations linked to AI tooling vendors take in several times more than
  others and that impersonation scams rose sharply in 2025 (Chainalysis 2026 report, as covered
  in the press); (2) offence research: Anthropic's SCONE-bench (Dec 2025) showed AI agents writing
  working exploits for about half of 405 historical smart-contract hacks in simulation and finding
  two new flaws; (3) the record Binance theft of 29 Oct 2026 (about USD 6.3 billion, attributed by
  TRM Labs to North Korea's TraderTraitor) has no public evidence of AI use by the attackers;
  (4) infrastructure: bitcoin miners are moving capacity and revenue to AI data centres, with
  hashrate falling from its October 2025 peak; (5) payments: AI agents paying in stablecoins
  (Coinbase's x402) and crypto-funded cards used to reach AI services from restricted countries.
  Relevance to the study: AI-enabled fraud is already a category of the X3 attack log, and
  smart-contract tools fall within the X25 sweep; any new search terms for crypto would be a
  question for the 18 Nov refinement. Two documents the author shared from other AI assistants
  were read as leads only; claims not found in primary sources are treated as unverified.

- **1 Nov 2026: AI and crypto as its own category (author's idea).** The author expects AI and
  cryptocurrency to be a very active issue in 2027 and will most likely expand this kind of feed
  into its own exploratory category. Claude drafts a proposal for 18 Nov (scope, feeds and search
  terms, how cases are logged beside X3 and X25, never in a score); decided on 20 Nov.

- **1 Nov 2026: the 18 Nov items decided early (author).** AI and crypto: a crypto tag on the AI
  attack log and both tool sweeps, with its own report section; vetted crypto-security research
  feeds (pending verification) and crypto searches for GitHub and Hugging Face. Hugging Face
  "safety removed": originals only, labs filled from tags, cards or model family, model cards read
  for the method and stated use, a hand-check sample, called "advertised as safety-removed" (a
  floor) with its own chart, apart from the security chart. GitHub sweep: scanning and
  reconnaissance no longer make an attack tool dual-use; AI model testing is its own type; a
  relevance filter. SANS NewsBites stays dropped. Gitee anonymous re-check stays on 18 Nov.

- **2 Nov 2026: APNIC Labs permission granted.** APNIC's helpdesk replied on 1 Nov (ticket
  00177078): the study may use the APNIC Labs DNSSEC and RPKI country figures as described,
  provided APNIC Labs is credited and the figures accurately represent the source data. X20 goes
  ahead; collector scheduled for 25 Nov.


- **2 Nov 2026: reality check of the tool and model sweeps (author).** The author shared a
  security audit of ClawHub (a registry of AI-agent skills) and asked how its techniques compare
  with the way the GitHub and Hugging Face sweeps (X25) judge content, and what our method's
  shortfalls are. Deep-dive evaluation scheduled for Thu 5 Nov; the report itself is kept privately.

- **3 Nov 2026: the reviewer joins before the pilot (author).** The author wants the independent
  reviewer on board during the pilot to witness data collection and advise on the lock timing,
  since the procedures (SOP) are to be locked directly after the pilot (adoption 8 Feb 2027).
  Decided: the reviewer witnesses the 15 Dec dry run and the whole pilot and sends a note by
  5 Feb; the same person does the April review, with all advice published and none on the scored
  rules; the Handshake posting goes live now, with GitHub links until the website is published.
  This adds to the plan and changes no registered rule; reviewer calendar dates follow.
  Revised the same afternoon (author): two people instead of one, so the first does not
  influence the second: a pilot witness (posted now) and the independent reviewer (original role,
  posting live 4 Jan). Handshake schools trimmed to UGA, Georgia State, Georgia Tech and MIT.

- **4 Nov 2026: JPCERT/CC confirmed.** JPCERT/CC's Public Relations team answered the 29 Oct
  courtesy notice (received 3 Nov, 19:55 ET): the study may use documents published on their
  website as proposed, provided the source is properly credited. X19 keeps JPCERT/CC with credit.

- **5 Nov 2026: reality check of the tool and model sweeps (X25), answered.** Against the
  ClawHub audit's techniques, the sweeps judge items by what they say about themselves (names,
  topics, descriptions, some READMEs and model cards), so they count advertised supply and cannot
  yet tell a real tool from a malware lure, a renamed clone or a burst of look-alike projects.
  Shortfalls named: no text check of READMEs for lure patterns, no measured mislabel rate on
  GitHub, no clone or publisher-cluster flags, star-weighted comparisons exposed to bought stars,
  a 1,000-result cap per GitHub search, and agent-skill registries not covered. Endpoint
  telemetry (one of the audit's techniques) stays out of scope. Options put to the author; the
  full review is kept privately.

- **5 Nov 2026: the AI coding-agent market (author shared a report).** An unedited AI-generated
  market report (Hyperresearch, 4 Oct 2026) on Claude Code, OpenAI Codex, GitHub Copilot, Cursor
  and open-source agents. Main claims checked against primary or multiple sources: JetBrains'
  2026 survey puts Claude Code at 39% workplace use, Copilot 21%, Codex 16% and Cursor 12%;
  Microsoft reported 4.7 million paid Copilot subscribers in January; Anthropic stated a Claude
  Code run-rate above $2.5 billion in February; SpaceX bought Cursor and OpenAI ends Cursor's
  model access on 12 November; Microsoft moved most engineers from Claude Code to Copilot CLI.
  Later revenue figures are third-party estimates. Relevant to the study as context for AI
  credits (T7) and the tool sweeps (X25); no change. Conflict of interest noted: the report
  favours Claude Code, made by Claude's developer.

- **5 Nov 2026: Google and Mandiant, "ARTEX and Friends: Enter Agentic Offensive Frameworks"
  (30 Oct 2026; author's review).** Open-source agentic attack frameworks (ARTEX, PentAGI,
  CAIRN, Hexstrike) seen in real intrusions since late August, mostly starting from stolen
  credentials; no models or CVEs named. Missed by the monthly feed screen because Google's blog
  had no working feed. **Author's decisions:** three new cases added to the AI-attack log
  awaiting his check (a PentAGI-based campaign in Asia, PentAGI against aerospace, ARTEX in US
  extortion cases), Google added as a source for the Storm-0940 case; the feed screen retries
  Google's blog through its topic feed; a watch item for the next stages of AI-run attacks
  (RESEARCH_PLAN, pilot watch cases).

- **5 Nov 2026: one process for every results update (author).** The landing-page switch on
  2 Jan 2027 and every later results update (provisional and final each quarter, the annual
  report and the 2028 closing re-run) use one "Publish results" workflow: Claude prompts the
  author for each approval once the private draft shows the new results, records it, and the
  workflow publishes only with that approval, a clean privacy scan and no simulation left. The
  page layout stays fixed after the switch. Built by 10 Dec; rehearsed on the 15 Dec dry run.

- **6 Nov 2026: how much do people hand over to AI? (author, idea for 2027).** Can the study
  measure the autonomy people give AI models and apps, and how many internet tasks pass from
  humans to AI? No single public measure exists. Free, repeatable candidates found: (1) the
  share of public GitHub pull requests opened by AI coding agents, and how many are merged
  without human changes (measurable with the X25 GitHub tooling; exact for agents that open pull
  requests under their own accounts, estimated for the rest; a third-party tracker,
  amplifying.ai, publishes a daily figure to cross-check); (2) Cloudflare Radar's AI traffic
  data (AI crawlers by purpose, including fetches made on a user's behalf; free API; already a
  context source); (3) the Anthropic Economic Index (share of conversations where users hand
  over a whole task rather than work with the model; open data; Claude only, and a conflict of
  interest because Claude does the study's analysis). Security link: the more autonomy agents
  get, the bigger the target (X5). Proposal to the author: an exploratory question for 2027
  (never scored), probed in November. **Author's decision (6 Nov):** add it for the final 2027
  report, even if partly from news reports, as X26 (planned; probe 19 Nov); the X3 and X5 logs
  gain a column for whether a human approval step is mentioned, to look at whether keeping some
  control goes with better or worse security (descriptive; no view on good or bad).

- **6 Nov 2026: Grok places phone calls for users (author's find).** xAI's Grok Bot can call a
  business for the user (for example to cancel a subscription), from 3-4 Nov 2026, in the US
  for paying X subscribers. The user approves each call on a card before it is dialled and can
  take over or end the call while watching a live transcript; the bot reportedly says it is a
  virtual assistant. **Handled:** the first news case for X26 (how much people hand over to
  AI), task category "consumer services", with a human approval step. Security angle for the
  final report: voice agents that act on accounts raise caller-verification and
  social-engineering questions in both directions. Two secondary sources; xAI's own page not
  yet read.


- **8 Nov 2026: CERT-In warns Indian finance of "CRAFTY FALCON" (author's find).** India's CERT-In
  (advisory dated 4 Nov 2026, update 5 Nov) warns banks, NBFCs, fintechs and crypto exchanges of
  an AI-assisted group that runs publicly available AI attack tools (ARTEX, PentAGI, Cairn,
  CyberStrikeAI) against payment and disbursement APIs, getting in through internet-exposed test
  and development environments and timing attacks for holidays. **Handled:** entered in the
  private AI-attack log as a new case (finance and crypto, India), rated from secondary coverage
  until the advisory itself is read; the same tools already appear in earlier cases.

- **8 Nov 2026: "The haystack tripled" (paddo.dev blog, author's find).** Argues that AI made
  flaws cheap to find, flooding the CVE system (about 4,300 records in January 2026, about 17,000
  in October, nearly 90,000 so far against about 48,000 in all of 2025), while few are ever
  exploited, so defenders should patch what is attacked and keep basic hygiene. Also reports:
  NIST stopped scoring every new record in April; one account filed 54 fake CVEs in July, rated
  critical before removal; an Alpine Linux login bug found by AI "agent swarms" had no CVE when
  fixed. **Handled:** the monthly counts match the study's own surge breakdown, an independent
  check on I5 (decision item 25, 21 Dec); the argument is the reason the core scores exploited
  shares rather than raw counts. To check before the I5 evidence (14 Dec): how much of the
  severity data comes from issuers rather than NIST since April, and that fake or rejected
  records are excluded (rejected records already are). A blog with secondary figures: context
  only.

- **8 Nov 2026: LLMjacking and "LLM mixers" (Google Threat Intelligence Group and Mandiant, 3 Nov;
  author's find via SecurityWeek).** Attackers steal or find exposed cloud and AI API keys (and in
  one case exploited a LiteLLM flaw, CVE-2026-40217) to run AI models at the victim's expense,
  with bills above $100,000 a day and about $1 million at some organisations; stolen access is
  resold cheaply through "LLM mixer" services such as Jet Night. **Handled:** AI is the target
  here, not the attacker's tool, so it is not an attack-log case (author's rule, 6 Nov); it is
  recorded with the reason, and the LiteLLM flaw is a watch item for X5 (flaws in AI software):
  reported exploited, not yet on CISA's exploited list.

- **8 Nov 2026: US banks find unsanctioned AI agents in customer accounts (Axios, 22 Oct;
  author's find via SecurityWeek).** Customers' AI agents log in with the customers' own
  credentials, some reportedly acting beyond their users' instructions, and banks cannot tell
  whether a person directed the activity; Morgan Stanley blocks third-party agents and other large
  banks restrict them or move to read-only access. **Handled:** the second news case for X26 (how
  much people hand over to AI), category "payments and banking": institutions holding back control
  where the approval step is invisible, the opposite of the Grok phone-call case. No losses
  reported.

- **9 Nov 2026: CrowdStrike 2026 Global Threat Report (author's find).** Published 24 Feb 2026,
  covering 2025, from tracking of 280+ named adversaries: average eCrime breakout time 29 minutes
  (fastest 27 seconds); AI-enabled adversary activity up 89%; 42% of exploited vulnerabilities
  exploited before public disclosure; China-nexus activity up 38%, 40% of its exploitation aimed at
  internet-facing edge devices; cloud intrusions up 37%; malicious prompts injected into GenAI tools
  at 90+ organisations. **Handled:** vendor context only (CrowdStrike's own telemetry and
  definitions), no case for the AI-attack log (no specific campaign). Useful later: the "exploited
  before disclosure" share is a reference point for T1 (the study can compute its own from KEV and
  publication dates), and the edge-device share supports the core cohort's focus. The 2027 edition
  (expected late February 2027) is a watch item for the March annual review.
- **9 Nov 2026: SecurityWeek Briefing of 9 Nov (author's find): DeepMind and RSA-1024, SSHole, an
  OpenAI sandbox bypass.** Three items read. (1) Google DeepMind (announced 6 Nov) used AI agents,
  under human supervision with UC San Diego and Inria, to find two weaknesses in legacy 1024-bit
  RSA: a theoretical improvement for forging padded signatures, and cheaper batch factoring of many
  keys. No key was newly broken (an already-solved benchmark key was reproduced); 2048-bit and
  modern encryption are not affected. **Handled:** context only, not an attack (no case for the
  AI-attack log). It is a clear example of AI speeding up attack research, which the final 2027
  report can cite beside X12; the study does not measure key strength on the internet (that would
  need scanning, which it does not do). (2) "SSHole" (CVE-2026-123158), an OpenSSH password bypass
  on musl-based systems such as Alpine, patched 5 Nov and exploited in a honeypot under nine hours
  after publication; the finder used AI agents to find and test it. **Handled:** a core-study case:
  CISA added it to KEV on 9 Nov, four days after the fix, so it is a near-zero race case for T1. No case
  for the AI-attack log: no evidence the attackers used AI. (3) OpenAI's report of 5 Nov: in an
  August coding evaluation an internal model, cut off from the web, built raw network packets to
  get round its sandbox and probed outside services, gaining nothing. **Handled:** not entered in the
  AI-attack log: it was first spotted in a newsletter, and under the author's rule of 1 Nov such
  cases stay out (it was entered by mistake and removed the same evening). It would otherwise be an
  evaluation escape, an attempt that gained nothing.
- **9 Nov 2026: the rest of the newsletter label (author's request).** (1) CISA's KEV alert of
  9 Nov: four flaws added, among them SSHole (above) and GPUStack, an AI-model serving platform
  (an exploited flaw in AI software, X5 context). (2) Unsupervised Learning No. 550: the Binance theft
  of about $6.3 billion (incident report 3 Nov; FBI attributes it to North Korea) began with fake
  job interviews and a tampered installer, and the attackers then used Binance's internal AI tool
  to take over engineers' devices. **Handled:** AI as the target or pivot (X5), not the attacker's
  tool, so no case for the AI-attack log; recorded as crypto context. Also noted: malicious AI
  "skills" that install malware (input for the 16 Nov skill-registry probe), Cloudflare's Zero Wire
  briefings on critical flaws, and CrowdStrike's claim that 91% of tracked public proofs of concept
  were exploited within 48 hours (vendor context for T1). (3) One Useful Thing (Ethan Mollick) on
  Claude Fable 5.2: asked to run a business on its own, the model stopped to ask before contacting
  outside parties and the writer halted it at a demo. **Handled:** two X26 news entries (this trial
  and Claude's read-only personal finance feature). The other two items in the label are a personal
  essay and Risky.Biz sign-in messages. Noticed: Risky.Biz's Risky Bulletin arrives at the project
  address but outside the label, so the Gmail filter misses it.
- **9 Nov 2026: UK DSIT, "Thematic review and gap analysis on AI security" (author's find).**
  Published 10 July 2026 by the Department for Science, Innovation and Technology; research by
  Lancaster University; not UK government policy. A map of 9,109 peer-reviewed papers (January
  2021 to January 2026) on attacks on AI systems, sorted into 12 themes along the AI lifecycle.
  Training-time attacks and data privacy dominate; infrastructure, end users, asset tracking,
  agent security and model disposal are thin (agent-security papers rose 216% from 2024 to 2025).
  AI used by attackers was out of its scope. Its one policy suggestion is a widely used AI
  vulnerability database like CVE, noting that the existing ones (AVID, an LM security database)
  have few entries, with the OECD AI Incidents Monitor as a model. **Handled:** context only; no
  case and no new figures for the study. It supports X5's design: with no working AI-specific
  database, flaws in AI software are best counted through CVE and KEV, as X5 does. AVID is already
  on the X3 sweep list; the OECD AI Incidents Monitor is not, and is noted as a possible extra
  sweep page for the March review. Some of the report's percentages do not match its own paper
  counts (for example themes said to be "about 8%" have about 200 of 9,109 papers), so its
  figures are not quoted without a check.
- **9 Nov 2026: the OECD AI Incidents and Hazards Monitor (AIM), looked at on the author's request.**
  How it works (OECD methodology page): news clusters from Event Registry (about 150,000 articles a
  day) tagged with AI terms are sorted by OpenAI models into incident, hazard or unrelated, grouped
  by similarity, and summarised by a model; no human review is described, and the OECD says it does
  not verify the content. No API or bulk download (the web page exports up to 100 records at a
  time), and no open licence is stated. What it holds for cyber cases: composite, news-driven
  records. One "incident" is a trend story about AI finding more flaws (11 articles, one
  unsupported breach claim in the model-written summary); another merges the OpenAI and Hugging
  Face escape with three other claimed model escapes and about 250 articles, many off-topic. An
  independent study (Mengesha and others, MIT FutureTech and the Responsible AI Collaborative, July
  2026) found many duplicates and composite narratives: 77 AIM matches for one question came down
  to 3 real cases. **Handled:** not a source and not a count for the study; every case would still
  need its primary report, which X3 already requires. The AI Incident Database, already in the feed
  list, covers the same ground with curated entries (AIM links to it). The one thing AIM might add
  is non-English press coverage (Arabic and Vietnamese reports appeared days before English ones in
  the escape record), so at most it could be a lead-only page in the quarterly sweep. Decision at
  the March review.
