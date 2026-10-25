"""Research probe (25 Oct 2026 brainstorm): patch adoption for attacked open-source flaws.

For every CVE first added to CISA KEV between --start and --end that OSV maps to packages in
npm, PyPI, Maven, Go or Cargo: the versions OSV lists as affected, and, from deps.dev's free
API, how many packages currently depend on affected versions versus all versions. A snapshot
of today only (history needs deps.dev's BigQuery tables). Research only.
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests

from ..collect.http import UA

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
SYS = {"npm": "npm", "PyPI": "pypi", "Maven": "maven", "Go": "go", "crates.io": "cargo"}


def _json(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
        time.sleep(0.2)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError):
        return None


GH = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
if os.environ.get("GITHUB_TOKEN"):
    GH["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def ghsa_ids(cve: str) -> list[str]:
    try:
        r = requests.get(f"https://api.github.com/advisories?cve_id={cve}", headers=GH, timeout=40)
        time.sleep(0.3)
        return [a["ghsa_id"] for a in r.json()] if r.ok else []
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return []


def dependents(system, name, version):
    j = _json(f"https://api.deps.dev/v3alpha/systems/{system}/packages/{quote(name, safe='')}/versions/{quote(version, safe='')}:dependents")
    return (j or {}).get("dependentCount")


def probe(start, end, max_versions=150) -> pd.DataFrame:
    kev = pd.DataFrame(_json(KEV_URL)["vulnerabilities"])
    kev = kev[(kev["dateAdded"] >= start) & (kev["dateAdded"] <= end)]
    rows = []
    for k in kev.itertuples():
        recs = [r for r in (_json(f"https://api.osv.dev/v1/vulns/{g}") for g in ghsa_ids(k.cveID)) if r]
        for a in (a for osv in recs for a in osv.get("affected") or []):
            pkg = a.get("package") or {}
            system = SYS.get(pkg.get("ecosystem", ""))
            if not system:
                continue
            affected = set(a.get("versions") or [])
            info = _json(f"https://api.deps.dev/v3/systems/{system}/packages/{quote(pkg['name'], safe='')}") or {}
            versions = [v["versionKey"]["version"] for v in info.get("versions") or []][-max_versions:]
            dep_aff = dep_all = 0
            for v in versions:
                n = dependents(system, pkg["name"], v) or 0
                dep_all += n
                if v in affected:
                    dep_aff += n
            rows.append({"cve_id": k.cveID, "kev_added": k.dateAdded, "ecosystem": system, "package": pkg["name"],
                         "versions_checked": len(versions), "affected_versions": len(affected),
                         "dependents_all": dep_all, "dependents_on_affected": dep_aff,
                         "share_on_affected": round(dep_aff / dep_all, 3) if dep_all else None})
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-01-01"); ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d = probe(a.start, a.end)
    d.to_csv(a.out / "depsdev_adoption.csv", index=False)
    s = ["# Patch adoption snapshot (deps.dev)", "", f"Package entries: {len(d)} from {d['cve_id'].nunique() if len(d) else 0} KEV flaws", ""]
    if len(d):
        s.append(d.sort_values("dependents_all", ascending=False).head(25).to_string(index=False))
    (a.out / "summary.md").write_text("\n".join(s))
    print("\n".join(s))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
