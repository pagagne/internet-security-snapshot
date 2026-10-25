"""The race worksheet's spreadsheet steps give the same median as the pipeline."""
import numpy as np
import pandas as pd

from snapshot import worksheet as W

PROBE = pd.DataFrame([
    {"cve_id": "CVE-1", "vendor": "A", "product": "x", "kev_added": "2026-07-10", "published": "2026-07-01",
     "github": "2026-07-05", "github_src": "GitHub advisory GHSA-aaaa-bbbb-cccc"},
    {"cve_id": "CVE-2", "vendor": "Microsoft", "product": "y", "kev_added": "2026-08-01", "published": "2026-07-20",
     "msrc_release": "2026-07-14"},
    {"cve_id": "CVE-3", "vendor": "B", "product": "z", "kev_added": "2026-09-01", "published": "2026-09-03"},
    {"cve_id": "CVE-4", "vendor": "C", "product": "w", "kev_added": "2026-06-30", "published": "2026-06-01"},
]).astype(object).where(lambda d: d.notna(), None)


def test_inputs_and_median_match():
    inp = W.race_inputs(PROBE, "2026Q3")
    assert list(inp["cve"]) == ["CVE-1", "CVE-2", "CVE-3"]          # CVE-4 is Q2
    assert inp.loc[0, "check_fix_date_at"].endswith("GHSA-aaaa-bbbb-cccc")
    assert inp.loc[2, "fix_date_source"].startswith("CVE publication")
    days = (pd.to_datetime(inp["attack_date_kev_added"]) - pd.to_datetime(inp["fix_date"])).dt.days
    res = W.race_result(inp, "2026Q3")
    assert res["median_days_fix_to_exploit"] == float(np.median(days)) == 5.0
    md = W.race_markdown(inp, res, "2026Q3", "test")
    assert "**5**" in md and "not a study result" in md


def test_sample_in_repo_is_consistent():
    from pathlib import Path
    d = Path(__file__).resolve().parents[1] / "docs/reviewer/sample-worksheet"
    inp = pd.read_csv(d / "inputs.csv", dtype=str)
    days = (pd.to_datetime(inp["attack_date_kev_added"]) - pd.to_datetime(inp["fix_date"])).dt.days
    assert f"**{float(np.median(days)):g}**" in (d / "README.md").read_text()
