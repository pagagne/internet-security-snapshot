# Quarterly Internet Security Snapshot: Listening Version

Oct 20, 2026 · @Paul

## Opening

This is a listening version of where the project stands, written to be read aloud. It runs about ten minutes.

It tells the story in order. First, the report we started with and the idea at its heart. Then why we changed course. Then the study we built instead: what it measures, how it works, and how it keeps itself honest. It ends with what's been done so far and what comes next.

There are no tables or links here. Everything you hear is also written down in full in the technical spec and in the project's public files.

## Where we started

The project began with a report on how artificial intelligence is changing internet security. It drew on news and research from around the world, including sources from China and Russia, and was fact-checked and then challenged by its own adversarial review.

At its heart was a thesis: the internet will be cleaned up and become more functional, but it will be a painful process. The report described a race between two curves. One is the falling cost of attack, now that capable AI models can find and exploit weaknesses cheaply. The other is the rising speed of repair, through faster patching, tighter deadlines and better defenses. In 2026 the attack curve was ahead. The thesis said the repair curve would catch up, with the worst of the pain in 2026 and 2027.

The adversarial review found that the thesis held up only in a softer form. Cleanup looked likely, but it might look more like a managed balance than a clean internet, and it might arrive later than hoped.

## Why the path changed

A report can argue for a thesis. It can't test one. So the next question was how to watch, month after month, whether things were actually moving the way the report expected.

The first idea was a live global dashboard. That turned out to be a large engineering project. It was cut back to a one-month snapshot, then a monthly measurement study, and finally to something one person can run for free: a quarterly snapshot, using only free public data, built by you with Claude's help.

The biggest change was in the questions themselves. The study no longer tries to prove that the internet will be cleaned up. It simply tracks whether internet security is getting better or worse, and how AI is involved. Your own expectations, such as the belief that AI will keep driving up the number of vulnerabilities found, are written down in advance as predictions that can turn out to be wrong.

## What we track each quarter, and what we hope to find

The study tracks seven questions every quarter. Each one has a fixed definition of what counts as better or worse, set before any data was seen.

The first and most important is the race. Are defenders closing exposed vulnerabilities faster than attackers start exploiting them? It's measured two ways. One is the number of days between a fix being released and the first sign of attacks. The other is whether half of the vulnerable systems on the internet disappear before attackers arrive. What we hope to find here is the clearest answer to the report's central claim: whether repair is catching up with attack.

The second question is how fast vulnerable systems disappear after a fix. We hope to learn whether organizations are patching faster than before, or whether exposed systems linger for months, as recent research suggests they often do.

The third is how fast newly announced flaws are attacked, and how often attacks start on or before the day a flaw is made public. We hope to see whether that window is still shrinking.

The fourth is how old the attacked flaws are. This one has no better or worse. Attacks on old flaws mean patching is failing; attacks on brand-new flaws mean attackers are getting faster. We hope to learn which story fits.

The fifth is discovery pressure: how many new vulnerabilities are published, compared with a year earlier. Your prediction is that it keeps rising as AI finds more flaws, and the study will show whether that holds.

The sixth is visible harm: ransomware victims posted on leak sites, and breaches that U.S. public companies report to regulators. We hope to see whether harm is rising or falling, and to understand how much of the change is real.

The seventh is how much vulnerability discovery is credited to AI tools. Your prediction is that it keeps rising.

A question is labeled improving or worsening, or rising or falling, once it moves the same way two quarters in a row. That rule is deliberately loose, so movement shows quickly. The confidence ranges are published alongside, so readers can judge how much is noise.

## How it works

Everything runs on free data and free services. The data comes from public sources: the official list of published vulnerabilities, the U.S. government's catalog of flaws known to be under attack, daily scores that estimate how likely a flaw is to be exploited, the Shadowserver Foundation's internet scans and decoy servers, ransomware leak-site trackers, and breach filings with the U.S. Securities and Exchange Commission.

Four times a year, on the first of January, April, July and October, an automated job on GitHub collects the previous quarter's data. It saves each file exactly as it was received, with a digital fingerprint, so anyone can check later that nothing changed. A first look is published that day. A month later the job runs again to catch late reports and corrections, and the final results come out.

At the center of the study is a small group of vulnerabilities followed closely. Each month a fixed rule picks up to four serious new flaws: one in firewalls and remote-access gateways, one in web and file-sharing servers, one in any other internet-facing product, and one credited to an AI tool, when there is one. Each flaw is tagged by the kind of weakness behind it, such as memory errors or broken logins. Each one is followed for ninety days, from the day it's announced, through the fix, the first public attack code, the first observed attacks, and the decline in vulnerable systems.

Within each group, the pick is made by a random draw that anyone can repeat: a fixed formula shuffles the month's eligible flaws, and the first one in the shuffle is chosen. That way the study doesn't favour vendors that happen to publish early in the month. The draw never looks at whether a flaw was attacked, because attacks are what the study is measuring.

## Keeping it honest, and the annual wrap-up

The whole plan was registered publicly on the Open Science Framework on the twentieth of October, 2026, before any results were computed. That registration fixes the questions, the definitions and the rules, so no one can pick a flattering number afterwards. Any change made later goes into a public log with its date and reason, and the original plan stays in place.

There's a conflict of interest to be open about. Claude, made by Anthropic, writes the code and drafts each quarter's results, and Anthropic is named in the report this study grew from. The safeguards are the frozen plan, public code, your approval of every release, and an outside reviewer for the first full quarter.

Once a year there's a wrap-up. Each March, the four free quarters of the year before are compared with better information published by others, to show how well the free system tracked reality.

For exposure, the study's figures are checked against historical internet scan data, ideally obtained through Censys's free research program, or a one-time purchase if not. The comparison shows how many vulnerabilities each source could measure, how close the numbers were, and whether the quarterly directions matched.

For harm, the leak-site and breach-filing trends are compared with figures published each year by cyber insurers, ransom negotiators and companies that trace ransom payments. That comparison matters because leak sites only list victims who refused to pay. If fewer victims pay, leak-site counts can rise even when attacks don't. The annual check is designed to catch exactly that, and to say plainly which way the free measures leaned.

The yearly comparison isn't graded with a pass mark. It's reported as it stands, so readers can decide how much to trust the quarterly numbers. The first one is due in March 2028, covering 2027.

## What's been done so far

In a single day, the plan was written, frozen and registered. A public GitHub repository holds the plan, the rules, and the first working code. Free accounts were set up with the data providers, and their keys are stored securely on GitHub.

Three organizations were asked in writing for permission to publish results built from their data: Shadowserver, VulnCheck and ransomware.live. Until each one says yes, nothing derived from its data is published.

The first two data collectors, for the government's list of attacked flaws and for the full set of published vulnerabilities, were tested on live data. Two things stood out, and they're early checks on the pipeline, not results.

First, the number of new vulnerabilities published has roughly tripled in a year: about thirty-seven thousand in the third quarter of 2026, against about twelve thousand a year earlier. That fits the prediction that AI is driving discovery up.

Second, of the vulnerabilities whose credits name an AI tool, about eighty-three percent credit Claude. That makes the conflict of interest concrete. The AI-discovery measure largely tracks Anthropic's own work, and the study will say so every time it reports that number.

## What comes next

On the twentieth of November, any data provider that hasn't answered gets a polite follow-up.

On the first of December, the study runs a dry run on October and November data. It tests the whole process from start to finish and is clearly marked as unscored.

On the first of January 2027, the first real quarter is published as a pilot, with the final version a month later. The first quarter that fully counts is the start of 2027, with its results in April and May.

In March 2028 comes the first annual wrap-up, comparing a full year of free results with the published reference figures.

The report asked whether the internet will be cleaned up. This study won't answer that by argument. It will answer it slowly, one quarter at a time, in the open, with every number traceable to its source and every change on the record. Whatever the answer turns out to be, it will be one that anyone can check.
