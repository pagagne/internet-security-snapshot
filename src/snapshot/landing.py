"""The landing page's two pictures (author's request and decisions, 31 Oct 2026).

1. Status banner: one small square per core data source. Green: it answered the daily check;
   red: it answered with an error or not at all; gray: not checked in this run; outlined:
   awaiting permission, never contacted. Drawn by the Source status workflow once a day and
   saved on the run-reports branch (landing/), so main gets no daily commits. Each check is one
   light request that reads only the first bytes. The picture carries its check time, because a
   stopped workflow would otherwise leave old colours looking fresh.
2. Coverage ring: every kind of data the study needs, one slice each, sized by the measures it
   feeds (3 x core indicators + 1 x exploratory measures), coloured when actually collected and
   gray when missing. Drawn from config/coverage.yaml into docs/landing/ (kept current by a test).

GitHub shows README pictures but strips styles and scripts, so both are SVG files, each in a
light and a dark version chosen with <picture>.

  python -m snapshot.landing build           the ring (docs/landing/coverage-{light,dark}.svg)
  python -m snapshot.landing check           fails if the ring is out of date
  python -m snapshot.landing status --out D  check the sources; write D/banner-{light,dark}.svg, status.json
  python -m snapshot.landing capture --label L --store S [--banner D]   dated snapshot + roll-up
  python -m snapshot.landing rollup --store S                          rebuild S/CHANGES.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import sys
import time
from html import escape
from pathlib import Path

import yaml

from .util import _repo_root

CONFIG = "config/coverage.yaml"
OUT_DIR = "docs/landing"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
THEMES = {
    "light": {"text": "#1f2328", "muted": "#59636e", "core": "#1D9E75", "companion": "#7F77DD",
              "missing": "#d0d7de", "gap": "#ffffff", "ok": "#1a7f37", "error": "#cf222e",
              "unchecked": "#d0d7de", "outline": "#8c959f"},
    "dark": {"text": "#e6edf3", "muted": "#9198a1", "core": "#1D9E75", "companion": "#7F77DD",
             "missing": "#3d444d", "gap": "#0d1117", "ok": "#3fb950", "error": "#f85149",
             "unchecked": "#3d444d", "outline": "#9198a1"},
}


def load(root: Path | None = None) -> dict:
    return yaml.safe_load(((root or _repo_root()) / CONFIG).read_text())


def weight(piece: dict) -> int:
    core = sum(1 for m in piece["measures"] if m.startswith("I"))
    return 3 * core + (len(piece["measures"]) - core)


def collected_share(pieces: list[dict]) -> int:
    tot = sum(weight(p) for p in pieces)
    return round(100 * sum(weight(p) for p in pieces if p["collected"]) / tot)


def ring_svg(pieces: list[dict], theme: str) -> str:
    c = THEMES[theme]
    cx = cy = 150
    r, ri = 130, 62
    tot = sum(weight(p) for p in pieces)
    a = -math.pi / 2
    out = []
    for i, p in enumerate(pieces, 1):
        b = a + 2 * math.pi * weight(p) / tot
        pt = lambda t, R: (cx + R * math.cos(t), cy + R * math.sin(t))
        large = 1 if b - a > math.pi else 0
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pt(a, r), pt(b, r), pt(b, ri), pt(a, ri)
        fill = c[p["tier"]] if p["collected"] else c["missing"]
        out.append(f'<path d="M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}'
                   f'A{ri} {ri} 0 {large} 0 {x3:.2f} {y3:.2f}Z" fill="{fill}" stroke="{c["gap"]}" stroke-width="2">'
                   f'<title>{i}. {escape(p["name"])}</title></path>')
        if b - a > 0.16:
            tx, ty = pt((a + b) / 2, (r + ri) / 2)
            ink = "#ffffff" if p["collected"] else c["muted"]
            out.append(f'<text x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle" font-size="11" fill="{ink}">{i}</text>')
        a = b
    out.append(f'<text x="{cx}" y="{cy + 2}" text-anchor="middle" font-size="26" font-weight="600" fill="{c["text"]}">'
               f'{collected_share(pieces)}%</text>')
    out.append(f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="12" fill="{c["muted"]}">collected</text>')
    # legend: two columns
    rows = math.ceil(len(pieces) / 2)
    for i, p in enumerate(pieces):
        col, row = divmod(i, rows)
        x, y = 315 + col * 245, 30 + row * 20
        fill = c[p["tier"]] if p["collected"] else c["missing"]
        ink = c["text"] if p["collected"] else c["muted"]
        out.append(f'<rect x="{x}" y="{y - 10}" width="11" height="11" rx="2" fill="{fill}"/>'
                   f'<text x="{x + 17}" y="{y}" font-size="12" fill="{ink}">{i + 1}. {escape(p["name"])}</text>')
    ly = 30 + rows * 20 + 10
    for k, (lab, key) in enumerate([("core, collected", "core"), ("companion, collected", "companion"), ("missing", "missing")]):
        x = 315 + k * 140
        out.append(f'<rect x="{x}" y="{ly - 9}" width="10" height="10" rx="2" fill="{c[key]}"/>'
                   f'<text x="{x + 15}" y="{ly}" font-size="11" fill="{c["muted"]}">{lab}</text>')
    out.append(f'<text x="315" y="{ly + 18}" font-size="11" fill="{c["muted"]}">Slice size: 3 per core indicator, 1 per exploratory measure it feeds.</text>')
    h = max(300, ly + 30)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{h}" viewBox="0 0 800 {h}" '
            f'font-family="{FONT}" role="img" aria-label="Data the study needs: {collected_share(pieces)}% collected">'
            + "".join(out) + "</svg>\n")


def build(root: Path | None = None) -> dict[str, str]:
    root = root or _repo_root()
    pieces = load(root)["pieces"]
    return {f"{OUT_DIR}/coverage-{t}.svg": ring_svg(pieces, t) for t in THEMES}


# ---- daily status -------------------------------------------------------------------------

def ping(src: dict, timeout: float = 30) -> dict:
    """One light request: read the status and the first bytes only."""
    import requests
    from .collect.http import UA, note_status
    ua = os.environ.get(src["ua_env"], "") if src.get("ua_env") else UA
    if src.get("ua_env") and not ua:
        return {"state": "unchecked", "detail": f"{src['ua_env']} not set"}
    for attempt in (1, 2):
        try:
            with requests.get(src["url"], headers={"User-Agent": ua}, timeout=timeout, stream=True) as r:
                note_status(src["url"], r.status_code)
                next(r.iter_content(512), b"")
                if r.status_code < 400:
                    return {"state": "ok", "code": r.status_code}
                res = {"state": "error", "code": r.status_code}
        except Exception as e:  # noqa: BLE001
            res = {"state": "error", "detail": type(e).__name__}
        if attempt == 1:
            time.sleep(5)
    return res


def banner_svg(sources: list[dict], results: dict, checked: str, theme: str) -> str:
    c = THEMES[theme]
    per_row, w = 5, 152
    out = [f'<text x="0" y="16" font-size="14" font-weight="600" fill="{c["text"]}">Core data sources</text>',
           f'<text x="760" y="16" text-anchor="end" font-size="11" fill="{c["muted"]}">checked {escape(checked)}</text>']
    for i, s in enumerate(sources):
        row, col = divmod(i, per_row)
        x, y = col * w, 44 + row * 26
        if s.get("pending"):
            sq = f'<rect x="{x + 0.75}" y="{y - 11.25}" width="11.5" height="11.5" rx="2" fill="none" stroke="{c["outline"]}" stroke-width="1.5"/>'
            ink = c["muted"]
        else:
            state = results.get(s["name"], {}).get("state", "unchecked")
            sq = f'<rect x="{x}" y="{y - 12}" width="13" height="13" rx="2" fill="{c[state]}"/>'
            ink = c["text"] if state != "unchecked" else c["muted"]
        out.append(sq + f'<text x="{x + 20}" y="{y}" font-size="12" fill="{ink}">{escape(s["name"])}</text>')
    ly = 44 + math.ceil(len(sources) / per_row) * 26 + 4
    for k, (lab, key) in enumerate([("answered", "ok"), ("error", "error"), ("not checked", "unchecked")]):
        x = k * 120
        out.append(f'<rect x="{x}" y="{ly - 9}" width="10" height="10" rx="2" fill="{c[key]}"/>'
                   f'<text x="{x + 15}" y="{ly}" font-size="11" fill="{c["muted"]}">{lab}</text>')
    out.append(f'<rect x="{360.75}" y="{ly - 8.25}" width="8.5" height="8.5" rx="2" fill="none" stroke="{c["outline"]}" stroke-width="1.5"/>'
               f'<text x="375" y="{ly}" font-size="11" fill="{c["muted"]}">awaiting permission</text>')
    h = ly + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="{h}" viewBox="-10 0 780 {h}" '
            f'font-family="{FONT}" role="img" aria-label="Core data source status, checked {escape(checked)}">'
            + "".join(out) + "</svg>\n")


def status(out: Path, now: dt.datetime | None = None, pause: float = 2.0) -> dict:
    sources = load()["sources"]
    now = now or dt.datetime.now(dt.timezone.utc)
    results = {}
    for s in sources:
        if s.get("pending"):
            results[s["name"]] = {"state": "pending"}
            continue
        results[s["name"]] = ping(s)
        time.sleep(pause)
    checked = now.strftime("%Y-%m-%d %H:%M UTC")
    out.mkdir(parents=True, exist_ok=True)
    for t in THEMES:
        (out / f"banner-{t}.svg").write_text(banner_svg(sources, results, checked, t))
    (out / "status.json").write_text(json.dumps({"checked": checked, "results": results}, indent=1) + "\n")
    return results


# ---- dated snapshots and the roll-up (author, 31 Oct 2026) ---------------------------------
# The landing page changes often, so its state is captured at the cutover, the pilot run and
# each quarterly run, with a roll-up of what changed (the annual one closes the year). Kept on
# the run-reports branch beside the daily banner (<store> = landing/): snapshots/<day>-<label>/
# and CHANGES.md, so main gets no automatic commits.


def capture(label: str, banner_dir: Path | None, day: str, store: Path, root: Path | None = None) -> Path:
    """Copy the ring, its config and (when given) the day's banner and status into
    <store>/snapshots/<day>-<label>/ with a summary.md."""
    import shutil
    root = root or _repo_root()
    d = store / "snapshots" / f"{day}-{label}"
    d.mkdir(parents=True, exist_ok=True)
    for t in THEMES:
        shutil.copy2(root / OUT_DIR / f"coverage-{t}.svg", d / f"coverage-{t}.svg")
    shutil.copy2(root / CONFIG, d / "coverage.yaml")
    status_line = "Banner: not available for this capture."
    if banner_dir and (banner_dir / "status.json").exists():
        for f in ("banner-light.svg", "banner-dark.svg", "status.json"):
            shutil.copy2(banner_dir / f, d / f)
        st = json.loads((d / "status.json").read_text())
        counts = {}
        for v in st["results"].values():
            counts[v["state"]] = counts.get(v["state"], 0) + 1
        status_line = (f"Banner checked {st['checked']}: " + ", ".join(f"{n} {k}" for k, n in sorted(counts.items())) + ".")
    cfg = yaml.safe_load((d / "coverage.yaml").read_text())
    pieces = cfg["pieces"]
    L = [f"# Landing-page snapshot: {label}, {day}", "",
         f"Data collected: **{collected_share(pieces)}%** of the ring (slices weighted 3 per core indicator, "
         "1 per exploratory measure). " + status_line, "",
         "![Coverage ring](coverage-light.svg)", ""]
    if (d / "banner-light.svg").exists():
        L += ["![Source status banner](banner-light.svg)", ""]
    L += ["| # | Data | Tier | Collected | Weight |", "|---|---|---|---|---|"]
    L += [f"| {i} | {p['name']} | {p['tier']} | {'yes' if p['collected'] else 'no'} | {weight(p)} |"
          for i, p in enumerate(pieces, 1)]
    (d / "summary.md").write_text("\n".join(L) + "\n")
    return d


def _snapshots(store: Path) -> list[Path]:
    base = store / "snapshots"
    return sorted(p for p in base.iterdir() if (p / "coverage.yaml").exists()) if base.exists() else []


def rollup_text(store: Path) -> str:
    snaps = _snapshots(store)
    L = ["# Landing page: what changed between snapshots", "",
         "Generated by `python -m snapshot.landing rollup` from `snapshots/` beside this file (author's request, "
         "31 Oct 2026: capture the landing page at the cutover, the pilot run and every quarterly run, with an "
         "annual roll-up). Do not edit by hand.", "",
         "| Snapshot | Collected | Sources answered | Change from the previous snapshot |", "|---|---|---|---|"]
    prev = None
    years: dict[str, list[tuple[str, dict, dict]]] = {}
    for s in snaps:
        cfg = yaml.safe_load((s / "coverage.yaml").read_text())
        st = json.loads((s / "status.json").read_text())["results"] if (s / "status.json").exists() else {}
        ok = sum(v["state"] == "ok" for v in st.values())
        checked = sum(v["state"] != "pending" for v in st.values())
        L.append(f"| [{s.name}](snapshots/{s.name}/summary.md) | {collected_share(cfg['pieces'])}% | "
                 f"{f'{ok} of {checked}' if st else '-'} | {_diff(prev, (cfg, st)) if prev else 'first snapshot'} |")
        prev = (cfg, st)
        years.setdefault(s.name[:4], []).append((s.name, cfg, st))
    for y, items in sorted(years.items()):
        if len(items) > 1:
            (a_name, a_cfg, a_st), (b_name, b_cfg, b_st) = items[0], items[-1]
            L += ["", f"## {y} roll-up: {a_name} to {b_name}", "",
                  f"Collected {collected_share(a_cfg['pieces'])}% to {collected_share(b_cfg['pieces'])}%. "
                  + _diff((a_cfg, a_st), (b_cfg, b_st))]
    if len(snaps) > 1:
        first, last = years[min(years)][0], years[max(years)][-1]
        L += ["", f"## Whole study so far: {first[0]} to {last[0]}", "",
              f"Collected {collected_share(first[1]['pieces'])}% to {collected_share(last[1]['pieces'])}%. "
              + _diff((first[1], first[2]), (last[1], last[2]))]
    return "\n".join(L) + "\n"


def _diff(a, b) -> str:
    (acfg, ast), (bcfg, bst) = a, b
    ap = {p["name"]: p for p in acfg["pieces"]}
    bp = {p["name"]: p for p in bcfg["pieces"]}
    out = []
    got = [n for n in bp if bp[n]["collected"] and not ap.get(n, {}).get("collected")]
    lost = [n for n in bp if not bp[n]["collected"] and ap.get(n, {}).get("collected")]
    added = [n for n in bp if n not in ap]
    dropped = [n for n in ap if n not in bp]
    reweighted = [n for n in bp if n in ap and weight(bp[n]) != weight(ap[n])]
    for lab, xs in (("now collected", got), ("no longer collected", lost), ("new", added),
                    ("removed", dropped), ("measures changed", reweighted)):
        if xs:
            out.append(f"{lab}: {', '.join(xs)}")
    moved = [f"{k} {ast.get(k, {}).get('state', '-')} to {v['state']}" for k, v in bst.items()
             if ast and ast.get(k, {}).get("state") != v["state"]]
    if moved:
        out.append("sources: " + ", ".join(moved))
    s = "; ".join(out) + "." if out else "no change."
    return s[0].upper() + s[1:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build"); sub.add_parser("check")
    st = sub.add_parser("status"); st.add_argument("--out", required=True, type=Path)
    cp = sub.add_parser("capture"); cp.add_argument("--label", required=True)
    cp.add_argument("--banner", type=Path); cp.add_argument("--date")
    cp.add_argument("--store", required=True, type=Path)
    ru = sub.add_parser("rollup"); ru.add_argument("--store", required=True, type=Path)
    a = ap.parse_args(argv)
    root = _repo_root()
    if a.cmd == "capture":
        import re
        if not re.fullmatch(r"[a-z0-9-]{1,40}", a.label):
            print("label: lower-case letters, digits and hyphens only"); return 2
        day = a.date or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        d = capture(a.label, a.banner, day, a.store, root)
        (a.store / "CHANGES.md").write_text(rollup_text(a.store))
        print(f"captured {d.name}; CHANGES.md updated")
        return 0
    if a.cmd == "rollup":
        (a.store / "CHANGES.md").write_text(rollup_text(a.store))
        print("CHANGES.md updated")
        return 0
    if a.cmd == "status":
        res = status(a.out)
        bad = [k for k, v in res.items() if v["state"] == "error"]
        print(f"{sum(v['state'] == 'ok' for v in res.values())} answered, {len(bad)} errors"
              + (f": {', '.join(bad)}" if bad else ""))
        return 0
    files = build(root)
    if a.cmd == "build":
        for f, text in files.items():
            (root / f).parent.mkdir(parents=True, exist_ok=True)
            (root / f).write_text(text)
        print(f"ring: {collected_share(load(root)['pieces'])}% collected; {len(files)} files")
        return 0
    stale = [f for f, text in files.items() if not (root / f).exists() or (root / f).read_text() != text]
    if stale:
        print("out of date: " + ", ".join(stale) + " (run python -m snapshot.landing build)")
        return 1
    print("landing pictures current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
