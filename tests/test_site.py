"""The project website (snapshot.site): home page current, run health is health only."""
import datetime as dt
import json

from snapshot import site


def test_home_page_current_and_carries_mission_and_credits():
    t = site.home_html()
    assert (site.SITE / "index.html").read_text() == t
    assert "<h2>Mission</h2>" in t and "Data sources and credits" in t and "Ransomware.live" in t
    assert 'href="reviewer/"' in t and 'href="health/"' in t


def test_health_page_from_run_reports(tmp_path):
    r = tmp_path / "reports" / "2026-12-01T1105Z-run123"
    r.mkdir(parents=True)
    (r / "manifest-2026Q4-dry-run.json").write_text(json.dumps({"quarter": "2026Q4", "run": "dry-run", "files": [
        {"source": "nvd", "status": "ok"}, {"source": "sec_edgar", "status": "gap", "note": "x"}],
        "server_pushback": {"nvd": {"api 429": 2}}}))
    (tmp_path / "landing").mkdir()
    (tmp_path / "landing" / "status.json").write_text(json.dumps({"checked": "2026-12-01", "results": {
        "NVD": {"state": "ok"}, "Shadowserver": {"state": "pending"}}}))
    h = site.health_html(tmp_path, dt.date(2026, 12, 2))
    assert "2026Q4 dry-run" in h and "gaps: sec_edgar" in h and "awaiting permission" in h
    assert "actions/runs/123" in h
    assert ">done<" in h                        # the 1 Dec practice run is recorded as run
    assert "Draft layout" in h                  # until the author approves the mock-up


def test_pilot_step_states():
    assert site._state(None, "2027-01-01", dt.date(2026, 12, 31)) == "waiting"
    assert site._state(None, "2027-01-01", dt.date(2027, 1, 1)) == "running"
    assert site._state(None, "2027-01-01", dt.date(2027, 1, 2)) == "late"
    assert site._state({"done": "x"}, "2027-01-01", dt.date(2027, 1, 2)) == "done"
