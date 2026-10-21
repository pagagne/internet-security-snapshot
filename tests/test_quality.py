import json
from pathlib import Path

import pandas as pd

from snapshot.collect import cve, ransomware
from snapshot.quality import build

FIX = Path(__file__).parent / "fixtures" / "cves"


def test_quality_report_on_small_bundle(tmp_path):
    b = tmp_path / "2026Q2" / "dry-run"
    (b / "cve").mkdir(parents=True)
    (b / "ransomware").mkdir()
    rows = [cve.parse_record(json.loads(p.read_text())) for p in FIX.glob("*.json")]
    df = pd.DataFrame(rows)
    df["ai_credited"] = df["ai_credit_terms"].map(bool)
    df.to_parquet(b / "cve/cve_records.parquet", index=False)
    ransomware.aggregate([{"victim": "x", "group": "g", "country": "", "activity": "unknown"}], 2026, 5).to_parquet(
        b / "ransomware/ransomware_counts.parquet", index=False)
    (b / "manifest.json").write_text(json.dumps({"quarter": "2026Q2", "run": "dry-run", "files": [
        {"source": "cve_org", "status": "ok", "note": ""}, {"source": "sec_edgar", "status": "gap", "note": "no key"}]}))
    md, metrics = build(b)
    assert "## 1. Sources" in md and "## 8. Ransomware" in md
    assert metrics["gaps"] == ["sec_edgar"]
    assert "x" not in md.split("## 8.")[1].split("postings")[0].replace("2026-05", "")
