# Evaluation flow and the T1 decision

Two diagrams. GitHub draws them from the Mermaid source below; PNG copies are in
`docs/diagrams/` for slides and the landing page. Yellow boxes are hand checks (Hand Check
app), blue boxes are the reported measures, dashed grey boxes are not yet measurable or
still to be decided.

## 1. How a flaw moves through the study each quarter

```mermaid
flowchart TD
  SRC["Free sources, pulled each quarter<br/>CVE.org · CISA KEV · NVD · EPSS<br/>SEC · Cloudflare Radar · ransomware.live"]
  SRC --> ALL["All CVEs published in the quarter"]
  SRC --> KEV["All CVEs first exploited in the quarter<br/>(added to CISA KEV)"]
  SRC --> HARM["Harm series<br/>leak-site posts · SEC 8-K Item 1.05"]

  ALL --> ELIG{"Eligible?<br/>CVSS ≥ 8 or critical<br/>published day 1–25"}
  ELIG -- no --> OUT["Not in the cohort"]
  ELIG -- yes --> SLOT["Sorted into slots<br/>a firewall/VPN · b web/collab · c other · d AI-credited"]
  SLOT --> DRAW["Seeded random draw<br/>1 pick per slot per month = up to 12 a quarter"]
  DRAW --> HC1{"Hand check<br/>slot c: reachable from the internet?<br/>slot d: did AI take part?"}
  HC1 -- no --> NEXT["Next CVE in draw order"] --> HC1
  HC1 -- yes --> FIX["Hand check: fix date<br/>confirm · correct · No fix yet · Still open"]

  ALL --> CRED["AI-credit texts"] --> AUTO{"Clear pattern?"}
  AUTO -- yes --> ACC["Auto-accepted<br/>10% spot-checked by hand"]
  AUTO -- no --> HC2["Hand check: Yes / No / Unsure"]
  ACC --> T7["T7 AI involvement<br/>floor · hand · ceiling range"]
  HC2 --> T7

  FIX --> EV["Event dates per CVE<br/>T0 published · T_patch fix · T_exploit first attack"]
  KEV --> EV2["Event dates per exploited CVE<br/>fix date pre-filled, ~15 hand-checked"]
  EV --> T1B["T1(b) and T2 exposure race<br/>waits for Shadowserver data"]
  EV --> T1REG["T1(a) as registered<br/>cohort only: almost never measurable"]
  EV2 --> T1A["T1(a) option (a)<br/>share attacked before a fix · median days"]
  KEV --> T3["T3 time from disclosure to attack"]
  KEV --> T4["T4 age of exploited flaws"]
  HARM --> T6["T6 visible harm"]
  ALL --> T5["T5 discovery volume<br/>(count of all CVEs)"]

  classDef hand fill:#fff4d6,stroke:#b8860b,color:#222
  classDef open fill:#f3f3f3,stroke:#888,stroke-dasharray:5 4,color:#444
  classDef measure fill:#e3effc,stroke:#2a6bb5,color:#123
  class HC1,FIX,HC2,ACC hand
  class T1REG,T1A,T1B open
  class T3,T4,T5,T6,T7 measure
```

Notes
- The cohort (left) feeds T1(b) and T2 once exposure data arrives, plus the root-cause and
  AI-vs-human comparisons. Its fix dates are the hand-checked T_patch.
- The exploited set (right) needs no draw: every CVE first added to CISA KEV in the quarter.
  It feeds T3 and T4 today, and T1(a) if option (a) is adopted (decision item 0).
- AI-credit texts (middle) feed T7; clear patterns are auto-accepted with a 10% spot check
  (`config/ai_credit_auto_accept.yaml`).

## 2. Decision item 0: how to measure T1(a), the race (21 Dec)

```mermaid
flowchart TD
  Q["Decision item 0 (21 Dec)<br/>How should T1(a), the race, be measured?"]
  Q --> A1{"Do we need a race number<br/>every quarter?"}
  A1 -- "no, report it as mostly 'no estimate'" --> B["(b) Keep as registered<br/>cohort only · 0.3–0.4 exploited picks a quarter"]
  A1 -- yes --> A2{"Is it acceptable to measure only<br/>flaws that were actually attacked?"}
  A2 -- no --> C["(c) Much larger cohort<br/>~2,000 picks · not practical"]
  A2 -- yes --> A["(a) All flaws first exploited in the quarter<br/>60–90 flaws · zero-day share 21–25% · median 5–8 days<br/>+ ~15 fix dates hand-checked"]
  A --> A3{"Also follow attacked flaws end to end<br/>with exposure data (T1b)?"}
  A3 -- "no" --> AFIN["Adopt (a)<br/>cohort unchanged"]
  A3 -- "yes, worth breaking the<br/>'no EPSS in selection' rule" --> AD["Adopt (a+d)<br/>EPSS-weighted draw in slots a–c<br/>2–3 attacked flaws a quarter as described cases<br/>other cohort figures re-weighted"]
  AD --> W["Only pays off once<br/>Shadowserver data arrives"]
  AFIN --> LOG["Log as deviation · run alongside the<br/>registered version for four quarters"]
  AD --> LOG
  B --> LOG2["No change to the plan"]

  classDef dec fill:#fff4d6,stroke:#b8860b,color:#222
  classDef out fill:#e3effc,stroke:#2a6bb5,color:#123
  classDef weak fill:#f3f3f3,stroke:#888,stroke-dasharray:5 4,color:#444
  class A1,A2,A3 dec
  class AFIN,AD,A out
  class B,C weak
```

Figures from `proposals/T1_OPTIONS.md` (Q2 and Q3 2026 back-test).
