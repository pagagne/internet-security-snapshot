from pathlib import Path

import pandas as pd

from snapshot import revisions


def _write(root: Path, rel: str, df: pd.DataFrame) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p, index=False)


def test_counts_changed_removed_added(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    _write(old, "kev/kev_entries.parquet", pd.DataFrame({
        "cve_id": ["CVE-1", "CVE-2", "CVE-3"], "date_added": ["2026-10-01", "2026-10-02", "2026-10-03"],
        "vendor": ["a", "b", "c"]}))
    _write(new, "kev/kev_entries.parquet", pd.DataFrame({
        "cve_id": ["CVE-1", "CVE-2", "CVE-4"], "date_added": ["2026-10-01", "2026-10-05", "2026-11-01"],
        "vendor": ["a", "b", "d"]}))
    r = revisions.compare(old, new)["kev/kev_entries.parquet"]
    assert (r["shared"], r["removed"], r["added"]) == (2, 1, 1)
    assert r["fields"]["date_added"]["changed"] == 1
    assert r["fields"]["date_added"]["examples"] == ["CVE-2"]
    assert "vendor" not in r["fields"]


def test_lists_nan_and_composite_keys(tmp_path):
    old, new = tmp_path / "old", tmp_path / "new"
    _write(old, "cve/cve_records.parquet", pd.DataFrame({
        "cve_id": ["CVE-1", "CVE-2"], "cwe_ids": [["CWE-79"], None], "cvss_base": [7.5, float("nan")]}))
    _write(new, "cve/cve_records.parquet", pd.DataFrame({
        "cve_id": ["CVE-1", "CVE-2"], "cwe_ids": [["CWE-79"], None], "cvss_base": [7.5, float("nan")]}))
    _write(old, "epss/epss_scores.parquet", pd.DataFrame({"cve": ["CVE-1", "CVE-1"], "date": ["d1", "d2"], "epss": [0.1, 0.2]}))
    _write(new, "epss/epss_scores.parquet", pd.DataFrame({"cve": ["CVE-1", "CVE-1"], "date": ["d1", "d2"], "epss": [0.1, 0.3]}))
    res = revisions.compare(old, new)
    assert res["cve/cve_records.parquet"]["fields"] == {}
    e = res["epss/epss_scores.parquet"]["fields"]["epss"]
    assert e["changed"] == 1 and e["examples"] == ["CVE-1/d2"]
    assert res["nvd/nvd_cves.parquet"] == {"skipped": "missing in both"}
    assert "Revision drift" in revisions.report(res, "a", "b")
