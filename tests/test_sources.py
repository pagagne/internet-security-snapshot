"""Switches for permissioned sources (config/sources.yaml) and their use by the pull."""
import json
import re
from pathlib import Path

import pytest
import yaml

from snapshot import pull, sources

ROOT = Path(__file__).resolve().parents[1]


def test_config_loads_and_matches_pullers():
    cfg = sources.load()
    assert set(cfg) == {"ransomware_live", "vulncheck", "shadowserver"}
    for s in cfg.values():
        assert s["pull"] is None or s["pull"] in pull.PULLERS


def test_nothing_published_without_written_permission():
    for key, s in sources.load().items():
        if s["publish"]:
            assert s["permission"] == "granted", key
    # Standing rule: VulnCheck-derived data stays private until written permission.
    v = sources.load()["vulncheck"]
    assert v["permission"] == "granted" or (not v["collect"] and not v["publish"])


def test_permission_matches_permissions_md():
    text = (ROOT / "docs/PERMISSIONS.md").read_text()
    words = {"awaiting": "awaiting", "granted": "granted", "declined": "declined"}
    for s in sources.load().values():
        row = next(l for l in text.splitlines() if l.startswith(f"| {s['name']} |"))
        assert words[s["permission"]] in row.lower(), (s["name"], row)


@pytest.mark.parametrize("bad, msg", [
    ({"permission": "awaiting", "collect": False, "publish": True, "pull": None}, "publish needs"),
    ({"permission": "declined", "collect": True, "publish": False, "pull": "ransomware"}, "declined"),
    ({"permission": "awaiting", "collect": True, "publish": False, "pull": None}, "no collector"),
    ({"permission": "maybe", "collect": False, "publish": False, "pull": None}, "permission must"),
])
def test_bad_switches_refused(tmp_path, bad, msg):
    p = tmp_path / "s.yaml"
    p.write_text(yaml.safe_dump({"permissioned": {"x": {"name": "X", **bad}}}))
    with pytest.raises(ValueError, match=msg):
        sources.load(p)


def test_pull_skips_switched_off_source_and_records_switches(tmp_path, monkeypatch):
    called = []
    monkeypatch.setitem(pull.PULLERS, "ransomware", lambda *a: called.append("ransomware"))
    monkeypatch.setitem(pull.PULLERS, "kev", lambda *a: called.append("kev"))
    monkeypatch.setattr(sources, "disabled_pulls", lambda: {"ransomware"})
    rc = pull.main(["--quarter", "2026Q3", "--run", "dry-run", "--sources", "kev,ransomware", "--out", str(tmp_path)])
    assert rc == 0 and called == ["kev"]
    m = json.loads((tmp_path / "2026Q3/dry-run/manifest.json").read_text())
    assert set(m["source_switches"]) == {"ransomware_live", "vulncheck", "shadowserver"}
    assert not any(e["status"] == "gap" for e in m["files"])


def test_workflow_default_leaves_choice_to_config():
    wf = (ROOT / ".github/workflows/quarterly-pull.yml").read_text()
    # Since 29 Oct the pull has no Run button; an API start without "sources" passes nothing,
    # so the switches in config/sources.yaml decide.
    assert "IN_SOURCES: ${{ github.event.client_payload.sources }}" in wf
    assert '[ -n "$IN_SOURCES" ] && ARGS+=(--sources' in wf
