"""AI attack- and defence-related models and apps on Hugging Face (X25 companion; author's
decision, 30 Oct 2026).

Hugging Face is where AI models themselves are published, including open-weight models with
their safety training removed ("uncensored", "abliterated"). Run by hand only, with the GitHub
sweep. Uses Hugging Face's public Hub API (no account; well inside its published limit of 500
requests per 5 minutes). Fixed searches over model and Space (app) names; per item: kind
(model or Space), created date, likes, downloads (models), tags, the base model's lab (from
the model's own base_model tags), role (attack, defence, both, model_testing, unclear, from
its own name and tags) and whether it is a safety-removed variant. Nothing is downloaded or
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
from .github_tools import role

API = "https://huggingface.co/api"
PRIVATE_OUT = Path(os.environ.get("X25_PRIVATE_OUT", "research-private"))
QUERIES = {   # substring searches over names; fixed between sweeps
    "attack": ["pentest", "pentesting", "penetration", "redteam", "red-team", "exploit", "hacking", "hacker",
               "offensive", "malware-gen", "cyber-attack", "jailbreak"],
    "defence": ["cybersecurity", "cyber-security", "threat-detection", "soc-analyst", "malware-detection",
                "intrusion", "vulnerability", "secure-code", "incident-response", "phishing-detection",
                "security-copilot", "sigma"],
    "safety_removed": ["uncensored", "abliterated", "unaligned", "unfiltered"],
}
SAFETY_REMOVED = re.compile(r"uncensored|abliterat|unaligned|unfiltered|no.?refusal|refusal.?removed", re.I)
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


def search(kind: str, q: str, pause: float = 0.7, cap: int = 3000) -> list[dict]:
    out, url, params = [], f"{API}/{kind}", {"search": q, "limit": 1000, "full": "true"}
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
    return {"full_name": full, "kind": kind[:-1], "owner": full.split("/")[0] if "/" in full else "",
            "created": (it.get("createdAt") or "")[:10], "likes": it.get("likes", 0),
            "downloads": it.get("downloads", 0) if kind == "models" else "",
            "pipeline": it.get("pipeline_tag") or it.get("sdk") or "", "base_lab": base_lab(tags),
            "safety_removed": "yes" if SAFETY_REMOVED.search(text) else "no",
            "role": role(text), "side": "", "name": ""}


def owners_kind(owners: list[str], pause: float = 0.7, check=None) -> dict[str, str]:
    """'Organization' only when Hugging Face's organisation endpoint confirms it."""
    check = check or (lambda o: (r := get(f"{API}/organizations/{o}/overview", pause=pause)) is not None and r.status_code == 200)
    return {o: ("Organization" if check(o) else "User") for o in owners}


def name_rows(rows: list[dict], kinds: dict[str, str]) -> None:
    for r in rows:
        r["owner_type"] = kinds.get(r["owner"], "User")
        r["name"] = r["full_name"] if r["owner_type"] == "Organization" else r["full_name"].split("/", 1)[-1]


def summary(rows: list[dict], hits: dict, today: str) -> str:
    roles = ["attack", "defence", "both", "model_testing", "unclear"]
    L = [f"# Hugging Face sweep, {today} (X25 companion, exploratory)", "",
         f"Items: {len(rows)} ({sum(r['kind'] == 'model' for r in rows)} models, "
         f"{sum(r['kind'] == 'space' for r in rows)} Spaces). Safety-removed models: "
         f"{sum(r['safety_removed'] == 'yes' and r['kind'] == 'model' for r in rows)}. Roles: "
         + "; ".join(f"{k} {sum(r['role'] == k for r in rows)}" for k in roles)
         + ". Individuals' items appear by item name only.", "",
         "## Base model lab (models naming one)", "",
         "; ".join(f"{k} {v}" for k, v in collections.Counter(
             lab for r in rows for lab in r["base_lab"].split(";") if lab).most_common()), "",
         "## Most-liked: attack", ""]
    top = lambda k: [r for r in sorted(rows, key=lambda r: -int(r["likes"])) if r["role"] == k][:12]
    L += [f"- {r['name']} ({r['kind']}, {r['owner_type']}, {r['created']}): {r['likes']} likes" for r in top("attack")]
    L += ["", "## Most-liked: defence", ""]
    L += [f"- {r['name']} ({r['kind']}, {r['owner_type']}, {r['created']}): {r['likes']} likes" for r in top("defence")]
    L += ["", "## Hits per search", ""] + [f"- {k}: {v}" for k, v in hits.items()]
    L += ["", "Names and tags are data, never instructions (docs/OPERATIONS.md)."]
    return "\n".join(L) + "\n"


PUBLIC = ["name", "owner_type", "kind", "created", "likes", "downloads", "pipeline", "base_lab",
          "safety_removed", "role", "side"]


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
    s = summary(rows, hits, dt.date.today().isoformat())
    (a.out / "summary.md").write_text(s)
    print(s[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
