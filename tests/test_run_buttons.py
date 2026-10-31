"""Run buttons (author's decision, 29 Oct 2026).

Workflows that contact anything outside the repository have no Run button: they start on their
timer or through GitHub's API (repository_dispatch). Repository-only workflows keep the button,
with a short explanation shown in the Run box."""
from pathlib import Path

import yaml

from snapshot import schedule as S

WF = Path(__file__).resolve().parents[1] / ".github" / "workflows"
EXTERNAL = {"quarterly-pull.yml": "quarterly-pull", "research.yml": "research",
            "honeypot.yml": "honeypot", "bigquery-check.yml": "bigquery-check",
            "feed-screen.yml": "feed-screen", "source-watch.yml": "source-watch"}
BUTTONS = ["checks.yml", "privacy.yml", "schedule.yml", "rebuild-check.yml", "diagrams.yml", "backup.yml",
           "manual-publish.yml"]


def _on(name):
    doc = yaml.safe_load((WF / name).read_text())
    return doc.get("on", doc.get(True))   # YAML 1.1 reads a bare `on` as True


def test_external_workflows_have_no_button():
    for name, event in EXTERNAL.items():
        on = _on(name)
        assert "workflow_dispatch" not in on, name
        assert on["repository_dispatch"]["types"] == [event], name


def test_internal_workflows_have_explained_button():
    for name in BUTTONS:
        about = _on(name)["workflow_dispatch"]["inputs"]["about"]
        assert len(about["description"]) > 40, name


def test_schedule_starts_runs_by_api_event():
    args = S.dispatch_args({"workflow": "quarterly-pull.yml", "inputs": {"quarter": "2026Q4", "run": "dry-run"}})
    assert args[:3] == ["api", "-X", "POST"] and args[3].endswith("/dispatches")
    assert "event_type=quarterly-pull" in args
    assert "client_payload[quarter]=2026Q4" in args and "client_payload[run]=dry-run" in args


def test_every_scheduled_dispatch_targets_an_api_workflow():
    for o in S.expand(S.load()):
        if o["dispatch"]:
            assert o["dispatch"]["workflow"] in EXTERNAL, o["uid"]
