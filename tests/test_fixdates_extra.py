from snapshot import fixdates as F


def test_dated_advisory_link_only_on_advisory_hosts():
    d, note = F.dated_advisory_link(["https://source.android.com/docs/security/bulletin/2026-08-01",
                                     "https://someblog.example.com/2026/07/15/exploit-writeup"])
    assert d == "2026-08-01" and "android" in note
    assert F.dated_advisory_link(["https://someblog.example.com/2026/07/15/x"]) == ("", "")


def test_order_and_no_ghsa_published(monkeypatch):
    calls = []
    monkeypatch.setattr(F, "prefill", lambda refs, pub: (pub, "ASSUMED x"))
    monkeypatch.setattr(F, "_vendor_json", lambda url: calls.append(url) or None)
    monkeypatch.setattr(F, "_get", lambda path: calls.append(path) or None)
    # nothing found anywhere: falls to datePublic, then to the assumed publication date
    assert F.prefill_exploited("CVE-2026-1", [], "Acme", "2026-07-02", "2026-06-30")[1].startswith("vendor disclosure")
    assert F.prefill_exploited("CVE-2026-1", [], "Acme", "2026-07-02")[1].startswith("ASSUMED")
    assert all("type=reviewed" in c for c in calls if c.startswith("/advisories"))
    # deps.dev release beats datePublic
    monkeypatch.setattr(F, "depsdev_patched_release", lambda c: ("2026-06-20", "deps.dev: pkg 1.2 released"))
    d, src, hand = F.prefill_exploited("CVE-2026-1", [], "Acme", "2026-07-02", "2026-06-30")
    assert (d, hand) == ("2026-06-20", False) and src.startswith("deps.dev")
