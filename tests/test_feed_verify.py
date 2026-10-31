"""Feed verification (author's safeguards, 29 Oct 2026)."""
from snapshot.research import feed_verify as V


def test_feed_links_stay_in_domain():
    f = {"domain": "example.org", "url": "https://example.org/feed/"}
    html = ('<link rel="alternate" type="application/rss+xml" href="/feed/">'
            '<link rel="alternate" type="application/rss+xml" href="https://evil.test/rss">'
            '<a href="https://blog.example.org/rss.xml">RSS</a>')
    assert V.feed_links(html, "https://example.org/", f) == ["https://example.org/feed/", "https://blog.example.org/rss.xml"]
