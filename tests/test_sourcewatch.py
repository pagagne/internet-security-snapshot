"""Weekly source watch (author's decision, 30 Oct 2026)."""
from pathlib import Path

import yaml

from snapshot import sourcewatch as W

ROOT = Path(__file__).resolve().parents[1]


def test_config_is_complete_and_https():
    srcs = yaml.safe_load((ROOT / W.CONFIG).read_text())["sources"]
    assert len({s["url"] for s in srcs}) == len(srcs)
    for s in srcs:
        assert s["url"].startswith("https://"), s["name"]
        assert s["kind"] in ("data", "terms") and s.get("used_by"), s["name"]
    used = " ".join(s["used_by"] for s in srcs if s["kind"] == "data")
    for core in ("cve", "kev", "nvd", "epss", "sec"):
        assert f"core {core}" in used, core


def test_visible_text_ignores_scripts_and_layout():
    a = W.visible_text("<p>Use with credit.</p><script>var t=1</script><div>  Rate: 1/hour</div>")
    b = W.visible_text("<div><p>Use   with credit.</p></div><script>var t=2</script><p>Rate: 1/hour</p>")
    assert a == b == "Use with credit.\nRate: 1/hour"


def test_shape():
    assert W.shape(b'{"b":1,"a":[]}', "application/json", "x") == "json keys: a,b"
    assert W.shape(b"cve,epss\nCVE-1,0.1\n", "text/csv", "x") == "text: cve,epss"
    assert W.shape(b"lastModifiedDate:2026-10-30T08:00\nsize:5\n", "text/plain", "x") == "fields: lastModifiedDate,size"
    assert W.shape(b'{"0":{"cik":1,"ticker":"A"},"1":{"cik":2,"ticker":"B"}}', "application/json", "x") \
        == "json numbered entries of: cik,ticker"


def _src(kind="data"):
    return {"name": "Example", "kind": kind, "url": "https://example.org/x", "used_by": "core kev"}


def test_first_run_sets_baseline_then_reports_changes(tmp_path):
    state, out = tmp_path / "state", tmp_path / "out"
    rec = {"name": "Example", "kind": "data", "url": "https://example.org/x", "status": 200,
           "final": "example.org/x", "ctype": "application/json", "bytes": 1000, "shape": "json keys: a"}
    _, ch = W.run([_src()], state, out, "2026-10-30", pause=0, fetch=lambda s: (dict(rec), None))
    assert ch == {} and "First run" in (out / "changes.md").read_text()
    moved = {**rec, "final": "example.org/new", "shape": "json keys: a,b", "bytes": 100}
    _, ch = W.run([_src()], state, out, "2026-11-04", pause=0, fetch=lambda s: (dict(moved), None))
    msg = " ".join(ch["Example"])
    assert "now ends up at" in msg and "structure changed" in msg and "size fell" in msg


def test_terms_copied_and_archived_only_when_wording_changes(tmp_path):
    state, out, saved = tmp_path / "state", tmp_path / "out", []
    def page(text):
        return lambda s: ({"name": "Example", "kind": "terms", "url": s["url"], "status": 200,
                           "final": "example.org/x", "ctype": "text/html",
                           "text_sha256": W.hashlib.sha256(text.encode()).hexdigest(),
                           "words": len(text.split())}, text)
    save = lambda u: saved.append(u) or "https://web.archive.org/web/1/" + u
    W.run([_src("terms")], state, out, "2026-10-30", pause=0, fetch=page("Credit required."), save=save)
    W.run([_src("terms")], state, out, "2026-11-04", pause=0, fetch=page("Credit required."), save=save)
    assert len(saved) == 1
    _, ch = W.run([_src("terms")], state, out, "2026-11-11", pause=0, fetch=page("No reuse allowed."), save=save)
    assert len(saved) == 2 and "wording changed" in ch["Example"][0]
    assert len(list((state / "terms" / "example").glob("*.txt"))) == 2
    assert "No reuse allowed." in (out / "changes.md").read_text()


def test_every_watched_terms_page_is_in_the_register():
    reg = (ROOT / "docs/TERMS_OF_USE.md").read_text()
    for s in yaml.safe_load((ROOT / W.CONFIG).read_text())["sources"]:
        if s["kind"] == "terms":
            assert s["url"] in reg, s["name"]
