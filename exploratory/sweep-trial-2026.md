# Trial AI-attack sweep, July-October 2026 (run 26 Oct 2026)

Run early at the author's request (planned for 5 Nov) to test the X3 sweep before its searches
are fixed for 2027 (`config/exploratory.yaml`, X3 `sweep`). Every candidate is in
`exploratory/ai_attack_sweeps.csv` (`sweep_quarter` = `trial-2026`); kept ones were added to
`exploratory/ai_attack_campaigns.csv`, each marked "awaiting author check".

## Result
- **33 candidates screened:** 10 kept (9 in the window plus 1 earlier backfill), 9 duplicates
  of entries already logged, 6 excluded, 8 to recheck (page unreadable from here, or the
  primary report not yet read).
- **The log grows from 13 to 23 entries.** The usual channels (AI-lab reports, big vendors)
  had produced 13 entries; the sweep found 9 more in July-October alone.
- **The languages paid off:** 6 of the 10 kept were found first or only outside English:
  JADEPUFFER (Portuguese), Brazil's social-security logins (Portuguese), ARTEX in Japan
  (Japanese only) and its Korean campaign (via the Japanese article), the Trend Micro case
  (German), and the FortiGate backfill (French).
- **Open-weight and open-source tools are already in use:** DeepSeek behind ARTEX (Korea),
  the open-source agent systems Hermes and OpenClaw (Taiwan), OpenClaw artifacts (GTIG),
  Cairn (already logged). Evidence for X12.

## Kept (awaiting the author's check)
| Reported | Case | Reported by | Entry | Language found |
|---|---|---|---|---|
| 2026-10-19 | ARTEX against ~20 Japanese companies (8 leaks) | GMO Cybersecurity | unknown | ja |
| 2026-10-07 | ARTEX (DeepSeek) against South Korean finance | CrowdStrike | unknown | ja |
| 2026-09-16 | Hijacked AI coding assistant spreads Shai-Hulud | Mandiant | supply chain | en |
| 2026-09-09 | Manus agent steals 375 Brazilian social-security logins | Cybernews (single source) | unknown | pt |
| 2026-09-08 | Agentic credential harvesting in under 6 hours | Google GTIG | credentials | en |
| 2026-08-13 | Taiwan government intrusion with Hermes/OpenClaw | Taiwan MODA; Dream; FT | unknown | en |
| 2026-07-29 | China-linked AI agent, recon and lateral movement | Trend Micro | unknown | de |
| 2026-07-21 | OpenAI evaluation models breach Hugging Face (evaluation escape, not a campaign) | OpenAI; Hugging Face | zero-day | en |
| 2026-07-04 | JADEPUFFER: AI agent runs a ransomware attack | Sysdig | CVE-2025-3248 | pt |
| 2026-02-24 | AI-assisted takeover of ~600 FortiGate firewalls (backfill) | Amazon | credentials | fr |

Questions for the author's check: does the Shai-Hulud case (the attacker used the victim's own
assistant) belong in X3 or in X5 (AI as the target)? Keep the single-source Brazil case?

## What the trial says about the search list (decision 9, 12 Nov)
- **Productive searches:** "AI agent cyberattack intrusion", "autonomous AI hacking
  campaign", "attackers used AI agent to exploit vulnerability", "AI coding assistant supply
  chain attack", and the sandbox-escape search (found the largest incident).
- **Mostly duplicates or other measures:** "LLM generated exploit used in the wild"
  (duplicates), "prompt injection ... data stolen" and "MCP server ... compromised" (AI as the
  target, which is X5's subject, not X3's).
- **Proposed changes:**
  1. Add "AI penetration testing tool used by attackers" and a fixed watch list of named
     offensive agent frameworks (ARTEX, Cairn, Hexstrike, Strix, OpenClaw, Hermes, Manus),
     searched by name each quarter, dated additions allowed.
  2. Move the prompt-injection and MCP searches to X5.
  3. Add fixed pages: GMO Cybersecurity, CrowdStrike, Sysdig, Cybernews research, Trend
     Micro research.
  4. Chinese and Russian searches returned almost nothing usable (the search tool favours
     US results, and several pages could not be read from here): replace them with fixed
     native-language pages (FreeBuf, Anquanke and Qi An Xin for Chinese; Kaspersky's Russian
     Securelist and Habr for Russian), and read pages the tool blocks in a browser.
  5. Keep Japanese, Korean, Spanish, Portuguese, German and French as searches.
- **Time:** about 1½ hours for this trial (all 10 English searches, one or two per other
  language, a few fixed pages). The full grid (10 searches in 9 languages plus about 20 pages)
  is estimated at 3-4 hours a quarter for Claude; the author's check about 20-30 minutes.

## To recheck before the 12 Nov review
Sysdig's JADEPUFFER report, GTIG's September report, CrowdStrike's ARTEX post and GMO's own
announcement (each kept entry currently cites a secondary page for at least part of its
detail); the Unit 42 "10-hour" ransomware case; Sysdig's Marimo case (date); the Aviatrix MCP
scanning note; OpenAI's latest misuse report; the unreadable Chinese, Korean and Russian
pages.
