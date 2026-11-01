"""Pre-filled fix dates for the review list. The author confirms or corrects each one.

Tried in order, using the CVE record's own links:
1. GitHub release tag link  -> the release's publish date
2. GitHub security advisory -> the advisory's publish date
3. GitHub commit link       -> the commit date
4. Otherwise                -> the CVE publication date, marked as an assumption
   (vendors usually publish the fix and the CVE together under coordinated disclosure)

Only GitHub's public API is queried (with GITHUB_TOKEN when set). Every pre-fill names
its source so the author can check it in one click.
"""

from __future__ import annotations

import os
import re
from functools import lru_cache

import requests

API = "https://api.github.com"
RELEASE = re.compile(r"github\.com/([^/]+)/([^/]+)/releases/tag/([^\s?#]+)")
ADVISORY = re.compile(r"github\.com/([^/]+)/([^/]+)/security/advisories/(GHSA-[\w-]+)")
COMMIT = re.compile(r"github\.com/([^/]+)/([^/]+)/commit/([0-9a-f]{7,40})")


@lru_cache(maxsize=2048)
def _get(path: str) -> dict | None:
    h = {"Accept": "application/vnd.github+json", "User-Agent": "internet-security-snapshot"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        r = requests.get(API + path, headers=h, timeout=30)
        return r.json() if r.ok else None
    except requests.RequestException:
        return None


def prefill(links: list[str], cve_published: str) -> tuple[str, str]:
    """Return (YYYY-MM-DD, source note)."""
    for url in links:
        if m := RELEASE.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/releases/tags/{m[3]}")
            if d and d.get("published_at"):
                return d["published_at"][:10], f"GitHub release {m[3]}"
        if m := ADVISORY.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/security-advisories/{m[3]}")
            if d and d.get("published_at"):
                return d["published_at"][:10], f"GitHub advisory {m[3]}"
        if m := COMMIT.search(url):
            d = _get(f"/repos/{m[1]}/{m[2]}/commits/{m[3]}")
            date = ((d or {}).get("commit") or {}).get("committer", {}).get("date")
            if date:
                return date[:10], f"fix commit {m[3][:10]} (fix may ship later in a release)"
    return cve_published[:10], "ASSUMED same day as CVE publication; check the advisory link"


# --- Vendor sources for exploited flaws (research item 1, 2026-10-23) ----------------------
# Probe on 175 KEV additions (Apr-Sep 2026): GitHub links dated 18; adding Microsoft's Update
# Guide API, Cisco CSAF and Palo Alto JSON dated 54; the CNA's datePublic covers 33 more.
# Vendor dates mostly equal CVE publication, but revision histories sometimes say the fix
# shipped later ("Updated fixed release information", "Fix release timeline"): those are
# flagged so they always go to the hand check.

MSRC_SUG = "https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?$filter=cveNumber eq '%s'"
CISCO_CSAF = "https://sec.cloudapps.cisco.com/security/center/contentjson/CiscoSecurityAdvisory/{sa}/csaf/{sa}.json"
PAN_JSON = "https://security.paloaltonetworks.com/json/{cve}"
# Added 29 Oct 2026 (schedule item kernel-fixdates-prefill): Linux kernel fixing commits, Siemens
# CSAF and Red Hat CSAF VEX. The 25 Oct probe dated 5 of 8 kernel KEV flaws from their commits.
KERNEL_SHA = re.compile(r"git\.kernel\.org/.*?/c/([0-9a-f]{12,40})")
SIEMENS_SSA = re.compile(r"cert-portal\.siemens\.com/productcert/\w+/(ssa-\d+)", re.I)
SIEMENS_CSAF = "https://cert-portal.siemens.com/productcert/csaf/{ssa}.json"
REDHAT_VEX = "https://security.access.redhat.com/data/csaf/v2/vex/{year}/{cve}.json"
CISCO_SA = re.compile(r"(cisco-sa-[\w-]+)")
FIX_LATER = re.compile(r"fix(ed)? release|fixed software|hotfix|fix release timeline|software fix|"
                       r"patch(es)? (is|are) now available|fixes? (is|are) now available", re.I)


def fix_later_signal(history: list[str]) -> bool:
    """True when a revision after the first one says fixed releases were added or changed."""
    return any(FIX_LATER.search(h or "") for h in history[1:])


@lru_cache(maxsize=4096)
def _vendor_json(url: str) -> dict | None:
    try:
        r = requests.get(url, headers={"User-Agent": "internet-security-snapshot", "Accept": "application/json"}, timeout=40)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError):
        return None


def prefill_exploited(cve_id: str, refs: list[str], vendor: str, published: str,
                      date_public: str = "") -> tuple[str, str, bool]:
    """Fix-date pre-fill for a CVE in the exploited set (option (a)).

    Returns (YYYY-MM-DD, source note, needs_hand_check). Order: GitHub links; Microsoft
    Update Guide; Cisco CSAF; Linux kernel commits; Siemens CSAF; Red Hat VEX; Palo Alto JSON;
    OSV fixing commit; deps.dev release of the first patched version; a full date written in an
    advisory link; CNA datePublic; else publication (assumed).
    """
    d, src = prefill(refs, published)
    if not src.startswith("ASSUMED"):
        return d, src, src.startswith("fix commit")
    v, joined = (vendor or "").lower(), " ".join(refs)
    if "microsoft" in v or "msrc.microsoft.com" in joined:
        j = _vendor_json(MSRC_SUG % cve_id) or {}
        val = j.get("value") or []
        if val and val[0].get("releaseDate"):
            return val[0]["releaseDate"][:10], "Microsoft Update Guide release date", False
    if m := CISCO_SA.search(joined):
        j = _vendor_json(CISCO_CSAF.format(sa=m.group(1))) or {}
        tr = (j.get("document") or {}).get("tracking") or {}
        if tr.get("initial_release_date"):
            hist = [h.get("summary", "") for h in tr.get("revision_history") or []]
            later = fix_later_signal(hist)
            return tr["initial_release_date"][:10], f"Cisco advisory {m.group(1)}" + (" (fixed releases changed later)" if later else ""), later
    if "linux" in v and "git.kernel.org" in joined:
        dates = []
        for sha in sorted({m.group(1) for r in refs for m in [KERNEL_SHA.search(r)] if m})[:8]:
            for repo in ("torvalds/linux", "gregkh/linux"):
                c = ((_get(f"/repos/{repo}/commits/{sha}") or {}).get("commit") or {})
                date = (c.get("committer") or c.get("author") or {}).get("date")
                if date:
                    dates.append(date[:10])
                    break
        if dates:
            return min(dates), "Linux kernel fixing commit (earliest of those named in the CVE record)", True
    if m := SIEMENS_SSA.search(joined):
        j = _vendor_json(SIEMENS_CSAF.format(ssa=m.group(1).lower())) or {}
        tr = (j.get("document") or {}).get("tracking") or {}
        if tr.get("initial_release_date"):
            hist = [h.get("summary", "") for h in tr.get("revision_history") or []]
            later = fix_later_signal(hist)
            return tr["initial_release_date"][:10], f"Siemens advisory {m.group(1).upper()}" + (" (fixes changed later)" if later else ""), later
    if "red hat" in v or "redhat" in v:
        j = _vendor_json(REDHAT_VEX.format(year=cve_id.split("-")[1], cve=cve_id.lower())) or {}
        fixes = [r.get("date", "")[:10] for vv in j.get("vulnerabilities") or []
                 for r in vv.get("remediations") or [] if r.get("category") == "vendor_fix" and r.get("date")]
        if fixes:
            return min(fixes), "Red Hat CSAF VEX: earliest vendor fix", False
    if "palo alto" in v or "paloaltonetworks" in joined:
        j = _vendor_json(PAN_JSON.format(cve=cve_id)) or {}
        cna = (j.get("containers") or {}).get("cna") or {}
        if cna.get("datePublic"):
            hist = [t.get("value", "") for t in cna.get("timeline") or []]
            later = fix_later_signal(hist)
            return cna["datePublic"][:10], "Palo Alto advisory" + (" (fix timeline changed later)" if later else ""), later
    # Added 1 Nov 2026 after the fix-date sources test (author's decision): small real gains
    d2 = osv_fix_commit(cve_id)
    if d2:
        return d2, "OSV: fixing commit named for this CVE (fix may ship later in a release)", True
    d2, note = depsdev_patched_release(cve_id)
    if d2:
        return d2, note, False
    d2, note = dated_advisory_link(refs)
    if d2:
        return d2, note, True
    if date_public:
        return date_public[:10], "vendor disclosure date (CVE datePublic); fix date not stated", True
    return published[:10], "ASSUMED same day as CVE publication; check the advisory link", True


# --- Extra sources (author's decision, 1 Nov 2026, after the private fixdate_sources test) ----
# Never used: the "published" date of GitHub's global advisory database. GitHub mirrors every
# CVE there as an unreviewed advisory on the day it is published, so that date is the CVE
# publication date again, not a fix date. Only reviewed advisories' patched versions are used.

OSV_VULN = "https://api.osv.dev/v1/vulns/{id}"
GH_GLOBAL_ADV = "/advisories?cve_id={cve}&type=reviewed"
DEPSDEV_VERSION = "https://api.deps.dev/v3/systems/{sys}/packages/{pkg}/versions/{ver}"
DEPSDEV_SYS = {"npm": "npm", "pip": "pypi", "maven": "maven", "go": "go", "nuget": "nuget",
               "rubygems": "rubygems", "rust": "cargo"}
DATE_IN_PATH = re.compile(r"(?<!\d)(20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])(?!\d)")
GIT_REPO = re.compile(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")
# Hosts whose links are advisories or bulletins, not write-ups by third parties
ADVISORY_HOST = re.compile(r"source\.android\.com|security|advisor|psirt|support\.|kb\.|bulletin|access\.redhat", re.I)


def osv_fix_commit(cve_id: str) -> str:
    """Earliest GitHub commit OSV names as fixing this CVE, or ''."""
    from urllib.parse import quote
    rec = _vendor_json(OSV_VULN.format(id=quote(cve_id))) or {}
    dates = []
    for af in rec.get("affected") or []:
        for rg in af.get("ranges") or []:
            m = GIT_REPO.search(rg.get("repo", "")) if rg.get("type") == "GIT" else None
            for ev in (rg.get("events") or []) if m else []:
                if ev.get("fixed"):
                    c = ((_get(f"/repos/{m.group(1)}/{m.group(2)}/commits/{ev['fixed']}") or {}).get("commit") or {})
                    when = (c.get("committer") or c.get("author") or {}).get("date")
                    if when:
                        dates.append(when[:10])
    return min(dates) if dates else ""


def depsdev_patched_release(cve_id: str) -> tuple[str, str]:
    """Release date of the first patched version in a reviewed GitHub advisory, via deps.dev."""
    from urllib.parse import quote
    found = []
    for adv in _get(GH_GLOBAL_ADV.format(cve=cve_id)) or []:
        for v in adv.get("vulnerabilities") or []:
            pkg, fix = v.get("package") or {}, v.get("first_patched_version")
            fix = fix.get("identifier") if isinstance(fix, dict) else fix
            sysname = DEPSDEV_SYS.get((pkg.get("ecosystem") or "").lower())
            if sysname and fix and pkg.get("name"):
                j = _vendor_json(DEPSDEV_VERSION.format(sys=sysname, pkg=quote(pkg["name"], safe=""),
                                                        ver=quote(fix, safe=""))) or {}
                if j.get("publishedAt"):
                    found.append((j["publishedAt"][:10], f"deps.dev: {pkg['name']} {fix} released (first patched version)"))
    return min(found) if found else ("", "")


def dated_advisory_link(refs: list[str]) -> tuple[str, str]:
    """A full date written in an advisory or bulletin link (e.g. Android bulletins), or ''."""
    from urllib.parse import urlparse
    found = []
    for r in refs:
        u = urlparse(r)
        if ADVISORY_HOST.search((u.hostname or "") + u.path) and (m := DATE_IN_PATH.search(u.path)):
            found.append((f"{m.group(1)}-{m.group(2)}-{m.group(3)}", f"date in advisory link ({u.hostname})"))
    return min(found) if found else ("", "")
