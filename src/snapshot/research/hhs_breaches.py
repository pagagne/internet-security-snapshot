"""Research probe (25 Oct 2026 brainstorm): can the HHS OCR breach portal's public list be
read automatically? Tries the portal's CSV export (a JSF form) and reports what it gets:
quarterly counts of "Hacking/IT Incident" breaches of 500+ people and people affected.
Entity names are never saved. Research only.
"""
from __future__ import annotations

import argparse
import io
import re
from pathlib import Path

import pandas as pd
import requests

from ..collect.http import UA

PAGE = "https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf"


def fetch() -> tuple[pd.DataFrame | None, list[str]]:
    notes = []
    s = requests.Session()
    s.headers["User-Agent"] = UA
    r = s.get(PAGE, timeout=60)
    notes.append(f"page {r.status_code}, {len(r.text)} bytes")
    vs = re.search(r'name="javax\.faces\.ViewState"[^>]*value="([^"]+)"', r.text)
    forms = re.findall(r'<form[^>]*id="([^"]+)"', r.text)
    csv_btn = re.findall(r'id="([^"]+)"[^>]*>(?:[^<]*<[^>]+>)*[^<]*CSV', r.text, re.I) or re.findall(r'(ocrForm:[\w:]+)[^>]*title="[^"]*CSV', r.text, re.I)
    notes.append(f"forms {forms[:5]}, viewstate {'yes' if vs else 'no'}, csv controls {csv_btn[:5]}")
    if not (vs and forms):
        return None, notes
    for btn in csv_btn[:3] or ["ocrForm:j_idt368"]:
        data = {forms[0]: forms[0], "javax.faces.ViewState": vs.group(1), btn: btn}
        p = s.post(PAGE, data=data, timeout=120)
        ctype = p.headers.get("content-type", "")
        notes.append(f"post {btn}: {p.status_code} {ctype} {len(p.content)} bytes")
        if "csv" in ctype or p.text[:200].count(",") > 5:
            try:
                return pd.read_csv(io.StringIO(p.text)), notes
            except Exception as e:  # noqa: BLE001
                notes.append(f"parse failed: {e!r}"[:200])
    return None, notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    d, notes = fetch()
    lines = ["# HHS OCR breach portal probe", ""] + [f"- {n}" for n in notes]
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
