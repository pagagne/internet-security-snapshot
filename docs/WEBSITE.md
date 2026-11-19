# The project website (updated 19 Nov 2026)

Built on 19 Nov 2026 (schedule item `pages-build`), published by the Website workflow
(`.github/workflows/pages.yml`) from the `site/` folder, and switched on by the author on 4 Dec
2026. Address: https://pagagne.github.io/internet-security-snapshot/ ; the Reviewer's Desk at
`/reviewer/`; run health at `/health/`. Project links may be shared publicly only from 4 Dec 2026.

## What is on it

| Section | Where it comes from | Who changes it |
|---|---|---|
| Home page: Mission | The README's Mission section, word for word | The author approves README wording; the page follows |
| Home page: links | `snapshot.site` (run health, Reviewer's Desk, the plan, OSF, code and documents) | Claude, shown to the author |
| Home page: Reports | A short line until the pilot report; Publish results adds the reports from 2 Jan 2027 | Publish results, after the author's approval |
| Home page: credits | `config/credits.yaml`, the same block as every report | Claude, checked automatically |
| Reviewer's Desk | `site/reviewer/` | Claude, for the reviewer |
| Run health | Built at each publish from the public run reports: the pilot, start to finish; last and next run; source answers and permission states; rebuild and privacy checks; recent runs | Nobody by hand; health only, never findings or counts |

## Step by step: switching it on (author, 4 Dec 2026)

1. On GitHub, open the repository, then **Settings > Pages**. Under "Build and deployment",
   set **Source** to **GitHub Actions**. Nothing is published yet.
2. Still in Settings, open **Secrets and variables > Actions > Variables**, choose **New
   repository variable**, name it `PAGES_ON`, value `on`, and save. Until this exists every
   Website run is skipped.
3. Open the **Actions** tab, choose **Website**, then **Run workflow** (leave the box ticked).
   Wait for the green tick, about two minutes.
4. Open https://pagagne.github.io/internet-security-snapshot/ and check the home page, the
   Reviewer's Desk and run health. Tell Claude what you see; Claude checks the published pages
   against the repository and records the go-live.
5. From now on the site rebuilds by itself after each listed workflow, so nothing else is
   needed day to day.

To switch it off again: set `PAGES_ON` to `off` (the site stays as last published), or under
Settings > Pages choose **Unpublish site** to take it down.

## Step by step: approving the sections still in draft

1. **Mission wording.** The home page shows the README's Mission section as it stands. Read it
   on the site; any change is made in the README with your approval, and the site follows on the
   next push.
2. **The pilot, start to finish** (run health). The layout is a draft until you approve the
   mock-up (schedule item `pilot-timeline-mockup`, 23 Nov 2026). Claude shows it to you; your
   changes go into `snapshot.site` and the draft note comes off.
3. **Reports.** Nothing to do before the pilot. On 2 Jan 2027 you approve the pilot report and
   press Publish results; that run also refreshes the website.

## Step by step: when results are published (from 2 Jan 2027)

1. Claude asks you to approve the report (option card) once the private draft has rebuilt.
2. You press **Publish results** on the Actions tab.
3. It refuses unless your approval is recorded, the privacy scan is clean, nothing says
   SIMULATION, every draft section is cleared and no release-hold issue is open.
4. It copies the report and its PDF to the public repository and updates the README page.
5. Its completion starts the Website workflow, which republishes the site with the report.
6. Claude checks both front doors and tells you they match.

## Rules

- Health only on run health: states, dates and links; no findings, counts or exploratory figures.
- The Website workflow runs the privacy scan on exactly what it publishes and stops on a finding.
- The home page is rebuilt and checked by the Checks workflow (`python -m snapshot.site check`).
- No project links in public postings, social media or forums before 4 Dec 2026.
