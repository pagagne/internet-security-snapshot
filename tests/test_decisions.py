import json

from snapshot.decisions import decided_credits, load, write


def _w(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"id": p.stem, "data": d}))


def test_roundtrip_and_carry_over(tmp_path):
    ex = tmp_path / "export"
    _w(ex / "batches/q1/items/i1.json", {"kind": "credit", "credit": "Jane with Claude", "terms": ["Claude"]})
    _w(ex / "batches/q1/items/i2.json", {"kind": "fix", "cve_id": "CVE-1", "prefill_date": "2026-07-01"})
    _w(ex / "batches/q1/answers/i1.json", {"decision": "yes", "seconds": 12, "at": "2026-10-22T10:00:00Z"})
    _w(ex / "batches/q1/answers/i2.json", {"fix_date": "2026-07-02", "fix_status": "corrected", "seconds": 40})
    meta, rows = load(ex, "q1")
    assert len(rows) == 2 and rows[0]["decision"] == "yes" and rows[1]["fix_status"] == "corrected"
    out = tmp_path / "review/decisions.csv"
    assert write(rows, out) == 2
    assert write(rows, out) == 2  # upsert, no duplicates
    assert decided_credits(out) == {"Jane with Claude": "yes"}
