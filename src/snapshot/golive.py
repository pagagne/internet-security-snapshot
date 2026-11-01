"""The go-live draft of the landing page (author's request, 31 Oct 2026).

"A behind-the-scenes go-live page: a duplicate of what the README shows now, plus the draft of
everything that goes live with the report, worked on in the background between the author and
Claude." Kept in the private repository only (go-live/README.md), rebuilt by the Manual publish
workflow after the private data, never published before the author says so.

Since 1 Nov 2026 (author) it is a mirror built from one layout (config/landing_layout.yaml):
the public README's sections in page order, with the draft sections placed where they will go:
the results (simulated on the latest private practice evaluation until the pilot), the AI tool
sweeps (X25), the attack log and the news feed screens (X3; host names only, no titles or links).
FLIP_PREVIEW.md beside it is the dry run of the flip: the page as it would go public, after the
privacy scan, and the reasons it may not yet. The flip itself is the author's, on 1 Jan 2027.

  python -m snapshot.golive build --out DIR     (run inside a checkout where exploratory/ is linked)
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from .util import _repo_root

PUBLIC_BLOB = "https://github.com/pagagne/internet-security-snapshot/blob/main/"
PUBLIC_RAW = "https://raw.githubusercontent.com/pagagne/internet-security-snapshot/main/"
SWEEPS = "exploratory/ai_tool_sweeps"
FIGS = "exploratory/ai_tool_landscape"
FEED_CHARTS = "exploratory/feed_charts"
DECISIONS = ["logged", "second source", "already logged", "your judgement", "excluded"]
DEC_NAMES = {"logged": "new case", "second source": "second source", "already logged": "already logged",
             "your judgement": "author's judgement", "excluded": "excluded"}
DEC_COLOURS = {"logged": "#1D9E75", "second source": "#5DCAA5", "already logged": "#9FE1CB",
               "your judgement": "#EF9F27", "excluded": "#C8C8C8"}


def public_readme(text: str) -> str:
    """Point the README's relative pictures and links at the public repository."""
    text = re.sub(r'(src|srcset)="(?!https?:)([^"]+)"', lambda m: f'{m[1]}="{PUBLIC_RAW}{m[2]}"', text)
    text = re.sub(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)", lambda m: f"]({PUBLIC_BLOB}{m[1]})", text)
    return text


def months(root: Path) -> list[str]:
    """Sorted months with a sorted feed screen (candidates and decisions present)."""
    out = []
    for f in sorted((root / "exploratory").glob("feed-screen-????-??-decisions.csv")):
        m = f.name[len("feed-screen-"):len("feed-screen-") + 7]
        if (root / f"exploratory/feed-screen-{m}-candidates.csv").exists():
            out.append(m)
    return out


def feed_counts(root: Path, month: str) -> tuple[collections.Counter, collections.Counter, int]:
    cands = list(csv.DictReader((root / f"exploratory/feed-screen-{month}-candidates.csv").open(encoding="utf-8")))
    dec = {int(r["n"]): r["decision"] for r in csv.DictReader((root / f"exploratory/feed-screen-{month}-decisions.csv").open(encoding="utf-8"))}
    hosts = collections.Counter((urlparse(c["link"]).hostname or "?").removeprefix("www.") for c in cands)
    return hosts, collections.Counter(dec.get(i, "") for i in range(len(cands))), len(cands)


def feed_charts(root: Path, month: str) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = root / FEED_CHARTS
    out.mkdir(parents=True, exist_ok=True)
    hosts, decs, n = feed_counts(root, month)
    top = hosts.most_common(10)[::-1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), dpi=130, gridspec_kw={"width_ratios": [1.4, 1]})
    a1.barh([h for h, _ in top], [c for _, c in top], color="#7F77DD")
    for i, (_, c) in enumerate(top):
        a1.text(c, i, f" {c}", va="center", fontsize=8)
    a1.set_xlabel("Items found"); a1.set_title("Which sites the items came from (top 10, host names only)")
    vals = [decs.get(d, 0) for d in DECISIONS]
    a2.bar([DEC_NAMES[d].replace(" ", "\n", 1) for d in DECISIONS], vals, color=[DEC_COLOURS[d] for d in DECISIONS])
    for i, v in enumerate(vals):
        a2.text(i, v, f"{v}", ha="center", va="bottom", fontsize=9)
    a2.set_title("What happened to them"); a2.tick_params(axis="x", labelsize=8)
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.suptitle(f"News feed screen, {month}: {n} items mentioning both AI and an attack")
    fig.tight_layout()
    name = f"feed-screen-{month}.png"
    fig.savefig(out / name); plt.close(fig)
    return [name]


ROLE_NAMES = {"agents_operated_intrusion": "AI agents ran the intrusion", "ai_assisted_operator": "AI helped a human attacker",
              "ai_generated_malware": "AI-written malware", "ai_enabled_fraud": "AI-enabled fraud or theft of AI use",
              "evaluation_escape": "AI under test reached real systems"}
ROLE_COLOURS = {"agents_operated_intrusion": "#b85c1e", "ai_assisted_operator": "#e0a526", "ai_generated_malware": "#6a51a3",
                "ai_enabled_fraud": "#2a9d8f", "evaluation_escape": "#888780"}


def attack_log_chart(root: Path) -> tuple[str, int, collections.Counter]:
    """X3 log: cases by the month reported and how AI was used (no victim names exist in the log)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = list(csv.DictReader((root / "exploratory/ai_attack_campaigns.csv").open(encoding="utf-8")))
    seen = sorted({r["date_reported"][:7] for r in rows if r["date_reported"]})
    ms, (y, m) = [], map(int, seen[0].split("-"))
    while f"{y}-{m:02d}" <= seen[-1]:                       # every month, so quiet months show as gaps
        ms.append(f"{y}-{m:02d}"); y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    roles = [k for k in ROLE_NAMES if any(r["ai_role"] == k for r in rows)]
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=130)
    bottom = [0] * len(ms)
    for k in roles:
        v = [sum(r["ai_role"] == k and r["date_reported"][:7] == m for r in rows) for m in ms]
        ax.bar(ms, v, bottom=bottom, color=ROLE_COLOURS[k], label=ROLE_NAMES[k], width=.6)
        bottom = [b + x for b, x in zip(bottom, v)]
    ax.set_ylabel("Cases logged"); ax.set_xlabel("Month the case was reported")
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set_title(f"Publicly reported attacks that used AI: {len(rows)} cases in the log, by how AI was used")
    ax.tick_params(axis="x", labelrotation=45, labelsize=8); ax.legend(frameon=False, fontsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    out = root / FEED_CHARTS
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "attack-log.png"); plt.close(fig)
    return "attack-log.png", len(rows), collections.Counter(r["ai_evidence"] for r in rows)


def x25_figures(root: Path) -> tuple[str, list[str]]:
    files = sorted((root / SWEEPS).glob("*.csv"))
    if not files:
        return "", []
    d = files[-1].stem
    want = [f"{d}-1-ai-use.png", f"{d}-3-new-per-month.png", f"{d}-2-tool-types.png"]
    return d, [w for w in want if (root / FIGS / w).exists()]


LAYOUT = "config/landing_layout.yaml"
PRACTICE = None   # override in tests; default: runs/research beside the linked private exploratory/


def _practice_dir(root: Path) -> Path:
    return Path(PRACTICE) if PRACTICE else (root / "exploratory").resolve().parent / "runs" / "research"


def load_layout(root: Path) -> dict:
    import yaml
    return yaml.safe_load((root / LAYOUT).read_text())


def readme_sections(readme: str) -> dict[str, str]:
    """README split by H2 heading; 'top' is everything before the first H2."""
    parts = re.split(r"^(?=## )", readme, flags=re.M)
    out = {"top": parts[0]}
    for p in parts[1:]:
        out[p.split("\n", 1)[0][3:].strip()] = p
    return out


def latest_practice(root: Path) -> tuple[str, dict] | tuple[None, None]:
    import json
    d = _practice_dir(root)
    runs = sorted(d.glob("*practice_eval/practice_eval.json")) if d.exists() else []
    return (runs[-1].parent.name, json.loads(runs[-1].read_text())) if runs else (None, None)


def _n(v, pct=False):
    if v is None:
        return "-"
    return f"{100 * v:.0f}%" if pct else (f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}")


RUN_REPORTS = "https://raw.githubusercontent.com/pagagne/internet-security-snapshot/run-reports/"
# Draft introduction for the landing page (author, 1 Nov 2026: Claude drafts, reviewed on 6 Nov)
INTRO_DRAFT = [
    "## What this page is",
    "",
    "The Internet Security Snapshot measures, every quarter through 2027, whether defenders are fixing "
    "internet-facing software flaws faster than attackers start exploiting them, and how AI is changing "
    "that race. It uses free public data only, on a plan registered in advance, so the results cannot be "
    "bent to fit a story.",
    "",
    "**How to read it.** The banner at the top shows whether each data source answered today, and the line "
    "under it what happened last in the study and what comes next. The rings show how much of the data the "
    "study needs is already collected. The timeline shows where the study stands. The latest results follow: "
    "one chart per question, each linking to the full report, with every quarter's provisional and final "
    "report kept as its own page and PDF. A result is labelled Improving, Worsening, Rising or Falling only "
    "when the registered rule says so; a label is never proof of a cause, including AI.",
    "",
]
REPORTS: dict = {}    # filled by main() from snapshot.reportpage.build (report pages and charts)


def results_section(root: Path, simulate: bool = True) -> list[str]:
    """Latest results on the landing page: a summary table, one chart per question (each linking
    to its section of the full report) and a link to the report (author, 1 Nov 2026). Until the
    pilot it is a simulation built end to end from the latest private practice evaluation."""
    from . import reportpage as RP
    info = REPORTS
    L = ["## Latest results", ""]
    key, R = info.get("latest"), info.get("latest_R")
    if not key:
        run, R0 = latest_practice(root) if simulate else (None, None)
        if not R0:
            return L + ["The first results appear with the Q4 2026 pilot report on 1 January 2027.", ""]
        key, R = f"{R0['quarter']}-{R0.get('run', 'final')}", R0 | {"_source": run}
    L += [f"> **SIMULATION, not a result.** Built end to end from the private evaluation of {R['quarter']} "
          f"({R.get('_source')}), a quarter outside the registered study, with fix dates before the author's hand "
          "check. The real section starts with the pilot report (1 Jan 2027) and the first scored quarter "
          "(Q1 2027, reported 1 Apr 2027).", "",
          f"**Quarter:** {R['quarter']} ({R.get('run', 'final').replace('-', ' ')}) &nbsp;·&nbsp; **Full report:** "
          f"[{key}](reports/{key}.md) &nbsp;·&nbsp; **Label:** none in a practice quarter.", "",
          "| Question | This quarter | 90% interval or range | Label |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | simulation |" for a, b, c in RP.summary_rows(R)]
    L += ["", "*One chart per question; each opens its section of the full report.*", ""]
    cells = [f'<a href="reports/{key}.md#{q[0].lower()}-{q[1].lower().replace(" ", "-").replace(chr(39), "")}">'
             f'<img src="reports/charts/{key}-{q[0]}.png" width="420" alt="{q[0]} {q[1]}"></a>' for q in RP.QUESTIONS]
    L += ["<p>"] + cells + ["</p>", ""]
    return L


def draft_section(root: Path, name: str) -> list[str]:
    L: list[str] = []
    if name == "results":
        return results_section(root)
    if name == "timeline":
        return ["## Where the study stands", "", f"![Study timeline]({RUN_REPORTS}landing/timeline.png)", "",
                "*Drawn daily from the study calendar (docs/schedule/schedule.yaml): ticks are done, the dashed "
                "line is today.*", ""]
    if name == "news":
        return ["<picture>", f'  <source media="(prefers-color-scheme: dark)" srcset="{RUN_REPORTS}landing/news-dark.svg">',
                f'  <img alt="Latest and next milestone of the study, from its calendar" src="{RUN_REPORTS}landing/news-light.svg">',
                "</picture>", ""]
    if name == "intro":
        return list(INTRO_DRAFT)
    if name == "x25":
        date, figs = x25_figures(root)
        if figs:
            L += [f"## AI security tools on GitHub (X25), sweep of {date}", "",
                  "How many security tools on GitHub use AI, on which kind of model, how fast they are "
                  "appearing, and what they do. Labels describe what a tool does, not who uses it or why.", ""]
            L += [x for f in figs for x in (f"![{f}](../{FIGS}/{f})", "")]
    elif name == "attack_log" and (root / "exploratory/ai_attack_campaigns.csv").exists():
        fig, n, ev = attack_log_chart(root)
        L += ["## Attacks that used AI (X3 log)", "",
              "Publicly reported cases where a real attacker used AI against real systems, or an AI under "
              "test reached real systems, from organisations' own reports. No victim names are recorded. "
              "Evidence of AI use: " + ", ".join(f"{k} {v}" for k, v in sorted(ev.items())) + ".", "",
              f"![Attack log](../{FEED_CHARTS}/{fig})", ""]
    elif name == "hf":
        figs = root / FIGS
        hf = sorted(figs.glob("hf-*-1-new-per-month.png")) if figs.exists() else []
        if hf:
            d = hf[-1].name[3:13]
            L += [f"## AI models on Hugging Face (X25), sweep of {d}", "",
                  "Security-related AI models and apps published on Hugging Face, including open-weight models whose "
                  "safety training has been removed, counted by month and by the lab of their base model. Nothing is "
                  "downloaded or run; individuals' items are never named by username.", ""]
            L += [x for s in ("1-new-per-month", "2-safety-removed-by-lab")
                  if (figs / f"hf-{d}-{s}.png").exists() for x in (f"![{s}](../{FIGS}/hf-{d}-{s}.png)", "")]
    elif name == "feed_screen":
        ms = months(root)
        if ms:
            L += ["## Monthly news feed screen (X3)", "",
                  "Each month about sixty security research, government and news feeds are read for items that "
                  "mention both AI and an attack; each is then sorted by hand. Shown by site host name only.", ""]
            for m in reversed(ms):
                hosts, decs, n = feed_counts(root, m)
                L += [f"![Feed screen {m}](../{FEED_CHARTS}/feed-screen-{m}.png)", "",
                      f"*{m}: {n} items from {len(hosts)} sites; " + ", ".join(
                          f"{DEC_NAMES[d]} {decs.get(d, 0)}" for d in DECISIONS) + ".*", ""]
    return L


def compose(root: Path, readme: str, layout: dict, mirror: bool = True) -> tuple[str, list[str]]:
    """The page in layout order. mirror=True: every section, drafts badged (the private mirror).
    mirror=False: what the page would be after the flip. Returns (text, problems)."""
    secs, problems, L = readme_sections(readme), [], []
    for s in layout["sections"]:
        if "readme" in s:
            body = secs.get(s["readme"])
            if body is None:
                problems.append(f"README section missing: {s['readme']}")
                continue
            L.append(public_readme(body).rstrip() + "\n")
        else:
            part = draft_section(root, s["draft"])
            if not part:
                continue
            if s.get("under_banner"):            # spliced in right under the banner picture (the news line)
                if not mirror and not s.get("cleared"):
                    problems.append(f"draft section not cleared by the author: {s['draft']}")
                badge = ([f"<sub>🟧 DRAFT (`{s['draft']}`): goes live at the flip</sub>", ""]
                         if mirror and s.get("status") == "draft" else [])
                block = "\n".join(part + badge)
                for i, prev in enumerate(L):
                    if "</picture>" in prev:
                        L[i] = prev.replace("</picture>", "</picture>\n\n" + block, 1)
                        break
                else:
                    L.append(block)
                continue
            if mirror and s.get("status") == "draft":
                part.insert(2, f"> 🟧 **DRAFT section** (`{s['draft']}`): private, goes live at the flip"
                               + ("" if s.get("cleared") else "; figures not yet cleared by the author") + ".")
                part.insert(3, "")
            if not mirror and not s.get("cleared"):
                problems.append(f"draft section not cleared by the author: {s['draft']}")
            L.append("\n".join(part).rstrip() + "\n")
    return "\n".join(L), problems


def flip_check(root: Path, readme: str, layout: dict) -> tuple[str, list[str]]:
    """Dry run of the flip: the page as it would go public, and every reason it may not yet."""
    from . import privacy
    text, problems = compose(root, readme, layout, mirror=False)
    problems += [f"line {line}: {kind}" for _, line, kind in privacy.scan_text("README.md", text)]
    if "SIMULATION" in text:
        problems.append("results section still shows the practice simulation (needs the pilot report)")
    return text, problems


def build_text(root: Path, readme: str) -> str:
    layout = load_layout(root)
    page, problems = compose(root, readme, layout, mirror=True)
    _, flip = flip_check(root, readme, layout)
    head = ["# Go-live mirror of the landing page (private)", "",
            "> **Private mirror** (author's decisions, 31 Oct and 1 Nov 2026). This is the landing page as it "
            f"will look after the flip on {layout.get('flip_date')}: the public sections exactly as they are "
            "today, with the draft sections in place and badged. Tweak it here; the flip makes it the real "
            "page through a guarded workflow. Order and status: `config/landing_layout.yaml`. Rebuilt by the "
            "Manual publish workflow; do not edit here.", "",
            f"**Practice flip today:** {'ready' if not flip else 'not ready, ' + str(len(flip)) + ' reason(s):'}", ""]
    head += [f"- {p}" for p in flip + problems] + ["", "---", ""]
    return "\n".join(head) + "\n" + page


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build"])
    ap.add_argument("--out", required=True, type=Path, help="folder for README.md (go-live/ in the private repository)")
    a = ap.parse_args(argv)
    root = _repo_root()
    if not (root / "exploratory").exists():
        print("exploratory/ not linked: the go-live draft needs the private data"); return 1
    for m in months(root):
        feed_charts(root, m)
    a.out.mkdir(parents=True, exist_ok=True)
    readme = (root / "README.md").read_text()
    from . import reportpage
    REPORTS.clear()
    if (root / "exploratory/ai_attack_campaigns.csv").exists():
        attack_log_chart(root)                   # the report's Part 2 uses it
    REPORTS.update(reportpage.build(_practice_dir(root), a.out, simulation=True,
                                    explo=(root / "exploratory").resolve()))   # every run, end to end
    (a.out / "README.md").write_text(build_text(root, readme))
    preview, _ = flip_check(root, readme, load_layout(root))
    (a.out / "FLIP_PREVIEW.md").write_text("<!-- What the public README would be after the flip (dry run). -->\n" + preview)
    print(f"go-live draft written to {a.out}/README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
