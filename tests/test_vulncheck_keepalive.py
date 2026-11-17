"""The VulnCheck token keep-alive (author's decision, 17 Nov 2026)."""
import pytest

from snapshot.collect import vulncheck


def test_not_due_makes_no_request(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("no request expected")
    monkeypatch.setattr("requests.get", boom)
    assert "not due" in vulncheck.keepalive(day=9)


def test_due_day_reports_ok_without_data(monkeypatch):
    monkeypatch.setenv("VULNCHECK_TOKEN", "tok-SECRET-123")

    class R:
        ok, status_code = True, 200
    monkeypatch.setattr("requests.get", lambda *a, **k: R())
    msg = vulncheck.keepalive(day=15)
    assert "OK" in msg and "SECRET" not in msg


def test_due_day_failure_raises(monkeypatch):
    monkeypatch.setenv("VULNCHECK_TOKEN", "x")

    class R:
        ok, status_code = False, 401
    monkeypatch.setattr("requests.get", lambda *a, **k: R())
    with pytest.raises(RuntimeError, match="401"):
        vulncheck.keepalive(day=1)


def test_keepalive_days_leave_a_second_chance():
    d = vulncheck.KEEPALIVE_DAYS
    assert len(d) >= 4 and max(b - a for a, b in zip(sorted(d), sorted(d)[1:])) < 30


def test_one_off_dates_are_due(monkeypatch):
    monkeypatch.setenv("VULNCHECK_TOKEN", "x")

    class R:
        ok, status_code = True, 200
    monkeypatch.setattr("requests.get", lambda *a, **k: R())
    assert "OK" in vulncheck.keepalive(day=17, date="2026-11-17")
