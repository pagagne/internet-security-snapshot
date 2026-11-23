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


def test_hold_issue_text():
    from snapshot.quality import hold_issue
    assert hold_issue({"hold_release": False}) is None
    t, b = hold_issue({"hold_release": True, "quarter": "2026Q4", "run": "final",
                       "history_flags": ["nvd/nvd_cves.parquet: 90 rows, expected about 200"]}, "https://x/run")
    assert t.startswith("[Author] Release hold: 2026Q4 final")
    assert "nvd/nvd_cves.parquet: 90 rows" in b and "Publishing waits" in b and "https://x/run" in b


def test_private_sources_leave_row_counts(tmp_path, monkeypatch):
    import pandas as pd
    from snapshot import private
    from snapshot.quality import source_counts
    b = tmp_path / "raw/2026Q4/dry-run"
    (b / "apnic").mkdir(parents=True)
    pd.DataFrame({"cc": ["ZZ", "YY"]}).to_parquet(b / "apnic/apnic_dnssec_by_country.parquet")
    monkeypatch.setattr(private, "private_pulls", lambda: {"apnic"})
    private.split(tmp_path / "raw", tmp_path / "private")
    assert not (b / "apnic").exists()
    counts, _ = source_counts(b)
    assert counts["apnic/apnic_dnssec_by_country.parquet"] == 2


def test_failed_report_holds_release():
    from snapshot import quality
    t = quality.hold_issue({"error": "AttributeError: boom"}, "https://example/run")
    assert t and "report failed" in t[0] and "boom" in t[1]
    assert quality.hold_issue({"quarter": "2026Q4", "run": "dry-run"}) is None


def test_sec_search_diagnostics_do_not_shadow_quarter(tmp_path):
    import json
    from snapshot import quality
    b = tmp_path / "b"
    (b / "sec").mkdir(parents=True)
    (b / "manifest.json").write_text(json.dumps({"quarter": "2026Q4", "run": "dry-run", "files": [
        {"source": "sec_edgar", "status": "ok", "retrieved_at": "2026-11-23T22:30:00Z"}]}))
    (b / "sec/sec_summary.json").write_text(json.dumps({
        "filings_item_1_05": 1, "original_8k": 1, "registrants_company_tickers": 7992,
        "per_1000_registrants": 0.13, "search_diagnostics": {"q1": {"total_hits": 3}}}))
    md, m = quality.build(b)
    assert m["window_fraction"] < 1.0 and "Search q1" in md
