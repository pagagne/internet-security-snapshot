"""Report pages, question charts and the study timeline (author's decisions, 1 Nov 2026).

The landing page carries status and charts; the findings live in separate report pages, one per
run: a provisional and a final page each quarter (the provisional page stays, frozen, with a
link to the final), the pilot, and the annual report. Each report is a page in the repository;
a PDF archive copy with a citation link follows before the pilot. Every chart on the landing
page links to its section of the latest report, one chart per registered question (T1-T7), and
a timeline strip shows where the study stands.

Every test run goes through the whole chain (author, 1 Nov 2026): evaluation result -> charts
and tables -> report page -> landing mirror. Until the pilot the input is the private practice
evaluation and every page is marked SIMULATION. Drafts are built in the private repository
(go-live/) and never published before the flip.

    python -m snapshot.reportpage build --results DIR --out DIR
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

QUESTIONS = [
    ("T1", "The race", "Are defenders closing exposed flaws faster than attackers exploit them?",
     "Median days from the fix to the first attack, for every flaw first added to CISA's exploited list in the quarter. Larger is better for defenders."),
    ("T2", "Exposure half-life", "How fast do vulnerable systems disappear after a patch?",
     "Median days until half the exposed systems are gone. Needs Shadowserver's scan data."),
    ("T3", "Speed of attack", "How fast are newly disclosed flaws exploited?",
     "Median days from publication to the first attack, and the share attacked on or before publication."),
    ("T4", "Old flaws", "Do attackers keep using flaws over a year old?",
     "Share of attacks seen by honeypots that target flaws over 12 months old. Needs Shadowserver's honeypot data."),
    ("T5", "Discovery pressure", "Is the number of published flaws rising?",
     "Published CVE records in the quarter against the same quarter in earlier years (rejected records excluded)."),
    ("T6", "Breaches", "Are breaches and ransomware rising?",
     "Ransomware leak-site postings (totals only) and SEC cyber-incident filings per 1,000 companies."),
    ("T7", "AI's share", "How often are AI tools credited with finding flaws?",
     "Share of the quarter's CVE records whose credits mention an AI tool or AI lab, with a floor and ceiling."),
]
GROUPS = [   # "At a glance" themes (author, 1 Nov 2026): plain heading, why it matters, its questions
    ("The race and the speed of attack", ["T1", "T3"],
     "Whether defenders get fixes out before attackers strike, and how quickly newly published flaws are "
     "attacked. A longer gap from fix to attack is good news for defenders; a shorter gap from publication "
     "to attack means less time to patch."),
    ("How long flaws stay exposed", ["T2", "T4"],
     "How fast vulnerable systems disappear from the internet after a fix, and how much attack traffic still "
     "targets flaws over a year old. Both need Shadowserver's data, which is awaiting permission."),
    ("How many flaws and breaches", ["T5", "T6"],
     "The pressure on defenders: how many new flaws are published compared with the same quarter in earlier "
     "years, and how many ransomware postings and company breach filings appear."),
    ("AI's role", ["T7"],
     "How often the people credited with finding a flaw mention an AI tool or AI lab: a floor (the tool is "
     "named in a clear role), a headline and a ceiling, since credits rarely say how a flaw was found."),
]
ACCENT, GRAY, LIGHT = "#1D9E75", "#B4B2A9", "#D3D1C7"


def load_results(d: Path) -> list[tuple[str, dict]]:
    """Every evaluation result under d, newest per quarter and run kept: [(key, R)] sorted."""
    best: dict[str, tuple[str, dict]] = {}
    found = sorted(d.glob("*practice_eval/practice_eval.json")) if d.exists() else []
    ev = d.parent / "evaluations"                 # evaluations made by the Quarterly pull (1 Nov 2026)
    found += sorted(ev.glob("*/evaluation.json")) if ev.exists() else []
    for f in sorted(found, key=lambda p: p.parent.name):
        R = json.loads(f.read_text())
        key = f"{R['quarter']}-{R.get('run', 'final')}"
        best[key] = (f.parent.name, R)           # later folders (newer runs) win
    order = lambda k: (k.rsplit("-", 1)[0], 0 if k.endswith("-provisional") else 1)   # provisional, then final
    return [(k, best[k][1] | {"_source": best[k][0]}) for k in sorted(best, key=order)]


def _ax(figsize=(6.4, 3.2)):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=figsize, dpi=130)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return plt, fig, ax


def _point_range(plt, ax, labels, vals, los, his, unit):
    xs = range(len(labels))
    for x, v, lo, hi in zip(xs, vals, los, his):
        if lo is not None and hi is not None:
            ax.plot([x, x], [lo, hi], color=LIGHT, lw=8, solid_capstyle="round", zorder=1)
        ax.plot([x], [v], "o", color=ACCENT, ms=9, zorder=2)
        ax.annotate(f"{v:g}{unit}", (x, v), xytext=(10, -4), textcoords="offset points", fontsize=9)
    ax.set_xticks(list(xs), labels)
    ax.set_xlim(-0.6, max(len(labels) - 0.4, 1.4))
    ax.set_ylim(bottom=0)


def chart(qid: str, series: list[tuple[str, dict]], path: Path, simulation: bool) -> bool:
    """One chart per question across every available quarter. Returns False if not available."""
    plt, fig, ax = _ax()
    labels = [k.split("-")[0] for k, _ in series]
    R = series[-1][1]
    ok = True
    if qid == "T1":
        vals = [r["I3"]["median_days_fix_to_exploit"] for _, r in series]
        ci = [r["I3"].get("ci90") or [None, None] for _, r in series]
        _point_range(plt, ax, labels, vals, [c[0] for c in ci], [c[1] for c in ci], " d")
        ax.set_ylabel("Days, fix to first attack")
        ax.set_title("T1 The race: median days from fix to first attack", loc="left", fontsize=10)
    elif qid == "T3":
        vals = [r["I2"]["median_days_t0_to_exploit"] for _, r in series]
        ci = [r["I2"].get("ci90") or [None, None] for _, r in series]
        _point_range(plt, ax, labels, vals, [c[0] for c in ci], [c[1] for c in ci], " d")
        ax.set_ylabel("Days, publication to first attack")
        share = R["I2"].get("share_exploited_on_or_before_t0")
        ax.set_title(f"T3 Speed of attack: median days (attacked on or before publication: {share:.0%})", loc="left", fontsize=10)
    elif qid == "T5":
        yrs = R["I5"]["published_by_year"]
        ys, vs = [str(y) for y in yrs], list(yrs.values())
        ax.bar(ys, vs, color=[LIGHT] * (len(vs) - 1) + [ACCENT], width=.6)
        for x, v in enumerate(vs):
            ax.text(x, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
        q = R["quarter"][-2:]
        ax.set_ylabel(f"Published CVE records in {q}")
        ax.set_title(f"T5 Discovery pressure: {q} of each year ({R['I5'].get('yoy_growth_pct'):+g}% on last year)", loc="left", fontsize=10)
    elif qid == "T6":
        rw = R.get("I7a_ransomware_postings") or {}
        if rw:
            ax.bar(list(rw), list(rw.values()), color=ACCENT, width=.6)
            for x, v in enumerate(rw.values()):
                ax.text(x, v, f"{v:,}", ha="center", va="bottom", fontsize=8)
            ax.set_ylabel("Ransomware postings (totals)")
        sec = (R.get("I7b_sec_8k_item105") or {}).get("per_1000")
        ax.set_title("T6 Breaches: ransomware postings by month"
                     + (f"; SEC filings {sec:.2f} per 1,000 companies" if sec is not None else ""), loc="left", fontsize=10)
        ok = bool(rw)
    elif qid == "T7":
        i8 = R["I8"]
        names = ["Floor", "Headline", "Ceiling"]
        vals = [i8.get("floor_pct", 0), i8.get("hand_pct", 0), i8.get("ceiling_pct", 0)]
        ax.bar(names, vals, color=[LIGHT, ACCENT, LIGHT], width=.6)
        for x, v in enumerate(vals):
            ax.text(x, v, f"{v:.1f}%", ha="center", va="bottom", fontsize=9)
        ax.set_ylabel("% of the quarter's CVE records")
        ax.set_title(f"T7 AI's share: credits mentioning AI ({i8.get('cves', 0):,} records)", loc="left", fontsize=10)
    else:                                   # T2, T4: waiting on a source
        ok = False
        ax.axis("off")
        why = R.get("not_computable", {}).get({"T2": "I1", "T4": "I4"}[qid], "not available")
        name = {q[0]: q[1] for q in QUESTIONS}[qid]
        ax.text(0.5, 0.6, f"{qid} {name}", ha="center", fontsize=12, color="#5F5E5A", transform=ax.transAxes)
        ax.text(0.5, 0.38, "Not available yet: " + why.split("(")[0].strip(), ha="center", fontsize=9,
                color="#888780", transform=ax.transAxes, wrap=True)
    if qid in ("T5", "T6") and ok:
        from matplotlib.ticker import FuncFormatter
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    if simulation:
        fig.text(0.99, 0.02, "SIMULATION", ha="right", fontsize=8, color="#BA7517", weight="bold")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return ok


def timeline(milestones: list[tuple[dt.date, str]], today: dt.date, path: Path) -> None:
    """The study's running timeline with a 'you are here' marker (from docs/schedule/schedule.yaml)."""
    import matplotlib.dates as md
    plt, fig, ax = _ax((11, 3.0))
    start, end = dt.date(2026, 10, 1), dt.date(2028, 4, 30)
    ax.plot([start, end], [0, 0], color=LIGHT, lw=6, solid_capstyle="round")
    ax.plot([start, min(today, end)], [0, 0], color=ACCENT, lw=6, solid_capstyle="round")
    for i, (d, text) in enumerate(m for m in milestones if start <= m[0] <= end):
        past = d <= today
        ax.plot([d], [0], "o", ms=7, color=ACCENT if past else "white", mec=ACCENT if past else GRAY, mew=1.5, zorder=3)
        y = (0.45, -0.45, 0.85, -0.85)[i % 4]     # four label rows so close milestones do not collide
        ax.annotate(("✓ " if past else "") + text, (d, 0), xytext=(d, y), fontsize=7, ha="center",
                    va="bottom" if y > 0 else "top", color="#2C2C2A" if past else "#5F5E5A",
                    arrowprops=dict(arrowstyle="-", color=LIGHT, lw=.8))
    ax.axvline(today, color="#D85A30", lw=1.2, ls="--")
    ax.text(today, 1.42, f"you are here, {today:%d %b %Y}", color="#D85A30", fontsize=8, ha="center")
    ax.set_ylim(-1.6, 1.6); ax.set_yticks([])
    ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_major_locator(md.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(md.DateFormatter("%b %Y")); ax.tick_params(axis="x", labelsize=8, length=0)
    ax.set_title("Where the study stands", loc="left", fontsize=10)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


TIMELINE_POINTS = [   # short labels for the strip; dates come from the schedule
    ("cutover", "Cutover"), ("dry-run", "Dry run"), ("freeze", "Core freeze"),
    ("pull-provisional@2027-01-01", "Pilot report"), ("pull-provisional@2027-04-01", "First scored quarter"),
    ("pull-provisional@2027-07-01", "Q2 2027"), ("pull-provisional@2027-10-01", "Q3 2027"),
    ("pull-provisional@2028-01-01", "Q4 2027"), ("annual-review@2028-03-15", "Annual report"),
    ("closing-rerun", "Closing re-run"),
]


def schedule_points() -> list[tuple[dt.date, str]]:
    from . import schedule as S
    occ = S.expand(S.load())
    by_uid = {o["uid"]: o["date"] for o in occ}
    by_id: dict[str, list] = {}
    for o in occ:
        by_id.setdefault(o["id"], []).append(o["date"])
    out = []
    for ref, label in TIMELINE_POINTS:
        d = by_uid.get(ref) or (by_id.get(ref) or [None])[0]
        if d:
            out.append((d, label))
    return sorted(out)


NEWS_THEMES = {"light": {"text": "#1f2328", "muted": "#59636e", "accent": "#1D9E75"},
               "dark": {"text": "#e6edf3", "muted": "#9198a1", "accent": "#5DCAA5"}}


def news(today: dt.date) -> tuple[str, str]:
    """Latest and next milestone from the study calendar (author, 1 Nov 2026: a one-line status
    under the banner, written automatically)."""
    from . import schedule as S
    table = S.readme_table(S.expand(S.load()), S.load_milestones())
    rows = []
    for line in table.split("\n")[2:]:
        when, text = [c.strip() for c in line.strip().strip("|").split("|", 1)]
        first = re.search(r"(\d{1,2})(?:-\d{1,2})? ([A-Z][a-z]{2})", when)
        year = re.search(r"(\d{4})", when)
        if first and year:
            rows.append((dt.datetime.strptime(f"{first[1]} {first[2]} {year[1]}", "%d %b %Y").date(), text.strip()))
    rows.sort()
    last = [r for r in rows if r[0] <= today][-1:] or [(None, "")]
    nxt = [r for r in rows if r[0] > today][:1] or [(None, "")]
    f = lambda r: f"{r[1]} ({r[0].day} {r[0]:%b %Y})" if r[0] else "-"
    return f(last[0]), f(nxt[0])


def news_svg(today: dt.date, theme: str) -> str:
    from xml.sax.saxutils import escape
    c = NEWS_THEMES[theme]
    last, nxt = news(today)
    cut = lambda s: s if len(s) <= 110 else s[:107] + "..."
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="46" viewBox="0 0 780 46" '
            f'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" role="img" '
            f'aria-label="Latest: {escape(last)}. Next: {escape(nxt)}">'
            f'<text x="0" y="17" font-size="12" fill="{c["text"]}"><tspan font-weight="600" fill="{c["accent"]}">Latest </tspan>'
            f'{escape(cut(last))}</text>'
            f'<text x="0" y="38" font-size="12" fill="{c["muted"]}"><tspan font-weight="600">Next </tspan>{escape(cut(nxt))}</text>'
            "</svg>\n")


def daily(out: Path, today: dt.date | None = None) -> None:
    """Drawn every day by the Source status run: the timeline strip and the news line."""
    today = today or dt.date.today()
    timeline(schedule_points(), today, out / "timeline.png")
    for theme in NEWS_THEMES:
        (out / f"news-{theme}.svg").write_text(news_svg(today, theme))


def _n(v, pct=False):
    if v is None:
        return "-"
    return f"{100 * v:.0f}%" if pct else (f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}")


def summary_rows(R: dict) -> list[tuple[str, str, str]]:
    i3, i2, i8, nc = R["I3"], R["I2"], R["I8"], R.get("not_computable", {})
    ci = lambda c, pct=False: "{} to {}".format(*[_n(x, pct) for x in (c or [None, None])])
    rows = [("T1 The race: median days from fix to first attack", _n(i3.get("median_days_fix_to_exploit")), ci(i3.get("ci90"))),
            ("T2 Exposure half-life", "not available" if "I1" in nc else "-", "-"),
            ("T3 Median days from publication to first attack", _n(i2.get("median_days_t0_to_exploit")), ci(i2.get("ci90"))),
            ("T3 Share attacked on or before publication", _n(i2.get("share_exploited_on_or_before_t0"), True), ci(i2.get("share_ci90"), True)),
            ("T4 Share of attacks on flaws over a year old", "not available" if "I4" in nc else "-", "-"),
            ("T5 Published CVE records, growth on the same quarter last year", f"{_n(R['I5'].get('yoy_growth_pct'))}%", "-")]
    if R.get("I7a_ransomware_postings"):
        rows.append(("T6 Ransomware postings in the quarter", _n(sum(R["I7a_ransomware_postings"].values())), "-"))
    if (R.get("I7b_sec_8k_item105") or {}).get("per_1000") is not None:
        rows.append(("T6 SEC cyber-incident filings per 1,000 companies", f"{R['I7b_sec_8k_item105']['per_1000']:.2f}", "-"))
    rows.append(("T7 Share of CVE records crediting AI (headline)", f"{i8.get('hand_pct', 0):.1f}%",
                 f"floor {i8.get('floor_pct', 0):.1f}%, ceiling {i8.get('ceiling_pct', 0):.1f}%"))
    return rows


def report_md(key: str, R: dict, series: list[tuple[str, dict]], simulation: bool, final_key: str | None,
              extra: list[str] | None = None) -> str:
    q, run = R["quarter"], R.get("run", "final")
    title = f"# Internet Security Snapshot: {q} report ({run})" + (" — SIMULATION" if simulation else "")
    L = [title, ""]
    if simulation:
        L += ["> **SIMULATION, not a result.** Built end to end from the private evaluation "
              f"({R.get('_source')}) of a quarter outside the registered study, with fix dates before the "
              "author's hand check, to test the whole flow and the report's design. Real reports start with "
              "the pilot (1 Jan 2027) and the first scored quarter (1 Apr 2027).", ""]
    if run == "provisional":
        L += ["> **Provisional.** Published within two days of the quarter's end, before the hand check. "
              + (f"The final report: [{final_key}]({final_key}.md)." if final_key else
                 "The final report follows one month later; this page then stays as it is, with a link to it."), ""]
    L += [f"PDF archive copy: [{key}.pdf]({key}.pdf)" + (" (simulation; not for citation)" if simulation else ""), "",
          "## How the three parts fit together", "",
          f"![Three separate streams](charts/{key}-flow.png)", "",
          "The report has three parts that are kept apart and never combined in the scores (author's rule, 31 Oct 2026). "
          "**Part 1, the core data,** is scored: public records of flaws, attacks, fixes and breaches answer the seven "
          "registered questions (T1-T7) and alone decide the labels. **Part 2, the news feeds,** is exploratory: each "
          "month about sixty feeds are read for reports of attacks that used AI, sorted by hand into the AI attack log "
          "(X3). **Part 3, the tool and model sweeps,** is exploratory: each month GitHub is searched for "
          "security tools and Hugging Face for security-related AI models, counted by how they use AI, what they do "
          "and whether safety training was removed (X25). Parts 2 and 3 give context beside the scores and meet "
          "Part 1 only in the discussion, never in a label.", "",
          "## Part 1. Core data: the seven scored questions", "",
          "### At a glance", "",
          "Labels (Improving, Worsening, Rising, Falling or No clear direction) are given from Q1 2027 by the "
          "registered rule, each with its companion check. " + ("None in a practice quarter." if simulation else ""), ""]
    rows = summary_rows(R)
    for head, qids, why in GROUPS:
        L += [f"#### {head}", "", why, ""]
        L += [f"- **{a}:** {b}" + (f" (90% interval or range: {c})" if c != "-" else "")
              for a, b, c in rows if a.split()[0] in qids]
        L.append("")
    L += ["<sub>All figures in one table:</sub>", "", "| <sub>Question</sub> | <sub>This quarter</sub> | "
          "<sub>90% interval or range</sub> | <sub>Label</sub> |", "|---|---|---|---|"]
    L += [f"| <sub>{a}</sub> | <sub>{b}</sub> | <sub>{c}</sub> | <sub>{'simulation' if simulation else 'see section'}</sub> |"
          for a, b, c in rows]
    L.append("")
    for qid, name, ask, how in QUESTIONS:
        L += [f"### {qid}. {name}", "", f"*{ask}*", "", how, "", f"![{qid}](charts/{key}-{qid}.png)", ""]
        if qid == "T1":
            b = R["I3"].get("bounds") or {}
            L += [f"- Flaws counted: {R['I3'].get('n')}; with both dates: {R['I3'].get('n_measured')}",
                  f"- Share attacked before any fix existed (exploratory X10): {_n(R['I3'].get('zero_day_share_x10'), True)}",
                  f"- Fix date known only as a range: {b.get('n_fix_date_bounded', '-')} flaws; attack evidence before the "
                  f"KEV listing: {b.get('n_exploit_before_kev', '-')} flaws. Using that earlier evidence, the median is at "
                  f"most {_n(b.get('median_days_high'))} days and the zero-day share runs from "
                  f"{_n(b.get('zero_day_share_low'), True)} to {_n(b.get('zero_day_share_high'), True)}.", ""]
        if qid == "T5":
            cc = R.get("I5_count_check") or {}
            L += ["Count check against NVD (flagged above 5%): " + "; ".join(
                f"{r['year']} {('%+.1f%%' % (100 * r['diff'])) if r.get('diff') is not None else 'no answer'}" for r in cc.get("rows", []))
                + (". Flagged: " + ", ".join(map(str, cc["flags"])) if cc.get("flags") else ". Nothing flagged."), "",
                  "How T5 is scored with the 2026 surge in its baseline is decided on 21 Dec 2026 (core-freeze item 25).", ""]
    L += ["### Data and checks", "", f"- Flaws first added to CISA KEV in the quarter: {R.get('kev_added_in_quarter')}",
          f"- Fix dates ({R.get('fix_inputs', 'frozen bundle')}): " + ", ".join(
              f"{k} {v}" for k, v in (R.get("prefill_sources") or {}).items()),
          f"- Still an assumed fix date (the hand check replaces these): {R.get('prefill_assumed')}",
          "- Whole calendar years of published records: " + ", ".join(
              f"{y} {v:,}" for y, v in (R.get("I5_calendar_years") or {}).items()), "",
          "### Not available yet", ""] + [f"- {k}: {v}" for k, v in (R.get("not_computable") or {}).items()]
    L += [""] + (extra or []) + ["", "## About this report", "",
          f"Run: {q}, {run}. Source: {R.get('_source')}. Method: the pre-registration (OSF DOI 10.17605/OSF.IO/3XT82) "
          "and docs/EVALUATION_FLOW.md. This page is frozen once published; corrections are added as dated notes.", ""]
    return "\n".join(L)


# --- The three streams and the exploratory parts (author, 1 Nov 2026) ----------------------------
def flow_diagram(path: Path) -> None:
    """Three streams, side by side, never combined in the scores."""
    from matplotlib.patches import FancyBboxPatch
    plt, fig, ax = _ax((11, 4.4))
    ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 7.2)
    cols = [("Part 1. Core data (scored)", "#1D9E75", ["CVE records, NVD, CISA KEV,", "EPSS, fix dates, SEC filings,", "ransomware totals"],
             ["Quarterly pull, frozen", "and hand-checked"], ["Seven questions T1-T7", "decide the labels"]),
            ("Part 2. News feeds (exploratory)", "#7F77DD", ["About sixty security, government", "and news feeds"],
             ["Monthly screen, sorted", "by hand"], ["AI attack log (X3)", "context only"]),
            ("Part 3. Tool and model sweeps (exploratory)", "#BA7517", ["GitHub security tools,", "Hugging Face AI models"],
             ["Monthly search, counted by", "AI use, type and safety"], ["AI tool and model supply", "(X25) context only"])]
    for i, (title, colr, a, b, c) in enumerate(cols):
        x = 0.3 + i * 4
        ax.text(x + 1.7, 6.85, title, ha="center", fontsize=10, weight="bold", color=colr)
        for j, lines in enumerate((a, b, c)):
            y = 5.2 - j * 1.85
            ax.add_patch(FancyBboxPatch((x, y), 3.4, 1.2, boxstyle="round,pad=0.05,rounding_size=0.15",
                                        fc=colr if j == 2 else "white", ec=colr, lw=1.4, alpha=1 if j == 2 else 1))
            ax.text(x + 1.7, y + 0.6, "\n".join(lines), ha="center", va="center", fontsize=8.5,
                    color="white" if j == 2 else "#2C2C2A")
            if j < 2:
                ax.annotate("", (x + 1.7, y - 0.62), (x + 1.7, y - 0.02), arrowprops=dict(arrowstyle="-|>", color=colr, lw=1.2))
    ax.plot([0.3, 11.7], [0.55, 0.55], color=LIGHT, lw=1)
    ax.text(6, 0.15, "The three meet only in each report's discussion: side by side, never combined in a score or label.",
            ha="center", fontsize=8.5, color="#5F5E5A")
    fig.tight_layout(); path.parent.mkdir(parents=True, exist_ok=True); fig.savefig(path); plt.close(fig)


DECISION_WORDS = {"logged": "Logged as a new case", "second source": "Second source for a logged case",
                  "already logged": "Already in the log", "your judgement": "Author's judgement pending",
                  "excluded": "Excluded", "": "Not yet sorted"}


def _quarter_months(quarter: str) -> list[str]:
    y, q = int(quarter[:4]), int(quarter[-1])
    return [f"{y}-{m:02d}" for m in range(3 * q - 2, 3 * q + 1)]


def news_rows(explo: Path, month: str) -> list[dict]:
    """The month's sorted feed items: title, link, site, our decision and our own note. No copied
    article text (author, 1 Nov 2026: titles and links with our notes; abstracts stay private)."""
    import csv
    from urllib.parse import urlparse
    cands = list(csv.DictReader((explo / f"feed-screen-{month}-candidates.csv").open(encoding="utf-8")))
    decs = {int(r["n"]): r for r in csv.DictReader((explo / f"feed-screen-{month}-decisions.csv").open(encoding="utf-8"))}
    out = []
    for i, c in enumerate(cands):
        d = decs.get(i, {})
        out.append({"date": c.get("date", ""), "title": c.get("title", ""), "link": c.get("link", ""),
                    "site": (urlparse(c.get("link", "")).hostname or "").removeprefix("www."), "feed": c.get("feed", ""),
                    "decision": DECISION_WORDS.get(d.get("decision", ""), d.get("decision", "")),
                    "note": (d.get("key_findings") or d.get("reason") or "").strip()})
    return sorted(out, key=lambda r: r["date"], reverse=True)


def _cell(s: str) -> str:
    return " ".join(str(s).split()).replace("|", "/")


def exploratory_parts(key: str, R: dict, explo: Path, rdir: Path) -> list[str]:
    """Part 2 (news feeds, X3) and Part 3 (GitHub sweep, X25) of a report, from the private data."""
    import shutil
    charts = rdir / "charts"
    charts.mkdir(parents=True, exist_ok=True)
    L = ["## Part 2. News feeds: attacks that used AI (exploratory)", "",
         "*Context only: never part of a score or label.* Each month about sixty security research, government and "
         "news feeds are read for items that mention both AI and an attack. Each item is then sorted by hand: logged "
         "as a new case in the AI attack log (X3), a second source for a case already logged, or excluded (for "
         "example, AI only as the bait or the target). Only reports where a real attacker used AI against real "
         "systems are logged.", ""]
    have = sorted(p.name[len("feed-screen-"):len("feed-screen-") + 7] for p in explo.glob("feed-screen-????-??-decisions.csv"))
    months = [m for m in _quarter_months(R["quarter"]) if m in have]
    note = ""
    if not months and have:
        months, note = [have[-1]], f" (no screen in {R['quarter']}; the latest month is shown)"
    feed_png = explo / "feed_charts"
    if (feed_png / "attack-log.png").exists():
        shutil.copy(feed_png / "attack-log.png", charts / f"{key}-x3-attack-log.png")
        L += [f"![AI attack log by month](charts/{key}-x3-attack-log.png)", ""]
    for m in months:
        rows = news_rows(explo, m)
        if (feed_png / f"feed-screen-{m}.png").exists():
            shutil.copy(feed_png / f"feed-screen-{m}.png", charts / f"{key}-x3-feeds-{m}.png")
            L += [f"![Feed screen {m}](charts/{key}-x3-feeds-{m}.png)", ""]
        page = f"{key}-news-{m}.md"
        (rdir / page).write_text("\n".join(
            [f"# News feed screen, {m}{note}", "",
             f"Back to the report: [{key}]({key}.md#part-2-news-feeds-attacks-that-used-ai-exploratory)", "",
             "Every item the screen found, newest first: the article's title and link, the site, what we did with it "
             "and our own one-line note. The articles belong to their publishers; follow the link to read them.", "",
             "| Date | Article | Site | What we did | Our note |", "|---|---|---|---|---|"]
            + [f"| {r['date']} | [{_cell(r['title'])}]({r['link']}) | {_cell(r['site'])} | {r['decision']} | <sub>{_cell(r['note'])}</sub> |"
               for r in rows]) + "\n")
        logged = sum(r["decision"].startswith("Logged") for r in rows)
        L += [f"**{m}{note}:** {len(rows)} items screened, {logged} logged as new cases. "
              f"[Open the clickable list of articles]({page}).", ""]
    if not months:
        L += ["No feed screen yet.", ""]
    trends = explo / "trends" / f"{R['quarter']}.md"     # optional, our own words (author, 1 Nov 2026)
    if trends.exists():
        L += ["### Trends we noticed this quarter", "", trends.read_text().strip(), ""]
    L += ["## Part 3. Tool and model sweeps: GitHub and Hugging Face (exploratory)", "",
          "*Context only: never part of a score or label.* Each month GitHub is searched for public security tools "
          "in several languages. Each tool is counted once by how it uses AI (a hosted closed model, an open-weight or "
          "local model, both, or none named) and by what it does. Labels describe what a tool does, not who uses it or "
          "why: much attack tooling serves defenders' red teams and the reverse. Tools are counted, never named by "
          "their owners' usernames.", "", "### GitHub: AI security tools", ""]
    sweeps = sorted((explo / "ai_tool_sweeps").glob("*.csv"))
    figs = explo / "ai_tool_landscape"
    if sweeps:
        d = sweeps[-1].stem
        for suffix, cap in (("1-ai-use", "How the tools use AI"), ("3-new-per-month", "New tools per month"),
                            ("2-tool-types", "What the tools do"), ("7-targets-by-group", "What they target, by group"),
                            ("8-open-weight", "Which open-weight models they use")):
            f = figs / f"{d}-{suffix}.png"
            if f.exists():
                shutil.copy(f, charts / f"{key}-x25-{suffix}.png")
                L += [f"**{cap}** (sweep of {d})", "", f"![{cap}](charts/{key}-x25-{suffix}.png)", ""]
    else:
        L += ["No GitHub sweep yet.", ""]
    L += ["### Hugging Face: AI models and apps", "",
          "Hugging Face is where AI models themselves are published, including open-weight models whose safety "
          "training has been removed (\"uncensored\" or \"abliterated\" variants). The sweep counts originals only "
          "(compressed copies of another model are counted once, through the original). Security-related models and "
          "apps are shown apart from models advertised as safety-removed, which are mostly general chat models; that "
          "label comes from the model's own name and tags, so it is a floor, and a hand-checked sample gives its "
          "accuracy. Nothing is downloaded or run; individuals' items are never named by username.", ""]
    hf = sorted(figs.glob("hf-*-1-new-per-month.png")) if figs.exists() else []
    if hf:
        d = hf[-1].name[3:13]
        for suffix, cap in (("1-new-per-month", "New security-related models and apps per month (originals)"),
                            ("3-safety-removed-per-month", "New models advertised as safety-removed per month (originals; a floor)"),
                            ("2-safety-removed-by-lab", "Advertised as safety-removed, by the lab of the model modified")):
            f = figs / f"hf-{d}-{suffix}.png"
            if f.exists():
                shutil.copy(f, charts / f"{key}-hf-{suffix}.png")
                L += [f"**{cap}** (sweep of {d})", "", f"![{cap}](charts/{key}-hf-{suffix}.png)", ""]
    else:
        L += ["No Hugging Face sweep yet.", ""]
    L += crypto_section(explo)
    return L


def crypto_section(explo: Path) -> list[str]:
    """AI and cryptocurrency, from the crypto tag on the existing logs (author, 1 Nov 2026)."""
    import csv
    from .research.crypto_tag import is_crypto
    L = ["## AI and cryptocurrency (exploratory, tagged)", "",
         "*Context only.* Cases and tools that touch cryptocurrency, picked out by a tag on the logs above rather "
         "than a separate measure (author's decision, 1 Nov 2026): AI-run crypto scams and thefts, AI-found "
         "smart-contract flaws, and AI tools and models for smart-contract and wallet security on both sides. It may "
         "become a measure of its own at the March 2027 review.", ""]
    log = explo / "ai_attack_campaigns.csv"
    if log.exists():
        rows = list(csv.DictReader(log.open(encoding="utf-8")))
        n = sum(is_crypto(r.get("campaign", ""), r.get("attack_method", ""), r.get("target_sectors", ""), r.get("notes", ""))
                for r in rows)
        L.append(f"- AI attack log: {n} of {len(rows)} cases touch cryptocurrency.")
    for label, folder in (("GitHub tools", "ai_tool_sweeps"), ("Hugging Face models and apps", "hf_sweeps")):
        files = sorted((explo / folder).glob("*.csv")) if (explo / folder).exists() else []
        if files:
            rows = list(csv.DictReader(files[-1].open(encoding="utf-8")))
            if rows and "crypto" in rows[0]:
                L.append(f"- {label} (sweep of {files[-1].stem}): {sum(r['crypto'] == 'yes' for r in rows)} tagged crypto.")
            else:
                L.append(f"- {label}: the crypto tag starts with the next sweep.")
    return L + [""]


def build(results_dir: Path, out: Path, simulation: bool = True, today: dt.date | None = None,
          pdf: bool = True, explo: Path | None = None) -> dict:
    """Write reports/<key>.md, reports/charts/<key>-T*.png and timeline.png under out.
    Returns {'latest': key or None, 'keys': [...], 'available': {qid: bool}}."""
    res = load_results(results_dir)
    info: dict = {"latest": None, "keys": [k for k, _ in res], "available": {}}
    timeline(schedule_points(), today or dt.date.today(), out / "timeline.png")
    if not res:
        return info
    finals = {k.rsplit("-", 1)[0]: k for k, _ in res if k.endswith("-final")}
    for i, (key, R) in enumerate(res):
        series = [(k, r) for k, r in res[: i + 1] if k.endswith(R.get("run", "final"))]
        for qid, *_ in QUESTIONS:
            ok = chart(qid, series, out / "reports" / "charts" / f"{key}-{qid}.png", simulation)
            if i == len(res) - 1:
                info["available"][qid] = ok
        final_key = finals.get(R["quarter"]) if R.get("run") == "provisional" else None
        md = out / "reports" / f"{key}.md"
        flow_diagram(out / "reports" / "charts" / f"{key}-flow.png")
        extra = exploratory_parts(key, R, explo, out / "reports") if explo else []
        md.write_text(report_md(key, R, series, simulation, final_key, extra))
        if pdf:                                  # archive copy beside the page (author, 1 Nov 2026)
            from . import reportpdf
            try:
                reportpdf.make(md)
            except Exception as e:  # noqa: BLE001  (a PDF problem never blocks the page)
                print(f"::warning::PDF of {key} failed: {e}")
    info["latest"] = res[-1][0]
    info["latest_R"] = res[-1][1]
    return info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "daily"])
    ap.add_argument("--results", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "daily":
        a.out.mkdir(parents=True, exist_ok=True)
        daily(a.out)
        print("timeline and news line drawn")
        return 0
    info = build(a.results, a.out)
    print(f"reports: {len(info['keys'])}; latest {info['latest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
