"""Monthly AI-attack feed screen (29 Oct 2026): parsing and filtering."""
import datetime as dt

from snapshot import feedscreen as F

RSS = b"""<?xml version="1.0"?><rss><channel>
<item><title>Attackers used an AI agent to breach cloud accounts</title><link>https://ex.org/a</link>
<pubDate>Mon, 26 Oct 2026 10:00:00 GMT</pubDate><description>LLM-driven intrusion</description></item>
<item><title>New patch for printer firmware</title><link>https://ex.org/b</link><pubDate>Mon, 26 Oct 2026 10:00:00 GMT</pubDate></item>
<item><title>Old AI agent attack story</title><link>https://ex.org/c</link><pubDate>Mon, 01 Jun 2026 10:00:00 GMT</pubDate></item>
</channel></rss>"""
ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry>
<title>Hackers abuse ChatGPT in phishing campaign</title><link href="https://ex.org/d"/><updated>2026-10-27T08:00:00Z</updated>
<summary>details</summary></entry></feed>"""


def test_parse_and_screen():
    since = dt.datetime(2026, 9, 25, tzinfo=dt.timezone.utc)
    ai, attack = F._rx(["AI agent", "LLM", "ChatGPT"]), F._rx(["breach", "phishing", "attack"])
    items = F.parse(RSS) + F.parse(ATOM)
    assert len(items) == 4 and items[3]["link"] == "https://ex.org/d"
    hits = F.screen(items, ai, attack, since)
    assert [h["link"] for h in hits] == ["https://ex.org/a", "https://ex.org/d"]


def test_whole_word_terms():
    ai = F._rx(["LLM", "Claude"])
    assert ai.search("an LLM agent")
    assert not ai.search("Claudette's bakery")


def test_cyrillic_ai_term_is_a_whole_word():
    ai = F._rx(["ИИ", "нейросет"])
    assert ai.search("атака с помощью ИИ") and ai.search("нейросети")
    assert not ai.search("кампании и операции")
