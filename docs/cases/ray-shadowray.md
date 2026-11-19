# Case note: Ray "ShadowRay" (CVE-2023-48022) (updated 19 Nov 2026)

Reference case, added 19 Nov 2026 at the author's request. It does **not** meet the watch-case
rule (`docs/RESEARCH_PLAN.md`, "Pilot watch cases": published in the quarter, CVSS 9.0 or more,
a national CERT alert), because it was published in November 2023, so it is followed as a
reference case outside the seeded draw. Reviewed with the author on 8 Feb 2027 with the pilot
watch cases. Nothing here changes a rule.

## Facts reported so far
- **What it is.** Ray (Anyscale) is an open-source framework for running AI and
  machine-learning work across clusters. Its job-submission API, exposed by default on the Ray
  Dashboard, has no authentication, so anyone who can reach it can run code (CVSS 3.1 9.8;
  published 28 Nov 2023; NVD lists Ray 2.6.3 and 2.8.0).
- **Disputed, never patched as a flaw.** Anyscale called it "a long-standing design decision"
  consistent with deploying Ray only on trusted networks. The four flaws reported with it were
  fixed in Ray 2.8.1; this one was not. Ray 2.52.0 and later offer optional token
  authentication.
- **Exploited at scale.** Oligo Security found thousands of exposed Ray servers compromised in
  the "ShadowRay" campaign (reported March 2024), and a self-spreading botnet, "ShadowRay
  2.0", in November 2025.
- **Lists.** Not in CISA KEV (several databases, Nov 2026); in VulnCheck KEV since
  26 Mar 2024. A different Ray flaw in the same API, CVE-2025-62593, was added to CISA KEV on
  17 Aug 2026.

## Points to review on 8 Feb 2027
- **Race (T1):** no fix date exists, because the maker does not treat it as a flaw, so time
  from fix to first attack cannot be measured. How should the study report flaws that are
  exploited but disputed (counted, set aside with a reason, or a separate line)?
- **Which exploited list:** widely exploited yet absent from CISA KEV while present in
  VulnCheck KEV: a concrete case for reading both lists (VulnCheck data stays private until
  its use is settled; permission for derived statistics granted 11 Nov 2026).
- **AI as a target:** an AI-infrastructure flaw exploited for years; relevant to the
  exploratory AI-as-a-target measures.
- **Unauthenticated by design:** similar "trusted network" designs in other AI tools (model
  servers, notebooks, agent frameworks) may behave the same way; a pattern to watch, not a
  count.

## Sources
- [NVD, CVE-2023-48022](https://nvd.nist.gov/vuln/detail/cve-2023-48022)
- [The Register, 27 Mar 2024 (Anyscale's position; Oligo's findings)](https://www.theregister.com/security/2024/03/27/thousands-of-firms-vulnerable-to-security-bug-in-ray-ai/779533)
- [Oligo Security, ShadowRay](https://oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild)
- [Cloud Security Alliance, 18 Aug 2026 (CVE-2025-62593 in KEV; ShadowRay 2.0)](https://labs.cloudsecurityalliance.org/research/csa-research-note-ray-cve-2025-62593-active-exploitation-202/)
