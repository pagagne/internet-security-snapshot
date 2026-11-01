import datetime as dt
import json

from snapshot import reportpage as RP

R = {"quarter": "2026Q3", "run": "final", "kev_added_in_quarter": 10, "prefill_assumed": 3,
     "prefill_sources": {"GitHub": 7, "assumed": 3},
     "I3": {"n": 10, "n_measured": 10, "median_days_fix_to_exploit": 15.0, "ci90": [7.0, 25.6], "zero_day_share_x10": 0.2,
            "bounds": {"n_fix_date_bounded": 2, "n_exploit_before_kev": 3, "median_days_high": 5.0,
                       "zero_day_share_low": 0.3, "zero_day_share_high": 0.8}},
     "I2": {"median_days_t0_to_exploit": 8.0, "ci90": [3.5, 17.5], "share_exploited_on_or_before_t0": 0.23, "share_ci90": [0.16, 0.31]},
     "I5": {"published_by_year": {"2025": 100, "2026": 120}, "yoy_growth_pct": 20.0},
     "I5_count_check": {"rows": [{"year": 2026, "ours": 120, "nvd": 121, "diff": -0.008}], "flags": []},
     "I5_calendar_years": {"2025": 400}, "I8": {"cves": 120, "floor_pct": 0.4, "hand_pct": 0.8, "ceiling_pct": 0.8},
     "I7a_ransomware_postings": {"2026-07": 9, "2026-08": 11}, "not_computable": {"I1": "needs Shadowserver", "I4": "needs Shadowserver"}}


def test_build_end_to_end(tmp_path, monkeypatch):
    res = tmp_path / "runs"
    for name, run in (("2026-11-01T1000Z-practice_eval", "provisional"), ("2026-11-01T1100Z-practice_eval", "final")):
        (res / name).mkdir(parents=True)
        (res / name / "practice_eval.json").write_text(json.dumps(R | {"run": run}))
    monkeypatch.setattr(RP, "schedule_points", lambda: [(dt.date(2027, 1, 1), "Pilot report")])
    info = RP.build(res, tmp_path / "out", today=dt.date(2026, 11, 1), pdf=False)
    assert info["keys"] == ["2026Q3-provisional", "2026Q3-final"] and info["latest"] == "2026Q3-final" and info["available"]["T2"] is False
    out = tmp_path / "out"
    assert (out / "timeline.png").exists() and len(list((out / "reports/charts").glob("*.png"))) == 16   # 7 questions + flow, twice
    prov = (out / "reports/2026Q3-provisional.md").read_text()
    assert "SIMULATION" in prov and "[2026Q3-final](2026Q3-final.md)" in prov      # provisional links to its final
    final = (out / "reports/2026Q3-final.md").read_text()
    assert "## T1. The race" in final and "charts/2026Q3-final-T7.png" in final and "Nothing flagged" in final


def test_pdf_markdown_subset(tmp_path):
    from snapshot import reportpdf as P
    h = P.md_to_html("# Title\n\n> **SIM** note\n\n| a | b |\n|---|---|\n| 1 | *x* |\n\n- one\n- [two](t.md)\n\ntext ![c](missing.png)", tmp_path)
    assert "<h1>Title</h1>" in h and "<blockquote><b>SIM</b> note</blockquote>" in h
    assert "<th>a</th>" in h and "<td><i>x</i></td>" in h and '<li><a href="t.md">two</a></li>' in h
    assert '<img src="missing.png"' in h


def test_news_and_daily(tmp_path):
    last, nxt = RP.news(dt.date(2027, 1, 10))
    assert "2027" in last and nxt and last != nxt
    RP.daily(tmp_path, dt.date(2026, 11, 1))
    assert (tmp_path / "timeline.png").exists()
    svg = (tmp_path / "news-light.svg").read_text()
    assert "Latest" in svg and "Next" in svg and (tmp_path / "news-dark.svg").exists()


def test_at_a_glance_grouped(tmp_path):
    md = RP.report_md("2026Q3-final", R | {"_source": "x"}, [], True, None)
    assert md.index("### The race and the speed of attack") < md.index("### AI's role") < md.index("<sub>All figures")
    assert "- **T1 The race" in md and "| <sub>T7" in md


def test_exploratory_parts_news_list(tmp_path):
    explo = tmp_path / "exploratory"; explo.mkdir()
    (explo / "feed-screen-2026-08-candidates.csv").write_text(
        "date,feed,title,link,ai_term,attack_term\n2026-08-02,F,A | title,https://www.example.org/a,ai,attack\n")
    (explo / "feed-screen-2026-08-decisions.csv").write_text(
        "n,decision,reason,abstract,key_findings,basis,report\n0,logged,r,COPIED ABSTRACT,Our note.,title,\n")
    L = RP.exploratory_parts("2026Q3-final", R, explo, tmp_path / "reports")
    text = "\n".join(L)
    assert "## Part 2." in text and "## Part 3." in text and "1 logged as new cases" in text
    page = (tmp_path / "reports/2026Q3-final-news-2026-08.md").read_text()
    assert "[A / title](https://www.example.org/a)" in page and "example.org" in page and "Our note." in page
    assert "COPIED ABSTRACT" not in page                    # abstracts stay private


def test_part3_hugging_face_and_optional_trends(tmp_path):
    explo = tmp_path / "exploratory"; (explo / "ai_tool_landscape").mkdir(parents=True)
    import shutil
    png = tmp_path / "x.png"; png.write_bytes(b"\x89PNG")
    shutil.copy(png, explo / "ai_tool_landscape" / "hf-2026-10-30-1-new-per-month.png")
    L = "\n".join(RP.exploratory_parts("2026Q3-final", R, explo, tmp_path / "reports"))
    assert "### Hugging Face" in L and "charts/2026Q3-final-hf-1-new-per-month.png" in L
    assert "Trends we noticed" not in L                                    # optional: absent unless written
    (explo / "trends").mkdir(); (explo / "trends" / "2026Q3.md").write_text("Our own words.")
    assert "Our own words." in "\n".join(RP.exploratory_parts("2026Q3-final", R, explo, tmp_path / "reports"))
