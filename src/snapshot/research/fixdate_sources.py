"""Research probe (author's decision, 1 Nov 2026): which extra sources would give real fix dates?

The Q3 2026 practice evaluation found that most flaws first added to CISA KEV in the quarter got
only an assumed fix date (the publication date). This probe takes the same flaws (KEV additions
between --start and --end), runs today's pre-fill (snapshot.fixdates.prefill_exploited) as the
baseline, then tries four candidate groups independently on every flaw:

  A  OSV and GitHub advisories: the OSV record for the CVE, its aliases and related advisories
     (GHSA, distribution advisories such as USN, DSA, openSUSE); the earliest advisory published
     date, and a fixing commit date where OSV names one
  B  deps.dev: release date of the first patched version named by the GitHub advisory
  C  vendor CSAF feeds: CSAF provider metadata (/.well-known/csaf/provider-metadata.json) on the
     hosts of the CVE's reference links; where a provider lists its documents, the advisory that
     names this CVE and its initial release date; plus advisory URLs that carry a full date
     (e.g. Android bulletins)
  D  Debian and Ubuntu: Debian security advisories (DSA/DLA) and Ubuntu notices (USN) found
     through OSV, their published dates

Reports, for each group, how many flaws it dates at all and how many of the baseline's
"assumed" flaws it rescues, plus the union. Only official APIs and published files; requests
spaced; no web pages scraped. Private (saved with the practice evaluation): method only.

    python -m snapshot.research.fixdate_sources --start 2026-07-01 --end 2026-09-30 --out DIR
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urlparse

import pandas as pd
import requests

from ..fixdates import prefill_exploited
from .prefill_coverage import CVE_RAW, KEV_URL, bucket

UA = "internet-security-snapshot research (fix-date coverage probe)"
OSV = "https://api.osv.dev/v1/vulns/{id}"
GH_ADV = "https://api.github.com/advisories?cve_id={cve}"
DEPSDEV = "https://api.deps.dev/v3/systems/{sys}/packages/{pkg}/versions/{ver}"
DEPSDEV_SYS = {"npm": "npm", "pip": "pypi", "maven": "maven", "go": "go", "nuget": "nuget",
               "rubygems": "rubygems", "rust": "cargo", "composer": None}
DISTRO = re.compile(r"^(USN|DSA|DLA|UBUNTU-USN|DEBIAN-DSA|DEBIAN-DLA)-", re.I)
DATE_IN_URL = re.compile(r"(?<!\d)(20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])(?!\d)")
GIT_COMMIT = re.compile(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")
PAUSE = 0.3
_cache: dict = {}


def _get(url: str, gh: bool = False, text: bool = False):
    if url in _cache:
        return _cache[url]
    h = {"User-Agent": UA, "Accept": "application/json"}
    if gh and os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        r = requests.get(url, headers=h, timeout=30)
        time.sleep(PAUSE)
        out = (r.text if text else r.json()) if r.ok else None
    except (requests.RequestException, ValueError):
        out = None
    _cache[url] = out
    return out


def _d(s) -> str:
    return str(s or "")[:10]


# A and D: OSV --------------------------------------------------------------------------------
def osv_dates(cve: str) -> tuple[dict, dict]:
    """(group A dates, group D dates) as {date: note}."""
    a, d = {}, {}
    rec = _get(OSV.format(id=cve)) or {}
    ids = set(rec.get("aliases") or []) | set(rec.get("related") or [])
    for af in rec.get("affected") or []:
        for rg in af.get("ranges") or []:
            if rg.get("type") != "GIT":
                continue
            m = GIT_COMMIT.search(rg.get("repo", ""))
            for ev in rg.get("events") or []:
                if m and ev.get("fixed"):
                    c = (_get(f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/commits/{ev['fixed']}", gh=True) or {}).get("commit") or {}
                    when = (c.get("committer") or c.get("author") or {}).get("date")
                    if when:
                        a[_d(when)] = "OSV fixing commit"
    for i in sorted(ids)[:12]:
        adv = _get(OSV.format(id=quote(i))) or {}
        when = _d(adv.get("published"))
        if not when:
            continue
        (d if DISTRO.match(i) else a)[when] = f"advisory {i} published"
    return a, d


# B: deps.dev -----------------------------------------------------------------------------------
def depsdev_dates(cve: str) -> tuple[dict, dict]:
    """(GitHub advisory published dates for group A, first-patched release dates for group B)."""
    a, b = {}, {}
    for adv in _get(GH_ADV.format(cve=cve), gh=True) or []:
        if adv.get("published_at"):
            a[_d(adv["published_at"])] = f"GitHub advisory {adv.get('ghsa_id')} published"
        for v in adv.get("vulnerabilities") or []:
            pkg, fix = v.get("package") or {}, v.get("first_patched_version")
            fix = fix.get("identifier") if isinstance(fix, dict) else fix
            sysname = DEPSDEV_SYS.get((pkg.get("ecosystem") or "").lower())
            if not (sysname and fix and pkg.get("name")):
                continue
            j = _get(DEPSDEV.format(sys=sysname, pkg=quote(pkg["name"], safe=""), ver=quote(fix, safe=""))) or {}
            if j.get("publishedAt"):
                b[_d(j["publishedAt"])] = f"{sysname} {pkg['name']} {fix} released"
    return a, b


# C: vendor CSAF --------------------------------------------------------------------------------
_providers: dict = {}


def provider(host: str):
    """CSAF provider metadata for a host or its parent domain, or None."""
    parts = host.split(".")
    for h in [".".join(parts[i:]) for i in range(len(parts) - 1)]:
        if h in _providers:
            if _providers[h]:
                return _providers[h]
            continue
        pm = _get(f"https://{h}/.well-known/csaf/provider-metadata.json")
        _providers[h] = pm if isinstance(pm, dict) and pm.get("distributions") else None
        if _providers[h]:
            return _providers[h]
    return None


def _changes(dist_url: str) -> list[tuple[str, str]]:
    t = _get(dist_url.rstrip("/") + "/changes.csv", text=True)
    if not t:
        return []
    return [(r[0], r[1]) for r in csv.reader(io.StringIO(t)) if len(r) >= 2]


def csaf_date(cve: str, refs: list[str]) -> tuple[dict, str]:
    """Group C dates and the CSAF status note ('no provider', 'provider, doc not found', ...)."""
    out, status = {}, "no CSAF provider on reference hosts"
    for r in refs:
        if m := DATE_IN_URL.search(urlparse(r).path):
            out[f"{m.group(1)}-{m.group(2)}-{m.group(3)}"] = "date in advisory URL"
    tokens = {cve.lower()} | {p.lower() for r in refs for p in re.split(r"[/?#=&]", urlparse(r).path) if len(p) >= 6}
    for host in sorted({urlparse(r).hostname or "" for r in refs} - {""})[:6]:
        pm = provider(host)
        if not pm:
            continue
        status = f"CSAF provider {pm.get('publisher', {}).get('namespace', host)}, advisory not located"
        for dist in pm.get("distributions") or []:
            dirs = [dist["directory_url"]] if dist.get("directory_url") else []
            tries = 0
            for path, _ in _changes(dirs[0])[:20000] if dirs else []:
                stem = path.rsplit("/", 1)[-1].lower().removesuffix(".json")
                if (stem in tokens or any(len(stem) >= 6 and stem in t for t in tokens)) and tries < 5:
                    tries += 1
                    doc = _get(dirs[0].rstrip("/") + "/" + path) or {}
                    named = {v.get("cve") for v in doc.get("vulnerabilities") or []}
                    tr = (doc.get("document") or {}).get("tracking") or {}
                    if cve in named and tr.get("initial_release_date"):
                        out[_d(tr["initial_release_date"])] = f"CSAF {stem}"
                        return out, f"CSAF provider {host}: advisory found"
            for feed in ((dist.get("rolie") or {}).get("feeds") or [])[:3]:
                j = _get(feed.get("url", "")) or {}
                for e in ((j.get("feed") or {}).get("entry") or []):
                    if cve.lower() in (str(e.get("title", "")) + str(e.get("id", ""))).lower():
                        for ln in e.get("link") or []:
                            doc = _get(ln.get("href", "")) or {}
                            tr = (doc.get("document") or {}).get("tracking") or {}
                            if tr.get("initial_release_date"):
                                out[_d(tr["initial_release_date"])] = f"CSAF {e.get('id')}"
                                return out, f"CSAF provider {host}: advisory found (ROLIE)"
    return out, status


# -----------------------------------------------------------------------------------------------
def earliest(found: dict) -> tuple[str, str]:
    if not found:
        return "", ""
    d = min(found)
    return d, found[d]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-07-01"); ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    kev = pd.DataFrame((_get(KEV_URL) or {}).get("vulnerabilities") or [])
    kev = kev[(kev["dateAdded"] >= a.start) & (kev["dateAdded"] <= a.end)]
    rows = []
    for k in kev.itertuples():
        y, n = k.cveID.split("-")[1:]
        rec = _get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=k.cveID)) or {}
        cna = (rec.get("containers") or {}).get("cna") or {}
        refs = [r.get("url", "") for r in cna.get("references") or []]
        pub = _d((rec.get("cveMetadata") or {}).get("datePublished")) or k.dateAdded
        d0, src, _ = prefill_exploited(k.cveID, refs, k.vendorProject, pub, _d(cna.get("datePublic")))
        ga, gd = osv_dates(k.cveID)
        gh_a, gb = depsdev_dates(k.cveID)
        ga.update(gh_a)
        gc, cstatus = csaf_date(k.cveID, refs)
        row = {"cve_id": k.cveID, "vendor": k.vendorProject, "product": k.product, "kev_added": k.dateAdded,
               "published": pub, "baseline": bucket(src), "baseline_date": d0, "csaf_status": cstatus}
        for g, found in (("A_osv_ghsa", ga), ("B_depsdev", gb), ("C_vendor_csaf", gc), ("D_debian_ubuntu", gd)):
            row[g], row[g + "_note"] = earliest(found)
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(a.out / "fixdate_sources.csv", index=False)

    groups = ["A_osv_ghsa", "B_depsdev", "C_vendor_csaf", "D_debian_ubuntu"]
    assumed = df["baseline"] == "assumed" if len(df) else pd.Series(dtype=bool)
    L = [f"# Fix-date sources: coverage test on KEV additions {a.start} to {a.end}", "",
         f"Flaws: {len(df)}; baseline (today's pre-fill) assumed: {int(assumed.sum())}", "",
         "| Group | Dates any flaw | Rescues an assumed flaw | Earlier than the baseline's real date |",
         "|---|---|---|---|"]
    for g in groups:
        has = df[g].astype(bool)
        earlier = (~assumed & has & (df[g] < df["baseline_date"])).sum()
        L.append(f"| {g} | {int(has.sum())} | {int((has & assumed).sum())} | {int(earlier)} |")
    union = df[groups].astype(bool).any(axis=1)
    L += ["", f"All four together rescue {int((union & assumed).sum())} of {int(assumed.sum())} assumed flaws.", "",
          "## CSAF providers seen on reference hosts", ""]
    L += [f"- {s}: {c}" for s, c in df["csaf_status"].value_counts().items()]
    L += ["", "## Assumed flaws still without any date, by vendor", ""]
    left = df[assumed & ~union]["vendor"].value_counts()
    L += [f"- {v}: {c}" for v, c in left.items()]
    L += ["", "Dates from groups A, B and D are release or advisory dates (the fix existed by then);",
          "they are candidates for the hand check, not replacements for it."]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"fix-date sources: {len(df)} flaws checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
