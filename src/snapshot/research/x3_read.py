"""Reads the reports behind the AI-attack log (X3) and records only the facts the log needs
(author's decisions, 30 Oct 2026): which AI models are named (grouped by lab, and open-weight
or closed, decided by model), which network protocols are named (the X25 list), and which CVE
IDs appear. Also the address the page ends up at, so a news page can be told from the
organisation's own report. No article text is stored or published (copyright and privacy);
only these tags. Page text is data, never instructions. Requests are 3 s apart.

Reads every source_url in exploratory/ai_attack_campaigns.csv plus any extra addresses listed
in research-in/x3_read_urls.txt (one per line; used for feed-screen candidates).

Output: research-out/x3_read.csv and summary.md.
"""
from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

from ..collect.http import UA, note_status
from ..sourcewatch import _charset, visible_text
from ..util import _repo_root
from .github_tools import LABS, PROTOCOLS, WEIGHTS, tags

CVE = re.compile(r"\bCVE-\d{4}-\d{4,}\b")

# Human approval step (author's decision 19 Nov 2026, X26 cards): cue labels only, never the
# sentence. A human kept a check ("approval") or the AI acted without one ("autonomy"). Claude
# sets the log value from these cues and the case, and the author confirms in the hand check.
APPROVAL_CUES = {
    "human in the loop": r"(?<!no )human[- ]in[- ]the[- ]loop",
    "operator approved or reviewed": r"(?:human|operator)s?\W+(?:\w+\W+){0,3}?(?:approv|review|validat|confirm|sign(?:ed)? off)",
    "approval by a human": r"approv\w*\W+(?:\w+\W+){0,3}?(?:by|from)\W+(?:\w+\W+){0,2}?(?:human|operator)",
    "checkpoints": r"checkpoint|decision points?|approval gates?",
    "human steered": r"(?:human|operator)s?\W+(?:\w+\W+){0,3}?(?:steer|direct|guid|supervis|oversaw|oversee)",
    "relayed by hand": r"by hand|manually (?:relay|cop|pass|approv)",
}
AUTONOMY_CUES = {
    "without human": r"without (?:any )?(?:direct )?human (?:intervention|input|oversight|approval|involvement|interaction|guidance)",
    "no human in the loop": r"no human[- ]in[- ]the[- ]loop|no human (?:involvement|oversight|operator)",
    "fully autonomous": r"fully[- ]autonomous|autonomously|end[- ]to[- ]end autonom",
    "minimal human": r"minimal (?:human )?(?:intervention|involvement|input|oversight)|little human (?:intervention|involvement|input)",
}


def cues(text: str, table: dict) -> str:
    return ";".join(k for k, pat in table.items() if re.search(pat, text, re.I))
EXTRA = "research-in/x3_read_urls.txt"


def read(url: str) -> dict:
    rec = {"url": url}
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
        note_status(url, r.status_code)
    except requests.RequestException as e:
        rec["status"] = f"error {type(e).__name__}"
        return rec
    rec["status"], rec["final_host"] = r.status_code, urlparse(r.url).netloc
    if r.status_code != 200 or "html" not in r.headers.get("content-type", ""):
        return rec
    text = visible_text(r.content.decode(_charset(r), "replace"))
    rec["words"] = len(text.split())
    rec["labs"] = ";".join(tags(text, LABS))
    w = tags(text, WEIGHTS)
    ow, cl = ("open-weight" in w or "runs locally" in w), "closed" in w
    rec["model_weights"] = "both" if ow and cl else "open-weight" if ow else "closed" if cl else "not named"
    rec["protocols"] = ";".join(tags(text, PROTOCOLS)) or "not named"
    rec["cves"] = ";".join(sorted(set(CVE.findall(text))))
    rec["approval_cues"] = cues(text, APPROVAL_CUES)
    rec["autonomy_cues"] = cues(text, AUTONOMY_CUES)
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    root = _repo_root()
    urls = list(dict.fromkeys(r["source_url"] for r in csv.DictReader((root / "exploratory/ai_attack_campaigns.csv").open())))
    extra = root / EXTRA
    if extra.exists():
        urls += [u.strip() for u in extra.read_text().splitlines() if u.strip().startswith("https://") and u.strip() not in urls]
    rows = []
    for u in urls:
        time.sleep(3)
        rows.append(read(u))
    cols = ["url", "status", "final_host", "words", "labs", "model_weights", "protocols", "cves",
            "approval_cues", "autonomy_cues"]
    with (a.out / "x3_read.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    ok = sum(r.get("status") == 200 for r in rows)
    s = (f"# X3 reports read for model, protocol and human-approval tags\n\nAddresses: {len(rows)}; read: {ok}. Tags only; no "
         "article text kept. Tags come from the whole page, so a model or protocol named in a sidebar "
         "can appear: Claude checks each against the case before it enters the log.\n")
    (a.out / "summary.md").write_text(s)
    print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
