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
