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


def test_auto_accept_patterns():
    from snapshot.autoaccept import auto_accept
    assert auto_accept("Alex Gaynor in collaboration with Claude and Anthropic Research") == "collaboration"
    assert auto_accept("The ASF using Claude Agents") == "using"
    assert auto_accept("Red Hat would like to thank Google Big Sleep for reporting this issue.") == "credited_directly"
    assert auto_accept("iglocska | Claude Fable 5.1") == "model_with_version"
    assert auto_accept("Amy Burnett of OpenAI") is None          # lab name only
    assert auto_accept("Paul Bottinelli (Trail of Bits in collaboration with OpenAI)") is None
    assert auto_accept("Prompt injection in Claude found by Jane Doe") is None   # AI is the subject
    assert auto_accept("Claude Bernard") is None                 # excluded name
    assert auto_accept("Jane Doe", credit_types=["tool"]) is None  # no tool term
    assert auto_accept("Claude (Anthropic)", credit_types=["tool"]) == "credit_type_tool"


def test_spot_check_is_seeded():
    from snapshot.autoaccept import spot_check
    keys = [f"k{i}" for i in range(40)]
    a, b = spot_check(keys, "s"), spot_check(keys, "s")
    assert a == b and len(a) == 4
