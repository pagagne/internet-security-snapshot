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


def test_reviewed_exemptions_follow_the_exact_text():
    """An exemption from the privacy scan holds only for the wording the author reviewed."""
    import yaml
    ms = {m["id"]: m for m in yaml.safe_load(explodoc.CONFIG.read_text())["measures"]}
    t = explodoc._text(ms["X26"]["method"])
    assert explodoc._mark("X26", "method", t) == " " + explodoc.MARK
    assert explodoc._mark("X26", "method", t + " changed") == ""
    assert explodoc._mark("X1", "method", t) == ""
