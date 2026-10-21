from snapshot.cohort import draw_key, draw_order, select_month


def test_draw_is_reproducible_and_order_independent():
    ids = ["CVE-2026-1", "CVE-2026-2", "CVE-2026-3", "CVE-2026-4"]
    a = draw_order("2027-02", "a_edge", ids)
    b = draw_order("2027-02", "a_edge", list(reversed(ids)))
    assert a == b
    assert sorted(a) == sorted(ids)


def test_draw_differs_by_month_and_slot():
    ids = [f"CVE-2026-{i}" for i in range(50)]
    assert draw_order("2027-02", "a_edge", ids) != draw_order("2027-03", "a_edge", ids)
    assert draw_order("2027-02", "a_edge", ids) != draw_order("2027-02", "b_web_collab", ids)


def test_draw_key_is_sha256_hex():
    k = draw_key("2027-02", "a_edge", "CVE-2026-1")
    assert len(k) == 64 and int(k, 16) >= 0


def test_select_skips_failed_checks_and_repeats():
    month = "2027-02"
    pools = {
        "a_edge": ["CVE-A1", "CVE-A2"],
        "b_web_collab": [],
        "c_other": ["CVE-C1", "CVE-C2", "CVE-C3"],
        "d_ai_credited": ["CVE-A1", "CVE-D1"],
    }
    first_c = draw_order(month, "c_other", pools["c_other"])[0]

    def check(slot, cve):
        if slot == "c_other":
            return cve != first_c          # first drawn fails internet-facing check
        return True

    res = {r.slot: r for r in select_month(month, pools, check)}
    assert res["a_edge"].pick in pools["a_edge"]
    assert res["b_web_collab"].pick is None and res["b_web_collab"].pool_size == 0
    assert res["c_other"].pick != first_c
    assert (first_c, "failed hand check") in res["c_other"].skipped
    assert res["d_ai_credited"].pick != res["a_edge"].pick


def test_select_waits_for_review():
    res = select_month("2027-02", {"c_other": ["CVE-C1"]}, lambda s, c: None)
    c = [r for r in res if r.slot == "c_other"][0]
    assert c.pick is None and c.pending == ["CVE-C1"]
