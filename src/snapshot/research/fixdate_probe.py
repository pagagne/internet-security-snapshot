"""Research probe (RESEARCH_PLAN.md item 1): which free, machine-readable sources can date
the fix for CVEs first exploited in a period?

For every CVE added to CISA KEV between --start and --end, tries:
  github     current pre-fill (release / advisory / commit links in the CVE record)
  msrc       Microsoft Security Update Guide API (releaseDate)
  cisco      Cisco CSAF advisory (initial release date; whether any product is "fixed")
  paloalto   Palo Alto Networks advisory JSON (CVE JSON 5: datePublic, timeline)
  fortinet   Fortinet PSIRT CSAF/CVRF (candidate URLs; status codes recorded)
  datepublic the CNA's datePublic in the CVE record (vendor's public disclosure date)
and writes one row per CVE plus a coverage summary. Research only: nothing here feeds the
locked measures until a decision says so.

Runs in GitHub Actions (vendor sites are not reachable from the authoring sandbox).
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA
from ..fixdates import prefill

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
CVE_RAW = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{y}/{b}/{c}.json"
CISCO_SA = re.compile(r"(cisco-sa-[\w-]+)")
FORTI = re.compile(r"(FG-IR-\d{2}-\d+)", re.I)

SAMPLES: dict[str, str] = {}
STATUS: dict[str, dict[str, int]] = {}


def _get(url: str, kind: str, accept="application/json"):
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Accept": accept}, timeout=40)
    except requests.RequestException as e:
        STATUS.setdefault(kind, {}).setdefault(type(e).__name__, 0)
        STATUS[kind][type(e).__name__] += 1
        return None
    STATUS.setdefault(kind, {}).setdefault(str(r.status_code), 0)
    STATUS[kind][str(r.status_code)] += 1
    time.sleep(0.3)
    if r.ok and kind not in SAMPLES:
        SAMPLES[kind] = r.text[:20000]
    return r if r.ok else None


def _json(r):
    try:
        return r.json() if r is not None else None
    except ValueError:
        return None


def cve_record(c: str) -> dict | None:
    y, n = c.split("-")[1:]
    return _json(_get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=c), "cve_record"))


def msrc(c: str) -> dict:
    out = {}
    j = _json(_get("https://api.msrc.microsoft.com/sug/v2.0/en-US/vulnerability?$filter=cveNumber eq '%s'" % c, "msrc_sug"))
    v = (j or {}).get("value") or []
    if v:
        out["msrc_release"] = (v[0].get("releaseDate") or "")[:10]
    j = _json(_get(f"https://api.msrc.microsoft.com/cvrf/v3.0/updates('{c}')", "msrc_cvrf"))
    v = (j or {}).get("value") or []
    if v:
        out["msrc_cvrf_doc"] = v[0].get("ID", "")
        out["msrc_cvrf_initial"] = (v[0].get("InitialReleaseDate") or "")[:10]
    return out


def cisco(sa: str) -> dict:
    j = _json(_get(f"https://sec.cloudapps.cisco.com/security/center/contentjson/CiscoSecurityAdvisory/{sa}/csaf/{sa}.json", "cisco_csaf"))
    if not j:
        return {}
    tr = (j.get("document") or {}).get("tracking") or {}
    hist = tr.get("revision_history") or []
    fixed = any("fixed" in (v.get("product_status") or {}) for v in j.get("vulnerabilities") or [])
    rem = [r.get("category") for v in j.get("vulnerabilities") or [] for r in v.get("remediations") or []]
    return {"cisco_initial": (tr.get("initial_release_date") or "")[:10], "cisco_revisions": len(hist),
            "cisco_fixed_status": fixed, "cisco_vendor_fix": "vendor_fix" in rem,
            "cisco_history": " | ".join(f"{(h.get('date') or '')[:10]} {h.get('summary', '')[:60]}" for h in hist[:6])}


def paloalto(c: str) -> dict:
    j = _json(_get(f"https://security.paloaltonetworks.com/json/{c}", "paloalto"))
    if not j:
        return {}
    cna = (j.get("containers") or {}).get("cna") or {}
    tl = cna.get("timeline") or []
    return {"pan_datepublic": (cna.get("datePublic") or "")[:10],
            "pan_timeline": " | ".join(f"{(t.get('time') or '')[:10]} {t.get('value', '')[:60]}" for t in tl[:6])}


def fortinet(fg: str) -> dict:
    fg = fg.upper()
    for kind, url in (("forti_csaf", f"https://filestore.fortinet.com/fortiguard/psirt/csaf_{fg.lower()}.json"),
                      ("forti_csaf2", f"https://fortiguard.fortinet.com/psirt/csaf/{fg}"),
                      ("forti_cvrf", f"https://filestore.fortinet.com/fortiguard/psirt/cvrf_{fg.lower()}.xml"),
                      ("forti_page", f"https://fortiguard.fortinet.com/psirt/{fg}")):
        r = _get(url, kind, accept="*/*")
        if r is None:
            continue
        j = _json(r)
        if j and "document" in j:
            return {"forti_initial": ((j["document"].get("tracking") or {}).get("initial_release_date") or "")[:10], "forti_src": kind}
        m = re.search(r"(?:Published|InitialReleaseDate)[^0-9]{0,40}(\d{4}-\d{2}-\d{2})", r.text)
        if m:
            return {"forti_initial": m.group(1), "forti_src": kind}
    return {}


def probe(start: str, end: str) -> pd.DataFrame:
    kev = pd.DataFrame(requests.get(KEV_URL, headers={"User-Agent": UA}, timeout=60).json()["vulnerabilities"])
    kev["added"] = pd.to_datetime(kev["dateAdded"])
    kev = kev[(kev["added"] >= start) & (kev["added"] <= end)]
    rows = []
    for k in kev.itertuples():
        c = k.cveID
        rec = cve_record(c) or {}
        meta, cna = rec.get("cveMetadata") or {}, (rec.get("containers") or {}).get("cna") or {}
        refs = [r.get("url", "") for r in cna.get("references") or []]
        tags = {t for r in cna.get("references") or [] for t in r.get("tags") or []}
        pub = (meta.get("datePublished") or "")[:10]
        gh, gh_src = prefill(refs, pub or "0000-00-00")
        row = {"cve_id": c, "vendor": k.vendorProject, "product": k.product, "kev_added": k.dateAdded,
               "published": pub, "assigner": meta.get("assignerShortName", ""),
               "datepublic": (cna.get("datePublic") or "")[:10],
               "has_patch_ref": "patch" in tags, "has_vendor_adv_ref": "vendor-advisory" in tags,
               "github": gh if not gh_src.startswith("ASSUMED") else "", "github_src": gh_src if not gh_src.startswith("ASSUMED") else ""}
        v, a = (k.vendorProject or "").lower(), " ".join(refs).lower()
        if "microsoft" in v or "msrc.microsoft.com" in a:
            row.update(msrc(c))
        if m := CISCO_SA.search(" ".join(refs)):
            row["cisco_sa"] = m.group(1); row.update(cisco(m.group(1)))
        if "palo alto" in v or "paloaltonetworks" in a:
            row.update(paloalto(c))
        if m := FORTI.search(" ".join(refs)):
            row["fortinet_id"] = m.group(1); row.update(fortinet(m.group(1)))
        rows.append(row)
    return pd.DataFrame(rows)


def summarize(d: pd.DataFrame) -> str:
    def has(col):
        return int(d[col].fillna("").astype(str).str.len().gt(0).sum()) if col in d else 0
    n = len(d)
    vendor_cols = ["msrc_release", "msrc_cvrf_initial", "cisco_initial", "pan_datepublic", "forti_initial"]
    d = d.copy()
    d["any_vendor"] = d[[c for c in vendor_cols if c in d]].fillna("").astype(str).apply(lambda r: any(r), axis=1) if any(c in d for c in vendor_cols) else False
    d["any_source"] = d["any_vendor"] | d["github"].fillna("").astype(str).str.len().gt(0)
    L = ["# Fix-date source probe", "", f"KEV additions probed: {n} (with a CVE record: {has('published')})", "",
         "| Source | CVEs dated |", "|---|---|",
         f"| GitHub links (current pre-fill) | {has('github')} |",
         f"| Microsoft Update Guide API | {has('msrc_release')} |",
         f"| Microsoft CVRF | {has('msrc_cvrf_initial')} |",
         f"| Cisco CSAF | {has('cisco_initial')} |",
         f"| Palo Alto JSON | {has('pan_datepublic') + has('pan_timeline')} |",
         f"| Fortinet | {has('forti_initial')} |",
         f"| CNA datePublic (disclosure, not fix) | {has('datepublic')} |",
         f"| **Any fix-date source (GitHub or vendor)** | **{int(d['any_source'].sum())}** |", "",
         "## Differences from CVE publication (days, vendor date minus publication)", ""]
    pub = pd.to_datetime(d["published"], errors="coerce")
    for col in ["github", "msrc_release", "cisco_initial", "pan_datepublic", "forti_initial", "datepublic"]:
        if col in d:
            x = (pd.to_datetime(d[col], errors="coerce") - pub).dt.days.dropna()
            if len(x):
                L.append(f"- {col}: n={len(x)}, same day {int((x == 0).sum())}, earlier {int((x < 0).sum())}, later {int((x > 0).sum())}, range {int(x.min())} to {int(x.max())}")
    if "cisco_fixed_status" in d:
        cs = d[d["cisco_initial"].fillna("").astype(str).str.len() > 0]
        L += ["", f"Cisco advisories listing a fixed release: {int(cs['cisco_fixed_status'].fillna(False).astype(bool).sum())} of {len(cs)}"]
    L += ["", "## HTTP status counts per source", "", "```", json.dumps(STATUS, indent=1), "```",
          "", "## Top vendors without any fix-date source", ""]
    miss = d[~d["any_source"]]["vendor"].value_counts().head(15)
    L += [f"- {v}: {c}" for v, c in miss.items()]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", default="2026-04-01")
    ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", type=Path, default=Path("research-out"))
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d = probe(a.start, a.end)
    d.to_csv(a.out / "fixdate_probe.csv", index=False)
    (a.out / "fixdate_probe.md").write_text(summarize(d))
    (a.out / "samples").mkdir(exist_ok=True)
    for k, t in SAMPLES.items():
        (a.out / "samples" / f"{k}.txt").write_text(t)
    print((a.out / "fixdate_probe.md").read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
