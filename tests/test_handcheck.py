"""Review list -> Hand Check app items (19 Nov 2026)."""
import pandas as pd

from snapshot.handcheck import items

COLS = ["month", "slot", "draw_rank", "cve_id", "product", "cvss", "published", "task", "question", "credit",
        "terms", "examples", "auto_rule", "spot_check", "retest", "links", "answer", "patch_date", "patch_source", "notes"]


def row(**k):
    r = {c: "" for c in COLS}; r.update(k); return r


def test_kinds_order_and_race_filter():
    d = pd.DataFrame([
        row(month="2025-10", slot="c_other", draw_rank="2", cve_id="CVE-2", task="yes_no_then_patch_date"),
        row(month="2025-10", slot="c_other", draw_rank="1", cve_id="CVE-1", task="yes_no_then_patch_date"),
        row(month="2025-10", slot="a_edge", draw_rank="1", cve_id="CVE-3", task="patch_date"),
        row(month="2025-11", slot="d_ai_credited", cve_id="(empty)", task="none"),
        row(month="2025-10", slot="race", cve_id="CVE-9", task="patch_date", question="Race list: x Check this one."),
        row(month="2025-10", slot="race", cve_id="CVE-8", task="patch_date", question="Race list: x"),
        row(month="2025-10,2025-11", slot="T7", cve_id="CVE-5", task="ai_credit", credit="Google Big Sleep",
            terms="Big Sleep", examples="CVE-5 CVE-6", question="Applies to 14 CVE(s).", auto_rule="mention", spot_check="True"),
    ])
    its, stats = items([d, d.iloc[[6]]])   # the same credit text in a second quarter is asked once
    kinds = [(i["kind"], i.get("cve_id")) for i in its]
    assert kinds == [("fix", "CVE-3"), ("slot_c", "CVE-1"), ("slot_c", "CVE-2"), ("empty", "(empty)"),
                     ("fix", "CVE-9"), ("credit", "CVE-5")]
    assert stats["race_skipped_no_check_needed"] == 1
    c = its[-1]
    assert c["covers"] == 14 and c["spot_check"] is True and c["terms"] == ["Big Sleep"]
    assert [i["order"] for i in its] == list(range(1, 7))
    assert its[4]["slot"] == "race_kev" and its[1]["group"] == its[2]["group"] == "2025-10|c_other"
