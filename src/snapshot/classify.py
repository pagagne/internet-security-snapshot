"""Rule-based classifiers driven by the frozen config files.

- AI-credit matching (indicator I8, cohort category d): config/ai_credit_terms.yaml
- Root-cause class from CWE (cohort tag): config/root_cause_map.yaml
- Cohort product category (a/b/c): config/cohort_rules.yaml
"""

from __future__ import annotations

import re
from functools import lru_cache

from .util import load_config


@lru_cache(maxsize=1)
def _ai_terms():
    cfg = load_config("ai_credit_terms.yaml")
    terms = (
        list(cfg.get("tool_names", []))
        + list(cfg.get("generic_phrases", []))
        + list(cfg.get("lab_names", []))
    )
    flags = 0 if cfg.get("match", {}).get("case_sensitive") else re.IGNORECASE
    whole = cfg.get("match", {}).get("whole_word", True)
    patterns = []
    for term in terms:
        body = re.escape(term)
        if whole:
            # Whole word: not glued to other letters or digits. Hyphens and
            # punctuation count as boundaries, so "GPT-5" matches "GPT".
            body = rf"(?<![A-Za-z0-9]){body}(?![A-Za-z0-9])"
        patterns.append((term, re.compile(body, flags)))
    exclusions = [re.compile(re.escape(x), flags) for x in cfg.get("exclusions", [])]
    return patterns, exclusions


@lru_cache(maxsize=1)
def lab_name_terms() -> frozenset[str]:
    """Terms that name an AI lab rather than a tool; matches need stricter review."""
    return frozenset(load_config("ai_credit_terms.yaml").get("lab_names", []))


def lab_name_only(terms: list[str]) -> bool:
    """True when every matched term is a lab name, i.e. no tool or AI phrase matched."""
    labs = lab_name_terms()
    return len(terms) > 0 and all(t in labs for t in terms)


def ai_credit_matches(credit_values: list[str]) -> list[str]:
    """Return the AI terms matched in a CVE's credit values (empty if none).

    A match is a candidate only; the pre-registration requires a hand check
    before it counts.
    """
    patterns, exclusions = _ai_terms()
    found: list[str] = []
    for value in credit_values:
        text = value or ""
        for ex in exclusions:
            text = ex.sub(" ", text)
        for term, pat in patterns:
            if pat.search(text) and term not in found:
                found.append(term)
    return found


# Words that suggest an AI tool may be involved, used only to surface possible
# newcomers for review; they never count as AI credits by themselves.
_AI_SIGNAL = re.compile(
    r"(?<![A-Za-z0-9])(AI|agent|agents|agentic|LLM|model|automated|autonomous|"
    r"machine learning|neural|copilot|bot)(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9])(?!CVE-|CWE-|GHSA-)[A-Z][A-Za-z]+-\d+(\.\d+)?(?![A-Za-z0-9])",  # e.g. "Foo-3.5", not CVE IDs
    re.IGNORECASE,
)


def unmatched_ai_signals(credit_values: list[str]) -> list[str]:
    """Credit texts that look AI-related but match no listed term.

    These are candidates for the newcomer watchlist, reviewed by hand each quarter.
    """
    out = []
    for value in credit_values:
        if value and _AI_SIGNAL.search(value) and not ai_credit_matches([value]):
            out.append(value)
    return out


@lru_cache(maxsize=1)
def _cwe_index() -> tuple[dict[int, str], list[str]]:
    cfg = load_config("root_cause_map.yaml")
    index: dict[int, str] = {}
    order: list[str] = []
    for cls, spec in cfg["classes"].items():
        order.append(cls)
        for cwe in spec.get("cwe", []) or []:
            index[int(cwe)] = cls
    return index, order


def root_cause_class(cwe_ids: list[str]) -> str:
    """Map a list of CWE identifiers (e.g. 'CWE-787') to one root-cause class.

    The first CWE (in record order) that maps to a class wins; otherwise
    'other_unknown'.
    """
    index, _ = _cwe_index()
    for cwe in cwe_ids:
        m = re.search(r"(\d+)", cwe or "")
        if m and int(m.group(1)) in index:
            return index[int(m.group(1))]
    return "other_unknown"


@lru_cache(maxsize=1)
def _category_rules():
    cfg = load_config("cohort_rules.yaml")
    cats = []
    for key in ("a_edge", "b_web_collab"):
        words = [w.lower() for w in cfg["categories"][key]["product_keywords"]]
        pats = [re.compile(rf"(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])") for w in words]
        cats.append((key, pats))
    return cats


def product_category(affected: list[str]) -> str:
    """Category a, b or c for a list of 'vendor|product' strings."""
    text = " ; ".join(a.lower().replace("|", " ") for a in affected)
    for key, pats in _category_rules():
        if any(p.search(text) for p in pats):
            return key
    return "c_other"


@lru_cache(maxsize=1)
def _ai_software_patterns():
    words = load_config("ai_software_products.yaml")["products"]
    return [re.compile(rf"(?<![a-z0-9]){re.escape(w.lower())}(?![a-z0-9])") for w in words]


def is_ai_software(affected) -> bool:
    """Exploratory X5: does any affected vendor|product name an AI software product?"""
    text = " ; ".join(str(a).lower().replace("|", " ") for a in affected)
    return any(p.search(text) for p in _ai_software_patterns())
