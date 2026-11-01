from snapshot.research import fixdate_sources as F


def test_date_in_url_and_earliest(monkeypatch):
    monkeypatch.setattr(F, "provider", lambda host: None)
    found, status = F.csaf_date("CVE-2026-1", ["https://source.android.com/docs/security/bulletin/2026-08-01",
                                               "https://example.com/advisory/123"])
    assert found == {"2026-08-01": "date in advisory URL"}
    assert status.startswith("no CSAF provider")
    assert F.earliest({"2026-08-03": "x", "2026-07-30": "y"}) == ("2026-07-30", "y")
    assert F.earliest({}) == ("", "")


def test_distro_ids():
    assert F.DISTRO.match("USN-7000-1") and F.DISTRO.match("DSA-5800-1") and not F.DISTRO.match("GHSA-xxxx")
