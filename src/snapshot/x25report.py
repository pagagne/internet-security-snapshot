"""The AI attack- and defence-tool landscape on GitHub (X25), generated from the sweeps.

Author's decisions, 30 Oct 2026: catalogue each hand-run sweep with charts and carry it in The
Snapshot manual; the January 2027 sweep is part of the pilot. Reads every sweep in
exploratory/ai_tool_sweeps/<date>.csv (a compact copy of the Research task github_tools output,
originals only) and writes exploratory/ai_tool_landscape.md with a set of charts per sweep (six, plus one protocol chart for every 12 protocols found) in
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
LABS = ["OpenAI", "Anthropic", "Google", "Meta", "Mistral", "DeepSeek", "Alibaba", "Nous Research", "Moonshot",
        "Zhipu", "xAI", "Microsoft", "Local runner"]
TARGETS = ["web apps and APIs", "cloud accounts", "Windows and Active Directory", "networks and hosts",
           "containers and Kubernetes", "mobile apps", "industrial and IoT", "source code and supply chain",
           "email and people", "endpoints and logs"]
TOOLKITS = ["MCP", "LangChain", "CrewAI", "AutoGen", "LlamaIndex", "Semantic Kernel", "OpenAI Agents SDK",
            "Claude Code / Agent SDK", "smolagents", "PydanticAI"]
from .research.github_tools import PROTOCOLS as _P
PROTOCOLS = list(_P)
WEIGHTS = ["open-weight", "closed", "runs locally"]
PER_CHART = 12   # protocols per chart: the number of protocol charts follows what a sweep finds


def load(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open()))


def months(rows, since="2025-01"):
    return sorted({r["created"][:7] for r in rows if r["created"] and r["created"][:7] >= since})


def open_share(rows: list[dict], ms: list[str]) -> tuple[list[str], list[float]]:
    """Per quarter: of the tools naming any AI model, the share naming an open-weight one (or
    running models locally)."""
    qs, out = [], []
    for q in sorted({f"{m[:4]} Q{(int(m[5:]) - 1) // 3 + 1}" for m in ms}):
        yr, qn = q.split(" Q")
        mons = {f"{yr}-{3 * (int(qn) - 1) + i:02d}" for i in (1, 2, 3)}
        named = [r for r in rows if r["created"][:7] in mons and r.get("weights")]
        if len(named) >= 5:
            qs.append(q)
            out.append(100 * sum(("open-weight" in r["weights"]) or ("runs locally" in r["weights"]) for r in named) / len(named))
    return qs, out


def stats(rows: list[dict]) -> dict:
    by = {k: [r for r in rows if r["role"] == k] for k in ROLES}
    ms = months(rows)
    return {
        "by": by, "months": ms,
        "per_month": {k: [sum(r["created"][:7] == m for r in by[k]) for m in ms] for k in SIDES},
        "stars": {k: sum(int(r["stars"]) for r in by[k]) for k in ROLES},
        **{f: {k: [sum(a in r[f].split(";") for r in by[k]) for a in lst] for k in SIDES}
           for f, lst in (("labs", LABS), ("weights", WEIGHTS), ("targets", TARGETS), ("toolkits", TOOLKITS),
                          ("protocols", PROTOCOLS))},
        "open_share": {k: open_share(by[k], ms) for k in SIDES},
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

    for num, field, lst, xlab, title in (
            (3, "labs", LABS, "Lab whose AI the project names", "Which lab's AI each side builds on"),
            (5, "targets", TARGETS, "What the project goes after (attack) or protects (defence)", "What each side focuses on")):
        fig, ax = plt.subplots(figsize=(11, 5), dpi=130)
        x = range(len(lst))
        for off, k in ((-.27, "attack"), (0, "defence"), (.27, "both")):
            ax.bar([i + off for i in x], s[field][k], .27, color=COLOURS[k], label=k.capitalize())
        ax.set_xticks(list(x), lst, rotation=30, ha="right", fontsize=9)
        ax.set_xlabel(xlab); ax.set_ylabel("Projects naming it")
        ax.set_title(f"{title} (sweep of {date})")
        ax.legend(frameon=False); ax.grid(axis="y", alpha=.3)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        fig.tight_layout(); n = f"{date}-{num}-{field}-by-side.png"; fig.savefig(out / n); plt.close(fig); names.append(n)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=130)
    x = range(len(WEIGHTS))
    for off, k in ((-.27, "attack"), (0, "defence"), (.27, "both")):
        a1.bar([i + off for i in x], s["weights"][k], .27, color=COLOURS[k], label=k.capitalize())
    a1.set_xticks(list(x), ["Open-weight model", "Closed model", "Runs models locally"])
    a1.set_xlabel("Kind of AI the project names"); a1.set_ylabel("Projects naming it")
    a1.set_title("Open-weight or closed, by role"); a1.legend(frameon=False); a1.grid(axis="y", alpha=.3)
    for k in ("attack", "defence"):
        qs, vals = s["open_share"][k]
        a2.plot(qs, vals, marker="o", lw=2, color=COLOURS[k], label=k.capitalize())
    a2.set_ylim(0, 100); a2.set_xlabel("Quarter the project was created")
    a2.set_ylabel("% naming an open-weight or local model"); a2.set_title("Share using open-weight AI, by quarter")
    a2.tick_params(axis="x", labelrotation=45, labelsize=8); a2.legend(frameon=False); a2.grid(axis="y", alpha=.3)
    for ax in (a1, a2):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.suptitle(f"Open-weight against closed AI (sweep of {date})")
    fig.tight_layout(); n = f"{date}-7-open-weight.png"; fig.savefig(out / n); plt.close(fig); names.append(n)
    found = sorted((p for i, p in enumerate(PROTOCOLS) if sum(s["protocols"][k][i] for k in SIDES)),
                   key=lambda p: -sum(s["protocols"][k][PROTOCOLS.index(p)] for k in SIDES))
    for c, start in enumerate(range(0, len(found), PER_CHART)):
        chunk = found[start:start + PER_CHART]
        fig, ax = plt.subplots(figsize=(11, 5), dpi=130)
        x = range(len(chunk))
        for off, k in ((-.27, "attack"), (0, "defence"), (.27, "both")):
            ax.bar([i + off for i in x], [s["protocols"][k][PROTOCOLS.index(p)] for p in chunk], .27,
                   color=COLOURS[k], label=k.capitalize())
        ax.set_xticks(list(x), chunk, rotation=30, ha="right", fontsize=9)
        ax.set_xlabel("Network protocol named by the project (most-named first)"); ax.set_ylabel("Projects naming it")
        ax.set_title(f"Network protocols each side names, {start + 1}-{start + len(chunk)} of {len(found)} found (sweep of {date})")
        ax.legend(frameon=False); ax.grid(axis="y", alpha=.3)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        fig.tight_layout(); n = f"{date}-6-protocols-{c + 1}.png"; fig.savefig(out / n); plt.close(fig); names.append(n)
    qs, qv = [], {k: [] for k in SIDES}
    for i, m in enumerate(s["months"]):
        q = f"{m[:4]} Q{(int(m[5:]) - 1) // 3 + 1}"
        if not qs or qs[-1] != q:
            qs.append(q)
            for k in SIDES:
                qv[k].append(0)
        for k in SIDES:
            qv[k][-1] += s["per_month"][k][i]
    fig = plt.figure(figsize=(11, 7), dpi=130)
    ax = fig.add_subplot(111, projection="3d")
    for yi, k in enumerate(SIDES):
        for xi, v in enumerate(qv[k]):
            ax.bar3d(xi, yi, 0, .6, .5, v, color=COLOURS[k], alpha=.9, shade=True)
    ax.set_xticks([i + .3 for i in range(len(qs))], [q.replace(" ", "\n") for q in qs], fontsize=8)
    ax.set_yticks([i + .25 for i in range(3)], ["Attack", "Defence", "Both"])
    ax.set_xlabel("Quarter the project was created", labelpad=12); ax.set_ylabel("Role", labelpad=8)
    ax.set_zlabel("New projects in the quarter")
    ax.set_title(f"New AI security tools on GitHub, by quarter and role (sweep of {date}; last quarter may be partial)")
    ax.view_init(elev=24, azim=-58)
    fig.tight_layout(); n = f"{date}-4-overview-3d.png"; fig.savefig(out / n); plt.close(fig); names.append(n)
    return names


HF_SWEEPS = "exploratory/hf_sweeps"
HF_SHOWN = ["attack", "defence", "general_security", "safety_removed"]
HF_COLOURS = {"attack": "#b85c1e", "defence": "#1f4e79", "general_security": "#5b8c5a", "safety_removed": "#8e44ad"}


def hf_charts(date: str, rows: list[dict], root: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = root / FIGS
    out.mkdir(parents=True, exist_ok=True)
    ms = sorted({r["created"][:7] for r in rows if r["created"][:7] >= "2025-01"})
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=130)
    for k in HF_SHOWN:
        ax.plot([f"{m[5:]}/{m[2:4]}" for m in ms], [sum(r["role"] == k and r["created"][:7] == m for r in rows) for m in ms],
                marker="o", ms=3, lw=2, color=HF_COLOURS[k], label=k.replace("_", " ").capitalize())
    ax.set_xlabel("Month the model or app was created (last month may be partial)"); ax.set_ylabel("New items that month")
    ax.set_title(f"Hugging Face: new security-related AI models and apps each month (sweep of {date})")
    ax.tick_params(axis="x", labelrotation=60, labelsize=8); ax.legend(frameon=False); ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); fig.savefig(out / f"hf-{date}-1-new-per-month.png"); plt.close(fig)
    sr = [r for r in rows if r["role"] == "safety_removed" and r["kind"] == "model"]
    labs = collections.Counter(l for r in sr for l in r["base_lab"].split(";") if l).most_common(10)
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=130)
    bars = ax.bar([l for l, _ in labs], [n for _, n in labs], color=HF_COLOURS["safety_removed"], width=.6)
    for b, (_, n) in zip(bars, labs):
        ax.text(b.get_x() + b.get_width() / 2, n, f"{n:,}", ha="center", va="bottom", fontsize=9)
    ax.set_xlabel("Lab whose model was modified (from the model's own base-model tag)"); ax.set_ylabel("Safety-removed models")
    ax.set_title(f"Hugging Face: whose models have their safety training removed (sweep of {date})")
    ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); fig.savefig(out / f"hf-{date}-2-safety-removed-by-lab.png"); plt.close(fig)


def hf_section(root: Path) -> list[str]:
    files = sorted((root / HF_SWEEPS).glob("*.csv"))
    if not files:
        return []
    L = ["## Hugging Face: the models themselves (companion)", "",
         "Hugging Face is where AI models are published, including open-weight models whose safety "
         "training has been removed (\"uncensored\", \"abliterated\"). Fixed searches over model and app "
         "(Space) names; roles from each item's own name and descriptive tags, with stricter rules than "
         "GitHub's (refined and tested 30 Oct 2026): attack, defence, both, general security (security "
         "assistants with no side), safety removed, model testing (including AI-alignment red-teaming), "
         "unrelated (image models, Hacker News apps, hate-speech classifiers, \"reward hacking\") and "
         "unclear. Individuals' items appear by item name only. First labels; Claude checks the "
         "most-liked and the author confirms. Each search reads up to 40,000 items, newest first.", ""]
    for f in reversed(files):
        date, rows = f.stem, load(f)
        c = collections.Counter(r["role"] for r in rows)
        L += [f"### Hugging Face sweep of {date}", "",
              f"{len(rows):,} items ({sum(r['kind'] == 'model' for r in rows):,} models, "
              f"{sum(r['kind'] == 'space' for r in rows):,} apps): "
              + ", ".join(f"{k.replace('_', ' ')} {c.get(k, 0):,}" for k in
                          ["attack", "defence", "both", "general_security", "safety_removed", "model_testing", "unrelated", "unclear"]) + ".", "",
              f"![Hugging Face chart 1, sweep of {date}](ai_tool_landscape/hf-{date}-1-new-per-month.png)", "",
              "*Hugging Face chart 1. Horizontal: the month each model or app was created. Vertical: new "
              "items that month. Lines: attack, defence, general security, safety removed.*", "",
              f"![Hugging Face chart 2, sweep of {date}](ai_tool_landscape/hf-{date}-2-safety-removed-by-lab.png)", "",
              "*Hugging Face chart 2. Horizontal: the lab whose model was modified, from the model's own "
              "base-model tag (models without one are not counted). Vertical: safety-removed models.*", ""]
    return L


def protocol_section(date: str, s: dict) -> list[str]:
    """One chart per PER_CHART protocols found, so the number of charts follows the data."""
    found = sorted((p for i, p in enumerate(PROTOCOLS) if sum(s["protocols"][k][i] for k in SIDES)),
                   key=lambda p: -sum(s["protocols"][k][PROTOCOLS.index(p)] for k in SIDES))
    n = (len(found) + PER_CHART - 1) // PER_CHART
    L = [f"Network protocols: {len(found)} of the {len(PROTOCOLS)} watched were named, so {n} protocol "
         f"chart{'s' if n != 1 else ''} (12 to a chart, most-named first). Not found this sweep: "
         + (", ".join(p for p in PROTOCOLS if p not in found) or "none") + ".", ""]
    for c in range(n):
        L += [f"![Protocol chart {c + 1} of {n}, sweep of {date}](ai_tool_landscape/{date}-6-protocols-{c + 1}.png)", ""]
    if n:
        L += ["*Protocol charts. Horizontal: the network protocol a project names. Vertical: projects "
              "naming it. Bars: attack, defence, both.*", ""]
    return L


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
         "**Privacy.** Repositories owned by individuals appear by project name only, never the "
         "owner's username; organisations by full name. The register and the full list are kept privately in "
         "the author's Drive (author's decision, 30 Oct 2026; GitHub's Acceptable Use Policies allow "
         "research use of public, non-personal information published open access). The terms of every "
         "site the sweeps read are in `docs/TERMS_OF_USE.md` (Part V), with dated copies kept weekly.", "",
         "**Schedule.** Run by hand only: baseline 30 Oct 2026; the January 2027 sweep (6 Jan) is part "
         "of the pilot; then mid-2027 (7 Jul) and the end of 2027 (8 Dec).", ""]
    for f in reversed(files):
        date = f.stem
        s = stats(load(f))
        by = s["by"]
        n = sum(len(v) for v in by.values())
        top = lambda k: "; ".join(f"{r['name']} ({int(r['stars']):,})" for r in sorted(
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
              f"![Chart 3. Which lab's AI each side builds on, sweep of {date}](ai_tool_landscape/{date}-3-labs-by-side.png)", "",
              "*Chart 3. Horizontal: the lab whose AI a project names (in its description, or its "
              "README for the most-starred). Vertical: projects naming it. Bars: attack, defence, both.*", "",
              f"![Chart 4. Overview in 3D, sweep of {date}](ai_tool_landscape/{date}-4-overview-3d.png)", "",
              "*Chart 4 (overview, author's choice 30 Oct 2026). Left to right: the quarter each project "
              "was created. Front to back: attack, defence, both. Height: new projects that quarter. "
              "For exact values use charts 1 and 2; in 3D, front bars can hide those behind.*", "",
              f"![Chart 5. What each side focuses on, sweep of {date}](ai_tool_landscape/{date}-5-targets-by-side.png)", "",
              "*Chart 5. Horizontal: what a project goes after (attack) or protects (defence). "
              "Vertical: projects naming it. Bars: attack, defence, both.*", "",
              "Agent toolkits named (attack / defence / both): " + "; ".join(
                  f"{t} {s['toolkits']['attack'][i]}/{s['toolkits']['defence'][i]}/{s['toolkits']['both'][i]}"
                  for i, t in enumerate(TOOLKITS)) + ".", "",
              f"![Chart 6. Open-weight against closed AI, sweep of {date}](ai_tool_landscape/{date}-7-open-weight.png)", "",
              "*Chart 6 (author's decision, 30 Oct 2026). Left: projects naming an open-weight model "
              "(downloadable, runs anywhere: Llama, Qwen, DeepSeek, Mistral's open models, Hermes, Gemma, "
              "gpt-oss), a closed model (used through the maker's service: GPT, Claude, Gemini, Grok) or "
              "local running (Ollama and similar); a project can name several. Right: per quarter, the "
              "share of projects naming any model that name an open-weight or local one (quarters with "
              "fewer than five such projects left out). Decided by model, not lab: Google, OpenAI and "
              "Mistral make both kinds.*", "",
              *protocol_section(date, s),
              "| Month | " + " | ".join(m for m in s["months"][-12:]) + " |",
              "|---|" + "---|" * len(s["months"][-12:])]
        for k in SIDES:
            L.append(f"| {k.capitalize()} | " + " | ".join(str(v) for v in s["per_month"][k][-12:]) + " |")
        L += ["", f"Most-starred attack tools: {top('attack')}.", "",
              f"Most-starred defence tools: {top('defence')}.", "",
              f"Most-starred tools doing both: {top('both')}.", ""]
    L += hf_section(root)
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
        for f in sorted((root / HF_SWEEPS).glob("*.csv")):
            hf_charts(f.stem, load(f), root)
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
