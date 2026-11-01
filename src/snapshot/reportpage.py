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
ACCENT, GRAY, LIGHT = "#1D9E75", "#B4B2A9", "#D3D1C7"


def load_results(d: Path) -> list[tuple[str, dict]]:
    """Every evaluation result under d, newest per quarter and run kept: [(key, R)] sorted."""
    best: dict[str, tuple[str, dict]] = {}
    for f in sorted(d.glob("*practice_eval/practice_eval.json")) if d.exists() else []:
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
    plt, fig, ax = _ax((11, 2.6))
    start, end = dt.date(2026, 10, 1), dt.date(2028, 4, 30)
    ax.plot([start, end], [0, 0], color=LIGHT, lw=6, solid_capstyle="round")
    ax.plot([start, min(today, end)], [0, 0], color=ACCENT, lw=6, solid_capstyle="round")
    for i, (d, text) in enumerate(m for m in milestones if start <= m[0] <= end):
        past = d <= today
        ax.plot([d], [0], "o", ms=7, color=ACCENT if past else "white", mec=ACCENT if past else GRAY, mew=1.5, zorder=3)
        y = 0.55 if i % 2 == 0 else -0.55
        ax.annotate(("✓ " if past else "") + text, (d, 0), xytext=(d, y), fontsize=7, ha="center",
                    va="bottom" if y > 0 else "top", color="#2C2C2A" if past else "#5F5E5A",
                    arrowprops=dict(arrowstyle="-", color=LIGHT, lw=.8))
    ax.axvline(today, color="#D85A30", lw=1.2, ls="--")
    ax.text(today, 1.15, f"you are here, {today:%d %b %Y}", color="#D85A30", fontsize=8, ha="center")
    ax.set_ylim(-1.3, 1.35); ax.set_yticks([])
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


def report_md(key: str, R: dict, series: list[tuple[str, dict]], simulation: bool, final_key: str | None) -> str:
    q, run = R["quarter"], R.get("run", "final")
    title = f"# Internet Security Snapshot: {q} report ({run})" + (" — SIMULATION" if simulation else "")
    L = [title, ""]
    if simulation:
        L += ["> **SIMULATION, not a result.** Built end to end from the private practice evaluation "
              f"({R.get('_source')}) of a quarter outside the registered study, with fix dates before the "
              "author's hand check, to test the whole flow and the report's design. Real reports start with "
              "the pilot (1 Jan 2027) and the first scored quarter (1 Apr 2027).", ""]
    if run == "provisional":
        L += ["> **Provisional.** Published within two days of the quarter's end, before the hand check. "
              + (f"The final report: [{final_key}]({final_key}.md)." if final_key else
                 "The final report follows one month later; this page then stays as it is, with a link to it."), ""]
    L += ["## At a glance", "", "| Question | This quarter | 90% interval or range | Label |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {'simulation' if simulation else 'see section'} |" for a, b, c in summary_rows(R)]
    L += ["", "Labels (Improving, Worsening, Rising, Falling or No clear direction) are given from Q1 2027 by "
          "the registered rule, each with its companion check. "
          + ("None in a practice quarter." if simulation else ""), ""]
    for qid, name, ask, how in QUESTIONS:
        L += [f"## {qid}. {name}", "", f"*{ask}*", "", how, "", f"![{qid}](charts/{key}-{qid}.png)", ""]
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
    L += ["## Data and checks", "", f"- Flaws first added to CISA KEV in the quarter: {R.get('kev_added_in_quarter')}",
          f"- Fix dates ({R.get('fix_inputs', 'frozen bundle')}): " + ", ".join(
              f"{k} {v}" for k, v in (R.get("prefill_sources") or {}).items()),
          f"- Still an assumed fix date (the hand check replaces these): {R.get('prefill_assumed')}",
          "- Whole calendar years of published records: " + ", ".join(
              f"{y} {v:,}" for y, v in (R.get("I5_calendar_years") or {}).items()), "",
          "## Not available yet", ""] + [f"- {k}: {v}" for k, v in (R.get("not_computable") or {}).items()]
    L += ["", "## About this report", "",
          f"Run: {q}, {run}. Source: {R.get('_source')}. Method: the pre-registration (OSF DOI 10.17605/OSF.IO/3XT82) "
          "and docs/EVALUATION_FLOW.md. This page is frozen once published; corrections are added as dated notes.", ""]
    return "\n".join(L)


def build(results_dir: Path, out: Path, simulation: bool = True, today: dt.date | None = None) -> dict:
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
        (out / "reports" / f"{key}.md").write_text(report_md(key, R, series, simulation, final_key))
    info["latest"] = res[-1][0]
    info["latest_R"] = res[-1][1]
    return info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build"])
    ap.add_argument("--results", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    info = build(a.results, a.out)
    print(f"reports: {len(info['keys'])}; latest {info['latest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
