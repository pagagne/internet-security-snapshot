# Case note: PHP2Shell (CVE-2026-109618, CVE-2026-109619)

Pilot watch case (`docs/RESEARCH_PLAN.md`, "Pilot watch cases"). The full note is due
3 Feb 2027 and reviewed with the author on 8 Feb 2027 (AI-credit rule evaluation session).
Until then this file collects the points to review. Nothing here changes a rule.

## Points to review (collected 25 Oct 2026)

**Facts reported so far**
- PHP memory-safety flaws, unauthenticated code execution, CVSS v4 9.2 each; reach PHP 5.4
  and later; highest risk on Apache with mod_php. Fixed 21 Oct 2026 in 8.5.12, 8.4.27,
  8.3.36, 8.2.35, with backports for 7.4, 8.0 and 8.1 (The Next Web).
- Release brought forward after details leaked (a Hacker News post, reportedly first
  reported by the Wall Street Journal); Cloudflare enabled WAF rules for all customers
  about nine hours before disclosure; CERT-EU and the UK NCSC advised taking unpatched systems
  offline; the NSA issued an alert; several sites took services down.
- Amazon's MadPot honeypots logged an exploit attempt on 17 Oct, four days before
  disclosure (Implicator, citing the AWS Security Blog). A proof of concept circulated;
  attackers adapted payloads against Cloudflare's rules. No confirmed mass exploitation
  reported as of 25 Oct; KEV status to be read from the pipeline's next pull.

**T7 (AI credits): the main lesson**
- PHP's advisory credits Calif, Wiz and OpenAI. Headline count: yes (OpenAI is an AI
  lab). Narrow count (AI tool named): no.
- The tools actually used appear only in press coverage: Calif found the first bug in
  August with OpenAI's GPT-5.6 Sol in an OpenAI-funded audit ("Patch the Planet"); Wiz found
  the flaws independently with Wiz Atlas, Google's Gemini 4 Argon and GPT-5.6 Sol. Google's
  part appears in neither count.
- For 8 Feb: evidence that credit fields understate AI involvement and that lab mentions
  catch more than tool names; consider an exploratory "AI involvement reported in vendor
  or finder write-ups" check on a sample (never scored from press text).

**T1(a) race and X10 zero-day share**
- Enters the race only if CISA lists it in Q4 2026 (or its exploitation flag turns
  "active"). Fix date is clean: 21 Oct, the vendor advisory.
- The honeypot attempt on 17 Oct predates the fix, but free data would date the first
  attack at the KEV listing, after the fix: counted as not a zero-day. Shows why X10 is a
  minimum, and what Shadowserver honeypot data (Plan 1) would add. An attempt is not a
  confirmed exploitation.

**Other measures**
- Cohort: eligible for October, slot c, only if the seeded draw picks it.
- X7: if the proof of concept reaches Exploit-DB, Metasploit or Nuclei, an earlier
  "attack possible" date.
- T1b/T2 exposure: the defender side (PHP on about 70% of websites) needs scan data
  (Shadowserver or Censys); not measured under Plan 2. Without scans, HTTP Archive's monthly
  crawl may show the share of sites reporting a fixed PHP version (test 2 Nov; author's
  concern of 26 Oct that many servers will stay unpatched, above all those on end-of-life
  PHP 5.4-7.3, which get no fix).
- T5 +2 CVEs; T4 not an old flaw; T6 outages were defensive, not ransomware or 8-K.

**Sources:** [The Next Web](https://thenextweb.com/news/php2shell-php-rce-ai-openai-wiz),
[Implicator](https://www.implicator.ai/amazon-logged-a-php2shell-exploit-attempt-four-days-before-disclosure/),
[Wiz CVE-2026-109618](https://www.wiz.io/vulnerability-database/cve/cve-2026-109618),
[SecurityWeek headline](https://www.securityweek.com/php2shell-patches-land-as-first-exploitation-attempts-hit-sensors/amp/) (page not readable 25 Oct).

## Patch information flow (added 26 Oct 2026, from TechCrunch 24 Oct, at the author's request)

How knowledge of the flaws and of the fix spread, as reported (sources disagree where noted):

| When | What | Who knew |
|---|---|---|
| 2024 (TechCrunch only) | Bugs first found, judged not exploitable, left unpatched. Conflicts with the other accounts (Calif found the first bug in Aug 2026 in an audit); unreconciled | Finders |
| Aug 2026 | Calif finds the first bug in the OpenAI-funded audit; Wiz finds them independently | Finders, OpenAI, Wiz |
| Date not reported | Calif alerts the PHP Foundation; coordinated disclosure under embargo; **patches given early to some large internet companies and web hosts** | Vendor + selected large operators |
| From 17 Oct | Amazon's honeypots log exploitation attempts; Amazon tells defenders to check from 17 Oct. How the attacker learned of the bugs is unknown | Attackers (at least one) |
| Days before 21 Oct | Details leak (Hacker News, reportedly the WSJ); **an unnamed company releases patches hours before the embargo ends** (PHP Foundation's complaint); release brought forward; Cloudflare WAF rules about 9 hours before | Anyone watching the leak or the early patch |
| 21 Oct | PHP Foundation publishes patches; CISA alert the same day; CERT-EU and NCSC advise taking unpatched systems offline; outages (e.g. Belgium's Smartschool) | Everyone |
| Late 23 Oct | Trail of Bits reports working exploits (two days after the public patch) | Researchers; exploit code not public |
| 24 Oct | Cloudflare sees an exponential rise in attempts after disclosure; no mass exploitation yet | |

**What it means for the study (points for 8 Feb; no rule change)**
- **"Fix date" has three candidates here:** the embargoed early patch to selected operators
  (date unknown), the leaked early release (hours before), and the public release (21 Oct).
  The study's fix date is the public vendor release, which is right for the internet at
  large, but the big operators were fixed earlier. Worth a hand-check note field "patched
  early for selected parties (embargo)" and, where a date is known, recording it beside the
  public date, so the race is not read as the same for everyone. The interval dates
  (`fix_lo`/`fix_hi`) could carry it: added to decision item 20 for the 21 Dec session
  (author, 26 Oct).
- **Attack before the public fix:** attempts from 17 Oct, four days before 21 Oct, possibly
  from the embargo leaking. A negative race value against the public fix; against an early
  private patch it may not be. Free data still dates the first attack at the KEV listing.
- **Patch to working exploit in two days** (Trail of Bits, by studying the fix): the
  "patch to public exploit code" fingerprint (X6-X11) would show it only if code is
  published to Exploit-DB, Metasploit or Nuclei.
- **Embargo leaks as an attack path:** the early, uneven spread of patch information is
  itself a risk the race measure cannot see; note it in the case note as context.
- **Discovery date disputed** (2024 or Aug 2026): no measure uses discovery dates, so no
  effect; record both.

**Source:** [TechCrunch, 24 Oct 2026](https://techcrunch.com/2026/10/24/php-ocalypse-how-two-critical-web-bugs-almost-broke-the-internet/)
