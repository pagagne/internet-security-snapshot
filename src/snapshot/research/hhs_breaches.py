"""Research probe (25 Oct 2026 brainstorm; second attempt 29 Oct): can the HHS OCR breach
portal's public list be read automatically?

The portal is a JavaServer Faces page whose CSV/Excel export is a form button. The first attempt
(25 Oct) posted a guessed button id and got the page back. This attempt lists every control
whose id, title, alt text or script mentions an export, posts the whole form (all hidden fields)
with each candidate, and also tries the "archive" view. It reports what comes back: quarterly
counts of "Hacking/IT Incident" breaches of 500+ people and people affected. Entity names are
never saved or printed. Research only; requests are spaced and few.
"""
from __future__ import annotations

import argparse
import io
import re
import time
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA, note_status

PAGE = "https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf"
EXPORT = re.compile(r"export|csv|xls|excel|download", re.I)
TAG = re.compile(r"<(input|a|button|img|span)\b([^>]*)>", re.I)
ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')


def _attrs(s: str) -> dict:
    return {k.lower(): v for k, v in ATTR.findall(s)}


def _form_fields(html: str, form_id: str) -> dict:
    m = re.search(rf'<form[^>]*id="{re.escape(form_id)}"[^>]*>(.*?)</form>', html, re.S | re.I)
    body = m.group(1) if m else html
    fields = {}
    for tag, a in TAG.findall(body):
        at = _attrs(a)
        if tag.lower() == "input" and at.get("name") and at.get("type", "text").lower() in ("hidden", "text"):
            fields[at["name"]] = at.get("value", "")
    fields.setdefault(form_id, form_id)
    return fields


def candidates(html: str) -> list[dict]:
    out = []
    for tag, a in TAG.findall(html):
        at = _attrs(a)
        text = " ".join(at.get(k, "") for k in ("id", "name", "title", "alt", "onclick", "value", "src"))
        if EXPORT.search(text) and (at.get("id") or at.get("name")):
            out.append({"tag": tag.lower(), "id": at.get("id") or at.get("name"),
                        "title": (at.get("title") or at.get("alt") or at.get("value") or "")[:60],
                        "onclick": at.get("onclick", "")[:160]})
    return out


def _parse(resp) -> pd.DataFrame | None:
    ctype = resp.headers.get("content-type", "")
    head = resp.content[:4]
    try:
        if "csv" in ctype or resp.text[:300].count(",") > 5:
            return pd.read_csv(io.StringIO(resp.text))
        if head[:2] == b"PK" or "spreadsheet" in ctype or "excel" in ctype:
            return pd.read_excel(io.BytesIO(resp.content))
    except Exception:  # noqa: BLE001
        return None
    return None


def fetch() -> tuple[pd.DataFrame | None, list[str]]:
    notes = []
    s = requests.Session()
    s.headers["User-Agent"] = UA
    r = s.get(PAGE, timeout=60)
    note_status(PAGE, r.status_code)
    notes.append(f"page {r.status_code}, {len(r.text)} bytes")
    forms = re.findall(r'<form[^>]*id="([^"]+)"', r.text)
    cands = candidates(r.text)
    notes.append(f"forms {forms}; export-like controls: " +
                 "; ".join(f"{c['tag']} {c['id']} '{c['title']}' {c['onclick'][:60]}" for c in cands[:12]))
    # Page outline for diagnosis: element ids, control titles and script/link targets only
    # (no visible text, so no entity names).
    outline = []
    for tag, attrs in TAG.findall(r.text):
        at = _attrs(attrs)
        if at.get("id") or at.get("title") or at.get("alt"):
            outline.append(f"{tag} id={at.get('id', '')} title={at.get('title', '')[:40]} alt={at.get('alt', '')[:40]} "
                           f"href={at.get('href', '')[:80]} src={at.get('src', '')[:80]}")
    outline += [f"script {x[:120]}" for x in re.findall(r'<script[^>]*src="([^"]+)"', r.text)]
    outline += [f"link {x[:120]}" for x in re.findall(r'<a[^>]*href="([^"#][^"]*)"', r.text)]
    notes.append("OUTLINE\n" + "\n".join(outline[:150]))
    form = "ocrForm" if "ocrForm" in forms else (forms[-1] if forms else None)
    if not form:
        return None, notes
    base = _form_fields(r.text, form)
    tried = set()
    for c in cands[:8]:
        cid = c["id"]
        if cid in tried:
            continue
        tried.add(cid)
        time.sleep(2)
        data = dict(base)
        data[cid] = cid
        # PrimeFaces command links name their trigger in the onclick script
        for m in re.findall(r"'([\w:]+)'\s*:\s*'([\w:]+)'", c["onclick"]):
            data[m[0]] = m[1]
        p = s.post(PAGE, data=data, timeout=120)
        note_status(PAGE, p.status_code)
        notes.append(f"post {cid}: {p.status_code} {p.headers.get('content-type', '')} {len(p.content)} bytes")
        d = _parse(p)
        if d is not None and len(d) > 10:
            notes.append(f"export worked with {cid}")
            return d, notes
    return None, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d, notes = fetch()
    lines = ["# HHS OCR breach portal probe (second attempt, 29 Oct 2026)", ""] + [f"- {n}" for n in notes]
    if d is not None:
        lines.append(f"\nColumns: {list(d.columns)}; rows {len(d)}")
        date_col = next((c for c in d.columns if "date" in c.lower()), None)
        type_col = next((c for c in d.columns if "type" in c.lower()), None)
        n_col = next((c for c in d.columns if "individual" in c.lower()), None)
        if date_col and type_col:
            d["q"] = pd.to_datetime(d[date_col], errors="coerce").dt.to_period("Q").astype(str)
            h = d[d[type_col].astype(str).str.contains("Hacking", case=False)]
            agg = h.groupby("q").agg(breaches=(type_col, "size"), **({"people": (n_col, "sum")} if n_col else {}))
            agg.tail(12).to_csv(a.out / "hacking_by_quarter.csv")
            lines.append("\n" + agg.tail(12).to_string())
    (a.out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
