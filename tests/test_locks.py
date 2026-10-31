"""Guards on the locked core and the exploratory layer. See docs/CHANGE_POLICY.md."""

import hashlib
from pathlib import Path

import re

import yaml

from conftest import needs_private

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


@needs_private
def test_ai_attack_campaign_log_is_well_formed():
    import csv
    rows = list(csv.DictReader((ROOT / "exploratory/ai_attack_campaigns.csv").open()))
    vectors = {"known_cve", "zero_day", "web_app_unknown", "credentials", "misconfiguration", "supply_chain", "phishing", "unknown"}
    roles = {"agents_operated_intrusion", "ai_assisted_operator", "ai_generated_malware", "ai_enabled_fraud",
             "evaluation_escape"}   # logged beside campaigns, never counted as one (amended 2026-10-26)
    for r in rows:
        assert r["entry_vector"] in vectors, r["campaign"]
        assert r["ai_role"] in roles, r["campaign"]
        assert r["source_url"].startswith("https://")
        assert r["confirmed_by_second_source"] in {"yes", "no"}
        assert r["conflict_of_interest"] in {"yes", "no"}
        # added 2026-10-29 (author): how strong the evidence of AI use is
        assert r["ai_evidence"] in {"confirmed", "assessed", "unrated"}, r["campaign"]
        # added 2026-10-29 (author, review item 13 option B): attack method and how it reached us
        from snapshot.x3catalogue import FOUND_VIA, METHODS
        assert r["attack_method"] in METHODS, r["campaign"]
        assert r["found_via"] in FOUND_VIA, r["campaign"]
        # added 2026-10-30 (author): open-weight or closed AI, and the network protocols used
        from snapshot.research.github_tools import PROTOCOLS
        assert r["model_weights"] in {"open-weight", "closed", "both", "not named", "to check"}, r["campaign"]
        assert r["protocols"] in {"not named", "to check"} or all(
            x in PROTOCOLS for x in r["protocols"].split(";")), (r["campaign"], r["protocols"])
        for cid in filter(None, r["cve_ids"].split(";")):
            assert re.fullmatch(r"CVE-\d{4}-\d{4,}", cid), (r["campaign"], cid)
