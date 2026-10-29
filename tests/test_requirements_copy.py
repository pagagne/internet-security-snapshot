"""requirements.txt is an exact copy of requirements.lock (29 Oct 2026).

GitHub's dependency graph does not read the name requirements.lock, so Dependabot alerts saw
only the 17 direct dependencies. The copy lets it see every pinned package. Installs still use
requirements.lock; regenerate both together (cp requirements.lock requirements.txt).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_requirements_txt_matches_lock():
    assert (ROOT / "requirements.txt").read_text() == (ROOT / "requirements.lock").read_text(), \
        "requirements.txt must be an exact copy of requirements.lock: cp requirements.lock requirements.txt"
