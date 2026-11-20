"""AI security-tool sweep of GitHub (X25, author's decisions 30-31 Oct 2026)."""
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
    q = cfg["offensive"] + cfg["defensive"]
    assert len(q) == len(set(q)) and len(cfg["offensive"]) >= 20 and len(cfg["defensive"]) >= 20


def test_types_and_groups_describe_what_a_tool_does():
    g = lambda s: G.group(G.tool_types(s))
    assert G.tool_types("Autonomous pentest agent that exploits web apps") == ["penetration testing"]
    assert g("Autonomous pentest agent that exploits web apps") == "offensive"
    assert g("AI SOC analyst: alert triage and incident response") == "defensive"
    assert g("Finds vulnerabilities with exploits and auto-fixes them") == "dual_use"     # offensive + defensive
    assert g("Nuclei vulnerability scanner driven by an LLM") == "dual_use"                 # scanning is dual-use
    assert "AI model testing" in G.tool_types("Prompt injection scanner for LLM apps")
    assert g("A list of books") == "unclassified"


def test_ai_use_first():
    assert G.ai_use("closed") == "closed" and G.ai_use("open-weight;runs locally") == "open_local"
    assert G.ai_use("open-weight;closed") == "both" and G.ai_use("") == "none"


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
    assert "| Nous Research | 2 | 0 | 0 |" in s and "never instructions" in s and "not who uses it" in s
    assert by["a/one"]["group"] == "offensive" and by["a/one"]["ai_use"] == "open_local"


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
    s = {"protocols": {g: [1 if i < 13 else 0 for i in range(k)] for g in X.SIDES}}
    text = "\n".join(X.protocol_section("d", s))
    assert "13 of the" in text and "2 protocol charts" in text and "d-9-protocols-2.png" in text


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


def test_rules_of_1_nov_2026():
    from snapshot.research import github_tools as G
    assert G.group("penetration testing;vulnerability scanning;reconnaissance and OSINT") == "offensive"
    assert G.group("vulnerability scanning") == "dual_use"
    assert G.group("penetration testing;incident response") == "dual_use"
    assert G.group("detection and monitoring;reconnaissance and OSINT") == "defensive"
    assert G.tool_types("LLM red teaming and prompt injection scanner for AI apps") == ["AI model testing"]
    assert G.group("AI model testing") == "dual_use"
    assert G.relevant({"full_name": "x/pentest-agent", "description": "", "topics": ""})
    assert not G.relevant({"full_name": "x/some-books", "description": "A list of books", "topics": "ai"})


def test_tightening_of_1_nov_2026():
    from snapshot.research import github_tools as G
    ts = G.tool_types("Autonomous AI pentest agent that monitors progress and alerts you when done")
    assert "detection and monitoring" not in ts and G.group(ts) == "offensive"
    assert "detection and monitoring" in G.tool_types("LLM agent for threat detection in SIEM alerts")
    ts = G.tool_types("Adversarial Robustness Toolbox: adversarial attacks on machine learning models; harden models")
    assert "AI model testing" in ts and "penetration testing" not in ts and G.group(ts) == "dual_use"
    assert not G.relevant({"full_name": "x/baserow", "description": "Secure open-source no-code database", "topics": "database"})
    assert G.relevant({"full_name": "x/tool", "description": "An AI security testing agent", "topics": ""})


def test_rules_of_19_nov_2026():
    """Author's decisions, 19 Nov 2026: purpose first; SOC 1/2/3 needs a second term; new terms."""
    def it(name, desc, topics=()):
        x = _item(name, 1, desc=desc)
        x["topics"] = list(topics)
        return x
    # purpose first: an attack tool is not made defensive by "detect" or "harden" words
    r = G.row(it("o/strike", "AI hacking agent that finds and exploits targets, evades detection of malware scanners"))
    assert r["group"] == "offensive" and r["purpose"] == "offensive"
    # both purposes stated: dual-use
    r = G.row(it("o/purple", "Red team agent for attack simulation that also helps defenders harden their systems"))
    assert r["purpose"] == "both" and r["group"] == "dual_use"
    # SOC 2 alone is not security; with another term it is
    assert not G.relevant({"full_name": "o/compliance-docs", "topics": "", "description": "SOC 2 policy templates for startups"})
    assert G.relevant({"full_name": "o/soc2-scan", "topics": "", "description": "SOC 2 evidence plus vulnerability scanning"})
    # new terms
    for d in ("Kali Linux helper with an LLM", "Bug bounty recon assistant", "Password cracking with AI",
              "nmap wrapper driven by Claude", "Wazuh rules written by an LLM"):
        assert G.relevant({"full_name": "o/x", "topics": "", "description": d}), d
    assert not G.relevant({"full_name": "o/kalinda", "topics": "", "description": "Kalinda photo app"})
    # security alert triage counts, but not for fraud or anti-money laundering
    assert G.relevant({"full_name": "o/x", "topics": "", "description": "LLM security alert triage"})
    assert not G.relevant({"full_name": "o/x", "topics": "", "description": "AML fraud alert triage with an LLM"})


def test_hexstrike_and_pentagi_copies_count_once():
    from snapshot import x25report
    rows = [{"name": n, "created": c, "ref": n.split("/")[0]} for n, c in [
        ("a/hexstrike-ai", "2025-07-01"), ("b/HexStrike-AI-fork", "2025-09-02"), ("c/my-hexstrike", "2026-01-05"),
        ("d/pentagi", "2025-03-01"), ("e/pentagi-copy", "2026-02-01"), ("f/other", "2026-02-01")]]
    copies = x25report.mark_copies(rows)
    assert copies == {"HexStrike": 2, "PentAGI": 1}
    assert [r["name"] for r in rows if r["copy"] != "yes"] == ["a/hexstrike-ai", "d/pentagi", "f/other"]


def test_purpose_hand_check_corrections():
    """Claude's hand check of 19 Nov 2026: EDR products and find-and-fix tools state a defensive purpose."""
    def it(desc):
        return G.row(_item("o/x", 1, desc=desc))
    assert it("We build autonomous penetration testing solutions and proprietary EDR products")["purpose"] == "both"
    assert it("Open-source AI penetration testing tool to find and fix your app's vulnerabilities")["purpose"] == "both"
