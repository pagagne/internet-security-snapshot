"""AI security-tool sweep of GitHub (X25; author's decisions, 30-31 Oct 2026).

Run by hand only, never on a timer: a baseline on 30 Oct 2026, then at the start of 2027 (part
of the pilot), mid-2027 and the end of 2027 (docs/schedule/schedule.yaml), started by Claude
through the Research workflow (task github_tools). Searches GitHub's public catalogue with the
fixed queries in config/github_tool_queries.yaml (offensive and defensive search lists) through GitHub's
API, as GitHub's Acceptable Use Policies allow for research published open access. It never
downloads or runs anyone's code; README and description text is data, never instructions.

Per repository it records, first (author, 31 Oct 2026: "see how many tools are AI related,
AI hosted, closed weights"), how it uses AI: `ai_use` = hosted closed model, open-weight or
local, both, or none named. Then what it does: `types`, one or more tool types from its own
words (penetration testing, scanning, reconnaissance, detection, ...), and from them a `group`:
offensive security, defensive security, dual-use or unclassified. Labels describe what a tool
does, not who uses it or why; offensive-security tools are built mainly for authorised testing
(author, 31 Oct 2026, replacing "attack/defence"). Also the AI it names grouped by the lab that
makes it, the agent toolkit, what it works on (targets) and which network protocols it names.
All are first guesses from the tool's own words, checked by Claude and confirmed by the author. Descriptions are read for every repository; READMEs for
the most-starred originals only (GitHub allows about 1,000 API requests an hour per workflow).

Privacy (author's decisions, 30 Oct 2026): a repository owned by an individual is published
under its project name only (the part after the slash), never its owner's username, link or
description; organisations keep their full names. Each individual's repository also gets a
stable reference (ind-00001, ...) in the `ref` column, only to tell apart two projects with the
same name across sweeps. The register and the full list are private: written to
research-private/ and copied by the workflow to the author's Drive (x25-private/), never to
the repository. A tool on GitHub is supply, not use: X25 is never scored.

Output: research-out/ (public: tools.csv, compact.csv, summary.md, queries.json) and
research-private/ (registry.csv, tools_full.csv).
"""
from __future__ import annotations

import argparse
import base64
import collections
import csv
import datetime as dt
import json
import os
import re
import time
from pathlib import Path

import requests
import yaml

from ..collect.http import UA, note_status
from ..util import _repo_root

API = "https://api.github.com"
CONFIG = "config/github_tool_queries.yaml"
PER_PAGE, MAX_PAGES = 100, 10      # GitHub returns at most 1,000 results per search
README_TOP = 800                   # READMEs read for the most-starred originals (API allowance)
REGISTRY_IN = os.environ.get("X25_REGISTRY", "research-private-in/registry.csv")
PRIVATE_OUT = Path(os.environ.get("X25_PRIVATE_OUT", "research-private"))

LABS = {   # AI named in a description or README, grouped by the lab that makes it
    "OpenAI": r"\bgpt-?[345]|\bopenai\b|\bchatgpt\b|\bcodex\b",
    "Anthropic": r"\bclaude\b|\banthropic\b",
    "Google": r"\bgemini\b|\bgemma\b|\bvertex ai\b",
    "Meta": r"\bllama[- ]?[234]|\bllama\b(?!\.cpp|index)",
    "Mistral": r"\bmistral\b|\bmixtral\b|\bcodestral\b",
    "DeepSeek": r"\bdeepseek\b",
    "Alibaba": r"\bqwen\b|\btongyi\b",
    "Nous Research": r"\bhermes\b",
    "Moonshot": r"\bkimi\b|\bmoonshot\b",
    "Zhipu": r"\bchatglm\b|\bglm-?[45]|\bzhipu\b",
    "xAI": r"\bgrok\b",
    "Microsoft": r"\bphi-?[234]\b",
    "Local runner": r"\bollama\b|\bllama\.cpp\b|\blm studio\b|\bvllm\b",
}
WEIGHTS = {   # open-weight against closed, decided by model, not lab (author, 30 Oct 2026)
    "open-weight": r"\bllama\b(?!\.cpp|index)|\bqwen|\bdeepseek|\bmistral\b(?! large)|\bmixtral\b|\bhermes\b|\bgemma\b|"
                   r"\bgpt-?oss\b|\bphi-?[234]\b|\bchatglm\b|\bglm-?[45]|\bkimi\b|\bfalcon\b|\bolmo\b|\bstarcoder|"
                   r"open.?weights?\b|open-source (llm|model)s?|local (llm|model)s?|self-hosted (llm|model)s?",
    "closed": r"\bgpt-?[345](?!-?oss)|\bchatgpt\b|\bopenai api\b|\bclaude\b|\bgemini\b|\bgrok\b|mistral large|"
              r"\bo[134](-mini)?\b(?= model)",
    "runs locally": r"\bollama\b|\bllama\.cpp\b|\blm studio\b|\bvllm\b|\blocalai\b|run(s|ning)? locally|offline (llm|model)",
}
TOOLKITS = {
    "MCP": r"\bmcp\b|model context protocol", "LangChain": r"\blangchain\b|\blanggraph\b",
    "CrewAI": r"\bcrewai\b", "AutoGen": r"\bautogen\b|\bag2\b", "LlamaIndex": r"\bllamaindex\b|\bllama.index\b",
    "Semantic Kernel": r"semantic kernel", "OpenAI Agents SDK": r"openai agents sdk|openai-agents",
    "Claude Code / Agent SDK": r"claude code|claude agent sdk|claude-agent-sdk", "smolagents": r"\bsmolagents\b",
    "PydanticAI": r"pydantic.?ai\b",
}
TARGETS = {   # what a tool works on (tests, scans or protects)
    "web apps and APIs": r"web ?app|website|\bxss\b|sql ?injection|\bsqli\b|\bowasp\b|\bburp\b|api security|\brest api\b",
    "cloud accounts": r"\baws\b|\bazure\b|\bgcp\b|google cloud|\bs3\b|\biam\b|cloud security|\bcspm\b",
    "Windows and Active Directory": r"active directory|\bkerberos\b|\bldap\b|\bbloodhound\b|\bntlm\b|\bwindows\b",
    "networks and hosts": r"\bnmap\b|port scan|network scan|\binternal network\b|\bhosts?\b scan|\bwi-?fi\b|wireless|bluetooth",
    "containers and Kubernetes": r"\bdocker\b|\bkubernetes\b|\bk8s\b|\bcontainers?\b",
    "mobile apps": r"\bandroid\b|\bios\b|mobile app|\bapk\b",
    "industrial and IoT": r"\bics\b|\bscada\b|\bmodbus\b|\bplc\b|\biot\b|\bot security\b|firmware|embedded",
    "source code and supply chain": r"source code|\bsast\b|dependenc(y|ies)|supply chain|\bnpm\b|\bpypi\b|github actions|ci/cd|code review",
    "email and people": r"phishing|social engineering|\bemail security\b",
    "endpoints and logs": r"\bedr\b|endpoint|\bsiem\b|\blogs?\b analysis|\bsysmon\b|event logs?",
}
PROTOCOLS = {   # a wide net (author, 30 Oct 2026): only protocols actually found are charted
    # web and APIs
    "HTTP/HTTPS": r"\bhttps?\b", "TLS/SSL": r"\btls\b|\bssl\b", "WebSocket": r"\bwebsockets?\b",
    "GraphQL": r"\bgraphql\b", "gRPC": r"\bgrpc\b", "OAuth/OIDC": r"\boauth\b|\boidc\b|openid connect",
    "SAML": r"\bsaml\b", "JWT": r"\bjwt\b",
    # remote access and file sharing
    "SSH": r"\bssh\b", "RDP": r"\brdp\b", "VNC": r"\bvnc\b", "Telnet": r"\btelnet\b", "WinRM": r"\bwinrm\b",
    "SMB": r"\bsmb\b", "FTP/SFTP": r"\bs?ftp\b", "NFS": r"\bnfs\b", "RPC/MSRPC": r"\bms-?rpc\b|\brpc\b",
    # Windows identity
    "LDAP": r"\bldaps?\b", "Kerberos": r"\bkerberos\b", "NTLM": r"\bntlm\b",
    # network plumbing
    "DNS": r"\bdns\b", "DHCP": r"\bdhcp\b", "ARP": r"\barp\b", "ICMP": r"\bicmp\b", "BGP": r"\bbgp\b",
    "OSPF": r"\bospf\b", "SNMP": r"\bsnmp\b", "NTP": r"\bntp\b", "IPv6": r"\bipv6\b", "VPN/IPsec": r"\bvpn\b|\bipsec\b|\bwireguard\b",
    # mail and messaging
    "SMTP": r"\bsmtp\b", "IMAP/POP3": r"\bimap\b|\bpop3\b", "SIP/VoIP": r"\bsip\b|\bvoip\b",
    "AMQP": r"\bamqp\b", "XMPP": r"\bxmpp\b",
    # industrial and IoT
    "MQTT": r"\bmqtt\b", "CoAP": r"\bcoap\b", "Modbus": r"\bmodbus\b", "DNP3": r"\bdnp3\b",
    "BACnet": r"\bbacnet\b", "OPC UA": r"\bopc[ -]?ua\b", "S7comm": r"\bs7(comm)?\b",
    "Zigbee": r"\bzigbee\b", "LoRaWAN": r"\blora(wan)?\b", "CAN bus": r"\bcan ?bus\b",
    # wireless
    "Wi-Fi/802.11": r"\bwi-?fi\b|802\.11|\bwpa[23]?\b", "Bluetooth/BLE": r"\bbluetooth\b|\bble\b",
    "RFID/NFC": r"\brfid\b|\bnfc\b", "Cellular (LTE/5G)": r"\blte\b|\b5g\b|\bgsm\b",
    # databases and services spoken on the wire
    "SQL databases": r"\bmysql\b|\bpostgres(ql)?\b|\bmssql\b|\boracle db\b", "Redis": r"\bredis\b",
    "MongoDB": r"\bmongodb\b", "Elasticsearch": r"\belasticsearch\b", "Docker API": r"docker (api|socket|daemon)",
    "Kubernetes API": r"kubernetes api|\bkube-?apiserver\b",
    # AI agent protocols
    "MCP": r"\bmcp\b|model context protocol", "A2A": r"\ba2a\b|agent2agent|agent-to-agent protocol",
}

TYPES = {   # what a tool does (author, 31 Oct 2026); a tool can have several
    "penetration testing": r"pen.?test|penetration|exploit|red.?team|offensive|post.?exploit|privilege escalation|"
                           r"\bc2\b|command.and.control|bug.?bount|\bctf\b|hack(ing|er|s)?\b|渗透|пентест|взлом",
    "vulnerability scanning": r"vulnerabilit\w* scan|scanner|\bnuclei\b|\bdast\b|fuzz|漏洞扫描",
    "reconnaissance and OSINT": r"\brecon|\bosint\b|subdomain|asset discovery|footprint|attack surface|情报收集",
    "phishing simulation": r"phishing|social engineering",
    "malware analysis": r"malware|reverse engineer|\byara\b|\bghidra\b|\bida pro\b|sandbox analysis",
    # phrases only (author, 1 Nov 2026): bare "detect", "monitor" and "alert" also describe attack
    # agents watching their own progress
    "detection and monitoring": r"(threat|intrusion|anomal\w*|malware|attack|phishing|fraud|breach|ransomware|exploit) detect\w*|"
                                r"detect\w* (of )?(threats?|intrusions?|attacks?|malware|anomal\w*|phishing|fraud|ransomware)|"
                                r"security (monitoring|alerts?|operations)|monitor\w* (for )?(threats?|attacks?|security)|"
                                r"\bsoc\b|\bsiem\b|\bedr\b|\bxdr\b|alert triage|\bsigma rules?\b|log analysis|threat hunt|检测",
    "code security review": r"code review|\bsast\b|static analysis|secure cod|secret scan|dependenc(y|ies) (scan|audit)|"
                            r"supply.chain security|auto.?fix|remediat",
    "threat intelligence": r"threat intel|\bcti\b|\biocs?\b|indicators? of compromise",
    "incident response": r"incident response|\bdfir\b|forensic|triage|应急",
    "hardening and compliance": r"harden|compliance|posture|vulnerability management|patch management|blue.?team|"
                                r"cyber.?defen[cs]e|defensive security|防御|защит",
    "AI model testing": r"prompt.?injection|jailbreak|guardrail|llm (vulnerabilit|red.?team|security test|fuzz)|"
                        r"red.?team(ing)? (for |of )?(llms?|ai models?|language models?|chatbots?|ai apps?)|model (safety|evaluation|robustness)|"
                        r"adversarial (robustness|machine learning|ml\b|examples?|attacks? (on|against) (ml|ai|models?|neural))",
}
MODEL_TESTING = re.compile(TYPES["AI model testing"], re.I)   # also used by the Hugging Face sweep
OFFENSIVE = {"penetration testing", "phishing simulation"}
DUAL = {"vulnerability scanning", "reconnaissance and OSINT", "AI model testing"}
GROUPS = ["offensive", "defensive", "dual_use", "unclassified"]
GROUP_NAMES = {"offensive": "Offensive security", "defensive": "Defensive security", "dual_use": "Dual-use",
               "unclassified": "Unclassified"}
AI_USE = ["closed", "open_local", "both", "none"]
AI_USE_NAMES = {"closed": "Hosted closed model", "open_local": "Open-weight or local", "both": "Both kinds",
                "none": "No model named"}

SAFEGUARD = re.compile(r"\b(scope|authori[sz](ed|ation)|permission|consent|allow-?list|in-scope|rules of engagement)\b", re.I)
NO_SAFEGUARD = re.compile(r"\bno (scope|authori[sz]ation|consent|guard)", re.I)


PUBLIC = ["name", "ref", "owner_type", "created", "pushed", "stars", "forks", "archived", "license", "language",
          "ai_use", "types", "group", "labs", "weights", "toolkits", "targets", "protocols", "readme_read", "readme_safeguard",
          "crypto", "topics", "description"]
COMPACT = ["name", "ref", "owner_type", "created", "stars", "forks", "ai_use", "types", "group", "labs", "weights", "toolkits", "targets",
           "protocols", "readme_read", "readme_safeguard", "crypto"]


def tool_types(text: str) -> list[str]:
    """What a tool does, from its own words (first guesses; checked by Claude, confirmed by the author).
    A tool that tests AI models is "AI model testing", not penetration testing or scanning: its
    red-teaming and scanning words are about the model (author, 1 Nov 2026)."""
    ts = tags(text, TYPES)
    return _model_testing_first(ts)


def _model_testing_first(ts: list[str]) -> list[str]:
    if "AI model testing" in ts:
        ts = [t for t in ts if t not in ("penetration testing", "vulnerability scanning")]
    return ts


def group(types: list[str] | str) -> str:
    """Offensive, defensive or dual-use, worked out from the tool types, never from intent.

    Rule of 1 Nov 2026 (author): scanning and reconnaissance are steps of an attack, so beside
    penetration testing they no longer make a tool dual-use; they count as dual-use only when they
    are a tool's only types. A tool with both offensive and defensive types stays dual-use, and so
    does a tool that only tests AI models."""
    ts = set(filter(None, types.split(";") if isinstance(types, str) else types))
    if not ts:
        return "unclassified"
    if "AI model testing" in ts:   # a model tester is not made defensive by hardening or monitoring words (1 Nov 2026)
        ts = ts - {"hardening and compliance", "detection and monitoring"}
    off, deff = bool(ts & OFFENSIVE), bool(ts - OFFENSIVE - DUAL)
    if off and deff:
        return "dual_use"
    if off:
        return "offensive"
    if deff:
        return "defensive"
    return "dual_use"           # only supporting types (scanning, reconnaissance) or AI model testing


def ai_use(weights: str) -> str:
    """How the tool uses AI: a hosted closed model, an open-weight or local one, both, or none named."""
    w = set(filter(None, weights.split(";")))
    op, cl = bool(w & {"open-weight", "runs locally"}), "closed" in w
    return "both" if op and cl else "closed" if cl else "open_local" if op else "none"


def finish(r: dict) -> None:
    r["types"] = ";".join(_model_testing_first([x for x in r["types"].split(";") if x]))
    r["group"] = group(r["types"])
    r["ai_use"] = ai_use(r["weights"])


# Relevance (author, 1 Nov 2026): a result counts only if a security term appears in its name,
# description or topics; book lists, political repositories and general apps found through a
# search's AI words are left out and counted as "not security" in the summary.
RELEVANT = re.compile(r"secur|pen.?test|penetration|exploit|vulnerab|\bcve\b|malware|phish|threat|red.?team|blue.?team|"
                      r"\bsoc\b|siem|intrusion|forensic|incident|hack|offensive|defen[cs]|ctf|osint|recon|fuzz|"
                      r"jailbreak|prompt.?injection|guardrail|attack|scanner|audit|cyber|渗透|安全|漏洞|пентест|безопасн|взлом", re.I)
# Tightened 1 Nov 2026 (author): in the description a passing word such as "secure" is not enough;
# it needs a security phrase or a specific security term
DESC_RELEVANT = re.compile(r"security (tool|testing|test|research|scanner|scan|audit|analysis|operations|team|assessment|agent|"
                           r"automation|copilot|assistant|framework|platform|monitoring)|cyber.?security|infosec|pen.?test|"
                           r"penetration|exploit|vulnerab|\bcve\b|malware|phishing|intrusion|threat|red.?team|blue.?team|"
                           r"\bsoc\b|siem|forensic|incident response|hacking|offensive security|\bctf\b|osint|fuzz|"
                           r"jailbreak|prompt.?injection|guardrail|attack surface|cyber.?attack|渗透|漏洞|网络安全|пентест|взлом", re.I)


LEFT_OUT: list[str] = []


def relevant(r: dict) -> bool:
    name_topics = r.get("full_name", "").replace("-", " ").replace("_", " ") + " " + r.get("topics", "")
    return bool(RELEVANT.search(name_topics) or DESC_RELEVANT.search(r.get("description", "")))


def tags(text: str, table: dict) -> list[str]:
    t = text.lower()
    return [k for k, rx in table.items() if re.search(rx, t, re.I)]


def safeguard(readme: str) -> str:
    if NO_SAFEGUARD.search(readme):
        return "says none"
    return "mentions" if SAFEGUARD.search(readme) else "not mentioned"


def gh(path: str, params: dict | None = None) -> requests.Response:
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    for _ in range(4):
        r = requests.get(API + path, params=params, headers=h, timeout=60)
        note_status(API + path, r.status_code)
        if r.status_code in (403, 429) and "rate limit" in r.text.lower():
            reset = int(r.headers.get("x-ratelimit-reset", time.time() + 60))
            time.sleep(min(max(reset - time.time(), 5), 900) + 1)
            continue
        return r
    return r


def search(query: str, pause: float = 2.5) -> list[dict]:
    items = []
    for page in range(1, MAX_PAGES + 1):
        time.sleep(pause)
        r = gh("/search/repositories", {"q": query, "per_page": PER_PAGE, "page": page, "sort": "stars"})
        if r.status_code != 200:
            break
        batch = r.json().get("items", [])
        items += batch
        if len(batch) < PER_PAGE:
            break
    return items


def _readme(full_name: str) -> str:
    r = gh(f"/repos/{full_name}/readme")
    if r.status_code != 200:
        return ""
    try:
        return base64.b64decode(r.json().get("content", "")).decode("utf-8", "replace")
    except (ValueError, KeyError):
        return ""


def _label(r: dict, text: str) -> None:
    for field, table in (("types", TYPES), ("labs", LABS), ("weights", WEIGHTS), ("toolkits", TOOLKITS), ("targets", TARGETS),
                         ("protocols", PROTOCOLS)):
        r[field] = ";".join(sorted(set(filter(None, r[field].split(";"))) | set(tags(text, table)),
                                   key=list(table).index))


def row(it: dict) -> dict:
    desc = (it.get("description") or "").replace("\n", " ")
    topics = it.get("topics") or []
    r = {
        "full_name": it["full_name"], "url": it.get("html_url", ""), "name": "",
        "owner_type": (it.get("owner") or {}).get("type", ""),
        "created": (it.get("created_at") or "")[:10], "pushed": (it.get("pushed_at") or "")[:10],
        "stars": it.get("stargazers_count", 0), "forks": it.get("forks_count", 0),
        "is_fork": it.get("fork", False), "archived": it.get("archived", False),
        "license": ((it.get("license") or {}).get("spdx_id") or ""), "language": it.get("language") or "",
        "topics": ";".join(topics), "description": desc[:240],
        "queries": "", "types": "", "group": "", "ai_use": "", "labs": "", "weights": "", "toolkits": "", "targets": "", "protocols": "",
        "readme_read": "no", "readme_safeguard": "",
    }
    _label(r, it.get("name", "") + " " + desc + " " + " ".join(topics))
    from .crypto_tag import is_crypto
    r["crypto"] = "yes" if is_crypto(it.get("name", ""), desc, " ".join(topics)) else "no"
    finish(r)
    return r


def sweep(queries, pause: float = 2.5, search_fn=search, readme_fn=None, readme_top: int = README_TOP):
    """queries: {"offensive": [...], "defensive": [...]} (search lists; a plain list is one list)."""
    if isinstance(queries, list):
        queries = {"offensive": queries}
    found, hits = {}, {}
    for side, qs in queries.items():
        for q in qs:
            items = search_fn(q, pause)
            hits[q] = len(items)
            for it in items:
                r = found.setdefault(it["full_name"], row(it))
                r["queries"] = ";".join(filter(None, [r["queries"], q]))
    dropped = [r for r in found.values() if not relevant(r)]
    LEFT_OUT[:] = [r["full_name"] for r in dropped]   # counted in the summary, never in a chart
    rows = sorted((r for r in found.values() if relevant(r)), key=lambda r: -r["stars"])
    readme_fn = readme_fn or _readme
    for r in [r for r in rows if not r["is_fork"]][:readme_top]:
        time.sleep(pause / 5)
        text = readme_fn(r["full_name"])
        if not text:
            r["readme_safeguard"] = "no readme"
            continue
        r["readme_read"] = "yes"
        r["readme_safeguard"] = safeguard(text)
        _label(r, text[:30000])
        finish(r)
    return rows, hits


def pseudonymise(rows: list[dict], registry: dict[str, str]) -> dict[str, str]:
    """Organisations keep their full names; an individual's repository is shown by its project
    name, with a stable reference from the private register (new references continue the
    numbering). Returns the updated register."""
    reg = dict(registry)
    nxt = max((int(c[4:]) for c in reg.values() if re.fullmatch(r"ind-\d{5}", c)), default=0) + 1
    for r in sorted(rows, key=lambda r: (r["created"], r["full_name"])):
        if r["owner_type"] == "Organization":
            r["name"], r["ref"] = r["full_name"], ""
            continue
        if r["full_name"] not in reg:
            reg[r["full_name"]] = f"ind-{nxt:05d}"
            nxt += 1
        r["name"], r["ref"] = r["full_name"].split("/", 1)[1], reg[r["full_name"]]
    return reg


def public(r: dict) -> dict:
    out = {k: r.get(k, "") for k in PUBLIC}
    if r["owner_type"] != "Organization":
        out["description"] = ""            # may name or describe the person
    return out


def summary(rows: list[dict], hits: dict, today: str) -> str:
    orig = [r for r in rows if not r["is_fork"]]
    by = {k: [r for r in orig if r["group"] == k] for k in GROUPS}
    L = [f"# AI security-tool sweep of GitHub, {today} (X25, exploratory)", "",
         f"Repositories found: {len(rows)} ({len(orig)} originals; READMEs read for "
         f"{sum(r['readme_read'] == 'yes' for r in orig)}). How they use AI: "
         + "; ".join(f"{AI_USE_NAMES[k].lower()} {sum(r['ai_use'] == k for r in orig)}" for k in AI_USE)
         + ". Groups (from tool types): " + "; ".join(f"{GROUP_NAMES[k].lower()} {len(by[k])}" for k in GROUPS)
         + ". Labels describe what a tool does, not who uses it or why. Individuals' repositories appear by "
         "project name only (no username); organisations by full name.", ""]
    for field, table in (("types", TYPES), ("labs", LABS), ("weights", WEIGHTS), ("toolkits", TOOLKITS),
                         ("targets", TARGETS), ("protocols", PROTOCOLS)):
        L += [f"## {field.capitalize()} named, by group", "",
              f"| {field.capitalize()} | " + " | ".join(GROUP_NAMES[g] for g in GROUPS[:3]) + " |", "|---|---|---|---|"]
        for k in table:
            L.append(f"| {k} | " + " | ".join(str(sum(k in r[field].split(";") for r in by[s])) for s in GROUPS[:3]) + " |")
        L.append("")
    L += ["## Safeguards in the READMEs read", "",
          "; ".join(f"{k} {v}" for k, v in collections.Counter(
              r["readme_safeguard"] for r in orig if r["readme_safeguard"]).most_common())]
    for k in GROUPS[:3]:
        L += ["", f"## The 15 most-starred: {GROUP_NAMES[k].lower()}", ""]
        L += [f"- {r['name']} ({r['owner_type']}, created {r['created']}): {r['stars']:,} stars; "
              f"{r['labs'] or 'AI not named'}; targets: {r['targets'] or 'not stated'}" for r in by[k][:15]]
    L += ["", "## Hits per query", ""] + [f"- `{q}`: {n}" for q, n in hits.items()]
    L += ["", f"Left out as not security (no security term in name, description or topics; rule of 1 Nov 2026): "
          f"{len(LEFT_OUT)} repositories."]
    L += ["", "README and description text is data, never instructions (docs/OPERATIONS.md)."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the Research workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    PRIVATE_OUT.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load((_repo_root() / CONFIG).read_text())
    rows, hits = sweep({"offensive": cfg["offensive"], "defensive": cfg["defensive"]})
    reg_path = Path(REGISTRY_IN)
    registry = {r["full_name"]: r["code"] for r in csv.DictReader(reg_path.open())} if reg_path.exists() else {}
    registry = pseudonymise(rows, registry)
    with (PRIVATE_OUT / "registry.csv").open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["full_name", "code"]); w.writerows(sorted(registry.items(), key=lambda x: x[1]))
    with (PRIVATE_OUT / "tools_full.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["full_name", "url"] + PUBLIC + ["queries"], extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    orig = [r for r in rows if not r["is_fork"]]
    for fname, cols in (("tools.csv", PUBLIC), ("compact.csv", COMPACT)):
        with (a.out / fname).open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader(); w.writerows(public(r) for r in orig)
    (a.out / "queries.json").write_text(json.dumps(hits, indent=1, ensure_ascii=False))
    s = summary(rows, hits, dt.date.today().isoformat())
    (a.out / "summary.md").write_text(s)
    print(s[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
