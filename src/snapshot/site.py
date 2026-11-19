"""The project website (schedule item pages-build; live from 4 Dec 2026 when the author switches on
GitHub Pages).

Three parts, published from the site/ folder by .github/workflows/pages.yml:

  site/index.html          home page: the README's Mission section (approved wording), links to
                           the plan, the reports, the Reviewer's Desk and run health, and the
                           credits block (config/credits.yaml). Built here, committed, checked.
  site/reviewer/           the Reviewer's Desk (already in the repository).
  site/health/index.html   run health, built at publish time from the public run-reports branch:
                           the pilot, start to finish; last and next run; source health with
                           pushback and permission state; rebuild and privacy checks; recent runs.
                           Health only: no findings or counts before the author's review.

    python -m snapshot.site home                      # write site/index.html
    python -m snapshot.site check                     # site/index.html current?
    python -m snapshot.site health --reports DIR      # DIR: a checkout of the run-reports branch
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

import yaml

from .util import _repo_root

ROOT = _repo_root()
SITE = ROOT / "site"
REPO = "https://github.com/pagagne/internet-security-snapshot"
RAW = "https://raw.githubusercontent.com/pagagne/internet-security-snapshot/run-reports/"

STYLE = """
:root{--paper:#f4f6f7;--card:#fff;--ink:#172028;--muted:#59646e;--line:#d6dce1;--accent:#0e5a61;
--ok:#2c6a37;--ok-soft:#e3f1e5;--due:#9a520a;--due-soft:#f8ecdc;--bad:#a12b2b;--bad-soft:#f8e4e4;
--f-body:"Public Sans","Segoe UI",Roboto,Helvetica,Arial,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--paper:#0f151a;--card:#161e25;--ink:#e4eaee;--muted:#9ba7b1;--line:#2a353e;
--accent:#62b4bb;--ok:#82c78f;--ok-soft:#17301d;--due:#e3a457;--due-soft:#33261a;--bad:#f08c8c;--bad-soft:#3a1d1d;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--f-body)}
main{max-width:860px;margin:0 auto;padding:28px 18px 60px}h1{font-size:1.7rem;margin:.2em 0}
h2{font-size:1.15rem;margin:1.8em 0 .5em;border-bottom:1px solid var(--line);padding-bottom:.25em}
a{color:var(--accent)}.muted{color:var(--muted);font-size:.92rem}.card{background:var(--card);border:1px solid var(--line);
border-radius:6px;padding:14px 16px;margin:10px 0}nav a{display:inline-block;margin:0 14px 8px 0;font-weight:600}
table{width:100%;border-collapse:collapse;font-size:.93rem}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.tag{font:12px var(--f-mono);padding:1px 6px;border-radius:4px;white-space:nowrap}
.ok{background:var(--ok-soft);color:var(--ok)}.wait{background:var(--paper);color:var(--muted);border:1px solid var(--line)}
.run{background:var(--due-soft);color:var(--due)}.late,.bad{background:var(--bad-soft);color:var(--bad)}
.draft{border-left:4px solid var(--due);padding-left:12px}img{max-width:100%}
"""


def page(title: str, body: str, note: str = "") -> str:
    return (f"<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{html.escape(title)}</title><style>{STYLE}</style></head>\n<body><main>\n"
            f"{body}\n<p class=\"muted\">{note}</p>\n</main></body></html>\n")


def _md(text: str) -> str:
    """The README's small Markdown subset (paragraphs, links, bold, lists)."""
    out, para, items = [], [], []
    num = re.compile(r"^(\d+)\.\s+")

    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"&lt;(https?://[^\s&]+)&gt;", r'<a href="\1">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return s

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()
        if items:
            if num.match(items[0]):
                start = num.match(items[0]).group(1)
                out.append(f'<ol start="{start}">' + "".join(f"<li>{inline(num.sub('', i))}</li>" for i in items) + "</ol>")
            else:
                out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for line in text.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("- ") or num.match(s):
            if para:
                flush()
            items.append(s[2:] if s.startswith("- ") else s)
        elif items and line.startswith(("  ", "   ")):
            items[-1] += " " + s                      # a list item's wrapped line
        elif s.startswith("**") and s.endswith("**") and len(s) < 80:
            flush()
            out.append(f"<h3>{inline(s.strip('*'))}</h3>")
        else:
            if items:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


def readme_section(name: str, readme: Path | None = None) -> str:
    text = (readme or ROOT / "README.md").read_text()
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def home_html() -> str:
    from .credits import block_md
    mission = readme_section("Mission")
    credits = re.sub(r"^## .*\n", "", block_md())
    body = f"""
<h1>Internet Security Snapshot</h1>
<p class="muted">A pre-registered, self-funded, non-commercial study, quarterly through 2027.</p>
<nav><a href="health/">Run health</a><a href="reviewer/">Reviewer's Desk</a>
<a href="{REPO}/blob/main/prereg/PREREGISTRATION.md">The plan</a>
<a href="https://doi.org/10.17605/OSF.IO/3XT82">OSF registration</a>
<a href="#reports">Reports</a><a href="{REPO}">Code and documents</a></nav>
<picture><source media="(prefers-color-scheme: dark)" srcset="{RAW}landing/countdown-dark.svg">
<img alt="Days until the next study run" src="{RAW}landing/countdown-light.svg"></picture>
<h2>Mission</h2>
{_md(mission)}
<h2 id="reports">Reports</h2>
<p>The first report, for the Q4 2026 pilot, is due in early January 2027; each quarter then has a
provisional report and a final report one month later. Until then this site shows the study's
run health only.</p>
<h2>Data sources and credits</h2>
{_md(credits)}
"""
    return page("Internet Security Snapshot", body,
                "Built from the repository by snapshot.site; the wording above is the README's.")


# --- run health --------------------------------------------------------------------------------
PILOT = [  # (step, schedule id or None, date, how it shows done)
    ("Practice run (dry run)", "dry-run", "2026-12-01"),
    ("Full test run", "dry-run-full", "2026-12-15"),
    ("Decisions session", "freeze-session", "2026-12-21"),
    ("Core lock and OSF update", "freeze", "2026-12-29"),
    ("Pilot collection (quarterly pull)", None, "2027-01-01"),
    ("Hand-check window", None, "2027-01-04"),
    ("Final run", None, "2027-02-01"),
]


def _schedule() -> dict:
    d = yaml.safe_load((ROOT / "docs/schedule/schedule.yaml").read_text())
    items = d["items"] if isinstance(d, dict) and "items" in d else next(v for v in d.values() if isinstance(v, list))
    return {i["id"]: i for i in items}


def _runs(reports: Path) -> list[dict]:
    """Quarterly-pull runs on the run-reports branch: date, run id, quarter, run type, gaps, pushback."""
    out = []
    for d in sorted((reports / "reports").glob("*-run*")):
        m = re.match(r"(\d{4}-\d\d-\d\dT\d{4}Z)-run(\d+)$", d.name)
        if not m:
            continue
        for man in sorted(d.glob("manifest-*.json")):
            try:
                j = json.loads(man.read_text())
            except ValueError:
                continue
            gaps = sorted({e["source"] for e in j.get("files", []) if e.get("status") != "ok"})
            out.append({"stamp": m.group(1), "run_id": m.group(2), "quarter": j.get("quarter"), "run": j.get("run"),
                        "gaps": gaps, "pushback": bool(j.get("server_pushback"))})
    return out


def _latest_line(folder: Path) -> tuple[str, str]:
    files = sorted(folder.glob("*.md")) if folder.exists() else []
    if not files:
        return "", "none yet"
    text = files[-1].read_text()
    first = next((l.strip("#- ").strip() for l in text.splitlines() if l.strip() and not l.startswith("## ")), "")
    return files[-1].stem[:16], first


def _state(item: dict | None, date: str, today: dt.date, done_by_run: bool = False) -> str:
    if done_by_run or (item and item.get("done")):
        return "done"
    d = dt.date.fromisoformat(date)
    if d == today:
        return "running"
    return "late" if d < today else "waiting"


def health_html(reports: Path, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    sch = _schedule()
    runs = _runs(reports)
    q4 = {r["run"] for r in runs if r["quarter"] == "2026Q4"}
    tag = lambda s: f'<span class="tag {dict(done="ok", waiting="wait", running="run", late="late").get(s, "wait")}">{s}</span>'
    rows = []
    for step, sid, date in PILOT:
        dry_after = any(r["quarter"] == "2026Q4" and r["run"] == "dry-run" and r["stamp"][:10] >= date for r in runs)
        by_run = (step.startswith("Pilot collection") and bool(q4 & {"provisional", "final"})) or \
                 (step.startswith("Final run") and "final" in q4) or \
                 (sid in ("dry-run", "dry-run-full") and dry_after)
        st = _state(sch.get(sid) if sid else None, date, today, by_run)
        if step == "Hand-check window":
            end = dt.date(2027, 1, 28)
            st = "done" if today > end else ("running" if today >= dt.date(2027, 1, 4) else "waiting")
            date = "2027-01-04 to 2027-01-28"
        rows.append(f"<tr><td>{date}</td><td>{html.escape(step)}</td><td>{tag(st)}</td></tr>")
    last = runs[-1] if runs else None
    gh = [i for i in sch.values() if i.get("owner") == "github" and str(i.get("date", "")) >= today.isoformat()
          and not i.get("done")]
    nxt = min(gh, key=lambda i: str(i["date"])) if gh else None
    status = {}
    sp = reports / "landing" / "status.json"
    if sp.exists():
        try:
            status = json.loads(sp.read_text())
        except ValueError:
            status = {}
    perms = yaml.safe_load((ROOT / "config/sources.yaml").read_text()).get("permissioned", {})
    words = {"ok": ("ok", "answered"), "error": ("bad", "error"), "unchecked": ("wait", "checked at each pull"),
             "pending": ("wait", "awaiting permission")}

    def answer(r):
        cls, word = words.get(r.get("state"), ("wait", str(r.get("state", "?"))))
        return f'<span class="tag {cls}">{html.escape(word)}</span>'
    src_rows = [f"<tr><td>{html.escape(n)}</td><td>{answer(r)}</td></tr>" for n, r in (status.get("results") or {}).items()]
    perm_rows = [f"<tr><td>{html.escape(p['name'])}</td><td>{html.escape(p['permission'])}</td>"
                 f"<td>{'collected' if p.get('collect') else 'not collected'}</td></tr>" for p in perms.values()]
    rb_when, rb = _latest_line(reports / "reports" / "rebuild-check")
    pv_when, pv = _latest_line(reports / "reports" / "privacy-scan")
    recent = "".join(
        f"<tr><td>{r['stamp'][:10]}</td><td>{r['quarter']} {r['run']}</td>"
        f"<td>{tag('late') .replace('>late<', '>gaps: ' + html.escape(', '.join(r['gaps'])) + '<') if r['gaps'] else tag('done').replace('>done<', '>complete<')}</td>"
        f"<td>{'yes' if r['pushback'] else 'none'}</td>"
        f"<td><a href=\"{REPO}/actions/runs/{r['run_id']}\">run log</a></td></tr>" for r in reversed(runs[-8:]))
    body = f"""
<h1>Run health</h1>
<p class="muted">Updated {today.isoformat()} from the public run reports. Health only: findings and counts
appear only after the author's review, in the reports. <a href="../">Home</a></p>
<h2>The pilot, start to finish</h2>
<div class="draft"><p class="muted">Draft layout, awaiting the author's approval of the mock-up.</p>
<table><tr><th>When</th><th>Step</th><th>State</th></tr>{''.join(rows)}</table>
<p class="muted">Hand-check progress (items done out of the total, never the answers) appears from 4 Jan 2027.
Changes from the plan: <a href="{REPO}/blob/main/prereg/DEVIATIONS.md">the deviations log</a>.</p></div>
<h2>Last and next run</h2>
<div class="card">Last quarterly run: {f"{last['stamp'][:10]}, {last['quarter']} {last['run']} (<a href='{REPO}/actions/runs/{last['run_id']}'>run log</a>)" if last else "none yet"}<br>
Next scheduled run: {f"{nxt['date']}, {html.escape(nxt['title'])}" if nxt else "none scheduled"}</div>
<h2>Sources</h2>
<p class="muted">Today's light check ({html.escape(str(status.get('checked', 'not yet run')))}):</p>
<table><tr><th>Source</th><th>Answer</th></tr>{''.join(src_rows) or '<tr><td colspan=2>not yet run</td></tr>'}</table>
<p class="muted">Sources that need permission:</p>
<table><tr><th>Source</th><th>Permission</th><th>Pull</th></tr>{''.join(perm_rows)}</table>
<h2>Checks</h2>
<div class="card">Rebuild check ({rb_when or '-'}): {html.escape(rb)}<br>Privacy scan ({pv_when or '-'}): {html.escape(pv)}</div>
<h2>Recent runs</h2>
<table><tr><th>Date</th><th>Run</th><th>Sources</th><th>Server pushback</th><th></th></tr>{recent or '<tr><td colspan=5>none yet</td></tr>'}</table>
<h2>Evaluations</h2>
<p>Kept private until the author has reviewed them; published with each report.</p>
"""
    return page("Run health - Internet Security Snapshot", body, "Built by snapshot.site from the run-reports branch.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["home", "check", "health"])
    ap.add_argument("--reports", type=Path, help="checkout of the run-reports branch (health)")
    ap.add_argument("--out", type=Path, default=SITE / "health" / "index.html")
    a = ap.parse_args(argv)
    if a.cmd == "home":
        (SITE / "index.html").write_text(home_html())
        print("wrote site/index.html")
        return 0
    if a.cmd == "check":
        ok = (SITE / "index.html").exists() and (SITE / "index.html").read_text() == home_html()
        print("site/index.html current" if ok else "site/index.html out of date (run: python -m snapshot.site home)")
        return 0 if ok else 1
    if not a.reports:
        ap.error("health needs --reports")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(health_html(a.reports))
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
