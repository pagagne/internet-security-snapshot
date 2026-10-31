"""Landing-page pictures (author's decisions, 31 Oct 2026)."""
from snapshot import landing as L


def test_ring_is_current():
    assert L.main(["check"]) == 0, "run: python -m snapshot.landing build"


def test_slice_weights_count_core_three_times():
    assert L.weight({"measures": ["I2", "I3", "X1"]}) == 7
    assert L.weight({"measures": ["X7"]}) == 1
    pieces = L.load()["pieces"]
    assert all(p["tier"] in {"core", "companion"} and isinstance(p["collected"], bool) for p in pieces)
    assert 0 < L.collected_share(pieces) < 100


def test_pending_sources_are_never_contacted(tmp_path, monkeypatch):
    called = []
    monkeypatch.setattr(L, "ping", lambda s: called.append(s["name"]) or {"state": "error" if s["name"] == "NVD" else "ok"})
    res = L.status(tmp_path, pause=0)
    pending = {s["name"] for s in L.load()["sources"] if s.get("pending")}
    assert pending and not pending & set(called)
    svg = (tmp_path / "banner-light.svg").read_text()
    assert 'fill="none"' in svg and L.THEMES["light"]["error"] in svg and "checked " in svg
    assert res["NVD"]["state"] == "error" and (tmp_path / "status.json").exists()


def test_snapshots_roll_up_changes(tmp_path):
    import json
    store = tmp_path / "landing"
    banner = tmp_path / "b"; banner.mkdir()
    for f in ("banner-light.svg", "banner-dark.svg"):
        (banner / f).write_text("<svg/>")
    (banner / "status.json").write_text(json.dumps({"checked": "x", "results": {"NVD": {"state": "ok"}}}))
    L.capture("baseline", banner, "2026-10-31", store)
    d = L.capture("pilot", None, "2027-01-01", store)
    cfg = (d / "coverage.yaml").read_text().replace(
        '"Public exploit code",              tier: companion, collected: false', '"Public exploit code",              tier: companion, collected: true')
    (d / "coverage.yaml").write_text(cfg)
    text = L.rollup_text(store)
    assert "Now collected: Public exploit code" in text and "## Whole study so far" in text
    assert (store / "snapshots" / "2026-10-31-baseline" / "summary.md").exists()
