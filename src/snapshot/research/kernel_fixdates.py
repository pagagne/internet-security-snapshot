"""Research probe (25 Oct 2026 brainstorm): can Linux kernel fixes be dated from public code
history instead of being "assumed = publication date"?

For every Linux kernel CVE first added to CISA KEV between --start and --end: the fixing
commits named in the CVE record (git.kernel.org stable links), the earliest commit date
(GitHub mirrors torvalds/linux, then gregkh/linux), and the first fixed version. Compared with
the CVE publication date and the KEV date. Research only.
"""
from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
CVE_RAW = "https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/{y}/{b}/{c}.json"
SHA = re.compile(r"git\.kernel\.org/.*?/c/([0-9a-f]{12,40})")
HDR = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    HDR["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def _json(url, headers=None):
    try:
        r = requests.get(url, headers=headers or {"User-Agent": UA}, timeout=40)
        time.sleep(0.3)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError):
        return None


def commit_date(sha: str):
    for repo in ("torvalds/linux", "gregkh/linux"):
        j = _json(f"https://api.github.com/repos/{repo}/commits/{sha}", HDR)
        if j and j.get("commit"):
            c = j["commit"]
            return (c.get("committer") or c.get("author") or {}).get("date", "")[:10], repo
    return None, None


def probe(start, end) -> pd.DataFrame:
    kev = pd.DataFrame(_json(KEV_URL)["vulnerabilities"])
    kev = kev[(kev["dateAdded"] >= start) & (kev["dateAdded"] <= end)]
    lin = kev[kev["vendorProject"].str.contains("Linux", case=False) & kev["product"].str.contains("Kernel", case=False)]
    rows = []
    for k in lin.itertuples():
        y, n = k.cveID.split("-")[1:]
        rec = _json(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=k.cveID)) or {}
        cna = (rec.get("containers") or {}).get("cna") or {}
        pub = ((rec.get("cveMetadata") or {}).get("datePublished") or "")[:10]
        shas = sorted({m.group(1) for r in cna.get("references") or [] for m in [SHA.search(r.get("url", ""))] if m})
        fixed = sorted({v.get("version") for a in cna.get("affected") or [] for v in a.get("versions") or []
                        if v.get("status") == "unaffected" and re.match(r"^\d+\.\d+(\.\d+)?$", v.get("version") or "")},
                       key=lambda s: [int(x) for x in s.split(".")])
        dates = [d for d, _ in (commit_date(s) for s in shas[:8]) if d]
        rows.append({"cve_id": k.cveID, "kev_added": k.dateAdded, "published": pub, "assigner": (rec.get("cveMetadata") or {}).get("assignerShortName"),
                     "fix_commits": len(shas), "earliest_commit": min(dates) if dates else None,
                     "first_fixed_version": fixed[0] if fixed else None})
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-04-01"); ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d = probe(a.start, a.end)
    d.to_csv(a.out / "kernel_fixdates.csv", index=False)
    if len(d):
        dated = d["earliest_commit"].notna()
        gap = (pd.to_datetime(d["published"]) - pd.to_datetime(d["earliest_commit"])).dt.days
        s = (f"# Linux kernel fix dates\n\nKernel flaws added to KEV: {len(d)}\n"
             f"With fixing commits in the CVE record: {int((d['fix_commits'] > 0).sum())}\n"
             f"Dated from a commit: {int(dated.sum())}\n"
             f"Days from fix commit to CVE publication (median, dated ones): {gap[dated].median()}\n"
             f"Commit before publication: {int((gap[dated] > 0).sum())} of {int(dated.sum())}\n")
    else:
        s = "# Linux kernel fix dates\n\nNo Linux kernel flaws added to KEV in the window.\n"
    (a.out / "summary.md").write_text(s)
    print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
