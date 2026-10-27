"""Server pushback (429/403) is counted, retried for 429, and shown in the quality report."""
import json

import pytest
import requests

from snapshot.collect import http


class _R:
    def __init__(self, code, url="https://example.org/x"):
        self.status_code, self.url = code, url

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


def test_429_counted_then_retried(monkeypatch):
    replies = iter([_R(429), _R(200)])
    monkeypatch.setattr(http.requests, "get", lambda *a, **k: next(replies))
    monkeypatch.setattr(http.time, "sleep", lambda s: None)
    http.PUSHBACK.clear()
    assert http.get("https://example.org/x").status_code == 200
    assert http.PUSHBACK == {"example.org 429": 1}


def test_403_counted_and_raised(monkeypatch):
    monkeypatch.setattr(http.requests, "get", lambda *a, **k: _R(403))
    http.PUSHBACK.clear()
    with pytest.raises(requests.HTTPError):
        http.get("https://example.org/x")
    assert http.PUSHBACK == {"example.org 403": 1}


def test_other_codes_not_counted():
    http.PUSHBACK.clear()
    http.note_status("https://example.org/x", 404)
    assert not http.PUSHBACK


def test_warning_annotation(monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    http.PUSHBACK.clear()
    http.note_status("https://api.example.org/a", 429)
    assert "::warning title=Server pushback::api.example.org replied 429" in capsys.readouterr().out
