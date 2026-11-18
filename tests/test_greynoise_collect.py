"""GreyNoise collector (X28, author 18 Nov 2026): counts and dates only, rolling window."""
import datetime as dt

from snapshot.collect import greynoise as G

TAGS = {"tags": [{"id": "1", "cves": ["CVE-1"], "created_at": "2026-10-21T00:00:00Z"},
                 {"id": "2", "cves": ["CVE-1"], "created_at": "2026-10-25T00:00:00Z"},
                 {"id": "3", "cves": ["CVE-2"], "created_at": "2026-11-03T00:00:00Z"}]}


def fake(counts):
    def get(path, key, params=None, pause=0):
        if path == "/v3/tags":
            return TAGS, "ok"
        cve = path.rsplit("/", 1)[-1]
        c = counts.get(cve, 0)
        return {"exploitation_activity": {"activity_seen": c > 0, "threat_ip_count_1d": c,
                                          "threat_ip_count_10d": c, "threat_ip_count_30d": c,
                                          "benign_ip_count_30d": 0, "last_seen": "2026-11-18T00:00:00Z",
                                          "ips": ["1.2.3.4"]}}, "ok"
    return get


def test_tag_dates_take_the_earliest_tag():
    t = G.tag_dates("k", fake({}))
    assert t["CVE-1"] == {"tag_first_created": "2026-10-21", "tags": 2}


def test_quarterly_counts_and_never_keeps_ips(tmp_path):
    s = G.quarterly("2026Q4", tmp_path, "k", fake({"CVE-1": 5}),
                    flaws=[{"cve": "CVE-1", "kev_date": "2026-10-26"}, {"cve": "CVE-9", "kev_date": "2026-11-01"}])
    assert s == {"quarter": "2026Q4", "flaws": 2, "tagged": 1, "tag_before_kev": 1, "activity_seen": 1, "calls": 3}
    text = (tmp_path / "quarter-2026Q4.csv").read_text()
    assert "1.2.3.4" not in text and "2026-10-21" in text


def test_quarter_bounds():
    assert G.quarter_bounds("2026Q4") == (dt.date(2026, 10, 1), dt.date(2026, 12, 31))
    assert G.quarter_bounds("2027Q1") == (dt.date(2027, 1, 1), dt.date(2027, 3, 31))


def test_weekly_first_seen_and_rolling_window(tmp_path):
    old = tmp_path / "weekly"; old.mkdir()
    (old / "2026-01-01.csv").write_text("x")
    s1 = G.weekly(tmp_path, "k", dt.date(2026, 11, 22), fake({"CVE-2": 3}))
    assert s1["cves"] == 2 and s1["new_first_seen"] == 1 and s1["pruned_files"] == 1
    s2 = G.weekly(tmp_path, "k", dt.date(2026, 11, 29), fake({"CVE-1": 4, "CVE-2": 3}))
    assert s2["new_first_seen"] == 1 and s2["first_seen_total"] == 2
    fs = (tmp_path / "first_seen.csv").read_text()
    assert "CVE-2,2026-11-22,2026-11-12,2026-11-03" in fs and "CVE-1,2026-11-29" in fs
    assert "1.2.3.4" not in (tmp_path / "weekly" / "2026-11-29.csv").read_text()
