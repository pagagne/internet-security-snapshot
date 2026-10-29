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


def test_prefill_exploited_kernel_siemens_redhat():
    assumed = ("2026-05-02", "ASSUMED same day")
    commits = {"/repos/torvalds/linux/commits/aaaaaaaaaaaa": {"commit": {"committer": {"date": "2026-03-10T00:00:00Z"}}},
               "/repos/torvalds/linux/commits/bbbbbbbbbbbb": None,
               "/repos/gregkh/linux/commits/bbbbbbbbbbbb": {"commit": {"committer": {"date": "2026-03-12T00:00:00Z"}}}}
    refs = ["https://git.kernel.org/stable/c/aaaaaaaaaaaa", "https://git.kernel.org/stable/c/bbbbbbbbbbbb"]
    with mock.patch.object(fixdates, "prefill", return_value=assumed), \
         mock.patch.object(fixdates, "_get", side_effect=lambda p: commits.get(p)):
        d, src, hand = fixdates.prefill_exploited("CVE-K", refs, "Linux", "2026-05-02")
        assert d == "2026-03-10" and "kernel" in src and hand is True
    ssa = {"document": {"tracking": {"initial_release_date": "2026-06-09T00:00:00Z",
                                     "revision_history": [{"summary": "Publication Date"}]}}}
    with mock.patch.object(fixdates, "prefill", return_value=assumed), \
         mock.patch.object(fixdates, "_vendor_json", return_value=ssa):
        d, src, hand = fixdates.prefill_exploited(
            "CVE-S", ["https://cert-portal.siemens.com/productcert/html/ssa-123456.html"], "Siemens", "2026-06-09")
        assert (d, hand) == ("2026-06-09", False) and "SSA-123456" in src
    vex = {"vulnerabilities": [{"remediations": [{"category": "vendor_fix", "date": "2026-04-20T00:00:00Z"},
                                                 {"category": "vendor_fix", "date": "2026-04-02T00:00:00Z"},
                                                 {"category": "workaround", "date": "2026-03-01T00:00:00Z"}]}]}
    with mock.patch.object(fixdates, "prefill", return_value=assumed), \
         mock.patch.object(fixdates, "_vendor_json", return_value=vex):
        d, src, hand = fixdates.prefill_exploited("CVE-2026-1", [], "Red Hat", "2026-04-02")
        assert (d, hand) == ("2026-04-02", False) and "Red Hat" in src
