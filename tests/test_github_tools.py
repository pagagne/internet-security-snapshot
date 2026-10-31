"""AI attack-tool sweep of GitHub (X25, author's decision 30 Oct 2026)."""
from pathlib import Path

import yaml

from snapshot.research import github_tools as G

from conftest import needs_private

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
    assert by["a/one"]["labs"] == "Nous Research" and by["a/one"]["toolkits"] == "MCP"
    assert by["a/one"]["readme_safeguard"] == "says none"
    assert by["b/two"]["readme_safeguard"] == "mentions"
    assert by["c/fork"]["readme_safeguard"] == ""          # forks: no README read
    s = G.summary(rows, hits, "2026-10-30")
    assert "| Nous Research | 2 | 0 | 0 |" in s and "never instructions" in s
    assert by["a/one"]["role"] == "attack" and by["a/one"]["side"] == "attack"


@needs_private
def test_landscape_page_is_current():
    from snapshot import x25report
    assert (ROOT / x25report.OUT).read_text() == x25report.build_text(ROOT)


def test_breakdown_tags():
    r = G.row(_item("o/x", 1, desc="Claude and Qwen agent on CrewAI that attacks AWS IAM and SMB shares over Kerberos"))
    assert r["labs"] == "Anthropic;Alibaba" and r["toolkits"] == "CrewAI"
    assert r["targets"] == "cloud accounts;Windows and Active Directory"
    assert r["protocols"] == "SMB;Kerberos"
    assert G.tags("MQTT and Modbus over OPC UA; A2A agents on BLE", G.PROTOCOLS) == ["MQTT", "Modbus", "OPC UA", "Bluetooth/BLE", "A2A"]


def test_protocol_charts_follow_the_data():
    from snapshot import x25report as X
    k = len(X.PROTOCOLS)
    s = {"protocols": {side: [1 if i < 13 else 0 for i in range(k)] for side in X.SIDES}}
    text = "\n".join(X.protocol_section("d", s))
    assert "13 of the" in text and "2 protocol charts" in text and "d-6-protocols-2.png" in text


def test_individuals_get_stable_codes_and_no_details():
    a, b, org = (G.row(_item(n, 1)) for n in ("alice/tool", "bob/tool", "acme/tool"))
    org["owner_type"] = "Organization"
    reg = G.pseudonymise([a, b, org], {"bob/tool": "ind-00007"})
    assert (b["name"], b["ref"]) == ("tool", "ind-00007") and (a["name"], a["ref"]) == ("tool", "ind-00008")
    assert org["name"] == "acme/tool" and org["ref"] == ""
    assert reg == {"bob/tool": "ind-00007", "alice/tool": "ind-00008"}
    pub = G.public(a)
    assert "full_name" not in pub and "url" not in pub and pub["description"] == ""
    assert "alice" not in " ".join(str(v) for v in pub.values())


@needs_private
def test_public_x25_files_name_no_individual():
    import csv, re
    for f in list((ROOT / "exploratory/ai_tool_sweeps").glob("*.csv")) + [ROOT / "exploratory/ai_attack_tools.csv"]:
        for r in csv.DictReader(f.open()):
            if r.get("owner_type", r.get("maker", "")) not in ("Organization", "organisation"):
                assert "/" not in r["name"], (f.name, r["name"])     # project name, never owner/project


def test_open_weight_by_model_not_lab():
    w = lambda d: G.tags(d, G.WEIGHTS)
    assert w("runs Gemma 3 via Ollama") == ["open-weight", "runs locally"]
    assert w("uses Gemini 2.5 and Claude") == ["closed"]
    assert w("gpt-oss-120b agent") == ["open-weight"] and w("GPT-4o agent") == ["closed"]
    assert w("Hermes on Mistral Large via OpenRouter") == ["open-weight", "closed"]
