import datetime as dt
import json
from pathlib import Path

import pytest

from snapshot.classify import ai_credit_matches, product_category, root_cause_class
from snapshot.collect.cve import parse_record
from snapshot.pull import infer_quarter, infer_run
from snapshot.util import Quarter

FIX = Path(__file__).parent / "fixtures" / "cves"


# --- quarters and run inference ---------------------------------------------

def test_quarter_bounds():
    q = Quarter.parse("2026Q4")
    assert q.start == dt.date(2026, 10, 1)
    assert q.end == dt.date(2026, 12, 31)
    assert Quarter.parse("2027Q1").end == dt.date(2027, 3, 31)
    assert str(q.shift(1)) == "2027Q1"
    assert str(q.shift(-4)) == "2025Q4"


@pytest.mark.parametrize(
    "day,quarter,run",
    [
        (dt.date(2027, 1, 1), "2026Q4", "provisional"),
        (dt.date(2027, 2, 1), "2026Q4", "final"),
        (dt.date(2027, 4, 1), "2027Q1", "provisional"),
        (dt.date(2027, 5, 1), "2027Q1", "final"),
        (dt.date(2026, 12, 1), "2026Q3", "dry-run"),
    ],
)
def test_run_inference(day, quarter, run):
    assert str(infer_quarter(day)) == quarter
    assert infer_run(day) == run


def test_bad_quarter():
    with pytest.raises(ValueError):
        Quarter.parse("2026-Q4")


# --- AI credit matching -------------------------------------------------------

@pytest.mark.parametrize(
    "credits,expected",
    [
        (["Google Big Sleep"], ["Big Sleep"]),
        (["Found by XBOW autonomous agent"], ["XBOW", "autonomous agent"]),
        (["Jane Doe with Claude (Anthropic)"], ["Claude"]),
        (["Claude Bernard"], []),                 # excluded personal name
        (["Nicky (@nicky-cc)"], []),
        (["Mythosphere Labs"], []),               # whole-word only
        (["reported via an LLM-assisted audit"], ["LLM"]),  # hyphen is a word boundary
        (["GPT-5.4-Cyber (OpenAI)"], ["GPT"]),
        (["LLM tooling by Acme"], ["LLM"]),
    ],
)
def test_ai_credit_matches(credits, expected):
    assert ai_credit_matches(credits) == expected


# --- root cause and category ----------------------------------------------------

def test_root_cause():
    assert root_cause_class(["CWE-787"]) == "memory_safety"
    assert root_cause_class(["NVD-CWE-noinfo", "CWE-89"]) == "injection_code_exec"
    assert root_cause_class(["CWE-22"]) == "path_file"
    assert root_cause_class([]) == "other_unknown"
    assert root_cause_class(["CWE-672"]) == "other_unknown"


def test_product_category():
    assert product_category(["Fortinet|FortiOS"]) == "a_edge"
    assert product_category(["Palo Alto Networks|PAN-OS"]) == "a_edge"
    assert product_category(["Progress|MOVEit Transfer"]) == "b_web_collab"
    assert product_category(["OpenClaw|OpenClaw"]) == "c_other"
    assert product_category(["Acme|Casablanca"]) == "c_other"  # 'asa' only as a whole word


# --- CVE record parsing ---------------------------------------------------------

def _load(name):
    return json.loads((FIX / name).read_text())


def test_parse_published_record():
    row = parse_record(_load("CVE-2026-45005.json"))
    assert row["cve_id"] == "CVE-2026-45005"
    assert row["state"] == "PUBLISHED"
    assert row["cna"] == "VulnCheck"
    assert row["date_published"].year == 2026
    assert row["cwe_ids"][0] == "CWE-672"
    assert row["affected"] == ["OpenClaw|OpenClaw"]
    assert row["has_cisa_adp"] is True


def test_parse_credits():
    row = parse_record(_load("CVE-2026-45000.json"))
    assert row["credit_values"][0].startswith("Nicky")
    assert row["ai_credit_terms"] == []


def test_parse_rejected_record():
    row = parse_record(_load("CVE-2026-45219.json"))
    assert row["state"] == "REJECTED"
    assert row["cvss_base"] is None
