from snapshot import fixdates as F


def test_release_day():
    assert F.release_day("Microsoft", "2026-06-09") == "2026-06-09"   # second Tuesday
    assert F.release_day("Microsoft", "2026-06-10") == "2026-06-09"   # within a day
    assert F.release_day("Microsoft", "2026-06-15") == ""
    assert F.release_day("Oracle", "2026-07-21") == "2026-07-21"      # third Tuesday, CPU month
    assert F.release_day("Oracle", "2026-08-18") == ""                # not a CPU month
    assert F.release_day("Android", "2026-05-01") == "2026-05-01"
    assert F.release_day("Fortinet", "2026-06-09") == ""
    assert F.release_day("SAP", "2026-11-10") == "2026-11-10"
    assert F.release_day("Sapphire", "2026-11-10") == ""
    assert F.release_day("Adobe", "not a date") == ""


def test_hint_only_on_note():
    d, note, hand = F.prefill_exploited("CVE-2026-1", [], "Adobe", "2026-06-09")
    assert d == "2026-06-09" and hand is True
    assert note.startswith("ASSUMED") and note.endswith(F.CALENDAR_HINT)
