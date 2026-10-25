"""Research probe (25 Oct 2026 brainstorm): how late is CISA KEV, compared with other free
sources of first-exploitation evidence?

For every CVE first added to CISA KEV between --start and --end:
  euvd   ENISA EU Vulnerability Database exploited list ("exploitedSince")
  p0     Google Project Zero "0day In the Wild" sheet (year tabs; discovery and patch dates)
  itw    inthewild.io database (earliest "exploitation" report)
and the gap, in days, from the earliest of these to the KEV date. Also reports how many KEV
additions each source covers, and whether EUVD's "exploitedSince" looks like a real date or a
placeholder. Research only; nothing feeds any measure.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sqlite3
import tempfile
import time
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA

KEV_URL = "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json"
EUVD = "https://euvdservices.enisa.europa.eu/api/exploitedvulnerabilities?page={p}&size=100"
P0_ID = "1lkNJ0uQwbeC1ZTRrxdtuPLCIl7mlUreoKfSIgajnSyY"
ITW_DB = "https://pub-4c1eae2a180542b19ea7c88f1e4ccf07.r2.dev/inthewild.db"
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.I)
NOTES: list[str] = []


def _get(url, **kw):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=kw.pop("timeout", 120), **kw)
        return r if r.ok else None
    except requests.RequestException as e:
        NOTES.append(f"{url[:80]}: {type(e).__name__}")
        return None


def euvd() -> pd.DataFrame:
    rows, seen = [], set()
    for p in range(0, 200):
        r = _get(EUVD.format(p=p))
        if r is None:
            NOTES.append(f"euvd page {p} failed"); break
        items = r.json()
        items = items.get("items", items) if isinstance(items, dict) else items
        if not items:
            break
        new = 0
        for it in items:
            if it.get("id") in seen:
                continue
            seen.add(it.get("id")); new += 1
            for c in CVE_RE.findall(it.get("aliases") or ""):
                rows.append({"cve_id": c.upper(), "euvd_id": it.get("id"),
                             "euvd_exploited_since": it.get("exploitedSince"),
                             "euvd_published": it.get("datePublished")})
        if new == 0:
            break
        time.sleep(0.5)
    d = pd.DataFrame(rows)
    if len(d):
        d["euvd_exploited_since"] = pd.to_datetime(d["euvd_exploited_since"], errors="coerce", format="mixed")
        top = d["euvd_exploited_since"].value_counts().head(5)
        NOTES.append("euvd exploitedSince most common values: " + "; ".join(f"{k.date() if pd.notna(k) else k}: {v}" for k, v in top.items()))
        NOTES.append(f"euvd exploited entries: {len(seen)}, with CVE aliases: {d['cve_id'].nunique()}")
    return d


def p0() -> pd.DataFrame:
    html = _get(f"https://docs.google.com/spreadsheets/d/{P0_ID}/htmlview")
    gids = {}
    if html is not None:
        for name, gid in re.findall(r'\{name: "([^"]+)", [^}]*?gid: "(\d+)"', html.text):
            gids[name] = gid
        if not gids:
            for gid, name in re.findall(r'id="sheet-button-(\d+)"[^>]*>(?:<[^>]+>)*([^<]+)<', html.text):
                gids[name.strip()] = gid
    NOTES.append(f"p0 tabs found: {sorted(gids)}")
    frames = []
    for name, gid in gids.items():
        if not re.search(r"20(2[3-9])", name):
            continue
        r = _get(f"https://docs.google.com/spreadsheets/d/{P0_ID}/export?format=csv&gid={gid}")
        if r is None:
            continue
        t = pd.read_csv(io.StringIO(r.text), dtype=str)
        t.columns = [c.strip() for c in t.columns]
        t["tab"] = name
        frames.append(t)
    if not frames:
        return pd.DataFrame(columns=["cve_id"])
    t = pd.concat(frames, ignore_index=True)
    cve_col = next((c for c in t.columns if "cve" in c.lower()), None)
    disc = next((c for c in t.columns if "discover" in c.lower()), None)
    patch = next((c for c in t.columns if "patch" in c.lower()), None)
    NOTES.append(f"p0 columns: {list(t.columns)[:14]}; rows {len(t)}")
    out = pd.DataFrame({"cve_id": t[cve_col].str.upper().str.strip() if cve_col else None,
                        "p0_discovered": pd.to_datetime(t[disc], errors="coerce") if disc else pd.NaT,
                        "p0_patched": pd.to_datetime(t[patch], errors="coerce") if patch else pd.NaT,
                        "p0_tab": t["tab"]})
    return out.dropna(subset=["cve_id"])


def itw() -> pd.DataFrame:
    r = _get(ITW_DB, timeout=600)
    if r is None:
        return pd.DataFrame(columns=["cve_id"])
    with tempfile.NamedTemporaryFile(suffix=".db") as f:
        f.write(r.content); f.flush()
        con = sqlite3.connect(f.name)
        tables = [x[0] for x in con.execute("select name from sqlite_master where type='table'")]
        schema = {t: [c[1] for c in con.execute(f"pragma table_info('{t}')")] for t in tables}
        NOTES.append(f"inthewild tables: {schema}")
        t = next((t for t, cols in schema.items() if "type" in cols and any("time" in c.lower() for c in cols)), None)
        if t is None:
            return pd.DataFrame(columns=["cve_id"])
        cols = schema[t]
        ts = next(c for c in cols if "time" in c.lower())
        idc = "id" if "id" in cols else cols[0]
        d = pd.read_sql(f"select {idc} as cve_id, type, {ts} as ts from {t}", con)
    NOTES.append("inthewild types: " + json.dumps(d["type"].value_counts().head(5).to_dict()))
    d = d[d["type"].str.lower().str.contains("exploitation", na=False)]
    d["ts"] = pd.to_datetime(d["ts"], errors="coerce", utc=True).dt.tz_localize(None)
    d["cve_id"] = d["cve_id"].str.upper()
    return d.groupby("cve_id", as_index=False)["ts"].min().rename(columns={"ts": "itw_first_report"})


def probe(start, end) -> pd.DataFrame:
    kev = pd.DataFrame(_get(KEV_URL).json()["vulnerabilities"])
    kev["kev_added"] = pd.to_datetime(kev["dateAdded"])
    k = kev[(kev["kev_added"] >= start) & (kev["kev_added"] <= end)][["cveID", "vendorProject", "product", "kev_added"]]
    k = k.rename(columns={"cveID": "cve_id"})
    e = euvd().groupby("cve_id", as_index=False).agg(euvd_exploited_since=("euvd_exploited_since", "min"))
    d = k.merge(e, on="cve_id", how="left")
    pz = p0()
    if len(pz):
        d = d.merge(pz.groupby("cve_id", as_index=False).agg(p0_discovered=("p0_discovered", "min"),
                                                           p0_patched=("p0_patched", "min")), on="cve_id", how="left")
    w = itw()
    if len(w):
        d = d.merge(w, on="cve_id", how="left")
    ev = [c for c in ("euvd_exploited_since", "p0_discovered", "itw_first_report") if c in d]
    d["earliest_other"] = d[ev].min(axis=1)
    d["days_before_kev"] = (d["kev_added"] - d["earliest_other"]).dt.days
    return d


def summarize(d: pd.DataFrame) -> str:
    n = len(d)
    L = [f"# KEV lag probe\n\nKEV additions in window: {n}\n", "| Source | KEV additions covered | dated before KEV | median days before KEV (when before) |", "|---|---|---|---|"]
    for c in ("euvd_exploited_since", "p0_discovered", "itw_first_report", "earliest_other"):
        if c not in d:
            continue
        has = d[c].notna()
        before = (d["kev_added"] - d[c]).dt.days
        b = before[has & (before > 0)]
        L.append(f"| {c} | {int(has.sum())} | {int((before > 0).sum())} | {float(b.median()) if len(b) else '-'} |")
    L += ["", "Notes:"] + [f"- {x}" for x in NOTES]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-04-01"); ap.add_argument("--end", default="2026-09-30")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d = probe(a.start, a.end)
    d.to_csv(a.out / "kev_lag.csv", index=False)
    s = summarize(d)
    (a.out / "summary.md").write_text(s)
    print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
