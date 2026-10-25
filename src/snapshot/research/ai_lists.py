"""Research probe (25 Oct 2026 brainstorm): do our AI-credit counts catch flaws that outside
lists say AI tools found?

Prototype on a small hand-entered external list (dated, with its source): Stingrai's
"AI-attributed CVE tracker" (verified credits, research cutoff July 2026) plus PHP2Shell
(press: The Next Web, 25 Oct 2026). For each CVE: the credit text in the CVE record, and
whether our headline count (any AI tool or lab) and narrow count (AI tool named) catch it,
using the same rules as T7 (snapshot.autoaccept). Research only.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests

from ..autoaccept import auto_accept
from ..classify import ai_credit_matches
from ..collect.http import UA

CVE_RAW = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{y}/{b}/{c}.json"
STINGRAI = "https://www.stingrai.io/blog/ai-attributed-cve-tracker-2026-verified-credits"
TNW = "https://thenextweb.com/news/php2shell-php-rce-ai-openai-wiz"
LIST = ([("CVE-2026-21536", "XBOW autonomous agent", "autonomous", STINGRAI),
         ("CVE-2026-45185", "XBOW (human finder; AI raced)", "human-found", STINGRAI),
         ("CVE-2025-6965", "Google Big Sleep", "autonomous", STINGRAI),
         ("CVE-2026-28952", "Calif.io with Claude / Anthropic Research", "ai-assisted", STINGRAI)]
        + [(f"CVE-2026-{n}", "depthfirst agent", "autonomous", STINGRAI) for n in range(39210, 39219)]
        + [("CVE-2026-109618", "Calif (GPT-5.6 Sol); Wiz (Wiz Atlas, Gemini 4 Argon, GPT-5.6 Sol)", "ai-assisted", TNW),
           ("CVE-2026-109619", "Calif (GPT-5.6 Sol); Wiz (Wiz Atlas, Gemini 4 Argon, GPT-5.6 Sol)", "ai-assisted", TNW)])


def credits(cve: str) -> tuple[str, list[str], str]:
    y, n = cve.split("-")[1:]
    try:
        r = requests.get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=cve), headers={"User-Agent": UA}, timeout=40)
        time.sleep(0.3)
        rec = r.json() if r.ok else {}
    except (requests.RequestException, ValueError):
        rec = {}
    cna = (rec.get("containers") or {}).get("cna") or {}
    vals = [c.get("value", "") for c in cna.get("credits") or []]
    types = [c.get("type", "") for c in cna.get("credits") or []]
    return " | ".join(vals), types, ("found" if rec else "no record")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for cve, finder, bucket, src in LIST:
        text, types, status = credits(cve)
        rows.append({"cve_id": cve, "external_finder": finder, "bucket": bucket, "source": src,
                     "record": status, "credit_text": text[:300],
                     "terms_matched": ", ".join(ai_credit_matches(text.split(" | "))),
                     "headline": auto_accept(text, types) is not None,
                     "narrow": auto_accept(text, types, tools_only=True) is not None})
    d = pd.DataFrame(rows)
    d.to_csv(a.out / "ai_lists.csv", index=False)
    ai = d[d["bucket"] != "human-found"]
    s = (f"# AI lists against our counts (prototype)\n\nExternal AI-found CVEs: {len(ai)} "
         f"(records found: {int((ai['record'] == 'found').sum())})\n"
         f"Caught by headline (automatic rule): {int(ai['headline'].sum())}\n"
         f"Caught by narrow (tool named): {int(ai['narrow'].sum())}\n"
         f"Human-found control flagged by headline: {int(d.loc[d['bucket'] == 'human-found', 'headline'].sum())}\n\n"
         + d[["cve_id", "external_finder", "record", "terms_matched", "headline", "narrow"]].to_string(index=False))
    (a.out / "summary.md").write_text(s)
    print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
