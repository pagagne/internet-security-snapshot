"""Race list in the pull's review list (1 Nov 2026 quality-check finding)."""
import pandas as pd

from snapshot import fixdates, review


def test_race_rows_cover_every_kev_addition_in_quarter(monkeypatch):
    seen = {}

    def fake(cve_id, refs, vendor, published, date_public=""):
        seen[cve_id] = (refs, vendor, published, date_public)
        return ("2026-07-01", "vendor disclosure date (CVE datePublic); fix date not stated", True)
    monkeypatch.setattr(fixdates, "prefill_exploited", fake)
    cve = pd.DataFrame({"cve_id": ["CVE-2026-1", "CVE-2026-2"],
                        "date_published": pd.to_datetime(["2026-06-30", "2026-08-01"], utc=True),
                        "date_public": pd.to_datetime(["2026-06-29", None], utc=True),
                        "fix_links": [["https://a"], []], "ref_links": [["https://b"], None]})
    kev = pd.DataFrame({"cve_id": ["CVE-2026-1", "CVE-2026-2", "CVE-2026-3"], "vendor": ["Acme", "Beta", "Old"],
                        "product": ["Gate", "App", "X"], "date_added": ["2026-07-03", "2026-09-30", "2026-06-30"]})
    rows = review.race_rows(cve, kev, "2026Q3", pause=0)
    assert [r["cve_id"] for r in rows] == ["CVE-2026-1", "CVE-2026-2"]          # Q3 additions only
    assert all(r["slot"] == "race" and r["task"] == "patch_date" for r in rows)
    assert seen["CVE-2026-1"] == (["https://a", "https://b"], "Acme", "2026-06-30", "2026-06-29")
    assert seen["CVE-2026-2"][3] == ""                                          # no disclosure date
    assert "attacked by 2026-07-03" in rows[0]["question"] and rows[0]["patch_date"] == "2026-07-01"


def test_evaluate_module_imports():
    from snapshot import evaluate
    assert callable(evaluate.main)
