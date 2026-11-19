"""One credits block for every output (config/credits.yaml, snapshot.credits)."""
from pathlib import Path

from snapshot import credits
from snapshot.reportpdf import _inline


def test_every_collected_source_is_credited_and_copies_current():
    assert credits.problems() == []


def test_required_wording():
    by = {s["key"]: s for s in credits.load()}
    assert "not endorsed or certified by the NVD" in by["nvd"]["notice"]
    assert "MITRE" in by["cve_program"]["notice"]
    assert by["ransomware_live"]["credit"] == "Source: Ransomware.live"
    assert by["greynoise"]["credit"] == "Data provided by GreyNoise."
    assert "APNIC Labs" in by["apnic_labs"]["credit"]
    assert "CC BY 4.0" in by["red_hat"]["credit"] and by["red_hat"]["link"]


def test_block_on_report_pages_and_pdf_links():
    from snapshot import reportpage
    assert "block_md" in Path(reportpage.__file__).read_text()
    md = credits.block_md()
    assert md.startswith("## Data sources and credits") and "Ransomware.live" in md
    assert '<a href="https://www.ransomware.live/">' in _inline("- x <https://www.ransomware.live/>", Path("."))
