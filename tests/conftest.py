"""Shared test settings.

Since 31 Oct 2026 (author's decision) the exploratory work lives in the private repository
pagagne/snapshot-manual. A checkout of this public repository has no exploratory/ folder, so
the tests that read its data are skipped there; they run wherever the private copy is present
(a Claude working copy, or a workflow that links it with tools/private.sh).
"""
from pathlib import Path

import pytest

PRIVATE = Path(__file__).resolve().parents[1] / "exploratory"
needs_private = pytest.mark.skipif(not PRIVATE.is_dir(), reason="private exploratory data not in this checkout")
