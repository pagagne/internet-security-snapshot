# Fix-date source probe

KEV additions probed: 175 (with a CVE record: 175)

| Source | CVEs dated |
|---|---|
| GitHub links (current pre-fill) | 18 |
| Microsoft Update Guide API | 21 |
| Microsoft CVRF | 16 |
| Cisco CSAF | 13 |
| Palo Alto JSON | 4 |
| Fortinet | 0 |
| CNA datePublic (disclosure, not fix) | 58 |
| **Any fix-date source (GitHub or vendor)** | **54** |

## Differences from CVE publication (days, vendor date minus publication)

- github: n=18, same day 4, earlier 14, later 0, range -37 to 0
- msrc_release: n=21, same day 17, earlier 4, later 0, range -6 to 0
- cisco_initial: n=13, same day 13, earlier 0, later 0, range 0 to 0
- pan_datepublic: n=2, same day 1, earlier 1, later 0, range -1 to 0
- datepublic: n=58, same day 36, earlier 22, later 0, range -31 to 0

Cisco advisories listing a fixed release: 0 of 13

## HTTP status counts per source

```
{
 "cve_record": {
  "200": 175
 },
 "cisco_csaf": {
  "200": 13
 },
 "msrc_sug": {
  "200": 27
 },
 "msrc_cvrf": {
  "200": 16,
  "503": 3,
  "ReadTimeout": 2,
  "404": 6
 },
 "forti_csaf": {
  "404": 6
 },
 "forti_csaf2": {
  "422": 6
 },
 "forti_cvrf": {
  "404": 6
 },
 "forti_page": {
  "200": 6
 },
 "paloalto": {
  "200": 2
 }
}
```

## Top vendors without any fix-date source

- Linux: 7
- Adobe: 6
- Fortinet: 6
- Microsoft: 6
- Google: 5
- Check Point: 4
- SonicWall: 4
- JFrog: 4
- Oracle: 4
- Citrix: 4
- MikroTik: 3
- TrueConf: 3
- PaperCut: 3
- N-able: 3
- Ubiquiti: 3
