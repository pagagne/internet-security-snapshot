"""Research probe (25 Oct 2026 brainstorm): what each candidate free source actually returns.

For each source, records the HTTP status, size and a short, scrubbed sample (IPv4/IPv6
addresses and e-mail addresses replaced) so collectors can be written against the real
format. Nothing here feeds any measure. Runs in GitHub Actions.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import requests

from ..collect.http import UA

IP4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
IP6 = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){3,7}[0-9a-fA-F]{1,4}\b")
MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

SOURCES = {
    "isc_urlsummary": "https://isc.sans.edu/feeds/urlsummary.txt",
    "isc_urlcategories": "https://isc.sans.edu/feeds/urlcategories.txt",
    "isc_api_webhoneypot": "https://isc.sans.edu/api/webhoneypotsummary/2026-10-24?json",
    "euvd_exploited": "https://euvdservices.enisa.europa.eu/api/exploitedvulnerabilities?page=0&size=5",
    "euvd_search_cve": "https://euvdservices.enisa.europa.eu/api/vulnerabilities?text=CVE-2024-3400&page=0&size=3",
    "p0_itw_sheet": "https://docs.google.com/spreadsheets/d/1lkNJ0uQwbeC1ZTRrxdtuPLCIl7mlUreoKfSIgajnSyY/export?format=csv",
    "inthewild_exploited": "https://inthewild.io/api/exploited",
    "inthewild_github_readme": "https://raw.githubusercontent.com/gmatuz/inthewilddb/master/README.md",
    "depsdev_package": "https://api.deps.dev/v3/systems/npm/packages/lodash",
    "depsdev_dependents": "https://api.deps.dev/v3alpha/systems/npm/packages/lodash/versions/4.17.21:dependents",
    "hhs_ocr_portal": "https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf",
    "bigsleep_tracker": "https://issuetracker.google.com/action/issues?q=componentid:1836411&count=25",
    "wordpress_plugin_stats": "https://api.wordpress.org/stats/plugin/1.0/wordfence",
    "debian_tracker_cve": "https://security-tracker.debian.org/tracker/CVE-2024-1086",
}


def scrub(text: str) -> str:
    return MAIL.sub("[email]", IP6.sub("[ip]", IP4.sub("[ip]", text)))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")   # unused; kept for the workflow
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, headers={"User-Agent": UA, "Accept": "*/*"}, timeout=90)
            body = r.content
            text = body[:200_000].decode("utf-8", "replace")
            summary[name] = {"url": url, "status": r.status_code, "bytes": len(body),
                             "content_type": r.headers.get("content-type", ""),
                             "lines": body.count(b"\n")}
            (a.out / f"{name}.sample.txt").write_text(scrub("\n".join(text.splitlines()[:60]))[:12000])
        except Exception as e:  # noqa: BLE001 - record and continue
            summary[name] = {"url": url, "error": repr(e)[:300]}
    (a.out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
