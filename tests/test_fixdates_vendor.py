from unittest import mock

from snapshot import fixdates


def test_fix_later_signal():
    assert not fixdates.fix_later_signal(["Initial public release."])
    assert fixdates.fix_later_signal(["Initial public release.", "Updated fixed release information and ..."])
    assert fixdates.fix_later_signal(["Initial publication.", "Updated the Fix release timeline for 10.2.16-h7."])
    assert not fixdates.fix_later_signal(["Initial public release.", "Added information about active exploitation."])


def test_prefill_exploited_cisco_and_fallbacks():
    csaf = {"document": {"tracking": {"initial_release_date": "2026-08-11T16:00:00Z", "revision_history": [
        {"summary": "Initial public release."}, {"summary": "Updated fixed release information."}]}}}
    with mock.patch.object(fixdates, "_vendor_json", return_value=csaf), \
         mock.patch.object(fixdates, "prefill", return_value=("2026-08-11", "ASSUMED same day")):
        d, src, hand = fixdates.prefill_exploited("CVE-X", ["https://sec.cloudapps.cisco.com/x/cisco-sa-abc-123"], "Cisco", "2026-08-11")
        assert (d, hand) == ("2026-08-11", True) and "cisco-sa-abc-123" in src
    with mock.patch.object(fixdates, "_vendor_json", return_value=None), \
         mock.patch.object(fixdates, "prefill", return_value=("2026-01-02", "ASSUMED same day")):
        assert fixdates.prefill_exploited("CVE-X", [], "Acme", "2026-01-02", "2025-12-20")[:2] == ("2025-12-20", "vendor disclosure date (CVE datePublic); fix date not stated")
        assert fixdates.prefill_exploited("CVE-X", [], "Acme", "2026-01-02")[2] is True
