import json
from pathlib import Path

from snapshot.collect import cve, nvd, ransomware
from snapshot.collect.epss import _keep
import pandas as pd

FIX = Path(__file__).parent / "fixtures" / "cves"


def test_vulnrichment_ssvc_from_cve_record():
    row = cve.parse_record(json.loads((FIX / "CVE-2026-45005.json").read_text()))
    assert row["ssvc_exploitation"] == "none"
    assert row["ssvc_automatable"] == "no"
    assert row["ssvc_technical_impact"] == "partial"
    assert row["ssvc_timestamp"].year == 2026


def test_ransomware_aggregate_drops_names():
    victims = [
        {"victim": "Acme Corp", "group": "akira", "country": "us", "activity": "Manufacturing", "domain": "acme.example"},
        {"victim": "Acme Corp", "group": "akira", "country": "us", "activity": "Manufacturing"},  # repost
        {"victim": "Beta GmbH", "group": "qilin", "country": "de", "activity": "Healthcare"},
    ]
    agg = ransomware.aggregate(victims, 2026, 9)
    assert set(agg.columns) == {"month", "dimension", "value", "count"}
    assert int(agg.query("dimension == 'all'")["count"].iloc[0]) == 2
    text = agg.to_csv()
    assert "Acme" not in text and "Beta" not in text and "acme.example" not in text


def test_nvd_parse():
    v = {"cve": {"id": "CVE-2026-1", "published": "2026-07-01T00:00:00.000", "lastModified": "x", "vulnStatus": "Analyzed",
                 "metrics": {"cvssMetricV31": [{"type": "Primary", "cvssData": {"baseScore": 9.8}}]},
                 "weaknesses": [{"description": [{"value": "CWE-787"}, {"value": "NVD-CWE-noinfo"}]}],
                 "configurations": [{"nodes": [{"cpeMatch": [{"vulnerable": True, "criteria": "cpe:2.3:o:fortinet:fortios:7.0:*:*:*:*:*:*:*"}]}]}],
                 "cisaExploitAdd": "2026-07-03"}}
    row = nvd.parse(v)
    assert row["nvd_cvss31"] == 9.8 and row["nvd_cwe_ids"] == ["CWE-787"]
    assert row["nvd_products"] == ["fortinet|fortios"] and row["nvd_kev_added"] == "2026-07-03"


def test_epss_keeps_recent_ids():
    df = pd.DataFrame({"cve": ["CVE-2019-1", "CVE-2025-2", "CVE-2026-3"]})
    assert list(_keep(df, 2025)["cve"]) == ["CVE-2025-2", "CVE-2026-3"]
