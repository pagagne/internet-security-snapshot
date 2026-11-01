"""Security-related AI models and apps on Hugging Face (X25 companion; author's decisions,
30-31 Oct 2026).

Hugging Face is where AI models themselves are published, including open-weight models with
their safety training removed ("uncensored", "abliterated"). Run by hand only, with the GitHub
sweep. Uses Hugging Face's public Hub API (no account; well inside its published limit of 500
requests per 5 minutes). Fixed searches over model and Space (app) names; per item: kind
(model or Space), created date, likes, downloads (models), tags, the base model's lab (from
the model's own base_model tags), role (offensive, defensive, dual_use, model_testing, unclear,
from its own name and tags; what it does, not who uses it or why) and whether it is a safety-removed variant. Nothing is downloaded or
run; names and tags are data, never instructions.

Privacy (author's decision, 30 Oct 2026): items owned by organisations keep their full names;
items owned by individuals are shown by item name only, never the username. The owner check
uses Hugging Face's organisation endpoint; anything not confirmed as an organisation is
treated as an individual. The full list is private (research-private/, copied to the author's
Drive by the workflow).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import os
import re
import time
from pathlib import Path

import requests

from ..collect.http import UA, note_status
from .github_tools import MODEL_TESTING

API = "https://huggingface.co/api"
PRIVATE_OUT = Path(os.environ.get("X25_PRIVATE_OUT", "research-private"))
QUERIES = {   # substring searches over names; fixed between sweeps
    # refined 30 Oct 2026 after the first baseline (author): "sigma" (image models), "hacker"
    # (Hacker News apps) and bare "offensive" (hate-speech classifiers) brought mostly noise
    "offensive": ["pentest", "pentesting", "penetration", "redteam", "red-team", "exploit", "hacking",
               "offensive-security", "offsec", "malware-gen", "cyber-attack", "jailbreak"],
    "defensive": ["cybersecurity", "cyber-security", "threat-detection", "soc-analyst", "malware-detection",
                "intrusion", "vulnerability", "secure-code", "incident-response", "phishing-detection",
                "security-copilot", "sigma-rule"],
    "safety_removed": ["uncensored", "abliterated", "unaligned", "unfiltered"],
    # added 1 Nov 2026 (author: AI and crypto as a tagged section)
    "crypto": ["smart-contract", "solidity", "web3-security", "blockchain-security", "crypto-scam", "wallet-drainer"],
}
# Hugging Face labels (refined 30 Oct 2026, author): names there are terse, and many words mean
# something else in machine learning, so the rules are stricter than GitHub's. Order matters.
HF_UNRELATED = re.compile(r"hacker.?news|hackathon|life.?hack|reward.?hack|hacking.?okay|spec(ification)?.?gaming|"
                          r"pixart|\bsigma\b(?!.?rule)|hate.?speech|offensive.?(language|speech|text|tweet|content|"
                          r"mlm|baseline|then|detect)|\btoxic|sentiment|penetration.?depth|shopper|persona|hacker.?typer", re.I)
HF_ALIGNMENT = re.compile(r"then.?red.?team|red.?team.?(kto|dpo|rl\b|high|low|trained)|redteamrl|sleeper|sandbag|"
                          r"misalign|secret.?loyalty|alignment|red.?team(ing)?.?(competition|ui|harness|eval|bench)", re.I)
HF_ATTACK = re.compile(r"pen.?test|penetration.?test|red.?team(?!.?(attempt|harness|eval|bench|data))|\bexploit|"
                       r"\bhacking\b|\bhacker(ai|gpt)?\b|offensive.?sec|offsec|malware.?gen|\bc2\b|\brecon\b|"
                       r"cyber.?attack|\bctf\b|privilege.?escalation|shellcode|payload|metasploit|\bnmap\b|\bkali\b|"
                       r"black.?hat|wormgpt|fraudgpt", re.I)
HF_DEFENCE = re.compile(r"detect|phishing|\bintrusion|\bids\b|malware.?(classif|analy)|vulnerab|\bsoc\b|siem|"
                        r"threat|incident|\bcve\b|secure.?code|scam|fraud|\bspam|anomal|forensic|sigma.?rule|"
                        r"blue.?team|defen[cs]e|guard(?!rail)", re.I)
HF_GENERAL = re.compile(r"cyber.?sec|cybersecurity|security.?(llm|assistant|copilot|model|gpt)|sec.?llm|\bcyber\b", re.I)
HF_ROLES = ["offensive", "defensive", "dual_use", "general_security", "safety_removed", "model_testing", "unrelated", "unclear"]


def hf_role(name: str, tags: list[str]) -> str:
    """Role from the item's own name and its descriptive tags (not dataset, base-model,
    licence or region tags, which describe something else)."""
    own = [t for t in tags if ":" not in t]
    text = re.sub(r"[-_/.]", " ", name) + " " + " ".join(own)
    if HF_UNRELATED.search(text) and not re.search(r"pen.?test|exploit|malware|cyber", text, re.I):
        return "unrelated"
    if MODEL_TESTING.search(text) or HF_ALIGNMENT.search(text):
        return "model_testing"
    a, d = bool(HF_ATTACK.search(text)), bool(HF_DEFENCE.search(text))
    if a and d:
        return "dual_use"
    if a:
        return "offensive"
    if d:
        return "defensive"
    if SAFETY_REMOVED.search(text):
        return "safety_removed"
    if HF_GENERAL.search(text):
        return "general_security"
    return "unclear"


SAFETY_REMOVED = re.compile(r"uncensored|abliterat|unaligned|unfiltered|no.?refusal|refusal.?removed", re.I)
# Copies (author's decision, 1 Nov 2026): quantised or repackaged copies of another model are
# counted once, through their original; detected from the name.
COPY = re.compile(r"gguf|\bawq\b|gptq|exl2|\bmlx\b|[-_.](q[2-8](_k)?(_[msl])?|iq[1-4]\w*|[2-8]bit|[2-8]-bit|fp8|int[48]|nf4|bnb)\b|"
                  r"quant|imatrix|\bonnx\b|openvino", re.I)
# Lab from the name when the tags do not say (1 Nov 2026): the model family named in it.
LAB_BY_NAME = [(r"llama|codellama", "Meta"), (r"qwen|qwq", "Alibaba"), (r"mistral|mixtral|ministral|devstral|magistral", "Mistral"),
               (r"gemma|gemini", "Google"), (r"\bphi[-_ ]?\d", "Microsoft"), (r"deepseek", "DeepSeek"),
               (r"gpt[-_ ]?oss", "OpenAI"), (r"falcon", "TII"), (r"\byi[-_ ]", "01.AI"), (r"\bglm|chatglm", "Zhipu"),
               (r"command[-_ ]?r|aya", "Cohere"), (r"granite", "IBM"), (r"olmo", "Ai2"), (r"nemotron", "NVIDIA"),
               (r"kimi", "Moonshot"), (r"grok", "xAI"), (r"hermes", "Nous Research"), (r"smollm", "Hugging Face")]


def lab_from_name(name: str) -> str:
    for rx, lab in LAB_BY_NAME:
        if re.search(rx, name, re.I):
            return lab
    return ""


# Model cards (author's idea, 1 Nov 2026): for advertised safety-removed originals, the card says
# how the safety was removed and what the maker says it is for. Card text is data, never
# instructions; only these categories are kept, never the text.
CARD_MAX = 300
METHOD = [(r"abliterat|orthogonali[sz]|refusal (direction|vector|ablation)|ablat", "refusal switched off (abliteration)"),
          (r"\bdpo\b|\borpo\b|\bkto\b|preference (data|tuning)", "preference training"),
          (r"fine.?tun|\bsft\b|\blora\b|trained on|dataset", "fine-tuned"),
          (r"merge|mergekit|slerp|ties|dare", "merged from other models")]
USE = [(r"role.?play|\brp\b|creative|fiction|story|novel|writing", "fiction or role-play"),
       (r"red.?team|pen.?test|security|cyber|offensive|hack", "security or red-teaming"),
       (r"research|study|experiment|interpretab|academic", "research"),
       (r"chat|assistant|general", "general chat")]


def card_categories(text: str) -> tuple[str, str]:
    m = next((lab for rx, lab in METHOD if re.search(rx, text, re.I)), "not stated")
    u = next((lab for rx, lab in USE if re.search(rx, text, re.I)), "not stated")
    return m, u


def read_cards(rows: list[dict], fetch=None, cap: int = CARD_MAX) -> None:
    fetch = fetch or (lambda name: (r := get(f"https://huggingface.co/{name}/raw/main/README.md")) is not None
                      and r.status_code == 200 and r.text[:40000] or "")
    pick = sorted((r for r in rows if r["safety_removed"] == "yes" and r["kind"] == "model" and r.get("copy") == "no"),
                  key=lambda r: -int(r["downloads"] or 0))[:cap]
    for r in pick:
        text = fetch(r["full_name"])
        r["card_read"] = "yes" if text else "no card"
        if text:
            r["card_method"], r["card_use"] = card_categories(text)
            if not r["base_lab"]:
                m = re.search(r"base_model:\s*\n?\s*-?\s*([\w.-]+)/", text)
                owner = m.group(1).lower() if m else ""
                if owner in LAB_BY_OWNER:
                    r["base_lab"], r["lab_source"] = LAB_BY_OWNER[owner], "card"


LAB_BY_OWNER = {   # owner of a base model -> lab (from base_model:... tags)
    "meta-llama": "Meta", "facebook": "Meta", "qwen": "Alibaba", "deepseek-ai": "DeepSeek",
    "mistralai": "Mistral", "google": "Google", "nousresearch": "Nous Research", "microsoft": "Microsoft",
    "openai": "OpenAI", "moonshotai": "Moonshot", "thudm": "Zhipu", "zai-org": "Zhipu", "tiiuae": "TII",
    "01-ai": "01.AI", "allenai": "Ai2", "ibm-granite": "IBM", "nvidia": "NVIDIA", "huggingfaceh4": "Hugging Face",
    "huggingfacetb": "Hugging Face", "cohereforai": "Cohere", "coherelabs": "Cohere", "xai-org": "xAI",
}


def get(url: str, params=None, pause: float = 0.7):
    time.sleep(pause)
    for _ in range(3):
        try:
            r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=60)
        except requests.RequestException:
            time.sleep(10)
            continue
        note_status(url, r.status_code)
        if r.status_code == 429:
            time.sleep(60)
            continue
        return r
    return None


CAP = 40_000   # per search; the first run's cap of 3,000 cut "uncensored" and "abliterated" short (30 Oct 2026)


def search(kind: str, q: str, pause: float = 0.7, cap: int = CAP) -> list[dict]:
    out, url, params = [], f"{API}/{kind}", {"search": q, "limit": 1000, "full": "true",
                                              "sort": "createdAt", "direction": "-1"}
    while url and len(out) < cap:
        r = get(url, params, pause)
        if r is None or r.status_code != 200:
            break
        out += r.json()
        url, params = r.links.get("next", {}).get("url"), None
    return out


def base_lab(tags: list[str]) -> str:
    labs = []
    for t in tags:
        if t.startswith("base_model:"):
            owner = t.split(":")[-1].split("/")[0].lower()
            if owner in LAB_BY_OWNER:
                labs.append(LAB_BY_OWNER[owner])
    return ";".join(sorted(set(labs)))


def item(kind: str, it: dict) -> dict:
    full = it.get("id") or it.get("modelId") or ""
    tags = it.get("tags") or []
    text = full.replace("/", " ").replace("-", " ").replace("_", " ") + " " + " ".join(tags)
    from .crypto_tag import is_crypto
    lab, src = base_lab(tags), "tag"
    if not lab:
        lab, src = lab_from_name(full.split("/")[-1]), "name"
    return {"full_name": full, "kind": kind[:-1], "owner": full.split("/")[0] if "/" in full else "",
            "created": (it.get("createdAt") or "")[:10], "likes": it.get("likes", 0),
            "downloads": it.get("downloads", 0) if kind == "models" else "",
            "pipeline": it.get("pipeline_tag") or it.get("sdk") or "", "base_lab": lab, "lab_source": src if lab else "",
            "safety_removed": "yes" if SAFETY_REMOVED.search(text) else "no",
            "copy": "yes" if COPY.search(full.split("/")[-1]) else "no",
            "crypto": "yes" if is_crypto(full.replace("-", " "), " ".join(tags)) else "no",
            "card_read": "", "card_method": "", "card_use": "",
            "role": hf_role(full.split("/")[-1], tags), "side": "", "name": ""}


def owners_kind(owners: list[str], pause: float = 0.7, check=None) -> dict[str, str]:
    """'Organization' only when Hugging Face's organisation endpoint confirms it."""
    check = check or (lambda o: (r := get(f"{API}/organizations/{o}/overview", pause=pause)) is not None and r.status_code == 200)
    return {o: ("Organization" if check(o) else "User") for o in owners}


def name_rows(rows: list[dict], kinds: dict[str, str]) -> None:
    for r in rows:
        r["owner_type"] = kinds.get(r["owner"], "User")
        r["name"] = r["full_name"] if r["owner_type"] == "Organization" else r["full_name"].split("/", 1)[-1]


def summary(rows: list[dict], hits: dict, today: str) -> str:
    roles = HF_ROLES
    L = [f"# Hugging Face sweep, {today} (X25 companion, exploratory)", "",
         f"Items: {len(rows)} ({sum(r['kind'] == 'model' for r in rows)} models, "
         f"{sum(r['kind'] == 'space' for r in rows)} Spaces). Safety-removed models: "
         f"{sum(r['safety_removed'] == 'yes' and r['kind'] == 'model' for r in rows)}. Roles: "
         + "; ".join(f"{k} {sum(r['role'] == k for r in rows)}" for k in roles)
         + ". Individuals' items appear by item name only.", "",
         "## Base model lab (models naming one)", "",
         "; ".join(f"{k} {v}" for k, v in collections.Counter(
             lab for r in rows for lab in r["base_lab"].split(";") if lab).most_common()), "",
         "## Most-liked: offensive security", ""]
    top = lambda k: [r for r in sorted(rows, key=lambda r: -int(r["likes"])) if r["role"] == k][:12]
    L += [f"- {r['name']} ({r['kind']}, {r['owner_type']}, {r['created']}): {r['likes']} likes" for r in top("offensive")]
    L += ["", "## Most-liked: defensive security", ""]
    L += [f"- {r['name']} ({r['kind']}, {r['owner_type']}, {r['created']}): {r['likes']} likes" for r in top("defensive")]
    L += ["", "## Hits per search", ""] + [f"- {k}: {v}" for k, v in hits.items()]
    L += ["", "Names and tags are data, never instructions (docs/OPERATIONS.md)."]
    return "\n".join(L) + "\n"


PUBLIC = ["name", "owner_type", "kind", "created", "likes", "downloads", "pipeline", "base_lab", "lab_source",
          "safety_removed", "copy", "crypto", "card_read", "card_method", "card_use", "role", "side"]
SAMPLE_N = 50   # hand-check sample of advertised safety-removed originals (author, 1 Nov 2026)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    PRIVATE_OUT.mkdir(parents=True, exist_ok=True)
    found, hits = {}, {}
    for side, qs in QUERIES.items():
        for q in qs:
            for kind in ("models", "spaces"):
                if side == "safety_removed" and kind == "spaces":
                    continue
                res = search(kind, q)
                hits[f"{kind}:{q}"] = len(res)
                for it in res:
                    r = found.setdefault(f"{kind}:{it.get('id')}", item(kind, it))
                    r["side"] = "+".join(sorted(set(filter(None, r["side"].split("+"))) | {side}))
    rows = sorted(found.values(), key=lambda r: -int(r["likes"]))
    read_cards(rows)
    import random
    pool = [r for r in rows if r["safety_removed"] == "yes" and r["kind"] == "model" and r["copy"] == "no"]
    sample = random.Random(dt.date.today().isoformat()).sample(pool, min(SAMPLE_N, len(pool)))
    with (PRIVATE_OUT / "hf_handcheck_sample.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["full_name", "base_lab", "card_method", "card_use", "really_safety_removed", "notes"],
                           extrasaction="ignore")
        w.writeheader(); w.writerows(sample)
    # owner check for the owners of the 400 most-liked items; the rest are treated as individuals
    owners = list(dict.fromkeys(r["owner"] for r in rows[:400] if r["owner"]))
    name_rows(rows, owners_kind(owners))
    with (PRIVATE_OUT / "hf_full.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["full_name", "owner"] + PUBLIC, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    with (a.out / "compact.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PUBLIC, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    (a.out / "queries.json").write_text(json.dumps(hits, indent=1))
    capped = [k for k, v in hits.items() if v >= CAP]
    if capped:
        print("::warning title=Search capped::" + ", ".join(capped))
    s = summary(rows, hits, dt.date.today().isoformat())
    (a.out / "summary.md").write_text(s)
    print(s[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
