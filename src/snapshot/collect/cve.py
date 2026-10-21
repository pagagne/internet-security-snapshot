"""CVE.org records from the CVEProject/cvelistV5 git repository.

The repository is cloned shallowly at its current head; the commit hash is
recorded in the manifest, so the exact record set can be re-fetched by anyone.
Raw JSON files are not copied (the public git history is the frozen record);
one normalized row per CVE is written to Parquet.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd

from ..classify import ai_credit_matches, root_cause_class
from ..util import parse_ts

REPO_URL = "https://github.com/CVEProject/cvelistV5"


def clone(dest: Path, sparse_paths: list[str] | None = None) -> str:
    """Shallow-clone cvelistV5 into `dest` and return the commit hash."""
    args = ["git", "clone", "-q", "--depth", "1"]
    if sparse_paths:
        args += ["--filter=blob:none", "--sparse"]
    subprocess.run(args + [REPO_URL, str(dest)], check=True)
    if sparse_paths:
        subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", *sparse_paths], check=True)
    return head_commit(dest)


def head_commit(repo: Path) -> str:
    out = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
    return out.stdout.strip()


def _best_cvss(containers: list[dict]) -> tuple[float | None, str | None, str | None]:
    """Highest CVSS base score across CNA and ADP metrics (v4.0, v3.1, v3.0)."""
    best: tuple[float | None, str | None, str | None] = (None, None, None)
    for cont in containers:
        for metric in cont.get("metrics", []) or []:
            for key in ("cvssV4_0", "cvssV3_1", "cvssV3_0"):
                block = metric.get(key)
                if not block:
                    continue
                score = block.get("baseScore")
                if score is None:
                    continue
                if best[0] is None or float(score) > best[0]:
                    best = (float(score), key, block.get("baseSeverity"))
    return best


def _cwes(containers: list[dict]) -> list[str]:
    out: list[str] = []
    for cont in containers:
        for pt in cont.get("problemTypes", []) or []:
            for desc in pt.get("descriptions", []) or []:
                cwe = desc.get("cweId")
                if cwe and cwe not in out:
                    out.append(cwe)
    return out


def _cisa_ssvc(adp: list[dict]) -> dict:
    """CISA Vulnrichment decision points (SSVC) from the CISA-ADP container.

    Vulnrichment is published into the CVE record itself, so no separate download is
    needed. Exploitation is none / poc / active; the timestamp is when CISA last scored it.
    """
    out = {"ssvc_exploitation": None, "ssvc_automatable": None, "ssvc_technical_impact": None, "ssvc_timestamp": None}
    for cont in adp:
        if (cont.get("providerMetadata", {}) or {}).get("shortName") != "CISA-ADP":
            continue
        for metric in cont.get("metrics", []) or []:
            other = metric.get("other") or {}
            if other.get("type") != "ssvc":
                continue
            content = other.get("content") or {}
            for opt in content.get("options", []) or []:
                for k, v in opt.items():
                    key = {"Exploitation": "ssvc_exploitation", "Automatable": "ssvc_automatable",
                           "Technical Impact": "ssvc_technical_impact"}.get(k)
                    if key:
                        out[key] = str(v).lower()
            out["ssvc_timestamp"] = parse_ts(content.get("timestamp"))
    return out


def parse_record(doc: dict) -> dict:
    """Normalize one CVE JSON 5 record to a flat row."""
    meta = doc.get("cveMetadata", {})
    containers = doc.get("containers", {})
    cna = containers.get("cna", {}) or {}
    adp = containers.get("adp", []) or []
    score, version, severity = _best_cvss([cna, *adp])
    credits = cna.get("credits", []) or []
    credit_values = [c.get("value", "") for c in credits]
    cwes = _cwes([cna, *adp])
    affected = [f"{a.get('vendor', '')}|{a.get('product', '')}" for a in cna.get("affected", []) or []]
    return {
        "cve_id": meta.get("cveId"),
        "state": meta.get("state"),
        "cna": meta.get("assignerShortName"),
        "date_reserved": parse_ts(meta.get("dateReserved")),
        "date_published": parse_ts(meta.get("datePublished")),
        "date_updated": parse_ts(meta.get("dateUpdated")),
        "cvss_base": score,
        "cvss_version": version,
        "cvss_severity": severity,
        "cwe_ids": cwes,
        "root_cause": root_cause_class(cwes),
        "affected": affected,
        "credit_values": credit_values,
        "credit_types": [c.get("type", "") for c in credits],
        "ai_credit_terms": ai_credit_matches(credit_values),
        "has_cisa_adp": any((a.get("providerMetadata", {}) or {}).get("shortName") == "CISA-ADP" for a in adp),
        **_cisa_ssvc(adp),
    }


def build_table(repo: Path) -> pd.DataFrame:
    """Parse every CVE record in a cvelistV5 checkout."""
    rows = []
    for path in sorted((repo / "cves").rglob("CVE-*.json")):
        with open(path, encoding="utf-8") as f:
            rows.append(parse_record(json.load(f)))
    df = pd.DataFrame(rows)
    if not df.empty:
        df["ai_credited"] = df["ai_credit_terms"].map(bool)
    return df
