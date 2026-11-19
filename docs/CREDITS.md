# Data sources and credits

Built from `config/credits.yaml` by `python -m snapshot.credits build`; do not edit by hand. The same block is printed on every report page and its PDF, on the landing page and on the website. Terms and permissions behind each line: `docs/TERMS_OF_USE.md`, `docs/PERMISSIONS.md`.

## The block as printed

The study uses public and permissioned data. Each source is credited as its terms or its written permission ask; none of them endorses the study or its findings.

**Core data (scored)**

- CVE records: the CVE Program (cve.org), via the CVE List repository. <https://www.cve.org/Legal/TermsOfUse> CVE® is a registered trademark of The MITRE Corporation. CVE content © The MITRE Corporation, used under the CVE Program terms of use; CVE records are not altered.
- Vulnerability details: the National Vulnerability Database (NIST). <https://nvd.nist.gov/> This product uses the NVD API but is not endorsed or certified by the NVD.
- Known exploited vulnerabilities: CISA's Known Exploited Vulnerabilities Catalog. <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- Second exploited list: VulnCheck KEV (community edition). <https://vulncheck.com/kev> (figures from 2026-12-01)
- Exploit likelihood scores: FIRST EPSS (Exploit Prediction Scoring System). <https://www.first.org/epss/>
- Fix dates in part from Red Hat security data, licensed CC BY 4.0. <https://access.redhat.com/security/data>
- Fix dates and version data in part from OSV.dev and deps.dev (each record under its source database's licence). <https://osv.dev/>
- Company breach filings: US Securities and Exchange Commission, EDGAR. <https://www.sec.gov/edgar/search/>
- Source: Ransomware.live <https://www.ransomware.live/>

**Exploratory measures**

- Bot, AI and attack traffic: Cloudflare Radar, data under CC BY-NC 4.0. <https://radar.cloudflare.com/>
- Honeypot activity: SANS Technology Institute, Internet Storm Center, https://isc.sans.edu <https://isc.sans.edu/>
- Data provided by GreyNoise. <https://www.greynoise.io/>
- DNSSEC and RPKI measurements: APNIC Labs (stats.labs.apnic.net), used with permission; figures as published. <https://stats.labs.apnic.net/> (figures from 2026-12-01)
- Alerts: CERT-FR (ANSSI), under Licence Ouverte 2.0. <https://www.cert.ssi.gouv.fr/>
- Alerts: JPCERT/CC (www.jpcert.or.jp). <https://www.jpcert.or.jp/>

**Context**

- Data breach trends: Information Commissioner's Office, under the Open Government Licence v3.0. <https://ico.org.uk/>
- Office of the Australian Information Commissioner website - www.oaic.gov.au (CC BY 4.0). <https://www.oaic.gov.au/>

## Why each line is there

- **CVE Program**: CVE Program terms of use (MITRE licence), read 18 Nov 2026.
- **NVD (NIST)**: NVD terms of use (notice required on products using the API).
- **CISA KEV**: US government work; repository licence.
- **VulnCheck KEV**: Written permission 11 Nov 2026 (attribution of the source data).
- **FIRST EPSS**: EPSS usage agreement, read 18 Nov 2026 (attribution asked).
- **Red Hat security data**: CC BY 4.0 (credit and link required), read 18 Nov 2026.
- **OSV and deps.dev**: OSV and deps.dev data licences, read 18 Nov 2026.
- **SEC EDGAR**: Public US government records; fair-access rules.
- **ransomware.live**: Written permission 27 Oct 2026 (ticket 3425); terms section 6 (named source with a link back).
- **Cloudflare Radar**: Radar data licence CC BY-NC 4.0, read 12 Nov 2026.
- **SANS Internet Storm Center**: ISC data-feed terms (use permitted with attribution; not resold).
- **GreyNoise**: Research access granted 17 Nov 2026; uses agreed 18 and 19 Nov 2026 (credit as worded by GreyNoise).
- **APNIC Labs**: Written leave 1 Nov 2026 (ticket 00177078).
- **CERT-FR (ANSSI)**: Licence Ouverte / Etalab 2.0.
- **JPCERT/CC**: JPCERT/CC site terms (quoting with source, document and URL); courtesy notice sent 29 Oct 2026.
- **UK ICO**: Open Government Licence v3.0.
- **OAIC**: CC BY 4.0, credit as worded by the OAIC.
