"""GreyNoise probe: never keeps an IP address (author, 17 Nov 2026)."""
from snapshot.research import greynoise_probe as g


def test_scrub_removes_ips_keeps_times_and_counts():
    body = {"activity": [{"timestamp": "2026-11-01T01:00:00Z", "ip_count": 5,
                          "ips": ["1.2.3.4", "2001:db8::1"], "note": "seen from 8.8.8.8"}],
            "source_ip": "9.9.9.9"}
    out = g.scrub(body)
    flat = str(out)
    for ip in ("1.2.3.4", "2001:db8::1", "8.8.8.8", "9.9.9.9"):
        assert ip not in flat
    assert out["activity"][0]["timestamp"] == "2026-11-01T01:00:00Z"
    assert out["activity"][0]["ip_count"] == 5


def test_series_summary_reads_points_dates_and_first_activity():
    body = {"activity": [{"timestamp": "2026-09-01T00:00:00Z", "count": 0},
                         {"timestamp": "2026-09-02T00:00:00Z", "count": 3},
                         {"timestamp": "2026-09-03T00:00:00Z", "count": 1}]}
    s = g.series_summary(body)
    assert s["points"] == 3 and s["first"].startswith("2026-09-01") and s["step_hours"] == 24
    assert s["first_day_with_activity"] == "2026-09-02"
    assert s["count_fields"]["count"]["sum"] == 4


def test_series_summary_reads_activity_windows():
    body = {"slug": "x", "activity": {"malicious": [
                {"start": "2026-11-06T00:00:00Z", "end": "2026-11-08T00:00:00Z", "timestamp": "2026-11-06T00:00:00Z"},
                {"start": "2026-11-12T00:00:00Z", "end": "2026-11-16T00:00:00Z", "timestamp": "2026-11-12T00:00:00Z"}]},
            "aggregations": {"classification": {"malicious": 18}},
            "metadata": {"granularity": "1d", "start_date": "2026-08-19", "end_date": "2026-11-17"}}
    s = g.series_summary(body)
    assert s["points"] == 2 and s["first_day_with_activity"] == "2026-11-06"
    assert s["metadata"]["start_date"] == "2026-08-19" and s["aggregations"]["malicious"] == 18
