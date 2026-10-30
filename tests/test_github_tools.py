"""AI attack-tool sweep of GitHub (X25, author's decision 30 Oct 2026)."""
from pathlib import Path

import yaml

from snapshot.research import github_tools as G

ROOT = Path(__file__).resolve().parents[1]


def _item(name, stars, created="2026-10-01", desc="Autonomous pentest agent on Hermes via MCP", fork=False):
    return {"full_name": name, "html_url": f"https://github.com/{name}", "owner": {"type": "User"},
            "created_at": created + "T00:00:00Z", "pushed_at": created + "T00:00:00Z",
            "stargazers_count": stars, "forks_count": 0, "fork": fork, "archived": False,
            "license": None, "language": "Python", "topics": ["ai-pentest"], "description": desc}


def test_queries_fixed_and_unique():
    cfg = yaml.safe_load((ROOT / G.CONFIG).read_text())
    q = cfg["attack"] + cfg["defence"]
    assert len(q) == len(set(q)) and len(cfg["attack"]) >= 20 and len(cfg["defence"]) >= 20


def test_roles():
    assert G.role("Autonomous pentest agent that exploits web apps") == "attack"
    assert G.role("AI SOC analyst: alert triage and incident response") == "defence"
    assert G.role("Finds vulnerabilities with exploits and auto-fixes them") == "both"
    assert G.role("Prompt injection scanner for LLM apps") == "model_testing"
    assert G.role("A list of books") == "unclear"


def test_sweep_merges_queries_and_reads_safeguards():
    data = {"q1": [_item("a/one", 50), _item("b/two", 5)], "q2": [_item("a/one", 50), _item("c/fork", 9, fork=True)]}
    rows, hits = G.sweep(list(data), pause=0, search_fn=lambda q, p: data[q],
                         readme_fn=lambda n: "No scope-guard, no consent." if n == "a/one" else "Use only on authorized targets.")
    assert hits == {"q1": 2, "q2": 2}
    by = {r["full_name"]: r for r in rows}
    assert len(rows) == 3 and by["a/one"]["queries"] == "q1;q2"
    assert by["a/one"]["models"] == "hermes;mcp"
    assert by["a/one"]["readme_safeguard"] == "says none"
    assert by["b/two"]["readme_safeguard"] == "mentions"
    assert by["c/fork"]["readme_safeguard"] == ""          # forks: no README read
    s = G.summary(rows, hits, "2026-10-30")
    assert "| 2026-10 | 2 |" in s and "never instructions" in s
    assert by["a/one"]["role"] == "attack" and by["a/one"]["side"] == "attack"
