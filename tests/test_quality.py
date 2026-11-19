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


def test_drift_flags():
    from snapshot.quality import drift_section
    cur = {"quarter": "2026Q3", "run": "dry-run", "gaps": ["radar"],
           "counts": {"nvd/nvd_cves.parquet": 100}, "fields": {"kev/kev_entries.parquet": {"vendor": "missing"}}}
    prev = {"quarter": "2026Q3", "run": "dry-run", "gaps": [], "counts": {"nvd/nvd_cves.parquet": 1000}}
    text = "\n".join(drift_section(cur, prev))
    assert "field `vendor` is missing" in text and "100 rows vs 1,000" in text and "radar: gap this run" in text
    assert "No drift flagged" in "\n".join(drift_section({"counts": {}, "fields": {}, "gaps": []}, None))


def test_row_count_history_check(tmp_path):
    """R9 / W1: zero rows, or below half the last four quarters' average, means hold the release."""
    from snapshot.quality import history_section, load_history
    hist = [
        {"quarter": "2026Q1", "run": "final", "counts": {"kev/kev_entries.parquet": 1000, "nvd/nvd_cves.parquet": 400}},
        {"quarter": "2026Q2", "run": "final", "counts": {"kev/kev_entries.parquet": 1100, "nvd/nvd_cves.parquet": 400}},
        {"quarter": "2026Q2", "run": "dry-run", "counts": {"kev/kev_entries.parquet": 1, "nvd/nvd_cves.parquet": 1}},
        {"quarter": "2026Q3", "run": "dry-run", "counts": {"kev/kev_entries.parquet": 1200}},
        {"quarter": "2026Q4", "run": "dry-run", "counts": {"kev/kev_entries.parquet": 5}},   # same quarter: ignored
    ]
    cur = {"quarter": "2026Q4", "window_fraction": 0.5,
           "counts": {"kev/kev_entries.parquet": 1150, "nvd/nvd_cves.parquet": 90, "sec/sec_8k_item105.parquet": 0}}
    text = "\n".join(history_section(cur, hist))
    assert cur["history_quarters"] == ["2026Q1", "2026Q2", "2026Q3"]
    # nvd: average 400 (the final run outranks the dry run), prorated to 200; 90 < 100 -> hold
    assert cur["hold_release"] and any(f.startswith("nvd/") for f in cur["history_flags"])
    assert not any(f.startswith("kev/") for f in cur["history_flags"])          # 1150 vs 1100
    assert "no history" in text                                                # sec has none
    # zero rows against a positive history always holds, whatever the size
    small = {"quarter": "2026Q4", "counts": {"sec/sec_8k_item105.parquet": 0}}
    history_section(small, [{"quarter": "2026Q3", "run": "final", "counts": {"sec/sec_8k_item105.parquet": 3}}])
    assert small["hold_release"]
    # a small history below the floor is not flagged for a dip
    dip = {"quarter": "2026Q4", "counts": {"sec/sec_8k_item105.parquet": 2}}
    history_section(dip, [{"quarter": "2026Q3", "run": "final", "counts": {"sec/sec_8k_item105.parquet": 10}}])
    assert not dip["hold_release"]
    # no history at all: said plainly, no hold
    none = {"quarter": "2026Q4", "counts": {"kev/kev_entries.parquet": 1}}
    assert "No earlier quarter" in "\n".join(history_section(none, []))
    assert not none["hold_release"]
    # backfill file and folder both load
    (tmp_path / "h").mkdir()
    (tmp_path / "h" / "a.json").write_text(json.dumps({"quarter": "2026Q3", "run": "final", "counts": {"x": 1}}))
    bf = tmp_path / "bf.yaml"
    bf.write_text("quarters:\n  2026Q1:\n    x: 5\n")
    runs = load_history(tmp_path / "h", bf)
    assert {(r["quarter"], r["run"]) for r in runs} == {("2026Q3", "final"), ("2026Q1", "backfill")}
