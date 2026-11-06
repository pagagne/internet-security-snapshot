import json
from snapshot import golive as G

README = "# T\n\nbanner\n\n## Mission\n\nm\n\n## Licence\n\nl\n"


def test_compose_mirror_and_flip(tmp_path, monkeypatch):
    run = tmp_path / "2026-11-01T0000Z-practice_eval"; run.mkdir()
    R = {"quarter": "2026Q3", "I3": {"median_days_fix_to_exploit": 15.0, "ci90": [7.0, 25.6]},
         "I2": {"median_days_t0_to_exploit": 8.0, "ci90": [3.5, 17.5], "share_exploited_on_or_before_t0": 0.23,
                "share_ci90": [0.16, 0.31]}, "I5": {"yoy_growth_pct": 10.0},
         "I8": {"hand_pct": 0.8, "floor_pct": 0.4, "ceiling_pct": 0.8}, "not_computable": {"I1": "", "I4": ""},
         "prefill_assumed": 3, "kev_added_in_quarter": 10}
    (run / "practice_eval.json").write_text(json.dumps(R))
    monkeypatch.setattr(G, "PRACTICE", str(tmp_path))
    layout = {"sections": [{"readme": "top", "status": "live"}, {"draft": "results", "status": "draft", "cleared": False},
                           {"readme": "Mission", "status": "live"}, {"readme": "Licence", "status": "live"}]}
    page, probs = G.compose(tmp_path, README, layout)
    assert not probs and page.index("banner") < page.index("Latest results") < page.index("## Mission")
    assert "DRAFT section" in page and "SIMULATION" in page and "results.md" in page and "results.md" in page
    results = G.results_page(tmp_path)                                     # the results page (author, 5 Nov 2026)
    assert "| 15 |" in results and "How to read this page" in results and "T7 AI's share" in results
    text, flip = G.flip_check(tmp_path, README, layout)
    assert "DRAFT section" not in text
    assert any("not cleared" in p for p in flip) and any("simulation" in p for p in flip)
    layout["sections"].append({"readme": "Gone", "status": "live"})
    assert G.compose(tmp_path, README, layout)[1] == ["README section missing: Gone"]
    layout["sections"] = [x for x in layout["sections"] if x.get("readme") != "Licence"]   # a public section left out
    assert any("not in the layout" in p and "Licence" in p for p in G.compose(tmp_path, README, layout)[1])


def test_real_readme_and_layout_match(tmp_path, monkeypatch):
    """Every public README section is in the landing layout and every layout section exists (5 Nov 2026)."""
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    monkeypatch.setattr(G, "PRACTICE", str(tmp_path))
    _, probs = G.compose(tmp_path, (root / "README.md").read_text(), G.load_layout(root))
    assert not [p for p in probs if "README section" in p], probs
