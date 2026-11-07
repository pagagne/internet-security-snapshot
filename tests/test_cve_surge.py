"""The 2026 surge breakdown (author, 7 Nov 2026)."""
import pandas as pd
from snapshot.research import cve_surge as S


def test_breakdown_counts_and_sensitivity():
    rows = []
    for i in range(30):
        rows.append({"state": "PUBLISHED", "date_published": "2026-08-01T00:00:00Z", "cna": f"c{i % 7}",
                     "cvss_severity": "HIGH", "root_cause": "memory", "ai_credited": i == 0})
    rows.append({"state": "REJECTED", "date_published": "2026-08-01T00:00:00Z", "cna": "c0",
                 "cvss_severity": None, "root_cause": None, "ai_credited": False})
    rows.append({"state": "PUBLISHED", "date_published": "2024-02-01T00:00:00Z", "cna": "c1",
                 "cvss_severity": None, "root_cause": None, "ai_credited": False})
    R = S.breakdown(S.published(pd.DataFrame(rows)))
    assert R["total"] == {"2024Q1": 1, "2026Q3": 30}
    assert R["ai_credited"]["2026Q3"] == 1
    assert R["without_top5"]["2026Q3"]["without_top5"] == 30 - sum(sorted([5, 5, 4, 4, 4, 4, 4], reverse=True)[:5])
    assert "## By issuing CNA" in S.report(R, "test")
