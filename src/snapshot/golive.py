"""The go-live draft of the landing page (author's request, 31 Oct 2026).

"A behind-the-scenes go-live page: a duplicate of what the README shows now, plus the draft of
everything that goes live with the report, worked on in the background between the author and
Claude." Kept in the private repository only (go-live/README.md), rebuilt by the Manual publish
workflow after the private data, never published before the author says so.

It holds:
  1. the public README as it stands (pictures and links pointed at the public repository);
  2. draft sections that are not public yet: the AI tool sweeps (X25: how tools use AI, the
     growth chart, what they do) and the monthly news feed screens (items by site host name and
     what happened to them; no titles or links to articles).

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


def build_text(root: Path, readme: str) -> str:
    L = ["# Go-live draft: the landing page, behind the scenes", "",
         "> **Private draft** (author's request, 31 Oct 2026). Nothing here is public. Part 1 duplicates the "
         "public README as it stands; part 2 is the draft of what goes live with the report. Rebuilt "
         "automatically by the Manual publish workflow; do not edit here, change the sources instead.", "",
         "---", "", "## Part 1. The public landing page today (copy)", ""]
    body = public_readme(readme)
    body = re.sub(r"^# ", "### ", body, count=1, flags=re.M)
    L += [body.strip(), "", "---", "", "## Part 2. Draft: what goes live with the report", "",
          "Descriptive charts only, from the private data: totals and host names, never article titles, "
          "links to articles, project owners or rows. Labels describe what a tool does, not who uses it "
          "or why.", ""]
    date, figs = x25_figures(root)
    if figs:
        L += [f"### AI security tools on GitHub (X25), sweep of {date}", "",
              "How many security tools on GitHub use AI, on which kind of model, how fast they are "
              "appearing, and what they do. Full report: Part III of The Snapshot.", ""]
        L += [x for f in figs for x in (f"![{f}](../{FIGS}/{f})", "")]
    if (root / "exploratory/ai_attack_campaigns.csv").exists():
        name, n, ev = attack_log_chart(root)
        L += ["### Attacks that used AI (X3 log)", "",
              "Publicly reported cases where a real attacker used AI against real systems, or an AI under "
              "test reached real systems, from organisations' own reports. No victim names are recorded. "
              "Evidence of AI use: " + ", ".join(f"{k} {v}" for k, v in sorted(ev.items())) + " (unrated cases "
              "await the author's check).", "", f"![Attack log](../{FEED_CHARTS}/{name})", ""]
    ms = months(root)
    if ms:
        L += ["### Monthly news feed screen (X3)", "",
              "Each month about sixty security research, government and news feeds are read for items that "
              "mention both AI and an attack; each item is then sorted by hand. Shown by site host name only.", ""]
        for m in reversed(ms):
            hosts, decs, n = feed_counts(root, m)
            L += [f"![Feed screen {m}](../{FEED_CHARTS}/feed-screen-{m}.png)", "",
                  f"*{m}: {n} items from {len(hosts)} sites; " + ", ".join(
                      f"{DEC_NAMES[d]} {decs.get(d, 0)}" for d in DECISIONS) + ".*", ""]
    L += ["### Still to draft", "",
          "- The quarterly results, once the pilot runs (1 Jan 2027).",
          "- Which of the above the author chooses to publish, and when.", ""]
    return "\n".join(L) + "\n"


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
    (a.out / "README.md").write_text(build_text(root, (root / "README.md").read_text()))
    print(f"go-live draft written to {a.out}/README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
