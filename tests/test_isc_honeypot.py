"""ISC honeypot capture keeps aggregates only and dates CVEs by their earliest URL."""
from snapshot.collect.isc_honeypot import aggregate

CATS = ["/a.php?x=1\tPHP RCE\tCVE-2026-109618 attempt", "/b\tScanning\tgeneric probe"]
SUM = ["/a.php?x=1\t2026-10-17\t2026-10-24\t40", "/b\t2025-01-01\t2026-10-24\t5",
       "/cgi-bin/x?cve-2024-3400\t2024-04-13\t2024-05-01\t3", "/zzz\t2020-01-01\t2020-01-02\t1"]


def test_aggregates_and_cve_dates():
    cat, cve, n = aggregate(CATS, SUM)
    assert n == {"categorised_urls": 2, "summary_urls": 4, "summary_urls_categorised": 2}
    php = [r for r in cve if r["cve"] == "CVE-2026-109618"][0]
    assert php["first_seen"] == "2026-10-17" and php["requests"] == 40
    assert any(r["cve"] == "CVE-2024-3400" for r in cve)          # CVE named in an uncategorised URL
    assert all("url" not in r for r in cat + cve)                   # never a URL in the output
    assert {r["category"] for r in cat} == {"PHP RCE", "Scanning"}
