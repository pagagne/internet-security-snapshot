"""Research probe (27-29 Oct 2026): the global sources for X19-X22 and X12.

Second round (29 Oct, the author's go-ahead of 28 Oct to refine now rather than on 12 Nov):
X21 added (Radar by continent, ransomware.live country coverage, counts only), moved
addresses retried, archive sources for the X19 feeds (a rolling feed has no history), and
for every text response the number of distinct CVE IDs and of data-file links found.

Asked by the author on 26 Oct (docs/INQUIRIES.md): can each source be read, dated and used?
For every candidate address it records the HTTP status, type, size and a short scrubbed sample
(IP and e-mail addresses removed), so the 12 Nov decisions (#3-8) rest on what the sources
actually return. Several addresses are tried per source because feed locations move; a 404 on
one is not a verdict on the source. Terms pages are fetched too, for docs/PERMISSIONS.md.
Nothing here feeds any measure. Requests are 1 s apart and name the study.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

import requests

from ..collect.http import UA, note_status
from .source_scout import scrub

SOURCES = {
    # X19: other countries' active-exploitation alerts
    "x19_certfr_alerts_rss": "https://www.cert.ssi.gouv.fr/alerte/feed/",
    "x19_certfr_advisories_rss": "https://www.cert.ssi.gouv.fr/avis/feed/",
    "x19_certfr_terms": "https://www.cert.ssi.gouv.fr/mentions-legales/",
    "x19_jpcert_rss_ja": "https://www.jpcert.or.jp/rss/jpcert.rdf",
    "x19_jpcert_rss_en": "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf",
    "x19_jpcert_alerts_page": "https://www.jpcert.or.jp/at/2026.html",
    "x19_bsi_wid_rss": "https://wid.cert-bund.de/content/public/securityAdvisory/rss",
    "x19_bsi_wid_page": "https://wid.cert-bund.de/portal/wid/kurzinformationen",
    "x19_krcert_notices_rss": "https://www.boho.or.kr/kr/rss.do?bbsId=B0000133",
    "x19_krcert_knvd": "https://knvd.krcert.or.kr/securityNotice.do",
    # round 2: history for the rolling feeds, and moved addresses
    "x19_certfr_alert_archive": "https://www.cert.ssi.gouv.fr/alerte/",
    "x19_certfr_alert_json": "https://www.cert.ssi.gouv.fr/alerte/CERTFR-2024-ALE-001/json/",
    "x19_jpcert_alerts_2025": "https://www.jpcert.or.jp/at/2025.html",
    "x19_jpcert_alerts_2024": "https://www.jpcert.or.jp/at/2024.html",
    "x19_bsi_wid_api": "https://wid.cert-bund.de/portal/api/securityadvisory?size=5&sort=published,desc",
    "x19_krcert_knvd_root": "https://knvd.krcert.or.kr/",
    "x19_jpcert_terms_ja": "https://www.jpcert.or.jp/policy.html",
    "x19_jpcert_terms_en": "https://www.jpcert.or.jp/english/policy.html",
    # X20: DNSSEC validation and RPKI route checking by country
    "x20_apnic_dnssec_world": "https://stats.labs.apnic.net/dnssec/XA",
    "x20_apnic_rpki_world": "https://stats.labs.apnic.net/rpki/XA",
    "x20_ripestat_country_resources": "https://stat.ripe.net/data/country-resource-list/data.json?resource=fr",
    "x20_ripestat_terms": "https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripestat-terms-of-service/",
    "x20_nist_rpki_monitor": "https://rpki-monitor.antd.nist.gov/",
    "x20_apnic_dnssec_fr": "https://stats.labs.apnic.net/dnssec/FR",
    "x20_apnic_rpki_fr": "https://stats.labs.apnic.net/rpki/FR",
    "x20_apnic_dnssec_jp": "https://stats.labs.apnic.net/dnssec/JP",
    "x20_apnic_labs_home": "https://labs.apnic.net/",
    "x20_ripestat_terms_2": "https://www.ripe.net/about-us/legal/ripestat-service-terms-and-conditions/",
    # X22: breach notifications outside the US
    "x22_uk_ico_trends": "https://ico.org.uk/action-weve-taken/data-security-incident-trends/",
    "x22_au_oaic_ndb": "https://www.oaic.gov.au/privacy/notifiable-data-breaches/notifiable-data-breaches-publications",
    "x22_sg_pdpc_decisions": "https://www.pdpc.gov.sg/organisations/regulations-and-decisions",
    "x22_enisa_incidents": "https://www.enisa.europa.eu/topics/incident-reporting",
    "x22_enisa_threats": "https://www.enisa.europa.eu/topics/state-of-cybersecurity-in-the-eu/threats-and-incidents",
    "x22_sg_pdpc_landscape": "https://www.pdpc.gov.sg/help-and-resources/2025/04/singapore-data-breach-landscape-20232024",
    # X12: open-weight model releases and the "capable" bar
    "x12_hf_deepseek": "https://huggingface.co/api/models?author=deepseek-ai&sort=createdAt&direction=-1&limit=20",
    "x12_hf_qwen": "https://huggingface.co/api/models?author=Qwen&sort=createdAt&direction=-1&limit=20",
    "x12_hf_meta": "https://huggingface.co/api/models?author=meta-llama&sort=createdAt&direction=-1&limit=20",
    "x12_hf_mistral": "https://huggingface.co/api/models?author=mistralai&sort=createdAt&direction=-1&limit=20",
    "x12_epoch_models_csv": "https://epoch.ai/data/all_ai_models.csv",
    "x12_epoch_notable_csv": "https://epoch.ai/data/notable_ai_models.csv",
    "x12_epoch_benchmarks": "https://epoch.ai/data/benchmark_data.zip",
}


CVE_RE = re.compile(rb"CVE-\d{4}-\d{4,}")
DATA_LINK_RE = re.compile(r'href="([^"]+\.(?:csv|xlsx?|json|zip|pdf|ods))"', re.I)
RADAR = "https://api.cloudflare.com/client/v4/radar"
CONTINENTS = ["AF", "AS", "EU", "NA", "OC", "SA"]


def _radar_token() -> str | None:
    raw = os.environ.get("CLOUDFLARE_TOKEN") or ""
    for cand in (line.strip() for line in raw.splitlines()):
        if not cand:
            continue
        r = requests.get(RADAR + "/http/summary/bot_class", params={"dateRange": "7d", "format": "json"},
                         headers={"Authorization": f"Bearer {cand}", "User-Agent": UA}, timeout=60)
        if r.ok:
            return cand
    return None


def x21_radar() -> dict:
    """Can the attack and bot series be split by continent? Point counts only, no values."""
    token = _radar_token()
    if not token:
        return {"error": "no working CLOUDFLARE_TOKEN"}
    out = {}
    for series, path in {"attacks_layer7": "/attacks/layer7/timeseries",
                         "bot_class": "/http/timeseries_groups/bot_class"}.items():
        for c in CONTINENTS:
            time.sleep(1.0)
            r = requests.get(RADAR + path, params={"dateRange": "52w", "aggInterval": "1w",
                                                   "continent": c, "format": "json"},
                             headers={"Authorization": f"Bearer {token}", "User-Agent": UA}, timeout=60)
            entry = {"status": r.status_code}
            try:
                res = r.json().get("result", {})
                ser = next((v for k, v in res.items() if k != "meta" and isinstance(v, dict)), {})
                entry["points"] = len(ser.get("timestamps", []))
            except (ValueError, AttributeError):
                pass
            out[f"{series}_{c}"] = entry
    return out


def x21_ransomware() -> dict:
    """Is the victim country filled in often enough for regional splits? One month, counts only.

    Uses the permitted api-pro endpoint through the existing collector, which reduces the list to
    counts in memory; nothing but these three numbers is written.
    """
    from ..collect import ransomware
    try:
        agg = ransomware.aggregate(ransomware._month_list(2026, 9), 2026, 9)
    except Exception as e:  # noqa: BLE001
        return {"error": repr(e)[:200]}
    total = int(agg.loc[agg.dimension == "all", "count"].sum())
    c = agg[agg.dimension == "country"]
    unknown = int(c.loc[c.value.isin(["UNKNOWN", ""]), "count"].sum())
    return {"month": "2026-09", "postings": total, "country_known_share": round(1 - unknown / total, 3) if total else None,
            "distinct_countries": int((~c.value.isin(["UNKNOWN", ""])).sum()), "credit": ransomware.CREDIT}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for i, (name, url) in enumerate(SOURCES.items()):
        if i:
            time.sleep(1.0)
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Accept": "*/*"}, timeout=90)
            note_status(url, r.status_code)
            body = r.content
            text = body[:200_000].decode("utf-8", "replace")
            summary[name] = {"url": url, "status": r.status_code, "bytes": len(body),
                             "content_type": r.headers.get("content-type", ""),
                             "last_modified": r.headers.get("last-modified", ""),
                             "lines": body.count(b"\n"),
                             "distinct_cves": len(set(CVE_RE.findall(body)))}
            links = DATA_LINK_RE.findall(body.decode("utf-8", "replace"))
            if links and not name.startswith("x12_"):
                summary[name]["data_links"] = sorted(set(links))[:20]
            if name.startswith("x12_hf_") and r.ok:
                try:
                    models = r.json()
                    summary[name]["models"] = [
                        {"id": m.get("id"), "created": (m.get("createdAt") or "")[:10],
                         "pipeline": m.get("pipeline_tag")} for m in models]
                except ValueError:
                    pass
            if not url.endswith(".zip"):
                (a.out / f"{name}.sample.txt").write_text(scrub("\n".join(text.splitlines()[:80]))[:15000])
        except Exception as e:  # noqa: BLE001 - record and continue
            summary[name] = {"url": url, "error": repr(e)[:300]}
    summary["x21_radar_by_continent"] = x21_radar()
    summary["x21_ransomware_country_coverage"] = x21_ransomware()
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1))
    ok = sum(1 for v in summary.values() if v.get("status") == 200)
    summary_x21 = {k: summary[k] for k in ("x21_radar_by_continent", "x21_ransomware_country_coverage")}
    print(json.dumps(summary_x21, indent=1))
    print(f"{ok} of {len(summary)} addresses answered 200")
    print(json.dumps({k: v.get("status", v.get("error")) for k, v in summary.items()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
