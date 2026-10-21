"""Guards on the locked core. See docs/CHANGE_POLICY.md."""

import hashlib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCKED = yaml.safe_load((ROOT / "prereg/LOCKED.yaml").read_text())
DEVIATIONS = (ROOT / "prereg/DEVIATIONS.md").read_text()


def _sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_locked_files_unchanged():
    changed = [p for p, spec in LOCKED["files"].items() if _sha(p) != spec["sha256"]]
    assert not changed, (
        f"Locked files changed: {changed}. A core change needs a dated row in "
        "prereg/DEVIATIONS.md and a new checksum in prereg/LOCKED.yaml."
    )


def test_preregistration_never_logged_as_changed():
    assert LOCKED["files"]["prereg/PREREGISTRATION.md"]["deviation"] is None


def test_each_change_has_a_deviation_entry():
    for path, spec in LOCKED["files"].items():
        if spec["deviation"]:
            assert f"| {spec['deviation']} |" in DEVIATIONS, f"{path}: no deviation row dated {spec['deviation']}"


def test_exploratory_measures_never_feed_labels():
    cfg = yaml.safe_load((ROOT / "config/exploratory.yaml").read_text())
    ids = [m["id"] for m in cfg["measures"]]
    assert len(ids) == len(set(ids))
    for m in cfg["measures"]:
        assert {"id", "name", "question", "sources", "added", "feeds_labels"} <= set(m)
        assert m["feeds_labels"] is False, f"{m['id']} must not feed labels"
