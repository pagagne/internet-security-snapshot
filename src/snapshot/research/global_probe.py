"""Research probe (27-28 Oct 2026): the global sources for X19-X22 and X12.

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
    # X20: DNSSEC validation and RPKI route checking by country
    "x20_apnic_dnssec_world": "https://stats.labs.apnic.net/dnssec/XA",
    "x20_apnic_rpki_world": "https://stats.labs.apnic.net/rpki/XA",
    "x20_ripestat_country_resources": "https://stat.ripe.net/data/country-resource-list/data.json?resource=fr",
    "x20_ripestat_terms": "https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripestat-terms-of-service/",
    "x20_nist_rpki_monitor": "https://rpki-monitor.antd.nist.gov/",
    # X22: breach notifications outside the US
    "x22_uk_ico_trends": "https://ico.org.uk/action-weve-taken/data-security-incident-trends/",
    "x22_au_oaic_ndb": "https://www.oaic.gov.au/privacy/notifiable-data-breaches/notifiable-data-breaches-publications",
    "x22_sg_pdpc_decisions": "https://www.pdpc.gov.sg/organisations/regulations-and-decisions",
    "x22_enisa_incidents": "https://www.enisa.europa.eu/topics/incident-reporting",
    # X12: open-weight model releases and the "capable" bar
    "x12_hf_deepseek": "https://huggingface.co/api/models?author=deepseek-ai&sort=createdAt&direction=-1&limit=20",
    "x12_hf_qwen": "https://huggingface.co/api/models?author=Qwen&sort=createdAt&direction=-1&limit=20",
    "x12_hf_meta": "https://huggingface.co/api/models?author=meta-llama&sort=createdAt&direction=-1&limit=20",
    "x12_hf_mistral": "https://huggingface.co/api/models?author=mistralai&sort=createdAt&direction=-1&limit=20",
    "x12_epoch_models_csv": "https://epoch.ai/data/all_ai_models.csv",
    "x12_epoch_notable_csv": "https://epoch.ai/data/notable_ai_models.csv",
    "x12_epoch_benchmarks": "https://epoch.ai/data/benchmark_data.zip",
}


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
                             "lines": body.count(b"\n")}
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
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1))
    ok = sum(1 for v in summary.values() if v.get("status") == 200)
    print(f"{ok} of {len(summary)} addresses answered 200")
    print(json.dumps({k: v.get("status", v.get("error")) for k, v in summary.items()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
