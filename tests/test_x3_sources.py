"""The x3_sources fingerprint/archive task (author's safeguards, 29 Oct 2026)."""
import hashlib

from snapshot.research import x3_sources


def test_refuses_plain_http():
    assert x3_sources.fingerprint("http://example.com/report") == ("not https", "", 0)


def test_fingerprint_is_sha256(monkeypatch):
    class R:
        status_code = 200
        def iter_content(self, n):
            yield b"report text"
    monkeypatch.setattr(x3_sources.requests, "get", lambda *a, **k: R())
    status, sha, size = x3_sources.fingerprint("https://example.org/r")
    assert (status, sha, size) == ("200", hashlib.sha256(b"report text").hexdigest(), 11)


def test_size_cap(monkeypatch):
    class R:
        status_code = 200
        def iter_content(self, n):
            while True:
                yield b"x" * 1_000_000
    monkeypatch.setattr(x3_sources.requests, "get", lambda *a, **k: R())
    assert x3_sources.fingerprint("https://example.org/big")[0] == "too large"


def test_archive_reuses_existing_snapshot(monkeypatch):
    class R:
        def json(self):
            return {"archived_snapshots": {"closest": {"available": True,
                    "url": "http://web.archive.org/web/2026/https://example.org/r"}}}
    monkeypatch.setattr(x3_sources.requests, "get", lambda *a, **k: R())
    assert x3_sources.archive("https://example.org/r").startswith("https://web.archive.org/web/")
