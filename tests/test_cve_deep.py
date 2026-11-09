"""Deep dive behind the surge (author, 8 Nov 2026)."""
import pandas as pd
from snapshot.research import cve_deep as D


def test_checks_run_on_small_data():
    cve = pd.DataFrame([
        {"cve_id": "CVE-2026-0001", "state": "PUBLISHED", "date_published": "2026-07-02T00:00:00Z", "date_updated": "2026-07-02T00:00:00Z",
         "cna": "a", "cvss_base": 9.8, "has_cisa_adp": True, "ssvc_exploitation": "active"},
        {"cve_id": "CVE-2026-0002", "state": "PUBLISHED", "date_published": "2026-07-03T00:00:00Z", "date_updated": "2026-07-03T00:00:00Z",
         "cna": "a", "cvss_base": None, "has_cisa_adp": False, "ssvc_exploitation": None},
        {"cve_id": "CVE-2026-0003", "state": "REJECTED", "date_published": None, "date_updated": "2026-07-20T00:00:00Z",
         "cna": "b", "cvss_base": None, "has_cisa_adp": False, "ssvc_exploitation": None}])
    kev = pd.DataFrame([{"cve_id": "CVE-2026-0001", "list": "cisa", "date_added": "2026-07-12T00:00:00Z"}])
    nvd = pd.DataFrame([{"nvd_published": "2026-07-02T00:00:00Z", "nvd_status": "Deferred", "nvd_cvss31": None, "nvd_cvss40": None}])
    R = {"severity": D.severity_sources(cve), "rejected": D.rejected(cve), "kev": D.kev(kev, cve), "nvd": D.nvd_enrichment(nvd)}
    assert R["severity"]["2026-07"] == {"records": 2, "scored": 1, "no_score": 1, "cisa_enriched": 1, "ssvc_active": 1, "ssvc_poc": 0}
    assert R["rejected"]["largest_bursts"][0] == {"month": "2026-07", "cna": "b", "rejected": 1}
    assert R["kev"]["added_2026"]["median_days_publish_to_kev_same_year"] == 10.0
    assert R["nvd"]["2026-07"]["status"] == {"Deferred": 1}
    assert "## D. Exploited flaws" in D.report(R, "test")
