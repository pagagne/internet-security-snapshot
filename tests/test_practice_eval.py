"""Practice evaluation on a tiny made-up bundle (1 Nov 2026)."""
import json

import pandas as pd

from snapshot.research import practice_eval as P


def test_practice_evaluation_runs(tmp_path, monkeypatch):
    b = tmp_path / "bundle"
    for d in ("cve", "kev"):
        (b / d).mkdir(parents=True)
    (b / "manifest.json").write_text(json.dumps({"quarter": "2026Q3", "run": "final", "files": []}))
    rows = []
    for i, (pub, state) in enumerate([("2026-07-05", "PUBLISHED"), ("2026-08-01", "PUBLISHED"),
                                      ("2025-08-01", "PUBLISHED"), ("2026-09-01", "REJECTED")]):
        rows.append({"cve_id": f"CVE-2026-{i}", "state": state, "date_published": pd.Timestamp(pub, tz="UTC"),
                     "credit_values": ["found with Claude"] if i == 0 else [], "credit_types": ["finder"] if i == 0 else [],
                     "ai_credit_terms": ["claude"] if i == 0 else [], "fix_links": [], "ref_links": [],
                     "ssvc_exploitation": None, "ssvc_timestamp": None})
    pd.DataFrame(rows).to_parquet(b / "cve/cve_records.parquet")
    pd.DataFrame([{"cve_id": "CVE-2026-0", "vendor": "Acme", "date_added": pd.Timestamp("2026-07-20", tz="UTC")},
                  {"cve_id": "CVE-2026-1", "vendor": "Acme", "date_added": pd.Timestamp("2026-08-03", tz="UTC")}]
                 ).to_parquet(b / "kev/kev_entries.parquet")
    monkeypatch.setattr(P, "prefill_exploited", lambda c, refs, v, pub, dp="": ("2026-07-10", "github fix commit", False))
    R, ev = P.evaluate(b, pause=0)
    assert R["kev_added_in_quarter"] == 2 and R["I5"]["published_by_year"][2026] == 2
    assert R["I8"]["ceiling"] == 1 and "not_computable" in R
    text = P.report(R)
    assert "Practice, not a result" in text and "I3." in text and len(ev) == 2
