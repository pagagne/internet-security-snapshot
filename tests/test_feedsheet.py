"""The monthly feed-screen spreadsheet (author's request, 31 Oct 2026)."""
import csv

import pytest

openpyxl = pytest.importorskip("openpyxl")
from snapshot import feedsheet as S


def _write(path, rows):
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def test_links_notes_and_decisions(tmp_path):
    c, d, out = tmp_path / "c.csv", tmp_path / "d.csv", tmp_path / "s.xlsx"
    _write(c, [{"date": "2026-10-29", "feed": "Wiz", "title": "A case", "link": "https://example.org/a", "ai_term": "AI", "attack_term": "breach"},
               {"date": "2026-10-28", "feed": "X", "title": "Other", "link": "https://example.org/b", "ai_term": "AI", "attack_term": "hack"}])
    _write(d, [{"n": "0", "decision": "logged", "reason": "new row", "abstract": "Short summary.",
                "key_findings": "One.\nTwo.", "basis": "read", "report": "https://example.org/report"}])
    S.build(S.rows(c, d), out)
    wb = openpyxl.load_workbook(out)
    ws = wb["Feed sweep"]
    assert ws["D2"].hyperlink.target == "https://example.org/a"
    assert "Short summary." in ws["D2"].comment.text and "DECISION: logged" in ws["D2"].comment.text
    assert ws["I2"].hyperlink.target == "https://example.org/report"
    assert ws["J2"].value == "Report read by Claude" and ws["J3"].value == "Not yet sorted"
    assert "not yet sorted" in ws["D3"].comment.text
    assert wb.sheetnames[0] == "Read one" and wb["Read one"]["B7"].value.startswith("=IFERROR(HYPERLINK(")


def test_unknown_decision_is_refused(tmp_path):
    c, d = tmp_path / "c.csv", tmp_path / "d.csv"
    _write(c, [{"date": "", "feed": "", "title": "t", "link": "https://e.org", "ai_term": "", "attack_term": ""}])
    _write(d, [{"n": "0", "decision": "maybe", "reason": "", "abstract": "", "key_findings": "", "basis": "", "report": ""}])
    with pytest.raises(ValueError):
        S.rows(c, d)
