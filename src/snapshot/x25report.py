"""AI security tools on GitHub (X25), generated from the sweeps.

Author's decisions, 30-31 Oct 2026: catalogue each hand-run sweep with charts and carry it in
The Snapshot manual; the January 2027 sweep is part of the pilot. The report leads with the
author's question, how many tools use AI and on which kind of model (hosted closed, open-weight
or local, both, none named), then what the tools do (tool types) and the groups worked out from
them (offensive security, defensive security, dual-use). Labels describe what a tool does, not
who uses it or why. Reads every sweep in exploratory/ai_tool_sweeps/<date>.csv (a compact copy
of the Research task github_tools output, originals only) and writes
exploratory/ai_tool_landscape.md with its charts in exploratory/ai_tool_landscape/. Exploratory
and never scored: a tool on GitHub is supply, not use; labels are first guesses until checked.

  python -m snapshot.x25report build     (charts need matplotlib; the text alone is checked)
"""
from __future__ import annotations

import argparse
import collections
import csv
import sys
from pathlib import Path

from .research.github_tools import AI_USE, AI_USE_NAMES, GROUP_NAMES, GROUPS, OFFENSIVE, DUAL
from .research.github_tools import PROTOCOLS as _P
from .research.github_tools import TYPES as _T
from .util import _repo_root

SWEEPS = "exploratory/ai_tool_sweeps"
OUT = "exploratory/ai_tool_landscape.md"
FIGS = "exploratory/ai_tool_landscape"
SIDES = GROUPS[:3]                      # offensive, defensive, dual_use (charted side by side)
COLOURS = {"offensive": "#b85c1e", "defensive": "#1f4e79", "dual_use": "#7a7a7a", "unclassified": "#c8c8c8"}
AI_COLOURS = {"closed": "#6a51a3", "open_local": "#2a9d8f", "both": "#e0a526", "none": "#d0d0d0"}
NOTE = ("Labels describe what a tool says it does, not who uses it or why; offensive-security tools are built "
        "mainly for authorised testing. Counts are of advertised projects; some may be renamed copies or "
        "malware lures posing as tools.")
LABS = ["OpenAI", "Anthropic", "Google", "Meta", "Mistral", "DeepSeek", "Alibaba", "Nous Research", "Moonshot",
        "Zhipu", "xAI", "Microsoft", "Local runner"]
TARGETS = ["web apps and APIs", "cloud accounts", "Windows and Active Directory", "networks and hosts",
           "containers and Kubernetes", "mobile apps", "industrial and IoT", "source code and supply chain",
           "email and people", "endpoints and logs"]
TOOLKITS = ["MCP", "LangChain", "CrewAI", "AutoGen", "LlamaIndex", "Semantic Kernel", "OpenAI Agents SDK",
            "Claude Code / Agent SDK", "smolagents", "PydanticAI"]
TYPES = list(_T)
PROTOCOLS = list(_P)
WEIGHTS = ["open-weight", "closed", "runs locally"]
PER_CHART = 12   # protocols per chart: the number of protocol charts follows what a sweep finds


def _type_group(t: str) -> str:
    return "offensive" if t in OFFENSIVE else "dual_use" if t in DUAL else "defensive"


COPY_MIN = 5   # author, 31 Oct 2026: a name uploaded 5+ times in a month by different makers is one tool plus copies


def load(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open()))


def mark_copies(rows: list[dict]) -> dict[str, int]:
    """Count a tool once when many makers upload projects with the same name in the same month
    (e.g. after a tool is in the news): the earliest stays, the rest get copy=yes. Returns the
    number of copies per name."""
    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        r["copy"] = ""
        groups[(r["name"].split("/")[-1].lower(), r["created"][:7])].append(r)
    copies: dict[str, int] = collections.Counter()
    for (name, _), rs in groups.items():
        makers = {r.get("ref") or r["name"].split("/")[0] for r in rs}
        if len(rs) >= COPY_MIN and len(makers) >= COPY_MIN:
            for r in sorted(rs, key=lambda r: (r["created"], r["name"]))[1:]:
                r["copy"] = "yes"
                copies[name] += 1
    return dict(copies)


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
    by = {k: [r for r in rows if r["group"] == k] for k in GROUPS}
    ms = months(rows)
    return {
        "n": len(rows), "by": by, "months": ms,
        "ai_use": {u: sum(r["ai_use"] == u for r in rows) for u in AI_USE},
        "ai_by_group": {g: {u: sum(r["ai_use"] == u for r in by[g]) for u in AI_USE} for g in GROUPS},
        "types": {t: sum(t in r["types"].split(";") for r in rows) for t in TYPES},
        "per_month": {k: [sum(r["created"][:7] == m for r in by[k]) for m in ms] for k in SIDES},
        "stars": {k: sum(int(r["stars"]) for r in by[k]) for k in GROUPS},
        **{f: {k: [sum(a in r[f].split(";") for r in by[k]) for a in lst] for k in SIDES}
           for f, lst in (("labs", LABS), ("weights", WEIGHTS), ("targets", TARGETS), ("toolkits", TOOLKITS),
                          ("protocols", PROTOCOLS))},
        "open_share": {k: open_share(by[k], ms) for k in SIDES},
    }


def _tidy(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def charts(date: str, s: dict, root: Path) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    out = root / FIGS
    out.mkdir(parents=True, exist_ok=True)
    names = []

    def save(fig, n):
        fig.text(0.5, 0.005, NOTE, ha="center", va="bottom", fontsize=8, color="#555555")
        fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out / n); plt.close(fig); names.append(n)

    # 1. How the tools use AI (the author's question)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=130, gridspec_kw={"width_ratios": [1, 1.3]})
    vals = [s["ai_use"][u] for u in AI_USE]
    bars = a1.bar([AI_USE_NAMES[u].replace(" ", "\n", 1) for u in AI_USE], vals, color=[AI_COLOURS[u] for u in AI_USE], width=.6)
    for b, v in zip(bars, vals):
        a1.text(b.get_x() + b.get_width() / 2, v, f"{v:,}\n({100 * v / max(s['n'], 1):.0f}%)", ha="center", va="bottom", fontsize=9)
    a1.set_ylim(0, max(vals) * 1.25); a1.set_ylabel("Projects"); a1.set_title("Which kind of AI model a project names")
    a1.tick_params(axis="x", labelsize=8); a1.grid(axis="y", alpha=.3); _tidy(a1)
    grp = [g for g in GROUPS if s["by"][g]]
    left = [0] * len(grp)
    for u in AI_USE:
        share = [100 * s["ai_by_group"][g][u] / max(len(s["by"][g]), 1) for g in grp]
        a2.barh([GROUP_NAMES[g] for g in grp], share, left=left, color=AI_COLOURS[u], label=AI_USE_NAMES[u])
        left = [l + v for l, v in zip(left, share)]
    a2.set_xlim(0, 100); a2.set_xlabel("% of the group's projects"); a2.invert_yaxis()
    a2.set_title("The same, within each group"); a2.legend(frameon=False, fontsize=8, loc="lower right"); _tidy(a2)
    fig.suptitle(f"How AI security tools on GitHub use AI (sweep of {date})")
    save(fig, f"{date}-1-ai-use.png")

    # 2. What the tools do (tool types)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=130)
    order = sorted(TYPES, key=lambda t: s["types"][t])
    ax.barh(order, [s["types"][t] for t in order], color=[COLOURS[_type_group(t)] for t in order])
    for i, t in enumerate(order):
        ax.text(s["types"][t], i, f" {s['types'][t]:,}", va="center", fontsize=8)
    ax.set_xlabel("Projects (a project can have several types)")
    ax.set_title(f"What the tools do (sweep of {date}); colour: the group a type counts towards")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=COLOURS[g], label=GROUP_NAMES[g]) for g in SIDES], frameon=False, fontsize=8)
    ax.grid(axis="x", alpha=.3); _tidy(ax)
    save(fig, f"{date}-2-tool-types.png")

    # 3. New projects each month, by group
    labels = [f"{m[5:]}/{m[2:4]}" for m in s["months"]]
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=130)
    for k in SIDES:
        ax.plot(labels, s["per_month"][k], marker="o", ms=3, lw=2, color=COLOURS[k], label=GROUP_NAMES[k])
    ax.set_xlabel("Month the project was created on GitHub (last month may be partial)")
    ax.set_ylabel("New projects that month")
    ax.set_title(f"New AI security tools on GitHub each month, by group (sweep of {date})")
    ax.tick_params(axis="x", labelrotation=60, labelsize=8); ax.grid(axis="y", alpha=.3); ax.legend(frameon=False); _tidy(ax)
    save(fig, f"{date}-3-new-per-month.png")

    # 4. Projects and stars, by group
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=130)
    for ax, vals, title, ylab in (
            (a1, [len(s["by"][k]) for k in SIDES], "How many projects", "Number of projects"),
            (a2, [s["stars"][k] for k in SIDES], "How much attention", "GitHub stars, all projects added up")):
        bars = ax.bar([GROUP_NAMES[k] for k in SIDES], vals, color=[COLOURS[k] for k in SIDES], width=.6)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,}", ha="center", va="bottom", fontsize=10)
        ax.set_title(title); ax.set_ylabel(ylab); ax.set_ylim(0, max(vals) * 1.15); ax.grid(axis="y", alpha=.3)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}")); _tidy(ax)
    fig.suptitle(f"Projects and attention by group (sweep of {date})")
    save(fig, f"{date}-4-projects-and-stars.png")

    for num, field, lst, xlab, title in (
            (5, "labs", LABS, "Lab whose AI the project names", "Which lab's AI each group builds on"),
            (7, "targets", TARGETS, "What the project works on", "What each group works on")):
        fig, ax = plt.subplots(figsize=(11, 5), dpi=130)
        x = range(len(lst))
        for off, k in zip((-.27, 0, .27), SIDES):
            ax.bar([i + off for i in x], s[field][k], .27, color=COLOURS[k], label=GROUP_NAMES[k])
        ax.set_xticks(list(x), lst, rotation=30, ha="right", fontsize=9)
        ax.set_xlabel(xlab); ax.set_ylabel("Projects naming it"); ax.set_title(f"{title} (sweep of {date})")
        ax.legend(frameon=False); ax.grid(axis="y", alpha=.3); _tidy(ax)
        save(fig, f"{date}-{num}-{field}-by-group.png")

    # 6. Overview in 3D, by quarter and group
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
    ax.set_yticks([i + .25 for i in range(3)], [GROUP_NAMES[k] for k in SIDES])
    ax.set_xlabel("Quarter the project was created", labelpad=12); ax.set_ylabel("Group", labelpad=8)
    ax.set_zlabel("New projects in the quarter")
    ax.set_title(f"New AI security tools on GitHub, by quarter and group (sweep of {date}; last quarter may be partial)")
    ax.view_init(elev=24, azim=-58)
    save(fig, f"{date}-6-overview-3d.png")

    # 8. Open-weight against closed, by group and over time
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=130)
    x = range(len(WEIGHTS))
    for off, k in zip((-.27, 0, .27), SIDES):
        a1.bar([i + off for i in x], s["weights"][k], .27, color=COLOURS[k], label=GROUP_NAMES[k])
    a1.set_xticks(list(x), ["Open-weight model", "Closed model", "Runs models locally"])
    a1.set_xlabel("Kind of AI the project names"); a1.set_ylabel("Projects naming it")
    a1.set_title("Open-weight or closed, by group"); a1.legend(frameon=False); a1.grid(axis="y", alpha=.3)
    for k in SIDES:
        q, vals = s["open_share"][k]
        a2.plot(q, vals, marker="o", lw=2, color=COLOURS[k], label=GROUP_NAMES[k])
    a2.set_ylim(0, 100); a2.set_xlabel("Quarter the project was created")
    a2.set_ylabel("% naming an open-weight or local model"); a2.set_title("Share using open-weight AI, by quarter")
    a2.tick_params(axis="x", labelrotation=45, labelsize=8); a2.legend(frameon=False); a2.grid(axis="y", alpha=.3)
    _tidy(a1); _tidy(a2)
    fig.suptitle(f"Open-weight against closed AI (sweep of {date})")
    save(fig, f"{date}-8-open-weight.png")

    found = sorted((p for i, p in enumerate(PROTOCOLS) if sum(s["protocols"][k][i] for k in SIDES)),
                   key=lambda p: -sum(s["protocols"][k][PROTOCOLS.index(p)] for k in SIDES))
    for c, start in enumerate(range(0, len(found), PER_CHART)):
        chunk = found[start:start + PER_CHART]
        fig, ax = plt.subplots(figsize=(11, 5), dpi=130)
        x = range(len(chunk))
        for off, k in zip((-.27, 0, .27), SIDES):
            ax.bar([i + off for i in x], [s["protocols"][k][PROTOCOLS.index(p)] for p in chunk], .27,
                   color=COLOURS[k], label=GROUP_NAMES[k])
        ax.set_xticks(list(x), chunk, rotation=30, ha="right", fontsize=9)
        ax.set_xlabel("Network protocol named by the project (most-named first)"); ax.set_ylabel("Projects naming it")
        ax.set_title(f"Network protocols each group names, {start + 1}-{start + len(chunk)} of {len(found)} found (sweep of {date})")
        ax.legend(frameon=False); ax.grid(axis="y", alpha=.3); _tidy(ax)
        save(fig, f"{date}-9-protocols-{c + 1}.png")
    return names


HF_SWEEPS = "exploratory/hf_sweeps"
HF_SHOWN = ["offensive", "defensive", "general_security"]   # safety-removed has its own chart (1 Nov 2026)
HF_COLOURS = {"offensive": "#b85c1e", "defensive": "#1f4e79", "general_security": "#5b8c5a", "safety_removed": "#8e44ad"}
HF_OLD = {"attack": "offensive", "defence": "defensive", "both": "dual_use"}   # sweeps before 31 Oct 2026


def hf_load(path: Path) -> list[dict]:
    """Rows of a Hugging Face sweep; sweeps before 1 Nov 2026 get the copy flag and a lab from the
    name here, so the fixes of 1 Nov apply to them too."""
    from .research.hf_tools import COPY, lab_from_name
    rows = load(path)
    for r in rows:
        r["role"] = HF_OLD.get(r["role"], r["role"])
        if not r.get("copy"):
            r["copy"] = "yes" if COPY.search(r["name"].split("/")[-1]) else "no"
        if not r.get("base_lab"):
            r["base_lab"] = lab_from_name(r["name"].split("/")[-1])
            r["lab_source"] = "name" if r["base_lab"] else ""
    return rows


def hf_charts(date: str, rows: list[dict], root: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = root / FIGS
    out.mkdir(parents=True, exist_ok=True)
    rows = [r for r in rows if r.get("copy") != "yes"]   # originals only (1 Nov 2026)
    ms = sorted({r["created"][:7] for r in rows if r["created"][:7] >= "2025-01"})
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=130)
    for k in HF_SHOWN:
        ax.plot([f"{m[5:]}/{m[2:4]}" for m in ms], [sum(r["role"] == k and r["created"][:7] == m for r in rows) for m in ms],
                marker="o", ms=3, lw=2, color=HF_COLOURS[k], label={"offensive": "Offensive security", "defensive": "Defensive security"}.get(k, k.replace("_", " ").capitalize()))
    ax.set_xlabel("Month the model or app was created (last month may be partial)"); ax.set_ylabel("New originals that month")
    ax.set_title(f"Hugging Face: new security-related AI models and apps each month, originals only (sweep of {date})")
    ax.tick_params(axis="x", labelrotation=60, labelsize=8); ax.legend(frameon=False); ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); fig.savefig(out / f"hf-{date}-1-new-per-month.png"); plt.close(fig)
    sr = [r for r in rows if r["safety_removed"] == "yes" and r["kind"] == "model"]
    labs = collections.Counter(l for r in sr for l in r["base_lab"].split(";") if l).most_common(10)
    unknown = sum(not r["base_lab"] for r in sr)
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=130)
    bars = ax.bar([l for l, _ in labs] + ["lab not stated"], [n for _, n in labs] + [unknown],
                  color=[HF_COLOURS["safety_removed"]] * len(labs) + ["#C8C8C8"], width=.6)
    for b, n in zip(bars, [n for _, n in labs] + [unknown]):
        ax.text(b.get_x() + b.get_width() / 2, n, f"{n:,}", ha="center", va="bottom", fontsize=9)
    ax.set_xlabel("Lab whose model was modified (base-model tag, the model card, or the model family named)")
    ax.set_ylabel("Originals advertised as safety-removed")
    ax.set_title(f"Hugging Face: whose models are advertised as safety-removed, originals only (sweep of {date})")
    ax.tick_params(axis="x", labelrotation=30, labelsize=8); ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); fig.savefig(out / f"hf-{date}-2-safety-removed-by-lab.png"); plt.close(fig)
    ms3 = sorted({r["created"][:7] for r in sr if r["created"][:7] >= "2024-01"})
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=130)
    ax.bar([f"{m[5:]}/{m[2:4]}" for m in ms3], [sum(r["created"][:7] == m for r in sr) for m in ms3], color=HF_COLOURS["safety_removed"])
    ax.set_ylabel("New originals"); ax.set_xlabel("Month created (last month may be partial)")
    ax.set_title(f"Hugging Face: new models advertised as safety-removed each month, originals only (sweep of {date}); a floor")
    ax.tick_params(axis="x", labelrotation=60, labelsize=7); ax.grid(axis="y", alpha=.3)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout(); fig.savefig(out / f"hf-{date}-3-safety-removed-per-month.png"); plt.close(fig)


def hf_section(root: Path) -> list[str]:
    files = sorted((root / HF_SWEEPS).glob("*.csv"))
    if not files:
        return []
    L = ["## Hugging Face: the models themselves (companion)", "",
         "Hugging Face is where AI models are published, including open-weight models whose safety "
         "training has been removed (\"uncensored\", \"abliterated\"). Fixed searches over model and app "
         "(Space) names; roles from each item's own name and descriptive tags, with stricter rules than "
         "GitHub's (refined and tested 30 Oct 2026; renamed 31 Oct 2026): offensive security, defensive "
         "security, dual-use, general security (security "
         "assistants with no side), safety removed, model testing (including AI-alignment red-teaming), "
         "unrelated (image models, Hacker News apps, hate-speech classifiers, \"reward hacking\") and "
         "unclear. Individuals' items appear by item name only. First labels; Claude checks the "
         "most-liked and the author confirms. Each search reads up to 40,000 items, newest first.", ""]
    for f in reversed(files):
        date, rows = f.stem, hf_load(f)
        c = collections.Counter(r["role"] for r in rows)
        L += [f"### Hugging Face sweep of {date}", "",
              f"{len(rows):,} items ({sum(r['kind'] == 'model' for r in rows):,} models, "
              f"{sum(r['kind'] == 'space' for r in rows):,} apps): "
              + ", ".join(f"{k.replace('_', ' ')} {c.get(k, 0):,}" for k in
                          ["offensive", "defensive", "dual_use", "general_security", "safety_removed", "model_testing", "unrelated", "unclear"]) + ".", "",
              f"![Hugging Face chart 1, sweep of {date}](ai_tool_landscape/hf-{date}-1-new-per-month.png)", "",
              "*Hugging Face chart 1. Horizontal: the month each model or app was created. Vertical: new "
              "items that month. Lines: offensive security, defensive security, general security, safety removed. "
              + NOTE + "*", "",
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
        L += [f"![Protocol chart {c + 1} of {n}, sweep of {date}](ai_tool_landscape/{date}-9-protocols-{c + 1}.png)", ""]
    if n:
        L += ["*Protocol charts. Horizontal: the network protocol a project names. Vertical: projects "
              "naming it. Bars: offensive security, defensive security, dual-use.*", ""]
    return L


def build_text(root: Path | None = None) -> str:
    root = root or _repo_root()
    files = sorted((root / SWEEPS).glob("*.csv"))
    L = ["# AI security tools on GitHub (X25, generated)", "",
         f"Generated by `python -m snapshot.x25report build` from `{SWEEPS}/`. Do not edit. "
         "Exploratory and never scored: a tool on GitHub is supply, not use.", "",
         "**The question (author, 31 Oct 2026).** How many of these tools actually use AI, and do they "
         "rely on hosted, closed models (used through the maker's online service: GPT, Claude, Gemini, "
         "Grok) or on open-weight models people download and run themselves (Llama, Qwen, DeepSeek, "
         "Mistral's open models, Hermes, Gemma, gpt-oss, or anything run through Ollama and similar)? "
         "Each project is labelled from the models it names: hosted closed model, open-weight or local, "
         "both, or no model named. \"No model named\" means its description (and, for the most-starred, "
         "its README) names none; it does not prove the tool uses no AI.", "",
         "**What the tools do.** Each project also gets one or more tool types from its own words "
         "(penetration testing, vulnerability scanning, reconnaissance, phishing simulation, malware "
         "analysis, detection and monitoring, code security review, threat intelligence, incident "
         "response, hardening and compliance, AI model testing). Groups are worked out from the types, "
         "never from intent: penetration testing and phishing simulation count as offensive security; "
         "scanning, reconnaissance and AI model testing as dual-use, because both sides use them every "
         "day; the rest as defensive security; a project whose types fall on both sides counts as "
         "dual-use. " + NOTE + " All labels are first guesses; Claude checks a hand-read sample and the "
         "author confirms (rules tested at the 18 Nov refinement).", "",
         "**What a sweep covers.** Not all of GitHub: 48 fixed searches (24 aimed at offensive-security "
         "tools, 24 at defensive-security tools, a few in Chinese and Russian; "
         "`config/github_tool_queries.yaml`) over the names, descriptions and topic tags of public "
         "repositories, forks left out, at most 1,000 results a search. Which search found a project "
         "does not decide its labels. Private and deleted repositories, and tools described in other "
         "words, are not seen. The same searches every time, so sweeps compare with each other.", "",
         "**Privacy.** Repositories owned by individuals appear by project name only, never the "
         "owner's username; organisations by full name. The register and the full list are kept "
         "privately (author's decisions, 30-31 Oct 2026; GitHub's Acceptable Use Policies allow research "
         "use of public, non-personal information published open access). The terms of every site the "
         "sweeps read are in `docs/TERMS_OF_USE.md` (Part V), with dated copies kept weekly.", "",
         "**Schedule.** Run by hand only: baseline 30 Oct 2026; the January 2027 sweep (6 Jan) is part "
         "of the pilot; then mid-2027 (7 Jul) and the end of 2027 (8 Dec).", ""]
    for f in reversed(files):
        date = f.stem
        all_rows = load(f)
        copies = mark_copies(all_rows)
        rows = [r for r in all_rows if r["copy"] != "yes"]
        s = stats(rows)
        by = s["by"]
        named = s["n"] - s["ai_use"]["none"]
        top = lambda k: "; ".join(f"{r['name']} ({int(r['stars']):,})" for r in sorted(
            by[k], key=lambda r: -int(r["stars"]))[:8])
        relabelled = bool(rows and rows[0].get("types_from"))
        L += [f"## Sweep of {date}", "",
              f"{s['n']:,} projects"
              + (f" (plus {sum(copies.values()):,} copies of tools uploaded many times in the same month, counted once: "
                 + ", ".join(f"{n} {c}" for n, c in sorted(copies.items(), key=lambda x: -x[1])) + ")" if copies else "")
              + ". **How they use AI:** "
              + ", ".join(f"{AI_USE_NAMES[u].lower()} {s['ai_use'][u]:,} ({100 * s['ai_use'][u] / max(s['n'], 1):.0f}%)" for u in AI_USE)
              + f". Of the {named:,} that name a model, {100 * s['ai_use']['closed'] / max(named, 1):.0f}% rely only on "
              f"hosted closed models, {100 * s['ai_use']['open_local'] / max(named, 1):.0f}% only on open-weight or local "
              f"ones and {100 * s['ai_use']['both'] / max(named, 1):.0f}% on both.", "",
              "**Groups:** " + ", ".join(f"{GROUP_NAMES[g].lower()} {len(by[g]):,}" for g in GROUPS) + ". "
              f"Stars: " + ", ".join(f"{GROUP_NAMES[g].lower()} {s['stars'][g]:,}" for g in SIDES) + "."
              + (" Tool types for this sweep were labelled afterwards from names, topic tags and "
                 "organisations' descriptions only (31 Oct 2026), so they undercount; later sweeps also "
                 "read descriptions of individuals' projects and the top READMEs." if relabelled else ""), "",
              f"![Chart 1. How the tools use AI, sweep of {date}](ai_tool_landscape/{date}-1-ai-use.png)", "",
              "*Chart 1 (the author's question). Left: projects by the kind of AI model they name, with the "
              "share of all projects. Right: the same within each group, as a share of the group. " + NOTE + "*", "",
              f"**In short.** About {round(100 * named / max(s['n'], 1))} in 100 of these security projects say which AI "
              f"model they use. Of those, about {round(100 * s['ai_use']['closed'] / max(named, 1))} in 100 depend only on "
              "a hosted, closed model reached over the internet (such as GPT, Claude or Gemini), about "
              f"{round(100 * s['ai_use']['open_local'] / max(named, 1))} in 100 only on open-weight models people download "
              f"and run themselves, and the rest, about {round(100 * s['ai_use']['both'] / max(named, 1))} in 100, on both. "
              "The other projects name no model; some may still use AI without saying so.", "",
              f"![Chart 2. What the tools do, sweep of {date}](ai_tool_landscape/{date}-2-tool-types.png)", "",
              "*Chart 2. Projects by tool type (a project can have several). Colour: the group the type "
              "counts towards.*", "",
              "**In short.** Each project is described by what it does, in its own words: testing systems "
              "the way an attacker would (offensive security, mostly for authorised red teams and "
              "penetration testers), detecting, investigating and fixing problems (defensive security), or "
              "work both sides do every day, such as scanning and reconnaissance (dual-use). The labels say "
              "what a tool does, never who uses it or why.", "",
              f"![Chart 3. New tools each month by group, sweep of {date}](ai_tool_landscape/{date}-3-new-per-month.png)", "",
              "*Chart 3. Horizontal: the month each project was created. Vertical: new projects that "
              "month. Lines: offensive security, defensive security, dual-use.*", "",
              f"![Chart 4. Projects and stars by group, sweep of {date}](ai_tool_landscape/{date}-4-projects-and-stars.png)", "",
              "*Chart 4. Left: how many projects each group has. Right: how much attention they get, as "
              "GitHub stars (bookmarks people give a project) added up over the group.*", "",
              f"![Chart 5. Which lab's AI each group builds on, sweep of {date}](ai_tool_landscape/{date}-5-labs-by-group.png)", "",
              "*Chart 5. Horizontal: the lab whose AI a project names. Vertical: projects naming it.*", "",
              f"![Chart 6. Overview in 3D, sweep of {date}](ai_tool_landscape/{date}-6-overview-3d.png)", "",
              "*Chart 6 (overview). Left to right: the quarter each project was created. Front to back: "
              "the three groups. Height: new projects that quarter. For exact values use charts 3 and 4.*", "",
              f"![Chart 7. What each group works on, sweep of {date}](ai_tool_landscape/{date}-7-targets-by-group.png)", "",
              "*Chart 7. Horizontal: what a project works on (web apps, cloud accounts, ...). Vertical: "
              "projects naming it.*", "",
              "Agent toolkits named (offensive / defensive / dual-use): " + "; ".join(
                  f"{t} {s['toolkits']['offensive'][i]}/{s['toolkits']['defensive'][i]}/{s['toolkits']['dual_use'][i]}"
                  for i, t in enumerate(TOOLKITS)) + ".", "",
              f"![Chart 8. Open-weight against closed AI, sweep of {date}](ai_tool_landscape/{date}-8-open-weight.png)", "",
              "*Chart 8. Left: projects naming an open-weight model, a closed model or local running, by "
              "group (a project can name several). Right: per quarter, the share of projects naming any "
              "model that name an open-weight or local one (quarters with fewer than five left out). "
              "Decided by model, not lab: Google, OpenAI and Mistral make both kinds.*", "",
              *protocol_section(date, s),
              "| Month | " + " | ".join(m for m in s["months"][-12:]) + " |",
              "|---|" + "---|" * len(s["months"][-12:])]
        for k in SIDES:
            L.append(f"| {GROUP_NAMES[k]} | " + " | ".join(str(v) for v in s["per_month"][k][-12:]) + " |")
        L += [""] + [x for k in SIDES for x in (f"Most-starred, {GROUP_NAMES[k].lower()}: {top(k)}.", "")]
    L += hf_section(root)
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    a = ap.parse_args(argv)
    root = _repo_root()
    text = build_text(root)
    if a.cmd == "build":
        for old in (root / FIGS).glob("*.png") if (root / FIGS).exists() else []:
            old.unlink()            # chart names follow the current layout; old files go
        for f in sorted((root / SWEEPS).glob("*.csv")):
            rows = load(f)
            mark_copies(rows)
            charts(f.stem, stats([r for r in rows if r["copy"] != "yes"]), root)
        for f in sorted((root / HF_SWEEPS).glob("*.csv")):
            hf_charts(f.stem, hf_load(f), root)
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
