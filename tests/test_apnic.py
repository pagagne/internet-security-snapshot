"""APNIC Labs world-map tables (X20): parsed as published. Synthetic figures only."""
import pytest

from snapshot.collect import apnic

DNSSEC = """<p>30 day average (01/10/2026 - 30/10/2026)</p>
      var table = new google.visualization.arrayToDataTable([
        ['CC', 'Country', 'DNSSEC Validates','Partial Validates','Total Validates','Samples','Weight','Weighted Samples']        ,
["<a href=\\"/dnssec/ZZ\\">ZZ</a>","<a href=\\"/dnssec/ZZ\\">Testland</a>, <a href=\\"/dnssec/XL\\">Some Region</a>, <a href=\\"/dnssec/XB\\">Somewhere</a>",{v: 12.50, f:'12.50%'}, {v: 1.25, f: '1.25%'}, {v: 13.75, f: '13.75%'},1000,0.50,500],
["<a href=\\"/dnssec/YY\\">YY</a>","<a href=\\"/dnssec/YY\\">Otherland</a>, <a href=\\"/dnssec/XL\\">Some Region</a>, <a href=\\"/dnssec/XB\\">Somewhere</a>",{v: 2.00, f:'2.00%'}, {v: 0.00, f: '0.00%'}, {v: 2.00, f: '2.00%'},20,1.00,20]
      ]);
"""
RPKI = """<p>7 day span (24/10/2026 - 30/10/2026)</p>
      var table = new google.visualization.arrayToDataTable([
        ['CC', 'Country', 'I-RoV Filtering','Samples','Weight','Weighted Samples']        ,
["<a href=\\"/rpki/ZZ\\">ZZ</a>","<a href=\\"/rpki/ZZ\\">Testland</a>, <a href=\\"/rpki/XL\\">Some Region</a>, <a href=\\"/rpki/XB\\">Somewhere</a>",{v: 40.00, f:'40.00%'},300,1.20,360],
      ]);
"""


def test_dnssec_table_as_published():
    df = apnic.parse("dnssec", DNSSEC)
    assert list(df.cc) == ["ZZ", "YY"]
    r = df.iloc[0]
    assert (r.dnssec_validating_pct, r.dnssec_partial_pct, r.dnssec_total_pct) == (12.5, 1.25, 13.75)
    assert (r.samples, r.weight, r.weighted_samples) == (1000, 0.5, 500)
    assert (r.country, r.region, r.continent) == ("Testland", "Some Region", "Somewhere")
    assert (r.window_days, r.window_kind, r.window_start, r.window_end) == (30, "average", "2026-10-01", "2026-10-30")


def test_rpki_table_as_published():
    r = apnic.parse("rpki", RPKI).iloc[0]
    assert (r.cc, r.rpki_irov_filtering_pct, r.samples, r.window_days, r.window_end) == ("ZZ", 40.0, 300, 7, "2026-10-30")


def test_block_or_challenge_is_a_gap_not_worked_around():
    with pytest.raises(RuntimeError, match="not worked around"):
        apnic.parse("dnssec", "<html>Please complete the captcha</html>")


def test_missing_table_or_window_fails_loudly():
    with pytest.raises(ValueError):
        apnic.parse("dnssec", "<p>nothing here</p>")
    with pytest.raises(ValueError, match="country table"):
        apnic.parse("rpki", "<p>7 day span (24/10/2026 - 30/10/2026)</p>")


def test_credit_line_names_apnic_labs():
    assert "APNIC Labs" in apnic.CREDIT
