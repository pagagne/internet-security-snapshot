"""Baseline-year list (pre-registration Section 10): the retrospective cohort is Q4 2025 to Q3 2026."""
from snapshot.research.baseline_list import QUARTERS


def test_baseline_quarters():
    assert QUARTERS == ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
