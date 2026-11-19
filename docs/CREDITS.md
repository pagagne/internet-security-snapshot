# Data sources and credits (updated 19 Nov 2026)

Built from `config/credits.yaml` by `python -m snapshot.credits build`; do not edit by hand. The same block is printed on every report page and its PDF, on the landing page and on the website. Terms and permissions behind each line: `docs/TERMS_OF_USE.md`, `docs/PERMISSIONS.md`.

## The block as printed

The study uses public and permissioned data. Every source whose data it uses is listed here, credited as its terms or its written permission ask; none of them endorses the study or its findings.

**Core data (scored)**

- CVE records: the CVE Program (cve.org), via the CVE List repository. <https://www.cve.org/Legal/TermsOfUse> Copyright © 1999-2026, The MITRE Corporation. CVE and the CVE logo are registered trademarks of The MITRE Corporation. Used under the CVE Program terms of use; CVE records are not altered.
- Vulnerability details: the National Vulnerability Database (NIST). <https://nvd.nist.gov/> This product uses the NVD API but is not endorsed or certified by the NVD.
- Known exploited vulnerabilities: CISA's Known Exploited Vulnerabilities Catalog. <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- Exploitation flags and added analysis: CISA Vulnrichment (published in the CVE records). <https://github.com/cisagov/vulnrichment>
- Second exploited list: VulnCheck KEV (community edition). <https://vulncheck.com/kev> (figures from 2026-12-01)
- Exploit likelihood scores: FIRST EPSS (Exploit Prediction Scoring System). <https://www.first.org/epss/>
- Fix dates in part from Red Hat security data, licensed CC BY 4.0. <https://access.redhat.com/security/data>
- Fix dates and version data in part from OSV.dev and deps.dev (each record under its source database's licence). <https://osv.dev/>
- Fix dates in part from the GitHub Advisory Database (reviewed advisories, CC BY 4.0). <https://github.com/advisories>
- Fix dates in part from vendors' own security advisories (Microsoft, Cisco, Palo Alto Networks, Siemens) and Linux kernel fixing commits (git.kernel.org). <https://git.kernel.org/>
- Company breach filings: US Securities and Exchange Commission, EDGAR. <https://www.sec.gov/edgar/search/>
- Source: Ransomware.live <https://www.ransomware.live/>

**Exploratory measures**

- Bot, AI and attack traffic: Cloudflare Radar, data under CC BY-NC 4.0. <https://radar.cloudflare.com/>
- Honeypot activity: SANS Technology Institute, Internet Storm Center, https://isc.sans.edu <https://isc.sans.edu/>
- Data provided by GreyNoise. <https://www.greynoise.io/>
- AI tool and model counts: public data from GitHub and Hugging Face, read through their official APIs; individuals' projects are never named. <https://huggingface.co/>
- AI attack log: every case cites the published report it comes from (security firms, government agencies, platforms); titles and links only. <https://github.com/pagagne/internet-security-snapshot/blob/main/config/feeds.yaml>
- DNSSEC and RPKI measurements: APNIC Labs (stats.labs.apnic.net), used with permission; figures as published. <https://stats.labs.apnic.net/> (figures from 2026-12-01)
- Alerts: CERT-FR (ANSSI), under Licence Ouverte 2.0. <https://www.cert.ssi.gouv.fr/>
- Alerts: JPCERT/CC (www.jpcert.or.jp). <https://www.jpcert.or.jp/>
- Alerts: BSI (Germany) and KrCERT/CC (Korea), each alert cited by title, date and link. <https://www.bsi.bund.de/>
- Health-sector breaches: US Department of Health and Human Services, Office for Civil Rights breach portal (counts only). <https://ocrportal.hhs.gov/ocr/breach/>
- Data breach trends: Information Commissioner's Office, under the Open Government Licence v3.0. <https://ico.org.uk/>
- Office of the Australian Information Commissioner website - www.oaic.gov.au (CC BY 4.0). <https://www.oaic.gov.au/>
- Breach notification counts: Singapore's Personal Data Protection Commission and ENISA (EU Agency for Cybersecurity) published reports, each cited by title and link. <https://www.enisa.europa.eu/>

## Why each line is there

- **CVE Program**: CVE Program terms of use (MITRE licence), read 18 Nov 2026.
- **NVD (NIST)**: NVD terms of use (notice required on products using the API).
- **CISA KEV**: US government work; repository licence.
- **CISA Vulnrichment**: US government work; repository licence (credited because the study uses it, 19 Nov 2026).
- **VulnCheck KEV**: Written permission 11 Nov 2026 (attribution of the source data).
- **FIRST EPSS**: EPSS usage agreement, read 18 Nov 2026 (attribution asked).
- **Red Hat security data**: CC BY 4.0 (credit and link required), read 18 Nov 2026.
- **OSV and deps.dev**: OSV and deps.dev data licences, read 18 Nov 2026.
- **GitHub Advisory Database**: GitHub Advisory Database licence (CC BY 4.0); used for first patched versions since 1 Nov 2026.
- **Vendor advisories and the Linux kernel**: Each vendor's site terms (fix dates only, cited per flaw); credited because the study uses them (19 Nov 2026).
- **SEC EDGAR**: Public US government records; fair-access rules.
- **ransomware.live**: Written permission 27 Oct 2026 (ticket 3425); terms section 6 (named source with a link back).
- **Cloudflare Radar**: Radar data licence CC BY-NC 4.0, read 12 Nov 2026.
- **SANS Internet Storm Center**: ISC data-feed terms (use permitted with attribution; not resold).
- **GreyNoise**: Research access granted 17 Nov 2026; uses agreed 18 and 19 Nov 2026 (credit as worded by GreyNoise).
- **GitHub and Hugging Face**: GitHub and Hugging Face terms (research use of public, non-personal information); credited because the study uses them (19 Nov 2026).
- **Published reports in the AI attack log**: Each publisher's terms; titles and links only (docs/TERMS_OF_USE.md, Other services).
- **APNIC Labs**: Written leave 1 Nov 2026 (ticket 00177078).
- **CERT-FR (ANSSI)**: Licence Ouverte / Etalab 2.0.
- **JPCERT/CC**: JPCERT/CC site terms (quoting with source, document and URL); courtesy notice sent 29 Oct 2026.
- **BSI and KrCERT/CC**: Public alerts, cited per alert (titles, CVE IDs and dates only); credited because the study uses them (19 Nov 2026).
- **HHS OCR breach portal**: US government records; counts only, no entity names.
- **UK ICO**: Open Government Licence v3.0.
- **OAIC**: CC BY 4.0, credit as worded by the OAIC.
- **Singapore PDPC and ENISA**: Published reports, counts cited per report; credited because the study uses them (19 Nov 2026).
