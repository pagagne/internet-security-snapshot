"""AI-fix probe (19 Nov 2026): marks are labels only."""
import pandas as pd

from snapshot.research import ai_fix_probe as P


def test_marks():
    msg = "Fix overflow\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
    assert P.marks(msg, "someone", "web-flow", "") == ["co-author: Claude"]
    assert P.marks("plain fix", "someone", "web-flow", "Copilot") == ["agent account opened the pull request"]
    assert P.marks("Generated with [Claude Code](https://claude.com)", "x", "y", "") == ["footer: generated with"]
    assert P.marks("plain fix", "a", "b", "c") == []


def test_sample_is_fixed_and_uses_commit_links():
    cve = pd.DataFrame({"cve_id": ["C1", "C2"], "date_published": ["2026-02-01", "2026-03-01"],
                        "fix_links": [["https://github.com/o/r/commit/abcdef1"], []],
                        "ref_links": [[], ["https://example.com/x"]]})
    s1, s2 = P.sample(cve, n=5), P.sample(cve, n=5)
    assert s1 == s2 and s1["2026H1"] == [("C1", "o", "r", "abcdef1")] and s1["2025H1"] == []
