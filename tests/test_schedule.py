"""The schedule (docs/schedule/schedule.yaml) is valid, its outputs are current, and the
daily job opens each issue once."""
import datetime as dt
import json

from snapshot import schedule as S


def test_items_valid_and_unique():
    items = S.load()
    assert len({i["id"] for i in items}) == len(items)
    assert all(i["owner"] in S.OWNERS for i in items)
    occ = S.expand(items)
    assert len({o["uid"] for o in occ}) == len(occ)


def test_outputs_current():
    plan, ics = S.build()
    assert S.main(["check"]) == 0, "run: python -m snapshot.schedule build"
    assert S.PLAN.read_text() == plan + "\n"
    assert ics.count("BEGIN:VEVENT") == len(S.expand(S.load()))


def test_dst_offsets():
    assert S.ny_offset(dt.date(2026, 7, 1)) == -4
    assert S.ny_offset(dt.date(2026, 12, 1)) == -5
    assert S.to_utc(dt.date(2026, 11, 12), "10:00", False).hour == 15


def test_dry_run_dispatched_on_1_dec():
    d = S.due(S.expand(S.load()), dt.date(2026, 12, 1), catch_up=0)
    runs = [o for o in d["runs"] if o["uid"].startswith("dry-run@")]
    assert runs and runs[0]["dispatch"]["workflow"] == "quarterly-pull.yml"


def test_catch_up_after_missed_days():
    occ = S.expand(S.load())
    late = S.due(occ, dt.date(2026, 12, 4))       # three days after the dry run
    assert any(o["uid"].startswith("dry-run@") for o in late["runs"])
    gone = S.due(occ, dt.date(2026, 12, 1) + dt.timedelta(days=S.CATCH_UP_DAYS + 1))
    assert not any(o["uid"].startswith("dry-run@") for o in gone["runs"])


def test_act_is_idempotent():
    calls, bodies = [], []

    def gh(args):
        calls.append(args)
        if args[:2] == ["issue", "list"]:
            return json.dumps([{"body": b} for b in bodies])
        if args[:2] == ["issue", "create"]:
            bodies.append(args[args.index("--body") + 1])
            return "https://github.com/x/y/issues/1\n"
        return ""

    day = dt.date(2026, 12, 1)
    first = S.act(day, gh=gh)
    assert first and any(l.startswith("run ") for l in first)
    n = len(calls)
    assert S.act(day, gh=gh) == []                 # second run: nothing new
    assert all(c[:2] == ["issue", "list"] for c in calls[n:])


def test_readme_schedule_generated():
    assert S.README.read_text() == S.build_readme(), "run: python -m snapshot.schedule build"
    table = S.readme_table(S.expand(S.load()), S.load_milestones())
    assert "| 1 Dec 2026 | Dry run" in table
    assert "| 1 Jan / 1 Feb 2027 |" in table


def test_reviewer_feed_and_no_reviewer_issues():
    occ = S.expand(S.load())
    rev = S.reviewer_occ(occ)
    assert rev and all(o["owner"] == "reviewer" or "reviewer" in o["feeds"] for o in rev)
    assert S.REVIEWER_ICS.read_text().count("BEGIN:VEVENT") == len(rev)
    for day in (dt.date(2027, 4, 3), dt.date(2027, 4, 29)):
        assert not any(o["owner"] == "reviewer" for o in S.due(occ, day)["issues"])


def _events(text):
    return [e.split("END:VEVENT")[0] for e in text.split("BEGIN:VEVENT")[1:]]


def test_feeds_in_sync():
    """Every entry in the reviewer's feed is byte-for-byte the same entry in the full feed."""
    full = set(_events(S.ICS.read_text()))
    rev = _events(S.REVIEWER_ICS.read_text())
    assert rev and all(e in full for e in rev)
    assert all(any(f"SUMMARY:[{who}]" in e for who in S.RESPONSIBLE.values()) for e in full)


def test_reviewer_desk_tasks_match_feed():
    import json
    tasks = json.loads(S.REVIEWER_JSON.read_text())["tasks"]
    assert [t["uid"] for t in tasks] == [o["uid"] for o in S.reviewer_occ(S.expand(S.load()))]
    assert all(t["title"][:1].isupper() for t in tasks)
