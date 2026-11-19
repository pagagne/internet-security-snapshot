"""X3 report reader: tags only, never article text (author's decisions, 30 Oct 2026)."""
from snapshot.research import x3_read as R


def test_tags_only(monkeypatch):
    class Resp:
        status_code = 200
        url = "https://vendor.example/report"
        headers = {"content-type": "text/html; charset=utf-8"}
        content = b"<p>The actor ran DeepSeek and Claude over SSH and SMB; CVE-2026-12345.</p>"
        encoding = "utf-8"
    monkeypatch.setattr(R.requests, "get", lambda *a, **k: Resp())
    rec = R.read("https://vendor.example/report")
    assert rec["model_weights"] == "both" and rec["protocols"] == "SSH;SMB" and rec["cves"] == "CVE-2026-12345"
    assert "DeepSeek and Claude" not in " ".join(str(v) for v in rec.values())


def test_approval_and_autonomy_cues_are_labels_only():
    from snapshot.research.x3_read import APPROVAL_CUES, AUTONOMY_CUES, cues
    t = "The operator reviewed each plan at checkpoints; later stages ran autonomously without human intervention."
    assert cues(t, APPROVAL_CUES) == "operator approved or reviewed;checkpoints"
    assert cues(t, AUTONOMY_CUES) == "without human;fully autonomous"
    assert cues("There was no human in the loop.", APPROVAL_CUES) == ""
    assert cues("There was no human in the loop.", AUTONOMY_CUES) == "no human in the loop"
