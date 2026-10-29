"""Watchdog for skipped timed runs (author's decision, 29 Oct 2026)."""
import datetime as dt
import json

from snapshot import watchdog as W

UTC = dt.timezone.utc


def at(y, m, d, h=12, mi=0):
    return dt.datetime(y, m, d, h, mi, tzinfo=UTC)


def fake_gh(runs_by_file, issues=""):
    calls = []

    def gh(args):
        calls.append(args)
        if args[:2] == ["api", args[1]] and "/issues?labels=watchdog" in args[1]:
            return json.dumps([issues])
        if "/runs?" in args[1]:
            name = args[1].split("/workflows/")[1].split("/")[0]
            return json.dumps(runs_by_file.get(name, []))
        return ""
    return gh, calls


def test_due_only_after_grace_and_within_lookback():
    assert W.due_times("quarterly-pull.yml", at(2027, 1, 1, 9, 59)) == []          # still in grace
    assert W.due_times("quarterly-pull.yml", at(2027, 1, 1, 10, 23)) == [at(2027, 1, 1, 6, 0)]
    assert W.due_times("quarterly-pull.yml", at(2027, 3, 1, 12)) == []             # March: no pull
    assert W.due_times("quarterly-pull.yml", at(2027, 1, 5, 12)) == []             # past look-back


def test_skipped_pull_is_started_as_provisional_once():
    gh, calls = fake_gh({})
    log = W.check(at(2027, 1, 1, 10, 23), gh=gh)
    assert log == ["start quarterly-pull.yml@2027-01-01T0600Z"]
    start = next(c for c in calls if c[:4] == ["api", "-X", "POST", "repos/pagagne/internet-security-snapshot/dispatches"])
    assert "event_type=quarterly-pull" in start
    assert "client_payload[run]=provisional" in start and "client_payload[quarter]=2026Q4" in start
    gh2, _ = fake_gh({}, issues="<!-- watchdog: quarterly-pull.yml@2027-01-01T0600Z -->")
    assert W.check(at(2027, 1, 1, 15, 37), gh=gh2) == []                          # never twice


def test_final_run_in_february_and_no_start_when_it_ran():
    assert W.payload("quarterly-pull.yml", at(2027, 2, 1, 6))["inputs"] == {"quarter": "2026Q4", "run": "final"}
    gh, calls = fake_gh({"quarterly-pull.yml": [123]})
    assert W.check(at(2027, 2, 1, 12, 7), gh=gh) == []


def test_button_workflows_restarted_by_workflow_dispatch():
    gh, calls = fake_gh({})
    assert W.check(at(2027, 3, 10, 12, 7), gh=gh) == ["start rebuild-check.yml@2027-03-10T0717Z"]
    assert any(c[-2:] == ["-f", "ref=main"] and "rebuild-check.yml" in c[3] for c in calls)


def test_dry_run_starts_nothing():
    gh, calls = fake_gh({})
    assert W.check(at(2027, 1, 2, 15, 37), dry=True, gh=gh)
    assert not any("POST" in c for c in calls)
