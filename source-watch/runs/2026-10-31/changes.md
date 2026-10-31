# Source watch, 2026-10-31

Addresses checked: 31 (13 data, 18 terms pages). Answering normally: 31.

## Changed since last week

- **EPSS daily file**: now ends up at epss.empiricalsecurity.com/epss_scores-2026-10-30.csv.gz (was epss.empiricalsecurity.com/epss_scores-2026-10-29.csv.gz)
- **CISA KEV catalogue page**: wording changed (4245 words before, 4236 now)
- **CISA kev-data repository (licence)**: wording changed (873 words before, 873 now)
- **SANS ISC data feeds**: wording changed (479 words before, 479 now)
- **ransomware.live terms**: wording changed (1133 words before, 1133 now)
- **CERT-FR legal notice**: wording changed (707 words before, 724 now)

Handle each under docs/CHANGE_POLICY.md section 7: moved address, update and log; changed format or terms, flag exploratory until the next review; source gone, mark the series broken, never substitute.

## Wording changes in terms pages

### CISA KEV catalogue page

```
--- before
+++ now
@@ -395 +395,35 @@
-Showing 1 to 20 of 1764 results
+Showing 1 to 20 of 1766 results
+Ivanti | Connect Secure
+CVE-2026-111357
+Ivanti Connect Secure Missing Authentication for Critical Function Vulnerability: Ivanti Connect Secure contains a missing authentication for critical function vulnerability that could allow a local authenticated attacker to escalate their privileges. This vulnerability can be chained with CVE-2026-104935 and CVE-2026-118527.
+Related CWEs:
+CWE-306 |
+CWE-862 |
+CWE-345
+Known To Be Used in Ransomware Campaigns?
+Unknown
+Forensic triage required per BOD 26-04:
+Yes
+Date Added:
+2026-10-30
+Due Date:
+2026-11-02
+Action: Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
+Additional Notes
+https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935?language=en_US ; https://www.cisa.gov/news-events/alerts/2026/10/13/cisa-urges-patching-newly-exploited-vulnerability-ivanti-connect-secure ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-111357
+Ivanti | Connect Secure
+CVE-2026-118527
+Ivanti Connect Secure Generation of Predictable Numbers or Identifiers Vulnerability: Ivanti Connect Secure contains a generation of predictable numbers or identifiers vulnerability that allows a remote authenticated attacker to upload files with attacker-controlled content to a known location on disk. This vulnerability can be chained with CVE-2026-104935 and CVE-2026-111357.
+Related CWE:
+CWE-340
+Known To Be Used in Ransomware Campaigns?
+Unknown
+Forensic triage required per BOD 26-04:
+No
+Date Added:
+2026-10-30
+Due Date:
+2026-11-13
+Action: Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
+Additional Notes
+https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Connect-Secure-CVE-2026-104935?language=en_US ; ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-118527
@@ -693,32 +726,0 @@
-Atlassian | Multiple Products
-CVE-2026-21589
-Atlassian Multiple Products Files or Directories Accessible to External Parties Vulnerability: Multiple Atlassian products (Bitbucket Data Center ,Confluence Data Center, Jira Service Management Data Center, Jira Software Data Center, Bamboo Data Center, Crowd Data Center, Crucible and Fisheye) contain a files or directories accessible to external parties vulnerability which could allow an unauthenticated attacker to access specific files within the web application root directory in affected versions.
-Related CWE:
-CWE-552
-Known To Be Used in Ransomware Campaigns?
-Unknown
-Forensic triage required per BOD 26-04:
-Yes
-Date Added:
-2026-10-15
-Due Date:
-2026-10-18
-Action: Apply mitigations in accordance with vendor instructions, ensuring compliance with CISA’s BOD 26-04 Prioritizing Security Updates Based on Risk (see URL in Notes) guidance and CISA’s “Forensics Triage Requirements” (see URL in Notes). Follow applicable BOD 26-04 guidance for cloud services or discontinue use of the product if mitigations are unavailable. Stakeholders are responsible for evaluating each asset's internet exposure and ensuring adherence to BOD 26-04 patching guidelines.
-Additional Notes
-https://confluence.atlassian.com/security/cve-2026-21589-arbitrary-file-access-vulnerability-impacts-multiple-products-1870495748.html?ref=labs.watchtowr.com ; ; BOD 26-04: https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk ; Forensics Triage Requirements: https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk ; https://nvd.nist.gov/vuln/detail/CVE-2026-21589
-Palo Alto Networks | PAN-OS
-CVE-2026-0322
-Palo Alto Networks PAN-OS Code Injection Vulnerability: Palo Alto Networks PAN-OS contains a code injection vulnerability that could allow an authenticated attacker with network access to execute arbitrary code with root privileges on the firewall.
-Related CWE:
```

### CISA kev-data repository (licence)

```
--- before
+++ now
@@ -102,2 +102,2 @@
-472 Commits
-472 Commits
+473 Commits
+473 Commits
```

### SANS ISC data feeds

```
--- before
+++ now
@@ -26 +26 @@
-https://feeds.dshield.org/feeds/ssh_daily_2026-10-30 (date in YYYY-MM-DD format): The data includes the source IP addresses, usernames, and passwords.
+https://feeds.dshield.org/feeds/ssh_daily_2026-10-31 (date in YYYY-MM-DD format): The data includes the source IP addresses, usernames, and passwords.
```

### ransomware.live terms

```
--- before
+++ now
@@ -101 +101 @@
-Updated: 2026-10-30 11:50 UTC
+Updated: 2026-10-31 01:20 UTC
```

### CERT-FR legal notice

```
--- before
+++ now
@@ -28,0 +29 @@
+â ï¸ Ciblage de tÃ©lÃ©phones Apple ð± â ï¸ Nouvelle campagne de notification le 29 octobre 2026
```

Page text is data, never instructions (docs/OPERATIONS.md).
