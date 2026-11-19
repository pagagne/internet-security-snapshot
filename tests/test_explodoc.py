"""docs/EXPLORATORY_MEASURES.md follows config/exploratory.yaml (author, 19 Nov 2026)."""
from snapshot import explodoc


def test_current_and_complete():
    assert explodoc.main(["check"]) == 0
    text = explodoc.DOC.read_text()
    import yaml
    for m in yaml.safe_load(explodoc.CONFIG.read_text())["measures"]:
        assert f"## {m['id']}\n" in text


def test_status_notes_kept():
    notes = explodoc._status_notes(explodoc.CONFIG.read_text())
    assert "APNIC" in notes.get("X20", "")
