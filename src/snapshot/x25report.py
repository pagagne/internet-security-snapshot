"""The AI attack- and defence-tool landscape on GitHub (X25), generated from the sweeps.

Author's decisions, 30 Oct 2026: catalogue each hand-run sweep with charts and carry it in The
Snapshot manual; the January 2027 sweep is part of the pilot. Reads every sweep in
exploratory/ai_tool_sweeps/<date>.csv (a compact copy of the Research task github_tools output,
originals only) and writes exploratory/ai_tool_landscape.md with three charts per sweep in
exploratory/ai_tool_landscape/. Exploratory and never scored: a tool on GitHub is supply, not
use, and the role labels are first guesses until checked.

  python -m snapshot.x25report build     (charts need matplotlib; the text alone is checked)
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

from .util import _repo_root

SWEEPS = "exploratory/ai_tool_sweeps"
OUT = "exploratory/ai_tool_landscape.md"
FIGS = "exploratory/ai_tool_landscape"
SIDES = ["attack", "defence", "both"]
ROLES = SIDES + ["model_testing", "unclear"]
COLOURS = {"attack": "#b85c1e", "defence": "#1f4e79", "both": "#7a7a7a"}
AI = ["mcp", "anthropic/claude", "openai/gpt", "ollama/local", "google/gemini", "langchain", "deepseek", "qwen", "hermes"]


def load(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open()))


def months(rows, since="2025-01"):
    return sorted({r["created"][:7] for r in rows if r["created"] and r["created"][:7] >= since})


def stats(rows: list[dict]) -> dict:
    by = {k: [r for r in rows if r["role"] == k] for k in ROLES}
    ms = months(rows)
    return {
        "by": by, "months": ms,
        "per_month": {k: [sum(r["created"][:7] == m for r in by[k]) for m in ms] for k in SIDES},
        "stars": {k: sum(int(r["stars"]) for r in by[k]) for k in ROLES},
        "ai": {k: [sum(a in r["models"].split(";") for r in by[k]) for a in AI] for k in SIDES[:2]},
    }


def charts(date: str, s: dict, root: Path) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    out = root / FIGS
    out.mkdir(parents=True, exist_ok=True)
    names = []
    labels = [f"{m[5:]}/{m[2:4]}" for m in s["months"]]
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=130)
    for k in SIDES:
        ax.plot(labels, s["per_month"][k], marker="o", ms=3, lw=2, color=COLOURS[k], label=k.capitalize())
    ax.set_xlabel("Month the project was created on GitHub (last month may be partial)")
    ax.set_ylabel("New projects that month")
    ax.set_title(f"New AI security tools on GitHub each month, by role (sweep of {date})")
    ax.tick_params(axis="x", labelrotation=60, labelsize=8)
    ax.grid(axis="y", alpha=.3); ax.legend(frameon=False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); n = f"{date}-1-new-per-month.png"; fig.savefig(out / n); plt.close(fig); names.append(n)

    rl = ["attack", "defence", "both"]
    names_ = ["Attack", "Defence", "Both"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=130)
    for ax, vals, title, ylab in (
            (a1, [len(s["by"][k]) for k in rl], "How many projects", "Number of projects"),
            (a2, [s["stars"][k] for k in rl], "How much attention", "GitHub stars, all projects added up")):
        bars = ax.bar(names_, vals, color=[COLOURS[k] for k in rl], width=.6)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,}", ha="center", va="bottom", fontsize=10)
        ax.set_title(title); ax.set_ylabel(ylab); ax.set_xlabel("Role (what the software does)")
        ax.set_ylim(0, max(vals) * 1.15); ax.grid(axis="y", alpha=.3)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.suptitle(f"Projects and attention by role (sweep of {date})")
    fig.tight_layout(); n = f"{date}-2-projects-and-stars.png"; fig.savefig(out / n); plt.close(fig); names.append(n)

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=130)
    x = range(len(AI))
    for off, k in ((-.2, "attack"), (.2, "defence")):
        ax.bar([i + off for i in x], s["ai"][k], .4, color=COLOURS[k], label=k.capitalize())
    ax.set_xticks(list(x), ["MCP", "Claude", "OpenAI", "Local (Ollama)", "Gemini", "LangChain", "DeepSeek", "Qwen", "Hermes"])
    ax.set_xlabel("AI named in the project's description or instructions"); ax.set_ylabel("Projects naming it")
    ax.set_title(f"Which AI each side builds on (sweep of {date})")
    ax.legend(frameon=False); ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); n = f"{date}-3-ai-by-side.png"; fig.savefig(out / n); plt.close(fig); names.append(n)
    return names


def build_text(root: Path | None = None) -> str:
    root = root or _repo_root()
    files = sorted((root / SWEEPS).glob("*.csv"))
    L = ["# AI attack and defence tools on GitHub (X25, generated)", "",
         f"Generated by `python -m snapshot.x25report build` from `{SWEEPS}/`. Do not edit. "
         "Exploratory and never scored: a tool on GitHub is supply, not use, and many attack tools "
         "serve authorised testing.", "",
         "**What a sweep covers.** Not all of GitHub: 48 fixed searches (24 for AI attack tools, 24 "
         "for AI defence tools, a few in Chinese and Russian; `config/github_tool_queries.yaml`) over "
         "the names, descriptions and topic tags of public repositories, forks left out, at most "
         "1,000 results a search. Private repositories, deleted ones and tools described in other "
         "words are not seen. The same searches every time, so sweeps compare with each other.", "",
         "**Roles.** Each repository is labelled by what it does, from its own words: attack (breaks "
         "into, scans or exploits systems), defence (detects, investigates, fixes or hardens), both, "
         "model testing (tests AI models themselves; kept apart) or unclear. These are first guesses; "
         "Claude checks every tool with 100+ stars and the author confirms. The attack and defence "
         "searches are not mirror images, so read each side's trend, not the gap between totals.", "",
         "**Schedule.** Run by hand only: baseline 30 Oct 2026; the January 2027 sweep (6 Jan) is part "
         "of the pilot; then mid-2027 (7 Jul) and the end of 2027 (8 Dec).", ""]
    for f in reversed(files):
        date = f.stem
        s = stats(load(f))
        by = s["by"]
        n = sum(len(v) for v in by.values())
        top = lambda k: "; ".join(f"{r['full_name']} ({int(r['stars']):,})" for r in sorted(
            by[k], key=lambda r: -int(r["stars"]))[:8])
        L += [f"## Sweep of {date}", "",
              f"{n:,} repositories: " + ", ".join(f"{k.replace('_', ' ')} {len(by[k]):,}" for k in ROLES) + ". "
              f"Stars: attack {s['stars']['attack']:,}, defence {s['stars']['defence']:,}, both {s['stars']['both']:,}.", "",
              f"![Chart 1. New tools each month by role, sweep of {date}](ai_tool_landscape/{date}-1-new-per-month.png)", "",
              "*Chart 1. Horizontal: the month each project was created. Vertical: new projects that "
              "month. Lines: attack, defence, both.*", "",
              f"![Chart 2. Projects and stars by role, sweep of {date}](ai_tool_landscape/{date}-2-projects-and-stars.png)", "",
              "*Chart 2. Two panels. Left: how many projects each role has. Right: how much "
              "attention they get, as GitHub stars (bookmarks people give a project) added up over all "
              "of that role's projects. Horizontal: role; vertical: the count, written on each bar.*", "",
              f"![Chart 3. AI named by each side, sweep of {date}](ai_tool_landscape/{date}-3-ai-by-side.png)", "",
              "*Chart 3. Horizontal: the AI named in a project's description or instructions. "
              "Vertical: projects naming it. Bars: attack and defence.*", "",
              "| Month | " + " | ".join(m for m in s["months"][-12:]) + " |",
              "|---|" + "---|" * len(s["months"][-12:])]
        for k in SIDES:
            L.append(f"| {k.capitalize()} | " + " | ".join(str(v) for v in s["per_month"][k][-12:]) + " |")
        L += ["", f"Most-starred attack tools: {top('attack')}.", "",
              f"Most-starred defence tools: {top('defence')}.", "",
              f"Most-starred tools doing both: {top('both')}.", ""]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    a = ap.parse_args(argv)
    root = _repo_root()
    text = build_text(root)
    if a.cmd == "build":
        for f in sorted((root / SWEEPS).glob("*.csv")):
            charts(f.stem, stats(load(f)), root)
        (root / OUT).write_text(text)
        print(f"{OUT}: built")
        return 0
    if not (root / OUT).exists() or (root / OUT).read_text() != text:
        print(f"{OUT} is out of date: run `python -m snapshot.x25report build`.")
        return 1
    print("X25 landscape is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
