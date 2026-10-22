# Sources for attacker-side AI (researched 2026-10-21)

Free sources that can show attacks run or assisted by AI. None measures AI attacks
directly at internet scale; together they give a lower bound and a direction.

| Source | What it shows | Cadence | Free data? | Use in the study |
|---|---|---|---|---|
| GreyNoise research blog | Campaigns seen on its sensor network, incl. the Sept 2026 PaperCut campaign run by AI agents, fake "AI crawler" credential scanning, and mass probing of LLM endpoints | Irregular, frequent | Blog posts free; some indicator lists on GitHub; full tags and feeds are paid | X3 log entries; strongest outside view of agent traffic |
| Google GTIG AI Threat Tracker | State and criminal misuse of Gemini, AI-built exploits, agentic recon tools | Roughly quarterly (Feb, May 2026) | Free reports, no counts | X3 log entries |
| Anthropic threat intelligence reports | Misuse of Claude, incl. highly autonomous intrusions | Irregular (Mar, Aug, Nov 2025; Sept 2026) | Free reports | X3 log entries, flagged as conflict of interest |
| OpenAI "Disrupting malicious uses of AI" | Misuse of ChatGPT and Codex, incl. cyber operations | About every four months (Feb, Jun, Oct) | Free reports | X3 log entries |
| Palisade Research LLM Agent Honeypot | Decoy servers that flag AI agents by prompt-injection traps and response timing; 1 confirmed agent in its first 7.6M interactions (Feb 2025) | Live dashboard (status to recheck) | Dashboard counts; no raw download | X3 context: the only direct measurement of AI agents in the wild |
| Imperva/Thales Bad Bot Report | Bot share of web traffic (53% in 2025, up from 51%) | Annual (April) | Free with registration | Annual-check reference for X4 |
| DataDome State of Bot & Agent Security | Agent and bot traffic against websites | Annual | Free with registration | Annual-check reference for X4 |
| Cloudflare Radar | Bot vs human traffic, AI bot activity, layer-7 attacks | Weekly API | Free API (token in place) | X4 series |
| OECD AI Incidents Monitor; AI Incident Database | News-based AI incident collections | Daily (automated) | Web search; no documented API | Cross-check that the X3 log isn't missing reported campaigns |
| MITRE ATLAS case studies | Documented attacks on and with AI | Occasional | Free | Cross-check and classification |

## What this adds to the core

- **Linking X3 to KEV:** when a logged campaign names CVEs, the study records which KEV
  entries were exploited by AI-run campaigns (e.g. CVE-2026-81578 and CVE-2026-82078,
  PaperCut, Sept 2026). Each quarter reports how many of that quarter's KEV additions
  are linked to an AI-run campaign. The core sees those flaws but can't otherwise tell
  that AI ran the attack.
- **Entry vectors:** of the 11 campaigns logged so far, only one used a known CVE. The
  rest used stolen credentials, phishing, misconfigurations, zero-days or bugs in
  website code, none of which the core can see.

## Gaps

- No free source counts AI-operated attacks across the internet. The honeypot work is
  the closest, at small scale.
- Most reports come from AI labs about their own models, so attacks using self-hosted
  open models are under-reported.
- Reports describe what was caught and published, not everything that happened.

## Worth asking about later (not free today)

- GreyNoise research or academic access to tags for agent-like scanning.
- Shadowserver honeypot data, if the pending permission comes through.
