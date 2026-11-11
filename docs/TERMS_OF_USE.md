# Terms of use: every site the study reads (updated 11 Nov 2026)

Register added 30 Oct 2026 at the author's request ("include all the terms of use of the sites
we're accessing"). One row per site: its terms page, the rules that matter to the study, and how
the study complies. Details and correspondence are in `docs/PERMISSIONS.md`; requests for
permission are logged there too.

**Dated copies.** Every terms page listed here with a link is checked weekly by the Source watch
workflow (`config/source_watch.yaml`): a dated text copy is kept on the run-reports branch
(`source-watch/terms/`) and in the Internet Archive whenever its wording changes, so the terms in
force when the data was used can always be shown (`docs/CHANGE_POLICY.md` section 7).
"To summarise" means the page is watched and copied but its rules have not yet been written up
here; Claude summarises them at the 18 Nov refinement. Nothing here is legal advice.

## Core and companion data

| Site | Terms page | Rules that matter | How the study complies |
|---|---|---|---|
| NVD (NIST) | https://nvd.nist.gov/developers/terms-of-use | API rate limits; a notice that the product uses the NVD API but is not endorsed by NVD | Keyed requests within the limits (pull), notice on outputs |
| CVE Program | https://www.cve.org/Legal/TermsOfUse | To summarise | CVE List read from the cvelistV5 repository |
| CISA KEV | https://github.com/cisagov/kev-data (the catalogue page itself changes daily, so it is not watched) | US government work; repository licence | Read from the kev-data repository; credited |
| FIRST EPSS | https://www.first.org/epss/ | To summarise | Daily files and API, spaced; credited |
| SEC EDGAR | https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data | Fair access: a User-Agent naming the requester with a contact address; request-rate ceiling | Contact User-Agent (secret `SEC_USER_AGENT`); few requests |
| Red Hat security data | https://access.redhat.com/security/data | To summarise | CSAF/VEX fix dates only |
| Microsoft, Cisco, Palo Alto, Siemens advisories | (vendor sites) | To summarise | Fix dates only, few requests |
| SANS Internet Storm Center | https://isc.sans.edu/feeds_doc.html | Attribution; no reselling; non-commercial licence; at most one download an hour | Two files once a month, an hour apart; aggregates only; credited |
| ransomware.live | https://www.ransomware.live/t&c | Fair Usage Policy; written yes on seven conditions (ticket 3425) | Aggregates only; no raw data; credited (`docs/PERMISSIONS.md`) |
| VulnCheck | (accepted at sign-up) | Nothing derived published without written leave | Private use only until VulnCheck confirms |
| Cloudflare Radar | https://developers.cloudflare.com/radar/ | To summarise (radar.cloudflare.com refuses automated readers) | API with the author's token; aggregates |
| JPCERT/CC | https://www.jpcert.or.jp/guide.html | Quoting free with source, document and URL; courtesy email; addresses may change | Titles, CVE IDs and dates; courtesy notice sent 29 Oct |
| CERT-FR (ANSSI) | https://www.cert.ssi.gouv.fr/mentions-legales/ | Licence ouverte; no logos; no framing | Titles, CVE IDs and dates, credited |
| UK ICO, OAIC | (see `docs/PERMISSIONS.md`) | OGL v3.0; CC BY 4.0 | Counts, credited |
| APNIC Labs | none published | Written leave granted 1 Nov 2026 (ticket 00177078): credit APNIC Labs; figures must accurately represent the source data | Per-country DNSSEC and RPKI figures for X20, credited to APNIC Labs, shown as published (no reworking beyond regional averages, which are labelled as ours) |
| RIPEstat | ripe.net terms | Art. 3.3 forbids re-distribution | Not used |
| deps.dev, OSV | https://docs.deps.dev/api/v3/index.html ; OSV: to summarise | deps.dev: the Google API Terms of Service apply; its generated data is CC BY 4.0 and may be cached; third-party data it aggregates (OSV, registries) follows each source's own terms. OSV advisories carry their sources' licences | Aggregates and version lists, credited. Since 1 Nov 2026 also fix dates for the race list: one OSV record and one deps.dev version lookup per flaw first added to KEV, spaced, once per run |
| GitHub Advisory Database (API) | GitHub terms (row below) | Reviewed advisories only. Read 1 Nov 2026: unreviewed advisories are published automatically from the NVD feed, so their date is the CVE's, not a fix date | Used since 1 Nov 2026 only for the first patched version of reviewed advisories (fix dates); never their publication date |

## AI tools and models (X25, Part III of the manual)

| Site | Terms page | Rules that matter | How the study complies |
|---|---|---|---|
| GitHub | https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies ; https://docs.github.com/en/site-policy/github-terms/github-terms-of-service | Research on public, non-personal information allowed if publications are open access; API use is not scraping; no spam, no selling personal data, no burdensome bulk activity; privacy rules for any personal data | Official API, spaced, by hand only; individuals' projects by project name, never username; full list private (author's Drive) |
| Hugging Face | https://huggingface.co/terms-of-service ; https://huggingface.co/content-policy ; https://huggingface.co/docs/hub/rate-limits | Terms silent on automated research use; content policy bars unauthorised bots, bulk activity, spam and publishing private details; 500 API requests per 5 minutes without an account | Official API, well under the limit, by hand only; same privacy rule |
| Gitee (China) | https://gitee.com/terms | Read 31 Oct 2026 (website terms of use; Chinese, governed by PRC law, Beijing courts). Run by 北京奥思研工智能科技有限公司 (OSCHINA). A limited licence to view the site's content; uploaders own their content; no framing or hot-linking and no "large volumes of external link requests"; no manipulating Stars or Forks; personal information protected under PRC law. Nothing on automated reading or research either way. Search through the official API needs a logged-in personal access token | Reviewed again 31 Oct 2026 (author's request) before any use: the terms allow viewing content; forbid framing, hot-linking, large volumes of external link requests and Star/Fork manipulation; are silent on the API, automation and research; the privacy policy calls the phone number a basis of the service, so an account without one may be limited later; searches are held in China under PRC law. The author's account has no bound phone (mainland numbers only) but could make a token (scope user_info, secret `GITEE_TOKEN`). Tested 31 Oct 2026 (author's approval): five searches through the official API, twice (scope user_info, then user_info and projects): every search answered with 0 results, while the website search (so.gitee.com) shows about 200 for the same term. Gitee's API search is closed to the study; the website is not read automatically (that would be scraping). **Not used** (31 Oct 2026); China is covered by the Chinese-language GitHub searches. The `gitee_probe` task stays for an anonymous re-check (18 Nov); the token and its secret were deleted the same day. If an account is not possible, China is covered by the Chinese-language GitHub searches |
| GitFlic, GitVerse (Russia) | — | Owners under US sanctions (Astra Group; Sberbank group) | **Not used** (author's decision, 30 Oct 2026) |
| SourceCraft (Russia, Yandex) | — | Checked 31 Oct 2026: Yandex itself was not found on the US blocking (SDN) list in our searches; its API needs a personal token, so an account with a Russian company would be needed. Not legal advice | **Not used** (author's decision, 31 Oct 2026); Russia covered through Russian-language GitHub searches |

## Other services

| Site | Rules that matter | How the study complies |
|---|---|---|
| Security news and research feeds (`config/feeds.yaml`) | Each site's own terms; RSS/Atom feeds are published for reading | Titles and links only, one read a month, 1 s apart; text is data, never instructions; every feed vetted to its official domain |
| Security newsletters to the project address (from 2 Nov 2026; seven, listed in the calendar item newsletter-setup) | Read 1 Nov 2026, summaries below; all are free subscriptions delivered by email | Read as delivered (the Gmail label "Snapshot newsletters"), never by visiting or scraping the sites. **Research only** (author, 1 Nov 2026): nothing from them is shown in a report or on the landing page, and they do not feed the AI attack log; any trends summary is our own words. No text copied or republished; nothing used to train any AI model |
| SANS NewsBites | https://www.sans.org/legal/terms-conditions | Website content may be viewed, printed or downloaded for personal, non-commercial use; reproduction or redistribution needs written consent. Separately bans uploading "SANS Materials" (defined as courseware and training materials) to any AI system, with liquidated damages | **Not subscribed** (author's decision, 1 Nov 2026): NewsBites appears to be website content, not "SANS Materials", but the AI clause is strict. Revisited on 18 Nov (what it would add, and whether SANS allows AI-assisted reading) |
| Risky Bulletin, Seriously Risky Business (Substack) | https://substack.com/tos | Personal or organisational use; no crawling or scraping; no copying or storing a significant portion of content; creators own their posts | Email only; titles, links and our notes only |
| The Record (Recorded Future News) | https://www.recordedfuture.com/legal/terms-of-use (6 Feb 2026) | The news site's own terms were not found; Recorded Future's terms (for its products) ban automated access, copying, publishing output and AI training | Treated conservatively: email only, titles, links and our notes; no automated reading of therecord.media |
| TLDR InfoSec | https://tldr.tech/terms | Silent on reuse, automation and AI; no bulk or unsolicited messages; informational only | Email only; titles, links and our notes |
| tl;dr sec, Unsupervised Learning | https://www.beehiiv.com/tou (6 Oct 2026; hosting to confirm at sign-up) | No data mining, robots, crawling or scraping; no proxies to get round blocks; creators own their content | Email only; titles, links and our notes |
| CISA email updates | https://www.cisa.gov/terms-use | General-information disclaimer; no reuse limits stated; US government | Email only; advisories cited by title and link |
| Internet Archive (Wayback Machine) | Save requests are a public service; fair use of its capacity | One save per changed page or logged report |
| GitHub Actions, Google Drive, Google Cloud (BigQuery) | The author's own accounts and their terms | Free tiers, capped queries, private data in Drive only |

## Request volume against each source's limits (audit, 11 Nov 2026)

The author asked for a check that no source is called more often than its rules allow. Every
automated request the study makes, by schedule:

- **Daily** (Source status, 21:47 UTC): one light request (status and first 512 bytes) to each of
  eight sources: the CVE List and CISA KEV repositories (GitHub API), NVD (one result), FIRST EPSS
  (one result), SEC EDGAR (contact User-Agent), Red Hat and Palo Alto (one advisory each) and the
  ransomware.live home page; 2 s apart, one retry after 5 s on an error. The Schedule and Privacy
  runs call only GitHub.
- **Weekly** (Source watch, Wednesdays): about 35 terms and documentation pages on about 25
  sites, at most three on any one site.
- **Monthly:** the ISC web-honeypot capture (two feed files, the 2nd); the AI-attack feed screen
  (one request to each of 68 feeds, the 5th); the Drive backup and the rebuild check (no outside
  requests).
- **Quarterly** (the pull and the final run a month later): the CVE List, KEV and the NVD mirror
  by git from GitHub (NVD's own feed files only as a fallback); four NVD API count queries 7 s
  apart; about 92 EPSS daily files 1 s apart and EPSS API pages 0.5 s apart; SEC full-text search
  0.2 s apart with the contact User-Agent; a few Cloudflare Radar calls with the token; three
  ransomware.live api-pro calls 5 s apart.
- **On demand:** Research tasks, started only by the author or the schedule.

Against the published limits: NVD allows 5 requests in 30 s without a key and 50 with one, and
asks for about 6 s between requests (the study waits 6.5 s without a key, 0.7 s with it, and 7 s
for the count queries); SEC asks for at most 10 requests a second and a contact User-Agent (5 a
second, contact set); ISC asks bots for at most 1 request a second, a contact in the User-Agent
(a URL is accepted) and no screen-scraping (two feed files a month, project URL in the
User-Agent). GitHub, FIRST, Red Hat, Palo Alto and Cloudflare are called far below any limit.

Three points went to the author (11 Nov): ransomware.live's three calls a pull are 5 s apart
while the study's own rule says one call every 30 minutes; the daily status ping reads the
ransomware.live home page although condition 1 says access only through the api-pro endpoint;
and ISC's bot rules ask researchers to tell ISC how its data is used, and its feed page asks for
at most one download an hour (the capture takes its two files back to back).

**Decided by the author, 11 Nov 2026:** ransomware.live's three calls a pull are now 30 minutes
apart; ransomware.live is no longer in the daily status check (shown as checked at each pull);
the ISC capture waits an hour between its two files; and a short courtesy note telling ISC how
the study uses its data is drafted for the author to send.
