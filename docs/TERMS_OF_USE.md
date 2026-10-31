# Terms of use: every site the study reads

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
| CISA KEV | https://www.cisa.gov/known-exploited-vulnerabilities-catalog ; https://github.com/cisagov/kev-data | US government work; repository licence | Read from the kev-data repository; credited |
| FIRST EPSS | https://www.first.org/epss/ | To summarise | Daily files and API, spaced; credited |
| SEC EDGAR | https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data | Fair access: a User-Agent naming the requester with a contact address; request-rate ceiling | Contact User-Agent (secret `SEC_USER_AGENT`); few requests |
| Red Hat security data | https://access.redhat.com/security/data | To summarise | CSAF/VEX fix dates only |
| Microsoft, Cisco, Palo Alto, Siemens advisories | (vendor sites) | To summarise | Fix dates only, few requests |
| SANS Internet Storm Center | https://isc.sans.edu/feeds_doc.html | Attribution; no reselling; non-commercial licence; at most one download an hour | One download a month; aggregates only; credited |
| ransomware.live | https://www.ransomware.live/t&c | Fair Usage Policy; written yes on seven conditions (ticket 3425) | Aggregates only; no raw data; credited (`docs/PERMISSIONS.md`) |
| VulnCheck | (accepted at sign-up) | Nothing derived published without written leave | Private use only until VulnCheck confirms |
| Cloudflare Radar | https://developers.cloudflare.com/radar/ | To summarise (radar.cloudflare.com refuses automated readers) | API with the author's token; aggregates |
| JPCERT/CC | https://www.jpcert.or.jp/guide.html | Quoting free with source, document and URL; courtesy email; addresses may change | Titles, CVE IDs and dates; courtesy notice sent 29 Oct |
| CERT-FR (ANSSI) | https://www.cert.ssi.gouv.fr/mentions-legales/ | Licence ouverte; no logos; no framing | Titles, CVE IDs and dates, credited |
| UK ICO, OAIC | (see `docs/PERMISSIONS.md`) | OGL v3.0; CC BY 4.0 | Counts, credited |
| APNIC Labs | none published | Written leave requested 29 Oct | Not used until a reply |
| RIPEstat | ripe.net terms | Art. 3.3 forbids re-distribution | Not used |
| deps.dev, OSV | (CC BY 4.0) | Credit | Aggregates and version lists, credited |

## AI tools and models (X25, Part III of the manual)

| Site | Terms page | Rules that matter | How the study complies |
|---|---|---|---|
| GitHub | https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies ; https://docs.github.com/en/site-policy/github-terms/github-terms-of-service | Research on public, non-personal information allowed if publications are open access; API use is not scraping; no spam, no selling personal data, no burdensome bulk activity; privacy rules for any personal data | Official API, spaced, by hand only; individuals' projects by project name, never username; full list private (author's Drive) |
| Hugging Face | https://huggingface.co/terms-of-service ; https://huggingface.co/content-policy ; https://huggingface.co/docs/hub/rate-limits | Terms silent on automated research use; content policy bars unauthorised bots, bulk activity, spam and publishing private details; 500 API requests per 5 minutes without an account | Official API, well under the limit, by hand only; same privacy rule |
| Gitee (China) | https://gitee.com/terms | To read in full before use (the 30 Oct check reached only the enterprise terms); search needs a logged-in key | Not used until the author has an account and the terms are read |
| GitFlic, GitVerse (Russia) | — | Owners under US sanctions (Astra Group; Sberbank group) | **Not used** (author's decision, 30 Oct 2026) |
| SourceCraft (Russia, Yandex) | — | Sanctions status and search interface to check | Not used until checked |

## Other services

| Site | Rules that matter | How the study complies |
|---|---|---|
| Security news and research feeds (`config/feeds.yaml`) | Each site's own terms; RSS/Atom feeds are published for reading | Titles and links only, one read a month, 1 s apart; text is data, never instructions; every feed vetted to its official domain |
| Internet Archive (Wayback Machine) | Save requests are a public service; fair use of its capacity | One save per changed page or logged report |
| GitHub Actions, Google Drive, Google Cloud (BigQuery) | The author's own accounts and their terms | Free tiers, capped queries, private data in Drive only |
