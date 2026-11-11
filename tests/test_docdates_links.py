"""Document dates in titles and the cross-reference check (author, 11 Nov 2026)."""
import datetime as dt

from snapshot import docdates, links, manual


def test_title_date_format_and_restamp():
    d = dt.date(2026, 11, 3)
    assert docdates.want_title("# Operations", d) == "# Operations (updated 3 Nov 2026)"
    assert docdates.want_title("# Operations (updated 1 Oct 2026)", d) == "# Operations (updated 3 Nov 2026)"
    assert docdates._strip_title("# A (updated 1 Oct 2026)\n\nbody") == "# A\n\nbody"


def test_slug_and_anchors():
    text = "# Title\n\n## The 2027 calendar\n\n## Notes\n\n## Notes\n\n```\n## not a heading\n```\n<a id=\"x-1\"></a>"
    a = links.anchors(text)
    assert {"the-2027-calendar", "notes", "notes-1", "x-1"} <= a and "not-a-heading" not in a


def test_manual_numbers_and_chapters():
    parts = [("Part I", ["a.md", "b.md"]), ("Part II", ["c.md"])]
    assert manual._numbers(parts) == {"a.md": "1.1", "b.md": "1.2", "c.md": "2.1"}
    body = "## One\n\ntext\n\n```\n## code\n```\n\n## Two"
    assert manual._chapters(body) == ["One", "Two"]
    marked = manual._mark_chapters(body, "docs/X.md")
    assert '<a id="doc-docs-x-md-c1"></a>' in marked and '<a id="doc-docs-x-md-c2"></a>' in marked


def test_repository_links_land():
    from snapshot.util import _repo_root
    assert links.check(_repo_root()) == []
