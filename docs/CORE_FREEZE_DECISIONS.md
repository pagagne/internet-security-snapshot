# Core freeze: decisions before scoring starts

The core (rules that decide the Improving/Worsening labels) must be final before the
Q4 2026 pilot is scored on 1-2 January 2027. After the freeze it changes only at a March
review (docs/CHANGE_POLICY.md). The exploratory layer stays open at all times.

- **Decision session:** 21 December 2026
- **Freeze:** by 31 December 2026 — tag `core-v1.2`, update `prereg/LOCKED.yaml`,
  log in `prereg/DEVIATIONS.md`, file an update on OSF.

Each item: decide **promote to core**, **keep exploratory**, or **drop**. Evidence comes
from the December dry run and the test runs.

| # | Item | Now | Question for the session | Evidence to bring |
|---|---|---|---|---|
| 1 | Root-cause map coverage | Core | Extend the CWE map and let NVD fill missing CWEs? (39% "other/unknown" in Q3 2026) | Top unmapped CWEs; effect of NVD fill |
| 2 | T6(b) SEC Item 1.05 | Core | Keep as is, or add voluntary Item 8.01 cyber disclosures alongside? (4 filings in Q3, all amendments) | Next run's SEC diagnostics |
| 3 | X6 Speed in the tail | Exploratory | Promote? It is tool-agnostic and catches faster attackers, incl. self-hosted models | Q3 2026 and baseline-year values |
| 4 | X7 Patch to public exploit code | Exploratory | Keep exploratory until a year of data shows it is stable? | Coverage of PoC-in-GitHub for cohort CVEs |
| 5 | X8 Breadth of exploitation | Exploratory | Promote or keep? | Quarter-to-quarter noise in baseline year |
| 6 | X9 Bug types exploited | Exploratory | Depends on item 1 | — |
| 7 | X10 Zero-day share | Exploratory | Feasible with free fix dates? | Share of unknown fix dates |
| 8 | X3 AI-run campaign log, X5 AI software, X11, X12 | Exploratory | Stay exploratory (curated or context) | — |
| 9 | AI credit term list | Core (v1.2) | Promote any watchlist candidates seen in credits by December? | Watchlist scan from the dry run |
| 10 | Slot (a) keyword "gateway" | Core | Too broad: the Q3 preview put Jupyter Enterprise Gateway (a data-science server) in the edge-device slot. Match "gateway" only with VPN/remote-access/SSL/security words? | Edge-slot picks from the baseline preview |
| 11 | Internet-facing rule for slot (d) | Core | Does the internet-facing requirement apply to AI-credited picks too? The preview offered Firefox and FreeBSD. | Slot d candidates in the baseline |
| 12 | Anything else | — | Brainstorm: what would we regret not measuring by 2028? | Notes |

Rules of thumb for promotion: computed from free data already collected; defined
before seeing its trend; stable enough that two quarters running in one direction
means something; does not depend on hand judgment beyond the existing checks.
