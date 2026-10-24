"""Re-shown items across kinds, per-kind consistency, and the second-coder check."""

import csv

import pandas as pd

from snapshot.agreement import _yes_no_stats, sample, score
from snapshot.decisions import FIELDS, consistency_by_kind, decided_credits, lower_bound_90, retest_items
from snapshot.events import load_fix_decisions


def _write(p, rows):
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def _row(**k):
    base = {"batch": "q1", "decided_by": "author", "decision": "", "fix_status": "", "fix_date": "", "credit": "",
            "cve_id": "", "answered_at": "1", "retest": ""}
    return base | k


def test_retest_draws_every_kind_and_skips_rules_and_retests(tmp_path):
    p = tmp_path / "d.csv"
    _write(p, [
        _row(item_id="1", kind="credit", credit="X of OpenAI", decision="no"),
        _row(item_id="2", kind="credit", credit="Y using Codex", decision="yes", decided_by="rule:using"),
        _row(item_id="3", kind="fix", cve_id="CVE-1", fix_status="confirmed", fix_date="2026-07-01", prefill_date="2026-07-01"),
        _row(item_id="4", kind="slot_c", cve_id="CVE-2", decision="yes"),
        _row(item_id="5", kind="fix", cve_id="CVE-1", fix_status="confirmed", fix_date="2026-07-09", retest="True", batch="q2", answered_at="2"),
    ])
    got = {(r["kind"], r["credit"] or r["cve_id"]) for r in retest_items(p, 20, "s")}
    assert got == {("credit", "X of OpenAI"), ("fix", "CVE-1"), ("slot_c", "CVE-2")}
    # the original fix item is re-shown with its original answer as reference, not the retest
    fix = [r for r in retest_items(p, 20, "s") if r["kind"] == "fix"][0]
    assert fix["item_id"] == "3"
    assert len(retest_items(p, 1, "s")) == 1


def test_retest_answers_never_replace_original_decisions(tmp_path):
    p = tmp_path / "d.csv"
    _write(p, [
        _row(item_id="1", kind="fix", cve_id="CVE-1", fix_status="confirmed", fix_date="2026-07-01"),
        _row(item_id="2", kind="fix", cve_id="CVE-1", fix_status="corrected", fix_date="2026-07-20", retest="True", answered_at="2"),
        _row(item_id="3", kind="credit", credit="Z (DepthFirst AI)", decision="no"),
        _row(item_id="4", kind="credit", credit="Z (DepthFirst AI)", decision="yes", retest="True", answered_at="2"),
    ])
    assert load_fix_decisions(p)["CVE-1"]["date"] == "2026-07-01"
    assert decided_credits(p)["Z (DepthFirst AI)"] == "no"
    c = consistency_by_kind(p)
    assert c["fix"]["pairs"] == 1 and c["fix"]["same"] == 0     # status and date both changed
    assert c["credit"] == {"pairs": 1, "same": 0, "rate": 0.0, "lower90": 0.0}


def test_fix_consistency_allows_one_day():
    import tempfile, pathlib
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "d.csv"
        _write(p, [_row(item_id="1", kind="fix", cve_id="C", fix_status="confirmed", fix_date="2026-07-01"),
                   _row(item_id="2", kind="fix", cve_id="C", fix_status="confirmed", fix_date="2026-07-02", retest="True", answered_at="2")])
        assert consistency_by_kind(p)["fix"]["same"] == 1


def test_lower_bounds_match_the_review():
    assert round(lower_bound_90(5, 5), 3) == 0.631
    assert round(lower_bound_90(20, 20), 3) == 0.891


def test_yes_no_stats_kappa_paradox():
    # 27 yes/yes, 1 no/no, 2 split: raw 0.93, kappa 0.46, AC1 0.92
    pairs = [("yes", "yes", 1)] * 27 + [("no", "no", 1)] + [("yes", "no", 1), ("no", "yes", 1)]
    s = _yes_no_stats(pairs)
    assert s["raw_agreement"] == 0.933 and s["cohen_kappa"] == 0.464 and s["gwet_ac1"] == 0.924
    assert s["agreement_on_yes"] > 0.95 and s["agreement_on_no"] == 0.5


def test_second_coder_sample_is_blinded_weighted_and_scored(tmp_path):
    p = tmp_path / "d.csv"
    rows = [_row(item_id=f"f{i}", kind="fix", cve_id=f"CVE-{i}", fix_status="confirmed", fix_date="2026-07-01",
                 prefill_source="GitHub release v1") for i in range(30)]
    rows += [_row(item_id=f"u{i}", kind="fix", cve_id=f"CVE-U{i}", fix_status="corrected", fix_date="2026-07-10",
                  prefill_source="ASSUMED same day as CVE publication") for i in range(6)]
    rows += [_row(item_id=f"c{i}", kind="slot_c", cve_id=f"CVE-C{i}", decision="yes") for i in range(4)]
    _write(p, rows)
    s = sample(p, "q1")
    assert len(s) == 20
    assert all(r["answer"] == "" and r["fix_date"] == "" for r in s)          # no author answers leak
    unc = [r for r in s if r["stratum"] == "uncertain"]
    assert len(unc) == 6 and all(r["weight"] == 1.0 for r in unc)            # all uncertain cases taken
    rout = [r for r in s if r["stratum"] == "routine"]
    assert len(rout) == 14 and rout[0]["weight"] == round(34 / 14, 4)
    assert sample(p, "q1") == s                                                # seeded
    # second coder agrees on everything except one fix date three days off
    for r in s:
        if r["kind"] == "slot_c":
            r["answer"] = "yes"
        else:
            r["fix_status"] = "confirmed" if r["stratum"] == "routine" else "corrected"
            r["fix_date"] = "2026-07-01" if r["stratum"] == "routine" else "2026-07-10"
    s[0]["fix_date"] = "2026-07-04" if s[0]["kind"] == "fix" else s[0]["fix_date"]
    res = score(p, "q1", s)
    assert res["fix_dates"]["status_agreement"] == 1.0
    assert res["fix_dates"]["share_within_1_day"] < 1.0


def test_retest_rows_show_the_original_prefill_not_the_answer():
    from snapshot.review import retest_rows
    cve = pd.DataFrame([{"cve_id": "CVE-1", "affected": ["acme|gateway"], "cvss_base": 9.1, "date_published": "2026-07-01",
                         "credit_values": [], "fix_links": [], "ref_links": []}])
    earlier = [_row(item_id="3", kind="fix", cve_id="CVE-1", month="2026-07", slot="a_edge", rank="1",
                    fix_status="corrected", fix_date="2026-07-15", prefill_date="2026-07-01", prefill_source="GitHub release v2"),
               _row(item_id="9", kind="fix", cve_id="CVE-404", fix_status="confirmed")]   # record not found: skipped
    rows = retest_rows(cve, earlier, ["2026-10", "2026-11", "2026-12"])
    assert len(rows) == 1
    r = rows[0]
    assert r["task"] == "patch_date" and r["retest"] is True
    assert r["patch_date"] == "2026-07-01" and r["patch_source"] == "GitHub release v2"
    assert "2026-07-15" not in str(r)
