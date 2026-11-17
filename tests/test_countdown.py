"""Countdown to the next study run on the landing page (author, 17 Nov 2026)."""
import datetime as dt

from snapshot import reportpage as R


def test_labels_and_days():
    assert R.next_run(dt.date(2026, 11, 17)) == (dt.date(2026, 12, 1), "Dry run 1 of the quarterly pull")
    assert R.next_run(dt.date(2026, 12, 2))[1] == "Dry run 2, with all available sources"
    assert R.next_run(dt.date(2026, 12, 16)) == (dt.date(2027, 1, 1), "Pilot run: Q4 2026 quarterly pull")
    assert R.next_run(dt.date(2027, 1, 2))[1] == "Pilot run: Q4 2026 final pull"
    assert R.next_run(dt.date(2027, 2, 2)) == (dt.date(2027, 4, 1), "Q1 2027 quarterly pull")


def test_svg_says_days_only():
    s = R.countdown_svg(dt.date(2026, 11, 17), "dark")
    assert "in 14 days" in s and "Tue 1 Dec 2026" in s and "hour" not in s
    assert "today" in R.countdown_svg(dt.date(2026, 12, 1), "light")
    assert "tomorrow" in R.countdown_svg(dt.date(2026, 11, 30), "light")
