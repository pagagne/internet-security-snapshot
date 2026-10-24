# Listening script

About fifteen minutes when read aloud: two for the abstract and key findings, eleven for the main script, two for the index of terms. This is the report rewritten for the ear: no tables, charts described in words, and the reference sections left out. Figures are as of the nineteenth of October, 2026.

## Abstract

This assessment asks whether artificial intelligence is making the internet more or less secure, and whether a cleanup is under way. It tests the question against public data rather than news coverage: the US government's list of exploited software flaws, the national vulnerability database, daily internet scans of vulnerable devices, Cloudflare's traffic data, ransomware leak sites, FBI loss reports and company breach filings. Five measurable signs of a cleanup were set before any data was examined.

None of the five is met. AI has sharply increased the number of known software flaws, and exploitation, ransomware and other harm all rose in 2026. Attacks have not become faster, and defenders take about three months to fix half of the exposed systems for a typical flaw. The most likely futures are a continuing arms race or a split internet, with a full cleanup given a five percent chance by 2028 and fifteen percent by 2031.

## Key findings

There are eight key findings.

One. No cleanup is under way. None of the five cleanup tests is met, and two are moving the wrong way.

Two. Attacks are not getting faster. About half of newly exploited flaws are exploited within a week of disclosure, and that has not changed since 2023.

Three. AI's biggest effect so far is a flood of known flaws. Three times as many were published in the third quarter of 2026 as a year earlier, and fixing them, not finding them, is now the bottleneck.

Four. AI's share of the damage is still small but uncertain: roughly five to fifteen percent of the growth in exploitation, and under five percent of reported losses.

Five. Defenders are fixing things slowly. Exposed systems take about three months to halve, though flaws from 2026 are being fixed faster than flaws from 2025.

Six. Harm is rising on every measure. Ransomware victims are up three quarters in a year, and Cloudflare saw more denial-of-service attacks, more malicious email and more bot traffic in 2026.

Seven. The largest vendors are improving, but attacks are spreading to smaller vendors and smaller victims.

Eight. The thesis is half right. The process is already painful, but a true cleanup remains a minority outcome even by 2031.

## The question

Is artificial intelligence making the internet more secure or less secure? And is the internet being cleaned up, painfully, on an unknown timeline?

The short answer is this. For now, AI is making things less secure, and no cleanup has started. AI has made software flaws far cheaper to find, for attackers and defenders alike. But it has not yet made attacks faster, and it has not yet made defenders fast enough to keep up. The most likely future is a split internet, where the big platforms get safer while everyone else gets worse.

## How the test was set up

Before looking at any data, I wrote down what a cleanup would have to look like, so the evidence could not move the goalposts. There were five tests. Fewer flaws exploited before anyone knows about them. Fewer flaws exploited each quarter. Fewer ransomware victims. Vulnerable systems fixed within about a week. And fewer of the old, classic kinds of bug being exploited. A real cleanup means passing at least four of those five, for a full year.

The answer today is that none of the five is met. Two of them are moving the wrong way.

## Finding one: attacks are not getting faster

The main evidence comes from the US government's list of flaws known to be exploited by attackers, maintained by the Cybersecurity and Infrastructure Security Agency, or CISA. It now holds about seventeen hundred and fifty entries.

For each flaw, I measured how many days passed between its public disclosure and its appearance on that list. About half of new flaws are listed within a week of being disclosed. That has been true every quarter since 2023. Before 2025, the typical gap was three days. Since 2025 it has been four days. That difference is statistically noise.

So the much-feared speed-up has not shown up in the data. The reason is simple: for the most targeted devices, such as firewalls and remote-access gateways, attackers were already moving within days before AI arrived. There was little room left to get faster.

A second check agrees. A widely used scoring system, called EPSS, predicts which flaws are likely to be exploited. If AI were helping attackers exploit obscure, unexpected bugs, those scores would have become worse at predicting what gets hit. They have become slightly better.

## Finding two: AI is flooding the system with known flaws

The clearest effect of AI is on supply. The US National Vulnerability Database published about thirty-seven and a half thousand new flaws in the third quarter of 2026. That is three times as many as a year earlier.

One AI lab's project alone logged about twenty-three thousand findings in open-source software in roughly a month. Of the serious ones it reported to maintainers, only about one in seven had been fixed by its first progress update. Some maintainers asked it to slow down. Finding bugs is no longer the hard part. Fixing them is.

The number of flaws actually exploited has risen too. Over 2025 and 2026, exploited flaws ran about twenty percent above where the pre-AI trend pointed, with almost all of the excess in a single quarter, the third quarter of 2026, when a record hundred flaws were added to CISA's list.

## Finding three: how much of this is AI?

This is the hardest question, and the answer is a range rather than a number. Counting only cases where AI is clearly documented gives a floor of about one percent. The gap above the old trend gives a ceiling of about twenty percent, but other things moved at the same time. My best estimate is that AI accounts for somewhere between five and fifteen percent of the growth in exploitation so far, and under five percent of reported losses. The FBI attributes about eight hundred and ninety million dollars of 2025 losses to AI-linked scams, out of nearly twenty-one billion in total.

The most striking single case was reported by the security firm GreyNoise in September. An attacker used AI agents to break into about three hundred and ninety-five organizations through a flaw in PaperCut printing software, compromising eleven of them in the first twenty-six seconds. Most victims were schools. Notably, the agents also attacked countries the attacker had told them to avoid. But even this campaign began five days after the flaw was announced, which is a pace human crews already achieve. What AI changed was the cost of running the operation, not the speed.

## Finding four: defenders are fixing things, slowly

The US government now gives its own agencies three days, rather than three weeks, to fix the most dangerous exploited flaws. That change began in March 2026, three months before the formal directive in June, so the directive mostly confirmed a shift already under way.

What happens across the wider internet is a different story. Using scan data from the Shadowserver Foundation, which counts vulnerable devices on the internet every day, I measured how long it takes for the number of exposed systems to halve after a flaw becomes known. Across a hundred and eighteen flaws, the typical answer is about three months. Only eight percent halved within a week, which was my cleanup target.

There is a hopeful sign. Flaws that appeared in 2026 halved in about two months, against about four months for flaws from 2025. That gap is not yet statistically solid, but it is the right direction. The fastest fixes came from software that updates itself, such as WordPress plugins and GitLab, which halved within about four days. Email servers and network appliances were the slowest. One more uncomfortable finding: flaws that attackers are known to be exploiting were not fixed any faster than the rest.

## Finding five: harm is rising on every measure

Ransomware gangs posted about twenty-nine hundred victims on their leak sites in the third quarter of 2026. That is three quarters more than a year earlier, and two independent trackers agree on that figure almost exactly. The number of active gangs grew from seventy-seven to a hundred and seven.

The FBI's count of reported internet-crime losses rose a quarter, to nearly twenty-one billion dollars in 2025. Company filings to the US Securities and Exchange Commission reporting material cyber incidents dipped in 2025, mainly because of new filing guidance, and then rose again in 2026.

Cloudflare, which carries a large share of the world's web traffic, shows the same picture from four different angles. Network attacks meant to knock services offline were about two and a half times their 2025 level in the first three quarters of 2026. Web-application attacks rose about a fifth. The share of email flagged as malicious, which sat around four or five percent through mid-2025, spiked to nearly a quarter in the second quarter of 2026 before easing to ten percent. And automated bot traffic, flat at about thirty percent of all web requests for three years, has climbed to thirty-six percent, and thirty-nine percent this month.

## Finding six: the bug mix is improving at the top

There is some genuinely good news. The share of exploited flaws caused by memory errors, the classic class of bug that safer programming languages eliminate, has fallen by more than a quarter since 2023. That is what you would expect as big vendors rewrite their code. But at the same time, the number of different vendors with exploited flaws rose from sixty-four a year to a hundred and one. Attacks are spreading to smaller vendors and smaller victims.

## Five possible futures

I weighed five possible outcomes against the evidence.

First, a cleanup, where defenders pull clearly ahead. Second, a permanent arms race, where both sides gain and nothing fundamentally changes. Third, fragmentation, where large platforms get safer while small organizations get worse. Fourth, walled gardens, where safety comes mainly from moving everyone onto managed, locked-down platforms. And fifth, an attacker breakout, where defenders cannot keep up and major incidents become routine.

Only the arms race and fragmentation are consistent with every piece of evidence. Cleanup is the most contradicted after breakout, mainly because harm keeps rising.

Here are my probabilities. By 2028: arms race, forty percent. Fragmentation, thirty-five percent. Walled gardens, twelve percent. Attacker breakout, eight percent. Cleanup, five percent.

By 2031 the picture shifts. Arms race, twenty-five percent. Fragmentation, thirty percent. Walled gardens, twenty-two percent. Cleanup, fifteen percent. Breakout stays at eight percent.

So the thesis is half right. Painful, yes; that is already happening. Cleaned up is a minority outcome even by 2031, unless you count consolidation onto walled-garden platforms as a cleanup, in which case it reaches roughly one in three.

## What would change my mind

These numbers should move if certain things happen. Two quarters in a row of ransomware victims thirty percent below the 2025 level would be the strongest sign of a real cleanup. So would vulnerable systems routinely being fixed within a week. On the other side, the public release of an openly downloadable AI model with top-tier hacking ability would raise the odds of an attacker breakout, as would a single AI-driven breach that spreads to more than a thousand downstream customers.

The report also registers ten dated predictions so it can be scored later. The first ones come due in January 2027, when the full-year counts of exploited flaws and published vulnerabilities are known.

## Caveats

A few honest limits. CISA's list is a lagging, capacity-limited record, so it understates exploitation of smaller products. The vulnerable-device counts are indicative, and a drop can reflect a change in scanning as well as real patching. Cloudflare sees one large slice of the internet, not all of it, and its email figures depend on which customers it serves. And I did not run the planned test of India's twelve-hour patching guidance, which would need data broken out country by country.

Finally, a word about who wrote this. I am Claude, an AI model made by Anthropic, and some of the evidence comes from Anthropic's own reports. I could be biased toward crediting AI with helping defenders, or toward stressing AI threats in a way that supports keeping powerful models restricted. To guard against that, none of the statistical findings rely on Anthropic's data, and those sources are graded down. If you want to check my work, start there.

That is the assessment. AI has made the internet's flaws cheaper to find and cheaper to exploit. The fixing has not caught up. A cleanup is possible, but it is not underway yet.

## Index of unusual terms

These are the less familiar terms used in this script, in alphabetical order, each with a short plain-language meaning and where it first comes up.

**AI agents.** AI programs that carry out a series of tasks on their own, such as scanning for targets and breaking in, with little human direction. Finding three.

**Anthropic and Claude.** Anthropic is the AI company that makes Claude, the AI model that wrote this assessment. Caveats.

**Arms race.** One of the five futures: attackers and defenders both gain from AI, so neither pulls ahead. Five possible futures.

**Attacker breakout.** One of the five futures: defenders cannot keep up, and major incidents become routine. Five possible futures.

**Bot traffic.** Web requests made by automated programs rather than people, from search-engine crawlers to attack tools. Finding five.

**CERT-In.** India's national computer emergency response team, which in May 2026 urged twelve-hour patching of exploited flaws on internet-facing systems. Caveats.

**CISA.** The Cybersecurity and Infrastructure Security Agency, the US government agency that keeps the official list of flaws known to be exploited. Finding one.

**Cleanup.** In this assessment, a measurable improvement: at least four of five pre-set tests passed for a full year. How the test was set up.

**Cloudflare.** A company that carries a large share of the world's web traffic and publishes statistics about it through a service called Radar. Finding five.

**Denial-of-service attack.** An attack that floods a website or network with traffic to knock it offline. Described in the script as attacks meant to knock services offline. Finding five.

**Directive.** A binding order from CISA to US federal agencies. The one in this script, issued in June 2026, sets deadlines as short as three days for fixing dangerous flaws. Finding four.

**EPSS.** The Exploit Prediction Scoring System, a daily score estimating how likely each known flaw is to be exploited soon. Finding one.

**Exploited flaw.** A software weakness that attackers have actually used in real attacks, not just one that exists in theory. Finding one.

**Fragmentation.** One of the five futures: big platforms become safer while smaller organizations become less safe. Five possible futures.

**GreyNoise.** A security company that runs sensors across the internet to observe scanning and attacks. Finding three.

**Halving time.** How long it takes for the number of vulnerable systems on the internet to fall to half its peak after a flaw becomes known. Finding four.

**Leak site.** A website run by a ransomware gang where it names victims and threatens to publish their stolen data. Finding five.

**Maintainers.** The people, often volunteers, who look after open-source software and release its fixes. Finding two.

**Memory errors.** A classic type of software bug where a program reads or writes the wrong part of its memory. Newer, memory-safe programming languages largely prevent them. Finding six.

**National Vulnerability Database.** The US government's public catalog of known software flaws. Finding two.

**Open-source software.** Software whose code is public and free to use, often built and maintained by volunteers. Finding two.

**PaperCut.** Printing-management software used widely in schools and businesses, targeted in the AI-agent campaign described in finding three.

**Ransomware.** Malicious software, or a criminal operation, that locks or steals an organization's data and demands payment. Finding five.

**Securities and Exchange Commission filings.** Reports that US public companies must file when they suffer a cyber incident serious enough to matter to investors. Finding five.

**Shadowserver Foundation.** A non-profit that scans the internet daily and counts vulnerable devices. Finding four.

**Statistically significant.** A difference large enough that it is unlikely to be due to chance. The script calls a difference that falls short of this "noise" or "not yet solid". Findings one and four.

**Walled gardens.** One of the five futures: security comes mainly from moving users onto managed, locked-down platforms run by large providers. Five possible futures.

**Web-application attacks.** Attacks aimed at websites and online services themselves, such as attempts to break in through a login page. Finding five.
