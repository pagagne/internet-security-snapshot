"""README workflow schedule (author's request, 31 Oct 2026)."""
from snapshot import workflows as W


def test_readme_workflow_table_is_current():
    assert W.main(["check"]) == 0, "run: python -m snapshot.workflows build"


def test_cron_in_plain_words():
    assert W.cron_text("23 11 * * *") == "daily at 11:23 UTC"
    assert W.cron_text("17 13 * * 3") == "Wednesdays at 13:17 UTC"
    assert W.cron_text("41 8 5 * *") == "the 5th of each month at 08:41 UTC"
    assert W.cron_text("0 6 1 1,4,7,10 *") == "1st Jan/Apr/Jul/Oct at 06:00 UTC"
