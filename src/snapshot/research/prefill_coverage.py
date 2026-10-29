"""Research probe (29 Oct 2026): how many exploited flaws get a real fix date from the pre-fill?

For every CVE first added to CISA KEV between --start and --end, runs
snapshot.fixdates.prefill_exploited exactly as the review list does, and counts the source of
each date (GitHub, Microsoft, Cisco, Linux kernel, Siemens, Red Hat, Palo Alto, CNA disclosure
date, or assumed). Measures the drop in "assumed" dates after the kernel and CSAF additions of
29 Oct (the 23 Oct probe on the same 175 flaws: 54 dated by vendor or GitHub sources, 33 by the
CNA's disclosure date). Research only; requests are spaced.
"""
from __future__ import annotations

import argparse
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA
from ..fixdates import prefill_exploited

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
CVE_RAW = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{y}/{b}/{c}.json"


def _json(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
        time.sleep(0.2)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError):
        return None


def bucket(src: str) -> str:
    s = src.lower()
    for key, name in [("assumed", "assumed"), ("github", "GitHub"), ("fix commit", "GitHub"),
                      ("microsoft", "Microsoft"), ("cisco", "Cisco"), ("kernel", "Linux kernel"),
                      ("siemens", "Siemens"), ("red hat", "Red Hat"), ("palo alto", "Palo Alto"),
                      ("disclosure date", "CNA disclosure date")]:
        if key in s:
            return name
    return "other"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-04-01"); ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    kev = pd.DataFrame(_json(KEV_URL)["vulnerabilities"])
    kev = kev[(kev["dateAdded"] >= a.start) & (kev["dateAdded"] <= a.end)]
    rows = []
    for k in kev.itertuples():
        y, n = k.cveID.split("-")[1:]
        rec = _json(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=k.cveID)) or {}
        cna = (rec.get("containers") or {}).get("cna") or {}
        refs = [r.get("url", "") for r in cna.get("references") or []]
        pub = ((rec.get("cveMetadata") or {}).get("datePublished") or "")[:10]
        d, src, hand = prefill_exploited(k.cveID, refs, k.vendorProject, pub or k.dateAdded,
                                         (cna.get("datePublic") or "")[:10])
        rows.append({"cve_id": k.cveID, "vendor": k.vendorProject, "kev_added": k.dateAdded,
                     "fix_date": d, "source": bucket(src), "needs_hand_check": hand})
    df = pd.DataFrame(rows)
    df.to_csv(a.out / "prefill_coverage.csv", index=False)
    c = Counter(df["source"]) if len(df) else Counter()
    lines = [f"# Fix-date pre-fill coverage, KEV additions {a.start} to {a.end}", "",
             f"Flaws: {len(df)}", ""] + [f"- {k}: {v}" for k, v in c.most_common()]
    if len(df):
        lines += ["", f"Assumed (no source found): {c.get('assumed', 0)} of {len(df)} "
                  f"({c.get('assumed', 0) / len(df):.0%}); needing a hand check: {int(df['needs_hand_check'].sum())}"]
    (a.out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
