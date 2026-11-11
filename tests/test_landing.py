"""Landing-page pictures (author's decisions, 31 Oct 2026)."""
from snapshot import landing as L


def test_ring_is_current():
    assert L.main(["check"]) == 0, "run: python -m snapshot.landing build"


def test_two_rings_kept_apart():
    p = {"measures": ["I2", "I3", "X1"]}
    assert L.weight(p, "core") == 2 and L.weight(p, "exploratory") == 1 and L.weight(p) == 7
    pieces = L.load()["pieces"]
    assert all(p["tier"] in {"core", "companion"} and isinstance(p["collected"], bool) for p in pieces)
    assert all(0 < L.collected_share(pieces, r) < 100 for r in L.RINGS)
    assert not any(L.weight(p, "core") == 0 for p in L.ring_pieces(pieces, "core"))   # rings kept apart


def test_pending_sources_are_never_contacted(tmp_path, monkeypatch):
    called = []
    monkeypatch.setattr(L, "ping", lambda s: called.append(s["name"]) or {"state": "error" if s["name"] == "NVD" else "ok"})
    res = L.status(tmp_path, pause=0)
    pending = {s["name"] for s in L.load()["sources"] if s.get("pending")}
    assert pending and not pending & set(called)
    assert "ransomware.live" not in called and res["ransomware.live"]["state"] == "unchecked"
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


def test_go_live_copy_points_at_the_public_repository():
    from snapshot import golive
    t = golive.public_readme('<img src="docs/landing/coverage-light.svg"> [SOP](docs/SOP_MANUAL_RUNS.md) [x](https://a.org)')
    assert 'src="https://raw.githubusercontent.com/pagagne/internet-security-snapshot/main/docs/landing/coverage-light.svg"' in t
    assert "(https://github.com/pagagne/internet-security-snapshot/blob/main/docs/SOP_MANUAL_RUNS.md)" in t
    assert "(https://a.org)" in t
