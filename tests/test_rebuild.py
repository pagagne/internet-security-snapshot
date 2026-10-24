"""Rebuild check on a small frozen bundle."""

import json
from pathlib import Path

import pandas as pd

from snapshot import quality, rebuild
from snapshot.collect import cve
from snapshot.util import Manifest, Quarter

FIX = Path(__file__).parent / "fixtures" / "cves"


def _bundle(tmp_path) -> Path:
    b = tmp_path / "2026Q2" / "dry-run"
    (b / "cve").mkdir(parents=True)
    df = pd.DataFrame([cve.parse_record(json.loads(p.read_text())) for p in FIX.glob("*.json")])
    df["ai_credited"] = df["ai_credit_terms"].map(bool)
    df.to_parquet(b / "cve/cve_records.parquet", index=False)
    m = Manifest(Quarter(2026, 2), "dry-run", b)
    m.add_file("cve_org", b / "cve/cve_records.parquet", "test")
    m.write()
    quality.main([str(b)])          # writes quality.json as a real run does
    return b


def test_clean_bundle_passes(tmp_path):
    b = _bundle(tmp_path)
    problems, notes = rebuild.run(b)
    assert problems == []
    assert notes and "no figures.json" in notes[0]
    assert rebuild.main([str(b)]) == 0


def test_changed_file_and_changed_figure_fail(tmp_path):
    b = _bundle(tmp_path)
    q = json.loads((b / "quality.json").read_text())
    q["counts"]["cve/cve_records.parquet"] += 1
    (b / "quality.json").write_text(json.dumps(q))
    pd.read_parquet(b / "cve/cve_records.parquet").head(1).to_parquet(b / "cve/cve_records.parquet", index=False)
    problems, _ = rebuild.run(b)
    assert any("checksum differs" in p for p in problems)
    assert any("quality.json" in p for p in problems)
    assert rebuild.main([str(b)]) == 1


def test_diff_ignores_last_digits_and_drift_flags():
    assert rebuild.diff({"a": 0.1 + 0.2, "drift_flags": ["x"]}, {"a": 0.3}) == []
    assert rebuild.diff({"a": 1}, {"a": 2}) == ["/a: published 1, recomputed 2"]
