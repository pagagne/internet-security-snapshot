from snapshot.research.ai_trackers import data_links, text_of


def test_text_of_drops_scripts_and_tags():
    t = text_of("<html><script>x=1</script><h1>Data</h1><p>MIT &amp; free</p></html>")
    assert "x=1" not in t and "Data" in t and "MIT & free" in t


def test_data_links_same_site_only():
    page = '<a href="/incidents.json">j</a><a href="https://other.example/x.csv">o</a><a href="/about/">a</a>'
    assert data_links("https://hackingincidents.ai/data/", page) == ["https://hackingincidents.ai/incidents.json"]
