"""The monthly feed-screen spreadsheet (author's request, 31 Oct 2026): "include hyperlinks so I
can read it with a click … the abstract and key findings should be readable somewhere in the
spreadsheet. Maybe pop up when highlighted."

One row per candidate of the AI-attack feed screen. The title is a link to the article; resting
the pointer on it shows a note with the abstract, key findings and decision. A "Read one" tab
shows any item in large text (useful on a phone, where notes may not show). Kept in the private
repository with the rest of the exploratory work (author, 31 Oct 2026).

Made twice a month: the Feed screen workflow builds it from candidates.csv with the decision
columns empty; after Claude sorts the candidates it is rebuilt with the decisions file
(columns n, decision, reason, abstract, key_findings, basis, report). Abstracts and findings are
Claude's own short summaries, never copied article text; `basis` says whether Claude read the
report ("read") or worked from the title and feed entry ("title"). Needs openpyxl
(requirements-sheet.lock).

  python -m snapshot.feedsheet --candidates C.csv [--decisions D.csv] --out F.xlsx
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

BASIS = {"read": "Report read by Claude", "title": "Title and feed entry", "": "Not yet sorted"}
FILLS = {"logged": "C6EFCE", "your judgement": "FFEB9C", "second source": "DDEBF7", "already logged": "EDEDED"}
DECISIONS = ["logged", "second source", "already logged", "your judgement", "excluded"]
COLS = [("#", 5), ("Date", 11), ("Feed", 20), ("Title (click to read)", 48), ("Abstract", 55), ("Key findings", 60),
        ("Decision", 14), ("Reason", 45), ("Report in the attack log", 34), ("Summary based on", 20),
        ("AI term", 12), ("Attack term", 12)]


def rows(candidates: Path, decisions: Path | None) -> list[dict]:
    cands = list(csv.DictReader(candidates.open(encoding="utf-8")))
    dec = {}
    if decisions and decisions.exists():
        dec = {int(r["n"]): r for r in csv.DictReader(decisions.open(encoding="utf-8"))}
    out = []
    for i, c in enumerate(cands):
        d = dec.get(i, {})
        if d.get("decision") and d["decision"] not in DECISIONS:
            raise ValueError(f"item {i}: unknown decision {d['decision']!r}")
        out.append({"n": i, "date": c.get("date", ""), "feed": c.get("feed", ""), "title": c.get("title", ""),
                    "link": c.get("link", ""), "abstract": d.get("abstract", ""), "key_findings": d.get("key_findings", ""),
                    "decision": d.get("decision", ""), "reason": d.get("reason", ""), "report": d.get("report", ""),
                    "basis": BASIS[d.get("basis", "")], "ai_term": c.get("ai_term", ""), "attack_term": c.get("attack_term", "")})
    return out


def build(items: list[dict], out: Path, source_note: str = "") -> None:
    from openpyxl import Workbook
    from openpyxl.comments import Comment
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.datavalidation import DataValidation

    F = "Arial"
    n = len(items)
    last = n + 1
    hdr_font, hdr_fill = Font(name=F, bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F3864")
    linkf = Font(name=F, size=10, color="0563C1", underline="single")
    body, wrap, thin = Font(name=F, size=10), Alignment(wrap_text=True, vertical="top"), Side(style="thin", color="BFBFBF")
    wb = Workbook()
    ws = wb.active
    ws.title = "Feed sweep"
    for c, (h, w) in enumerate(COLS, 1):
        cell = ws.cell(1, c, h)
        cell.font, cell.fill, cell.alignment = hdr_font, hdr_fill, wrap
        ws.column_dimensions[cell.column_letter].width = w
    for r in items:
        row = r["n"] + 2
        vals = [r["n"], r["date"], r["feed"], r["title"], r["abstract"], r["key_findings"], r["decision"],
                r["reason"], "", r["basis"], r["ai_term"], r["attack_term"]]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row, c, v)
            cell.font, cell.alignment, cell.border = body, wrap, Border(bottom=thin)
        t = ws.cell(row, 4)
        if r["link"].startswith("https://") or r["link"].startswith("http://"):
            t.hyperlink, t.font = r["link"], linkf
        note = (f"ABSTRACT\n{r['abstract'] or '(not yet sorted)'}\n\nKEY FINDINGS\n{r['key_findings'] or '-'}"
                f"\n\nDECISION: {r['decision'] or 'not yet sorted'}")
        cm = Comment(note, "Claude")
        cm.width, cm.height = 420, 260
        t.comment = cm
        if r["report"]:
            p = ws.cell(row, 9, r["report"])
            p.hyperlink, p.font = r["report"], linkf
        ws.row_dimensions[row].height = 75
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = f"A1:L{last}"
    for k, col in FILLS.items():
        ws.conditional_formatting.add(f"G2:G{last}", FormulaRule(formula=[f'$G2="{k}"'],
                                                                  fill=PatternFill("solid", fgColor=col)))
    # Read one item
    rd = wb.create_sheet("Read one", 0)
    rd.column_dimensions["A"].width, rd.column_dimensions["B"].width = 24, 100
    rd["A1"] = "Read one item"
    rd["A1"].font = Font(name=F, bold=True, size=14)
    rd["A3"], rd["B3"] = "Item # (choose)", 0
    rd["A3"].font = Font(name=F, bold=True)
    rd["B3"].font = Font(name=F, bold=True, color="0000FF", size=12)
    rd["B3"].fill = PatternFill("solid", fgColor="FFFF00")
    rd["B3"].alignment = Alignment(horizontal="left")
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2=str(max(n - 1, 0)),
                        promptTitle="Pick an item", prompt=f"Type an item number from the # column of the Feed sweep tab (0 to {max(n - 1, 0)}).")
    dv.showInputMessage = True
    rd.add_data_validation(dv)
    dv.add("B3")
    key = f"MATCH($B$3,'Feed sweep'!$A$2:$A${last},0)"

    def look(col):
        return f"INDEX('Feed sweep'!${col}$2:${col}${last},{key})"

    link = f"INDEX(Links!$B$2:$B${last},MATCH($B$3,Links!$A$2:$A${last},0))"
    lines = [("Date", look("B")), ("Feed", look("C")), ("Title", f"HYPERLINK({link},{look('D')})"),
             ("Abstract", look("E")), ("Key findings", look("F")), ("Decision", look("G")), ("Reason", look("H")),
             ("Report in the attack log", f'IF({look("I")}="","(none)",HYPERLINK({look("I")},{look("I")}))'),
             ("Summary based on", look("J"))]
    for k, (lab, f) in enumerate(lines, 5):
        rd.cell(k, 1, lab).font = Font(name=F, bold=True)
        c = rd.cell(k, 2, f'=IFERROR({f},"")')
        c.font = Font(name=F, size=11, color="0563C1", underline="single") if lab in ("Title", "Report in the attack log") else Font(name=F, size=11)
        c.alignment = wrap
        rd.row_dimensions[k].height = 60 if lab in ("Abstract", "Key findings", "Reason") else 22
    rd["A16"] = "How to use"
    rd["A16"].font = Font(name=F, bold=True)
    notes = ["Type an item number in the yellow cell B3; its details appear above. Click the title to open the article.",
             "On the Feed sweep tab, rest the pointer on any title to see its abstract and key findings in a pop-up note; click the title to open the article.",
             "Decision colours: green = logged as a new case; yellow = your judgement; blue = second source; grey = already logged; white = excluded or not yet sorted.",
             "'Summary based on': 'Report read by Claude' means Claude read the organisation's report; 'Title and feed entry' means the summary comes from the title, the feed entry and the screen only.",
             "Abstracts and findings are Claude's own short summaries, not text copied from the articles. Feed and article text was treated as data, never instructions.",
             source_note or "Source: the monthly AI-attack feed screen (X3, exploratory; never scored)."]
    for k, t in enumerate(notes, 17):
        c = rd.cell(k, 2, t)
        c.font, c.alignment = Font(name=F, size=10), wrap
        rd.row_dimensions[k].height = 30
    lk = wb.create_sheet("Links")
    lk.append(["#", "Article URL"])
    for r in items:
        lk.append([r["n"], r["link"]])
    for row in lk.iter_rows():
        for c in row:
            c.font = Font(name=F, size=10)
    lk.column_dimensions["B"].width = 110
    sm = wb.create_sheet("Counts")
    sm["A1"], sm["B1"] = "Decision", "Items"
    for c in ("A1", "B1"):
        sm[c].font, sm[c].fill = hdr_font, hdr_fill
    for k, d in enumerate(DECISIONS + [""], 2):
        sm.cell(k, 1, d or "not yet sorted").font = Font(name=F)
        crit = f'"{d}"' if d else '""'
        sm.cell(k, 2, f"=COUNTIF('Feed sweep'!$G$2:$G${last},{crit})").font = Font(name=F)
    tot = len(DECISIONS) + 3
    sm.cell(tot, 1, "Total").font = Font(name=F, bold=True)
    sm.cell(tot, 2, f"=SUM(B2:B{tot - 1})").font = Font(name=F, bold=True)
    sm.column_dimensions["A"].width = 18
    wb.calculation.fullCalcOnLoad = True   # no cached values: the reader's program works them out on opening
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--decisions", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--note", default="")
    a = ap.parse_args(argv)
    items = rows(a.candidates, a.decisions)
    build(items, a.out, a.note)
    print(f"{a.out}: {len(items)} items, {sum(bool(r['decision']) for r in items)} sorted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
