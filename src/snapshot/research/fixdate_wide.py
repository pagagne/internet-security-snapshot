"""Research probe (author, 15 Nov 2026): can the fix-date process be widened and the hand check
aimed better? A wider follow-up to fixdate_sources (1 Nov), which found CSAF only on the hosts
named in CVE references and judged OSV/GitHub advisory dates to be mirror dates.

For every CVE first added to CISA KEV between --start and --end, runs today's pre-fill
(snapshot.fixdates.prefill_exploited) as the baseline, then tries, independently:

  E  CSAF, found properly: providers listed by the BSI CSAF aggregator, the CSAF: line of each
     vendor's security.txt, and /.well-known/csaf/provider-metadata.json on the vendor's main
     domains (not only reference hosts). For each provider that matches a KEV vendor, its
     documents changed in the window are indexed by the CVEs they name (initial release date and
     whether a later revision says fixed releases changed).
  F  Vendor release calendars: does the vendor's date (baseline or E) fall on its known release
     day (Microsoft, Adobe and SAP second Tuesday; Oracle third Tuesday of Jan/Apr/Jul/Oct;
     Android monthly bulletins)? A calendar match is a strong, explainable date.
  G  Wayback Machine: the first capture with HTTP 200 of each vendor-advisory, patch or
     release-notes reference in the CVE record (CDX API). The fix was public by that day at the
     latest: an independent upper bound to check any suggested date against.
  H  Where checking matters: the gap between the best candidate fix date and the KEV addition
     date (a proxy for first exploitation; the study's own date comes from the race rules).
     Flaws added before, or within 7 days after, the fix date are "near the line".

Writes one row per CVE and summary.md (coverage per group, agreement between sources, how many
hand checks each change would remove, what still has no date, by vendor). Only official APIs,
published files and the Internet Archive's CDX API; requests spaced; a host that answers 403 or
429 twice is left alone for the rest of the run (no working around refusals). Private: method
only, saved with the other fix-date research.

    python -m snapshot.research.fixdate_wide --start 2026-04-01 --end 2026-10-31 --out DIR
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import re
import time
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, urlparse

import pandas as pd
import requests

from ..fixdates import prefill_exploited
from .prefill_coverage import CVE_RAW, KEV_URL, bucket

UA = "internet-security-snapshot research (fix-date wide probe; contact via github.com/pagagne)"
AGGREGATOR = "https://wid.cert-bund.de/.well-known/csaf-aggregator/aggregator.json"
CDX = ("https://web.archive.org/cdx/search/cdx?url={u}&output=json&limit=1"
       "&fl=timestamp,statuscode&filter=statuscode:200")
FIX_LATER = re.compile(r"fix(ed)? release|fixed software|hotfix|fix release timeline|software fix|"
                       r"patch(es)? (is|are) now available|fixes? (is|are) now available|"
                       r"updated? (the )?(fixed|remediation|solution)", re.I)
REF_TAGS = {"vendor-advisory", "patch", "release-notes", "mitigation"}
# Vendor (KEV vendorProject, lower case, first word) -> domains to look for CSAF on.
DOMAINS = {
    "microsoft": ["microsoft.com"], "oracle": ["oracle.com"], "fortinet": ["fortinet.com", "fortiguard.com"],
    "adobe": ["adobe.com"], "google": ["google.com"], "apple": ["apple.com"], "citrix": ["citrix.com", "cloud.com"],
    "sonicwall": ["sonicwall.com"], "check": ["checkpoint.com"], "ivanti": ["ivanti.com"],
    "vmware": ["vmware.com", "broadcom.com"], "broadcom": ["broadcom.com"], "sap": ["sap.com"],
    "samsung": ["samsung.com"], "zyxel": ["zyxel.com"], "d-link": ["dlink.com"], "qnap": ["qnap.com"],
    "synology": ["synology.com"], "juniper": ["juniper.net"], "f5": ["f5.com"], "atlassian": ["atlassian.com"],
    "progress": ["progress.com"], "sophos": ["sophos.com"], "trend": ["trendmicro.com"], "zimbra": ["zimbra.com"],
    "mitel": ["mitel.com"], "hewlett": ["hpe.com"], "hpe": ["hpe.com"], "dell": ["dell.com"], "lenovo": ["lenovo.com"],
    "ibm": ["ibm.com"], "schneider": ["se.com"], "abb": ["abb.com"], "siemens": ["siemens.com"],
    "huawei": ["huawei.com"], "hikvision": ["hikvision.com"], "netgear": ["netgear.com"], "tp-link": ["tp-link.com"],
    "veeam": ["veeam.com"], "solarwinds": ["solarwinds.com"], "connectwise": ["connectwise.com"],
    "gitlab": ["gitlab.com"], "apache": ["apache.org"], "cisco": ["cisco.com"], "palo": ["paloaltonetworks.com"],
    "red": ["redhat.com"], "linux": ["kernel.org"], "mozilla": ["mozilla.org"], "commvault": ["commvault.com"],
    "smartertools": ["smartertools.com"], "gladinet": ["gladinet.com"], "sitecore": ["sitecore.com"],
    "crushftp": ["crushftp.com"], "wazuh": ["wazuh.com"], "erlang": ["erlang.org"], "kentico": ["kentico.com"],
    "nakivo": ["nakivo.com"], "trimble": ["trimble.com"], "cleo": ["cleo.com"], "craft": ["craftcms.com"],
    "sysax": ["sysax.com"], "arcserve": ["arcserve.com"], "beyondtrust": ["beyondtrust.com"],
    "qualcomm": ["qualcomm.com"], "arm": ["arm.com"], "android": ["android.com", "google.com"],
    "rockwell": ["rockwellautomation.com"], "phoenix": ["phoenixcontact.com"], "bosch": ["bosch.com"],
    "netscaler": ["citrix.com", "cloud.com"], "watchguard": ["watchguard.com"], "sangoma": ["sangoma.com"],
}
DOCS_PER_PROVIDER = 2500
PAUSE = {"default": 0.3, "web.archive.org": 1.2}
_cache: dict = {}
_refused: Counter = Counter()
STATUS: dict = defaultdict(Counter)


def _get(url: str, text: bool = False, kind: str = "other"):
    if url in _cache:
        return _cache[url]
    host = urlparse(url).hostname or ""
    if _refused[host] >= 2:
        STATUS[kind]["skipped (host refused)"] += 1
        return None
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*"}, timeout=40)
        STATUS[kind][str(r.status_code)] += 1
        if r.status_code in (403, 429):
            _refused[host] += 1
        time.sleep(PAUSE.get(host, PAUSE["default"]))
        out = (r.text if text else r.json()) if r.ok else None
    except (requests.RequestException, ValueError) as e:
        STATUS[kind][type(e).__name__] += 1
        out = None
    _cache[url] = out
    return out


def _d(s) -> str:
    return str(s or "")[:10]


def vkey(vendor: str) -> str:
    return (vendor or "").lower().split()[0] if vendor else ""


# E: CSAF providers ---------------------------------------------------------------------------
def provider_urls(domains: set[str]) -> dict[str, str]:
    """domain -> provider-metadata URL, from the aggregator, security.txt and well-known paths."""
    found: dict[str, str] = {}
    agg = _get(AGGREGATOR, kind="csaf_aggregator") or {}
    for p in agg.get("csaf_providers") or []:
        meta = p.get("metadata") or {}
        url = meta.get("url") or ""
        host = urlparse(url).hostname or ""
        for d in domains:
            if host == d or host.endswith("." + d):
                found.setdefault(d, url)
    for d in sorted(domains - set(found)):
        for host in (d, "www." + d):
            t = _get(f"https://{host}/.well-known/security.txt", text=True, kind="security_txt")
            for line in (t or "").splitlines():
                if line.lower().startswith("csaf:"):
                    found.setdefault(d, line.split(":", 1)[1].strip())
            if d in found:
                break
            pm = _get(f"https://{host}/.well-known/csaf/provider-metadata.json", kind="csaf_wellknown")
            if isinstance(pm, dict) and pm.get("distributions"):
                found[d] = f"https://{host}/.well-known/csaf/provider-metadata.json"
                break
    return found


def index_provider(pm_url: str, since: str) -> tuple[dict, str]:
    """CVE -> (initial release date, fix-later flag, doc id) for documents changed since `since`."""
    pm = _get(pm_url, kind="csaf_metadata") or {}
    idx: dict = {}
    n = 0
    for dist in pm.get("distributions") or []:
        base = dist.get("directory_url")
        paths = []
        if base:
            t = _get(base.rstrip("/") + "/changes.csv", text=True, kind="csaf_changes") or ""
            paths = [base.rstrip("/") + "/" + r[0] for r in csv.reader(io.StringIO(t))
                     if len(r) >= 2 and r[1][:10] >= since]
        for feed in ((dist.get("rolie") or {}).get("feeds") or [])[:4]:
            j = _get(feed.get("url", ""), kind="csaf_rolie") or {}
            for e in (j.get("feed") or {}).get("entry") or []:
                if _d(e.get("updated") or e.get("published")) >= since:
                    paths += [ln.get("href", "") for ln in e.get("link") or [] if str(ln.get("href", "")).endswith(".json")]
        for url in list(dict.fromkeys(paths))[:DOCS_PER_PROVIDER - n]:
            n += 1
            doc = _get(url, kind="csaf_doc") or {}
            tr = (doc.get("document") or {}).get("tracking") or {}
            if not tr.get("initial_release_date"):
                continue
            hist = [h.get("summary", "") for h in tr.get("revision_history") or []]
            later = any(FIX_LATER.search(h or "") for h in hist[1:])
            for v in doc.get("vulnerabilities") or []:
                c = v.get("cve")
                if c and (c not in idx or _d(tr["initial_release_date"]) < idx[c][0]):
                    idx[c] = (_d(tr["initial_release_date"]), later, tr.get("id", ""))
    return idx, f"{n} documents read"


# F: release calendars ------------------------------------------------------------------------
def nth_weekday(y: int, m: int, weekday: int, n: int) -> dt.date:
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(weekday - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def calendar_day(vendor: str, date: str) -> str:
    """The vendor's scheduled release day nearest `date` if within 1 day, else ''."""
    if not date:
        return ""
    d = dt.date.fromisoformat(date)
    v = vkey(vendor)
    cands = []
    for mm in (d.month - 1, d.month, d.month + 1):
        y, m = d.year + (mm - 1) // 12, (mm - 1) % 12 + 1
        if v in ("microsoft", "adobe", "sap"):
            cands.append(nth_weekday(y, m, 1, 2))
        if v == "oracle" and m in (1, 4, 7, 10):
            cands.append(nth_weekday(y, m, 1, 3))
        if v == "android" or (v == "google" and "android" in vendor.lower()):
            cands.append(dt.date(y, m, 1))
    best = min(cands, key=lambda c: abs((c - d).days), default=None)
    return best.isoformat() if best and abs((best - d).days) <= 1 else ""


# G: Wayback first capture ---------------------------------------------------------------------
def first_capture(url: str) -> str:
    j = _get(CDX.format(u=quote(url, safe="")), kind="wayback_cdx")
    if isinstance(j, list) and len(j) > 1 and j[1]:
        ts = j[1][0]
        return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
    return ""


# ---------------------------------------------------------------------------------------------
def days(a: str, b: str) -> int | None:
    try:
        return (dt.date.fromisoformat(a) - dt.date.fromisoformat(b)).days
    except ValueError:
        return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-04-01"); ap.add_argument("--end", default="2026-10-31")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    kev = pd.DataFrame((_get(KEV_URL, kind="kev") or {}).get("vulnerabilities") or [])
    kev = kev[(kev["dateAdded"] >= a.start) & (kev["dateAdded"] <= a.end)]

    # E: providers for the vendors in this window
    vendors = {vkey(v) for v in kev["vendorProject"]}
    domains = {d for v in vendors for d in DOMAINS.get(v, [f"{v}.com"] if v.isalnum() else [])}
    providers = provider_urls(domains)
    since = (dt.date.fromisoformat(a.start) - dt.timedelta(days=400)).isoformat()
    csaf: dict = {}
    prov_note = {}
    for d, url in sorted(providers.items()):
        if url in prov_note:
            continue
        idx, note = index_provider(url, since)
        prov_note[url] = f"{d}: {note}, {len(idx)} CVEs indexed"
        for c, val in idx.items():
            if c not in csaf or val[0] < csaf[c][0]:
                csaf[c] = val

    rows = []
    for k in kev.itertuples():
        y, n = k.cveID.split("-")[1:]
        rec = _get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=k.cveID), kind="cve_record") or {}
        cna = (rec.get("containers") or {}).get("cna") or {}
        refs = cna.get("references") or []
        urls = [r.get("url", "") for r in refs]
        pub = _d((rec.get("cveMetadata") or {}).get("datePublished")) or k.dateAdded
        d0, src, flagged = prefill_exploited(k.cveID, urls, k.vendorProject, pub, _d(cna.get("datePublic")))
        base = bucket(src)
        e = csaf.get(k.cveID)
        vendor_date = d0 if base not in ("assumed", "CNA disclosure date") else (e[0] if e else "")
        cal = calendar_day(k.vendorProject, vendor_date or pub)
        tagged = [r.get("url", "") for r in refs if REF_TAGS & set(r.get("tags") or [])]
        caps = [c for c in (first_capture(u) for u in tagged[:3]) if c]
        g = min(caps) if caps else ""
        cands = [x for x in (d0 if base != "assumed" else "", e[0] if e else "", g) if x]
        best = min(cands) if cands else pub
        gap = days(k.dateAdded, best)
        rows.append({
            "cve_id": k.cveID, "vendor": k.vendorProject, "product": k.product, "kev_added": k.dateAdded,
            "published": pub, "baseline": base, "baseline_date": d0, "baseline_flagged": bool(flagged),
            "E_csaf_date": e[0] if e else "", "E_csaf_fix_later": bool(e and e[1]), "E_csaf_doc": e[2] if e else "",
            "F_calendar_day": cal, "G_wayback_first": g, "G_tagged_refs": len(tagged),
            "G_minus_baseline": days(g, d0) if g and base != "assumed" else None,
            "G_minus_published": days(g, pub) if g else None,
            "best_date": best, "kev_minus_best": gap,
            "near_line": gap is not None and gap <= 7,
        })
    df = pd.DataFrame(rows)
    df.to_csv(a.out / "fixdate_wide.csv", index=False)

    n = len(df)
    assumed = df["baseline"] == "assumed"
    weak = df["baseline"].isin(["assumed", "CNA disclosure date"])
    hand_now = assumed | df["baseline_flagged"] | (df["baseline"] == "CNA disclosure date")
    e_has, g_has, f_has = df["E_csaf_date"].astype(bool), df["G_wayback_first"].astype(bool), df["F_calendar_day"].astype(bool)
    L = [f"# Fix dates, wide probe: KEV additions {a.start} to {a.end}", "",
         f"Flaws: {n}. Today's pre-fill: real vendor or GitHub date {int((~weak).sum())}, "
         f"CNA disclosure date {int((df['baseline'] == 'CNA disclosure date').sum())}, assumed {int(assumed.sum())}. "
         f"Go to the hand check today: {int(hand_now.sum())}.", "",
         "## Baseline sources", ""]
    L += [f"- {s}: {c}" for s, c in df["baseline"].value_counts().items()]
    L += ["", "## E. CSAF found through the aggregator, security.txt and vendor domains", "",
          f"Providers found for this window's vendors: {len(providers)} of {len(domains)} domains tried.", ""]
    L += [f"- {v}" for v in prov_note.values()] or ["- none"]
    L += ["", f"Flaws dated by CSAF: {int(e_has.sum())}; of these, assumed or disclosure-only in the baseline: "
          f"{int((e_has & weak).sum())}; revision says fixed releases changed later: {int(df['E_csaf_fix_later'].sum())}.",
          "", "## F. Release calendars", "",
          f"Vendor date on the vendor's scheduled release day (within a day): {int(f_has.sum())} flaws."]
    for v, c in df[f_has]["vendor"].value_counts().items():
        tot = int((df["vendor"] == v).sum())
        L.append(f"- {v}: {c} of {tot}")
    gb = df["G_minus_baseline"].dropna()
    gp = df["G_minus_published"].dropna()
    L += ["", "## G. Wayback Machine first capture of advisory and patch links", "",
          f"Flaws with a tagged vendor-advisory/patch/release-notes link: {int((df['G_tagged_refs'] > 0).sum())}; "
          f"with a first capture: {int(g_has.sum())} (assumed in the baseline: {int((g_has & assumed).sum())}).",
          f"First capture minus the baseline's real date (days): median {gb.median() if len(gb) else 'n/a'}, "
          f"within 1 day {int((gb.abs() <= 1).sum())} of {len(gb)}, capture earlier by more than 1 day {int((gb < -1).sum())}.",
          f"First capture minus CVE publication (days): median {gp.median() if len(gp) else 'n/a'}, "
          f"before publication {int((gp < 0).sum())} of {len(gp)}.",
          "A capture is an upper bound: the page existed by then. A capture well before the suggested date "
          "means the suggested date is too late and needs a look.", "",
          "## H. Where checking matters (KEV addition date as a proxy for first exploitation)", "",
          f"Near the line (added before or within 7 days after the best candidate fix date): {int(df['near_line'].sum())} of {n}.",
          f"Added more than 30 days after it: {int((df['kev_minus_best'] > 30).sum())}.",
          f"Hand checks today: {int(hand_now.sum())}. If the full check went only to near-the-line flaws, "
          f"flagged revisions and flaws whose sources disagree by more than 1 day, it would be about "
          f"{int((df['near_line'] | df['baseline_flagged'] | df['E_csaf_fix_later'] | (df['G_minus_baseline'].fillna(0) < -1)).sum())}; "
          "the rest could be sampled. This is a sizing estimate, not a decision.", "",
          "## Still without any real date (no vendor, GitHub, CSAF or capture), by vendor", ""]
    left = df[assumed & ~e_has & ~g_has]["vendor"].value_counts()
    L += [f"- {v}: {c}" for v, c in left.items()] or ["- none"]
    L += ["", "## Requests", ""]
    L += [f"- {k}: " + ", ".join(f"{s} {c}" for s, c in v.most_common()) for k, v in STATUS.items()]
    L += ["", "Candidate dates are inputs to the hand check, never replacements for it. Research only."]
    (a.out / "summary.md").write_text("\n".join(L) + "\n")
    print(f"fix-date wide probe: {n} flaws checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
