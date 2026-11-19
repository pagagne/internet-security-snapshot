"""X26 probe (19 Nov 2026): counts only, no names kept."""
import json

from snapshot.research import x26_probe as X


def test_query_forms():
    assert X.query({"author": "app/copilot-swe-agent"}, "2026-10-01", "2026-10-31", True) == \
        "is:pr created:2026-10-01..2026-10-31 author:app/copilot-swe-agent is:merged"
    assert "head:codex/" in X.query({"head": "codex/"}, "a", "b")


def test_human_changed():
    agent = [{"author": {"login": "Copilot"}, "committer": {"login": "web-flow"}}]
    assert not X.human_changed(agent)
    assert X.human_changed(agent + [{"author": {"login": "someone"}, "committer": {"login": "someone"}}])


def test_github_part_keeps_no_names():
    def get(url, h, params=None, pause=0):
        if url.endswith("/commits"):
            return [{"author": {"login": "maintainer-x"}, "committer": {"login": "web-flow"}}], "ok"
        items = [{"pull_request": {"url": "https://api.github.com/repos/owner-y/repo-z/pulls/1"},
                  "user": {"login": "Copilot"}, "repository_url": "owner-y/repo-z"}]
        return {"total_count": 7, "incomplete_results": False, "items": items}, "ok"
    out = X.github_part("2026-10-01", "2026-10-31", get, pause=0)
    text = json.dumps(out)
    assert "maintainer-x" not in text and "owner-y" not in text and "repo-z" not in text
    s = out["agents"]["GitHub Copilot coding agent"]["sample"]
    assert s["checked"] == 1 and s["with_human_commit"] == 1
    assert out["agents"]["OpenAI Codex (branch codex/)"].get("sample") is None
