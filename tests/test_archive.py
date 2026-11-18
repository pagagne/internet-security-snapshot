"""Logs and outputs saved to Drive before GitHub's 90-day deletion (author, 18 Nov 2026)."""
import datetime as dt

from snapshot import archive as A

NOW = dt.datetime(2026, 12, 31, tzinfo=dt.timezone.utc)


def _ago(days):
    return (NOW - dt.timedelta(days=days)).isoformat().replace("+00:00", "Z")


def test_logs_between_75_and_90_days_not_yet_saved():
    runs = [{"id": 1, "status": "completed", "created_at": _ago(80)},
            {"id": 2, "status": "completed", "created_at": _ago(60)},
            {"id": 3, "status": "completed", "created_at": _ago(95)},
            {"id": 4, "status": "completed", "created_at": _ago(76)},
            {"id": 5, "status": "in_progress", "created_at": _ago(80)}]
    assert A.logs_to_save(runs, {"4"}, NOW) == ["1"]


def test_pull_bundles_copied_only_when_missing_from_drive():
    arts = [{"id": 10, "name": "snapshot-111", "created_at": _ago(80), "expired": False},
            {"id": 11, "name": "snapshot-222", "created_at": _ago(80), "expired": False},
            {"id": 12, "name": "diagram-pngs", "created_at": _ago(80), "expired": False},
            {"id": 13, "name": "snapshot-333", "created_at": _ago(10), "expired": False}]
    assert A.artifacts_to_copy(arts, ["2026-10-27-run111/"], NOW) == ["11"]
