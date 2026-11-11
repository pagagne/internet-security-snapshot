"""VulnCheck KEV collector, private split and I6 (permission 11 Nov 2026)."""
import io
import json
import zipfile

import pandas as pd

from snapshot.collect import vulncheck
from snapshot import private, sources
from snapshot.research.practice_eval import i6_agreement


def _zip(records, as_dict=True):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("vulncheck-kev.json", json.dumps({"data": records} if as_dict else records))
    return buf.getvalue()


RECS = [
    {"cve": ["CVE-2026-0001"], "date_added": "2026-10-05T00:00:00Z", "cisa_date_added": "2026-10-09T00:00:00Z",
     "vulncheck_reported_exploitation": [{"url": "u", "date_added": "2026-10-04T00:00:00Z"}],
     "vulncheck_xdb": [{"xdb_id": "x", "date_added": "2026-10-03T00:00:00Z"}], "knownRansomwareCampaignUse": "Known"},
    {"cve": ["CVE-2026-0002", "cve-2026-0003"], "date_added": "2026-11-01T00:00:00Z"},
]


def test_records_and_table():
    for as_dict in (True, False):
        t = vulncheck.build_table(vulncheck.records(_zip(RECS, as_dict)))
        assert set(t["cve_id"]) == {"CVE-2026-0001", "CVE-2026-0002", "CVE-2026-0003"}
    r = t.set_index("cve_id").loc["CVE-2026-0001"]
    assert str(r["vc_first_reported"])[:10] == "2026-10-04" and r["vc_ransomware"]
    ex = vulncheck.exploit_rows(t)
    assert set(ex["source"]) == {"vulncheck_kev"} and ex.set_index("cve_id").loc["CVE-2026-0001", "date"] == "2026-10-05"


def test_raw_stays_private():
    s = sources.load()["vulncheck"]
    assert s["permission"] == "granted" and s["raw_public"] is False and s["pull"] == "vulncheck"
    assert "vulncheck" in private.private_pulls()


def test_i6_agreement():
    kev = pd.DataFrame({"cve_id": ["A", "B", "C"], "added": pd.to_datetime(["2026-10-10", "2026-11-01", "2026-08-01"])})
    vc = pd.DataFrame({"cve_id": ["A", "B", "D"], "vc_date_added": pd.to_datetime(["2026-10-05", "2026-11-03", "2026-12-01"], utc=True)})
    r = i6_agreement(kev, vc, pd.Timestamp("2026-10-01"), pd.Timestamp("2026-12-31"))
    assert r["n"] == 4 and r["on_both"] == 2 and r["on_cisa"] == 3 and r["on_vulncheck"] == 3
    assert r["median_days_vulncheck_before_cisa"] == 1.5 and r["share_vulncheck_first"] == 0.5
