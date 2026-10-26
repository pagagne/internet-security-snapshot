# Capacity: storage, memory and run time for a full run

Asked by the author on 26 Oct 2026: what a complete run needs if every source is approved and
running. **Measured** figures come from the resource profile run on the GitHub runner
(26 Oct, `research/2026-10-26T2339Z-resource_profile` on the run-reports branch) and the
Q3 2026 test pull of 22 Oct. **Estimated** figures are for sources not yet collected, from their
published formats; each is marked and will be replaced by a measurement at the 15 Dec full dry
run.

## The machine
GitHub's standard runner for this public repository: 4 CPUs, 16 GB memory, 92 GB free disk
(measured). A job may run up to 6 hours. Public repositories pay nothing for these minutes.

## Per quarterly pull (92 days of data)

| Part | Storage | Run time | Peak memory | Basis |
|---|---|---|---|---|
| CVE records | 37.3 MB | 2.3 min | 1.47 GB | measured |
| EPSS daily scores | 74.3 MB | 1.3 min | 1.11 GB | measured |
| CISA KEV, NVD, SEC, Cloudflare Radar | 3.0 MB | 2.1 min | 0.38 GB | measured |
| ransomware.live (aggregates) | 0.01 MB | 0.2 min | small | measured |
| **Core, measured total** | **114.6 MB** | **about 6 min** | **1.47 GB** | |
| VulnCheck KEV (private) | 30 MB (10-50) | 1 min | 0.3 GB | estimate |
| Shadowserver dashboard series | 10 MB (2-30) | 5 min | 0.3 GB | estimate |
| Censys, GreyNoise, CrowdSec counts | 4 MB | 8 min | 0.3 GB | estimate |
| Exploratory and global sources (X12, X14-X22, Project Zero, kernel dates) | 30 MB | 7 min | 0.8 GB | estimate (honeypot measured: 0.04 MB, 1.2 min, 0.77 GB per month) |
| BigQuery results (HTTP Archive, deps.dev) | 6 MB | 5 min | small | estimate; 200-700 GB scanned per quarter, inside the 1 TB a month free tier with byte caps |
| Evaluation (labels, page, hand-check lists, worksheets) | 5 MB | 3 min | about 2 GB | estimate |
| Job overhead (install, checks, upload) | | 2 min | | measured |
| **Full pull** | **about 200 MB** | **about 38 min** | **about 2 GB of 16 GB** | |

The quarterly AI-attack sweep (X3) is Claude's work, not the runner's: about 3-4 hours a quarter,
under 1 MB of logs.

## Per run type

| Run | What runs | Storage | Run time on GitHub |
|---|---|---|---|
| Test run (15 Dec full dry run, 75 days) | one pull | about 170 MB | about 35 min |
| Pilot run (Q4 2026) | provisional (1 Jan) and final (1 Feb) pulls, plus the archived container image (about 250 MB, estimate) with the final | about 650 MB | about 76 min |
| Quarterly run (each 2027 quarter) | as the pilot, plus three monthly honeypot captures | about 650 MB | about 80 min |
| Year 2027 | four quarterly runs | about 2.6 GB archived | about 5½ hours |

## Where it is kept
- **Run bundles:** GitHub artifacts, kept 90 days (at most about 1.3 GB at a time).
- **Archive:** Zenodo with each final release, publishable data only (no VulnCheck entries,
  ransomware.live aggregates only once permitted): about 2.6 GB for 2027, well inside Zenodo's
  50 GB per record.
- **Logs and reports:** the run-reports branch, a few MB a year.
- **Private backup:** the author's Google Drive (decided 26 Oct; `docs/BACKUP.md`): every
  pull's full bundle, including private data and dry runs, and a monthly copy of the
  repository; about 3 GB for 2027.

## Limits and risks
Found on 26 Oct: nothing runs out of capacity in 2027. Two gaps, both closed by the Drive
backup: full raw data (provisional runs, dry runs, private VulnCheck data) had no lasting home
after GitHub's 90 days, and everything sat in one GitHub account.
- Memory and disk are not a constraint: the largest step uses under a tenth of the runner's
  memory, and a full pull writes 0.2 GB against 92 GB free.
- The real limits are outside GitHub: BigQuery's free 1 TB a month (each query capped in bytes),
  Censys credits, and polite request rates (ransomware.live no more often than every 30
  minutes; Shadowserver read without scraping unless permitted).
- The estimates are checked against measurements on 15 Dec; this page is updated then.
