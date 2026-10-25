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
  (Shadowserver or Censys); not measured under Plan 2.
- T5 +2 CVEs; T4 not an old flaw; T6 outages were defensive, not ransomware or 8-K.

**Sources:** [The Next Web](https://thenextweb.com/news/php2shell-php-rce-ai-openai-wiz),
[Implicator](https://www.implicator.ai/amazon-logged-a-php2shell-exploit-attempt-four-days-before-disclosure/),
[Wiz CVE-2026-109618](https://www.wiz.io/vulnerability-database/cve/cve-2026-109618),
[SecurityWeek headline](https://www.securityweek.com/php2shell-patches-land-as-first-exploitation-attempts-hit-sensors/amp/) (page not readable 25 Oct).
