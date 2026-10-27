"""Private by design: non-publishable sources never reach public run outputs."""
import json

import pandas as pd

from snapshot import private, quality, sources


def test_ransomware_is_private_until_permitted():
    assert "ransomware" in private.private_pulls()
    assert not sources.may_publish("ransomware_live")


def test_split_moves_private_folders_only(tmp_path):
    raw, priv = tmp_path / "raw", tmp_path / "private"
    for d in ["2026Q4/dry-run/ransomware", "2026Q4/dry-run/kev"]:
        (raw / d).mkdir(parents=True)
        (raw / d / "x.parquet").write_text("x")
    moved = private.split(raw, priv)
    assert [p.relative_to(priv).as_posix() for p in moved] == ["2026Q4/dry-run/ransomware"]
    assert not (raw / "2026Q4/dry-run/ransomware").exists() and (raw / "2026Q4/dry-run/kev").exists()


def test_quality_report_withholds_ransomware_figures(tmp_path):
    (tmp_path / "manifest.json").write_text(json.dumps({"quarter": "2026Q3", "run": "dry-run", "files": []}))
    d = tmp_path / "ransomware"; d.mkdir()
    pd.DataFrame({"month": ["2026-07"], "dimension": ["all"], "value": ["all"], "count": [952]}) \
        .to_parquet(d / "ransomware_counts.parquet", index=False)
    text, _ = quality.build(tmp_path)
    assert "withheld" in text and "952" not in text


def test_pull_note_has_no_figures():
    src = open(private.__file__.replace("private.py", "pull.py")).read()
    assert "monthly totals" not in src


def test_split_marks_manifest_and_rebuild_accepts_it(tmp_path):
    from snapshot import rebuild
    raw, priv = tmp_path / "raw", tmp_path / "private"
    b = raw / "2026Q4/dry-run"
    (b / "ransomware").mkdir(parents=True)
    (b / "ransomware/ransomware_counts.parquet").write_text("x")
    (b / "manifest.json").write_text(json.dumps({"files": [
        {"source": "ransomware_live", "file_path": "ransomware/ransomware_counts.parquet", "sha256": "abc"}]}))
    private.split(raw, priv)
    m = json.loads((b / "manifest.json").read_text())
    assert m["files"][0]["kept_privately"] is True
    assert rebuild.verify_files(b) == []
