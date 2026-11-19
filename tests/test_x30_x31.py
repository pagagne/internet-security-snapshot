"""X30 and X31 readings (19 Nov 2026): matching and per-quarter counts."""
import json

import pandas as pd

from snapshot.research import x30_x31 as X


def test_ai_match_uses_name_parts_and_summary():
    terms = {"openai", "langchain", "ai", "mcp"}
    assert X.ai_match("openai-helper", "Malicious code in openai-helper (PyPI)", terms) == ["openai"]
    assert X.ai_match("mail-utils", "Malicious code in mail-utils (npm)", terms) == []     # 'ai' inside a word
    assert X.ai_match("@scope/mcp-server-x", "", terms) == ["mcp"]
    assert X.ai_match("x", "Impersonates the langchain package", terms) == ["langchain"]


def test_scan_and_summarise(tmp_path):
    d = tmp_path / "osv/malicious/npm/a"; d.mkdir(parents=True)
    (d / "MAL-1.json").write_text(json.dumps({"id": "MAL-1", "published": "2026-08-01T00:00:00Z", "summary": "x",
                                               "affected": [{"package": {"name": "openai-sdk-fake"}}]}))
    (d / "MAL-2.json").write_text(json.dumps({"id": "MAL-2", "published": "2026-08-02T00:00:00Z", "summary": "y",
                                               "affected": [{"package": {"name": "lodash-x"}}]}))
    mal = X.malicious_rows(tmp_path, {"openai"})
    c = tmp_path / "cves/2026/1xxx"; c.mkdir(parents=True)
    (c / "CVE-2026-1.json").write_text(json.dumps({"cveMetadata": {"cveId": "CVE-2026-1", "state": "REJECTED",
        "dateRejected": "2026-08-03T00:00:00Z"}, "containers": {"cna": {"rejectedReasons": [{"value": "AI-generated report, not a vulnerability."}]}}}))
    (c / "CVE-2026-2.json").write_text(json.dumps({"cveMetadata": {"cveId": "CVE-2026-2", "state": "PUBLISHED",
        "datePublished": "2026-08-04T00:00:00Z"}, "containers": {"cna": {"tags": ["disputed"]}}}))
    cves = X.cve_rows(tmp_path)
    S = X.summarise(mal, cves)
    assert S["x30"]["2026Q3 npm"] == {"all": 2, "ai": 1}
    assert S["x31"]["2026Q3 rejected"] == {"n": 1, "ai_reason": 1}
    assert S["x31"]["2026Q3 disputed"] == {"n": 1, "ai_reason": 0}
