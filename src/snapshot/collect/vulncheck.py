"""VulnCheck KEV (community data), from VulnCheck's offline backup of the vulncheck-kev index.

Permission (11 Nov 2026, docs/PERMISSIONS.md): VulnCheck's only requirement for community data
is attribution of the source data; the study publishes derived statistics only, labelled
"VulnCheck KEV", and never republishes entries. So the per-CVE table this module writes stays in
the private part of each bundle (config/sources.yaml: raw_public false; snapshot.private moves
it out of every public output), and only figures derived from it are published.

One request a pull for the backup's signed download link, then one download (docs/TERMS_OF_USE.md,
"Request volume"). Needs the VULNCHECK_TOKEN secret; without it the pull records a gap.

Per CVE: when VulnCheck listed it (date_added), its earliest reported-exploitation source
(vulncheck_reported_exploitation[].date_added), its earliest public exploit in VulnCheck XDB,
CISA's listing date as VulnCheck records it, and the canary and ransomware flags.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import zipfile

import pandas as pd

from .http import get

API = "https://api.vulncheck.com/v3/backup/vulncheck-kev"
CREDIT = "VulnCheck KEV (https://vulncheck.com/kev), community data, used with attribution"


def _token() -> str:
    t = os.environ.get("VULNCHECK_TOKEN")
    if not t:
        raise RuntimeError("VULNCHECK_TOKEN not set: the VulnCheck pull needs the community API token "
                           "(GitHub secret; docs/PERMISSIONS.md)")
    return t


def download() -> tuple[bytes, dict]:
    """The newest vulncheck-kev backup (zip bytes) and its listing entry (filename, sha256, date)."""
    meta = get(API, headers={"Authorization": f"Bearer {_token()}"}, timeout=60).json()
    entries = meta.get("data") or []
    if not entries:
        raise RuntimeError("VulnCheck returned no backup for vulncheck-kev")
    e = sorted(entries, key=lambda x: str(x.get("date_added") or ""))[-1]
    blob = get(e["url"], timeout=300).content
    if e.get("sha256") and hashlib.sha256(blob).hexdigest() != e["sha256"].lower():
        raise RuntimeError("VulnCheck backup failed its checksum")
    return blob, {k: e.get(k) for k in ("filename", "sha256", "date_added")}


def records(blob: bytes) -> list[dict]:
    """Every KEV record in the backup zip (JSON files holding a list, or {"data": [...]}, or one
    record per line)."""
    out: list[dict] = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for name in z.namelist():
            if not name.lower().endswith((".json", ".jsonl")):
                continue
            text = z.read(name).decode("utf-8")
            try:
                doc = json.loads(text)
                items = doc.get("data", []) if isinstance(doc, dict) else doc
            except json.JSONDecodeError:
                items = [json.loads(line) for line in text.splitlines() if line.strip()]
            out += [r for r in items if isinstance(r, dict)]
    return out


def _min_date(items, key="date_added"):
    ds = pd.to_datetime([i.get(key) for i in (items or []) if isinstance(i, dict) and i.get(key)],
                        utc=True, errors="coerce")
    ds = ds[~ds.isna()]
    return ds.min() if len(ds) else pd.NaT


def build_table(recs: list[dict]) -> pd.DataFrame:
    rows = []
    for r in recs:
        cves = r.get("cve") or []
        if isinstance(cves, str):
            cves = [cves]
        base = {
            "vc_date_added": pd.to_datetime(r.get("date_added"), utc=True, errors="coerce"),
            "vc_first_reported": _min_date(r.get("vulncheck_reported_exploitation")),
            "vc_first_xdb": _min_date(r.get("vulncheck_xdb")),
            "vc_cisa_date_added": pd.to_datetime(r.get("cisa_date_added"), utc=True, errors="coerce"),
            "vc_canaries": bool(r.get("reported_exploited_by_vulncheck_canaries")),
            "vc_ransomware": str(r.get("knownRansomwareCampaignUse") or "").lower() == "known",
            "n_reported_sources": len(r.get("vulncheck_reported_exploitation") or []),
        }
        for c in cves:
            if isinstance(c, str) and c.upper().startswith("CVE-"):
                rows.append({"cve_id": c.upper(), **base})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # one row per CVE: the earliest listing wins if a CVE appears in two records
    return df.sort_values("vc_date_added").drop_duplicates("cve_id", keep="first").reset_index(drop=True)


def exploit_rows(table: pd.DataFrame) -> pd.DataFrame:
    """Rows for snapshot.events (cve_id, source, date): VulnCheck's dated record of each CVE,
    its KEV listing date (the registered T_exploit reads "the earliest dated record in ...
    VulnCheck KEV"). The earliest reported-exploitation date is kept in the table for exploratory
    use only."""
    if table is None or table.empty:
        return pd.DataFrame(columns=["cve_id", "source", "date"])
    t = table.dropna(subset=["vc_date_added"])
    return pd.DataFrame({"cve_id": t["cve_id"], "source": "vulncheck_kev",
                         "date": t["vc_date_added"].dt.tz_convert(None).dt.date.astype(str)})
