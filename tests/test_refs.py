import datetime as dt
from pathlib import Path

from snapshot import refs

ROOT = Path(__file__).resolve().parents[1]


def _occ(day, days=1):
    return {"dry-run": [{"date": day, "days": days}]}


def test_date_keeps_year_style():
    occ = _occ(dt.date(2026, 12, 1))
    assert refs.want("date", "dry-run", None, "1 Dec", occ, {}) == "1 Dec"
    assert refs.want("date", "dry-run", None, "3 Dec 2026", occ, {}) == "1 Dec 2026"


def test_span_and_missing():
    occ = _occ(dt.date(2027, 1, 4), days=25)
    assert refs.want("date", "dry-run", "1", "x", occ, {}) == "4–28 Jan"
    assert refs.want("date", "dry-run", "2", "x", occ, {}) is None
    assert refs.want("date", "nope", None, "x", occ, {}) is None


def test_status_keeps_capital():
    assert refs.want("status", "vulncheck", None, "Awaiting", {}, {"vulncheck": "granted"}) == "Granted"
    assert refs.want("status", "vulncheck", None, "awaiting", {}, {"vulncheck": "granted"}) == "granted"


def test_mark_is_rewritten(tmp_path):
    m = refs.MARK.search("on <!-- date:freeze -->28 Dec<!-- /date --> we lock")
    assert m.groups() == ("date", "freeze", None, "28 Dec")


def test_repository_is_consistent():
    assert refs.run(ROOT, write=False) == []
