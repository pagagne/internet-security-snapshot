# Exploratory layer: AI-operated attacks

The core study sees attacks only through published flaws (CVEs), the CISA exploited list,
ransomware leak sites and SEC filings. Attacks run by AI agents against websites often use
bugs that never get a CVE, so the core cannot see them. This folder tracks them as
exploratory measures (X3, X4 in `config/exploratory.yaml`); they never decide a label.

## `ai_attack_campaigns.csv` (X3)

One row per publicly reported campaign. Victim names are never recorded.

| Column | Meaning |
|---|---|
| ai_role | `agents_operated_intrusion` (AI agents carry out the intrusion), `ai_assisted_operator` (a human attacker uses AI for parts of the work), `ai_generated_malware`, `ai_enabled_fraud` |
| entry_vector | `known_cve`, `zero_day` (unknown flaw, no CVE yet), `web_app_unknown` (bugs in site code, no CVE), `credentials`, `misconfiguration`, `supply_chain`, `phishing`, `unknown` |
| cve_ids | Any CVEs named in the report, separated by semicolons |
| confirmed_by_second_source | `yes` if an independent source reports the same campaign |
| conflict_of_interest | `yes` when the report comes from Anthropic, whose model writes this study's code |

Rows are added when found, and swept quarterly before each provisional run. Counts are a
lower bound: they reflect what gets reported, not everything that happens.
