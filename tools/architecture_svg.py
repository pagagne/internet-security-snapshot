"""Draws the architecture diagram in the column format (Free sources | Pull | Store |
Process | Publish). One spec, two outputs: docs/diagrams/architecture.svg for GitHub
(fixed colours) and, with --widget, the module for the Claude Docs copy (theme tokens).
Edit the spec below, then run: python tools/architecture_svg.py
"""
import sys

W, H = 760, 536
TITLE = "Every number follows one path from free sources to publication"
COLS = {"src": (16, 164), "pull": (198, 112), "store": (326, 112), "proc": (456, 124), "pub": (598, 146)}
HEAD_Y = 62
HEADERS = [("h-sources", "src", "Free sources"), ("h-pull", "pull", "Pull"), ("h-store", "store", "Store"),
           ("h-process", "proc", "Process"), ("h-publish", "pub", "Publish")]
# (id, column, y, height, kind, [(text-id, words, bold)])   kind: box | pending | hand
BOXES = [
    ("git", "src", 76, 44, "box", [("git-1", "Git histories: CVE,", 0), ("git-2", "KEV, Vulnrichment", 0)]),
    ("epss", "src", 130, 44, "box", [("epss-1", "EPSS daily archive,", 0), ("epss-2", "NVD, vendor advisories", 0)]),
    ("sec", "src", 184, 44, "box", [("sec-1", "Harm: SEC 8-K", 0), ("sec-2", "breach filings", 0)]),
    ("radar", "src", 238, 30, "box", [("radar-1", "Cloudflare Radar", 0)]),
    ("shadow", "src", 300, 58, "pending", [("shadow-1", "Shadowserver: exposure", 0), ("shadow-2", "series, honeypot stats", 0), ("shadow-3", "hoped for by 1 Jan 2027", 0)]),
    ("vulncheck", "src", 368, 58, "pending", [("vc-1", "VulnCheck KEV", 0), ("vc-2", "(community tier)", 0), ("vc-3", "hoped for by 1 Jan 2027", 0)]),
    ("ransom", "src", 436, 58, "pending", [("rl-1", "Harm: ransomware.live", 0), ("rl-2", "leak-site post counts", 0), ("rl-3", "hoped for by 1 Jan 2027", 0)]),
    ("pull", "pull", 76, 418, "box", [("pull-1", "Quarterly pull", 1), ("pull-2", "GitHub Actions,", 0), ("pull-3", "1 Jan, Apr,", 0), ("pull-4", "Jul, Oct", 0), ("pull-5", "", 0), ("pull-6", "final re-run", 0), ("pull-7", "one month later", 0)]),
    ("store", "store", 76, 296, "box", [("store-1", "Frozen bundles", 1), ("store-2", "repo releases", 0), ("store-3", "+ Zenodo;", 0), ("store-4", "git pinned", 0), ("store-5", "by commit", 0)]),
    ("private", "store", 382, 112, "box", [("pv-1", "Private backup", 1), ("pv-2", "author's Drive:", 0), ("pv-3", "full data, incl.", 0), ("pv-4", "not yet", 0), ("pv-5", "publishable", 0)]),
    ("normalize", "proc", 76, 96, "box", [("norm-1", "Normalize", 1), ("norm-2", "data checks,", 0), ("norm-3", "cohort rule", 0)]),
    ("analysis", "proc", 196, 160, "box", [("ana-1", "Analysis", 1), ("ana-2", "timing, baselines,", 0), ("ana-3", "uncertainty ranges", 0), ("ana-4", "", 0), ("ana-5", "Claude drafts,", 0), ("ana-6", "author approves", 0)]),
    ("hand", "proc", 380, 114, "hand", [("hand-1", "Hand Check app", 1), ("hand-2", "author's checks:", 0), ("hand-3", "fix dates,", 0), ("hand-4", "AI credits", 0)]),
    ("evalpage", "pub", 76, 92, "box", [("ev-1", "Evaluation page", 1), ("ev-2", "provisional,", 0), ("ev-3", "then final", 0)]),
    ("archive", "pub", 184, 92, "box", [("ar-1", "Quarter archive", 1), ("ar-2", "quarter-by-quarter", 0), ("ar-3", "index", 0)]),
    ("timelines", "pub", 292, 92, "box", [("tl-1", "Cohort timelines", 1), ("tl-2", "up to 12 flaws", 0), ("tl-3", "a quarter", 0)]),
    ("zenodo", "pub", 400, 94, "box", [("zb-1", "Zenodo bundle", 1), ("zb-2", "data + code, DOI", 0)]),
]
NOTES = [("await", 16, 291, "Awaiting permission"),
         ("key", 16, 522, "Dashed: sources awaiting permission (asked 20 Oct 2026, follow-up 20 Nov). Highlighted: the author's hand checks.")]


def geom(col, y, h):
    x, w = COLS[col]
    return x, y, w, h


def mid(b):
    _, col, y, h, *_ = b
    x, w = COLS[col]
    return x + w / 2, y + h / 2


def by(i):
    return next(b for b in BOXES if b[0] == i)


def arrows():
    a = []
    px = COLS["pull"][0]
    for b in BOXES:
        if b[1] == "src":
            x, y, w, h = geom(b[1], b[2], b[3])
            a.append((f"M{x + w} {y + h / 2}H{px - 2}", b[4] == "pending"))
    a.append((f"M{COLS['pull'][0] + COLS['pull'][1]} 224H{COLS['store'][0] - 2}", False))
    pv = by("private")
    a.append((f"M{COLS['pull'][0] + COLS['pull'][1]} {pv[2] + pv[3] / 2}H{COLS['store'][0] - 2}", False))
    n = by("normalize")
    a.append((f"M{COLS['store'][0] + COLS['store'][1]} {n[2] + n[3] / 2}H{COLS['proc'][0] - 2}", False))
    cx = COLS["proc"][0] + COLS["proc"][1] / 2
    an, hd = by("analysis"), by("hand")
    a.append((f"M{cx} {n[2] + n[3]}V{an[2] - 2}", False))
    a.append((f"M{cx} {hd[2]}V{an[2] + an[3] + 2}", False))
    bus = COLS["proc"][0] + COLS["proc"][1] + 9
    a.append((f"M{COLS['proc'][0] + COLS['proc'][1]} {an[2] + an[3] / 2}H{bus}", False))
    pubs = [b for b in BOXES if b[1] == "pub"]
    ys = [b[2] + b[3] / 2 for b in pubs]
    a.append((f"M{bus} {min(ys)}V{max(ys)}", None))
    for y in ys:
        a.append((f"M{bus} {y}H{COLS['pub'][0] - 2}", False))
    return a


def text_lines(b):
    _, col, y, h, kind, lines = b
    x, w = COLS[col]
    lines = [l for l in lines]
    n = len(lines)
    top = y + h / 2 - (n * 16) / 2 + 12
    out = []
    for i, (tid, words, bold) in enumerate(lines):
        if not words:
            continue
        out.append((tid, x + w / 2, top + 16 * i, words, bold, kind))
    return out


def render(widget):
    if widget:
        ink, quiet, edge, boxfill = "var(--cds-text-primary)", "var(--cds-text-secondary)", "var(--cds-chart-axis)", "var(--cds-chart-reference-tint)"
        hand_fill, hand_edge = "var(--cds-chart-categorical-1)", "var(--cds-chart-categorical-1)"
    else:
        ink, quiet, edge, boxfill = "#222222", "#666666", "#a8a89e", "#f4f4f2"
        hand_fill, hand_edge = "#fff4d6", "#b8860b"
    tid = (lambda t: f" data-claude-text-id='{t}'") if widget else (lambda t: "")
    anc = (lambda t: f" data-claude-anchor='{t}'") if widget else (lambda t: "")
    fs = "fontSize" if widget else "font-size"
    fw = "fontWeight" if widget else "font-weight"
    ta = "textAnchor" if widget else "text-anchor"
    sw = "strokeWidth" if widget else "stroke-width"
    sd = "strokeDasharray" if widget else "stroke-dasharray"
    fo = "fillOpacity" if widget else "fill-opacity"
    me = "markerEnd" if widget else "marker-end"
    p = []
    head = f"<svg viewBox='0 0 {W} {H}' role='img' aria-label='{TITLE}' {fs}='11.5'" + ("" if widget else " xmlns='http://www.w3.org/2000/svg' font-family='Helvetica, Arial, sans-serif'") + ">"
    p.append(head)
    p.append(f"<defs><marker id='arch-arrow' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' fill='{edge}'/></marker></defs>")
    if not widget:
        p.append(f"<rect width='{W}' height='{H}' fill='#ffffff'/>")
    p.append(f"<text{tid('title')} x='16' y='28' {fs}='15' {fw}='600' fill='{ink}'>{TITLE}</text>")
    for t, col, words in HEADERS:
        x, w = COLS[col]
        p.append(f"<text{tid(t)} x='{x + w / 2:g}' y='{HEAD_Y}' {ta}='middle' {fs}='13' {fw}='600' fill='{ink}'>{words}</text>")
    p.append(f"<g{anc('connectors')} fill='none' stroke='{edge}' {sw}='1.25'>")
    for d, dashed in arrows():
        mark = "" if dashed is None else f" {me}='url(#arch-arrow)'"
        p.append(f"<path d='{d}'{mark}" + (f" {sd}='4 3'" if dashed else "") + "/>")
    p.append("</g>")
    for b in BOXES:
        x, y, w, h = geom(b[1], b[2], b[3])
        kind = b[4]
        p.append(f"<g{anc(b[0])}>")
        if kind == "box":
            p.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='{boxfill}' stroke='{edge}' {sw}='1'/>")
        elif kind == "pending":
            p.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='none' stroke='{edge}' {sw}='1' {sd}='4 3'/>")
        else:
            p.append(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='{hand_fill}'" + (f" {fo}='0.12'" if widget else "") + f" stroke='{hand_edge}' {sw}='1.5'/>")
        for t, tx, ty, words, bold, k in text_lines(b):
            colr = quiet if k == "pending" else ink
            style = f" {fw}='600' {fs}='12.5'" if bold else ""
            if k == "pending" and words.startswith("hoped"):
                style = f" {fs}='10.5' font-style='italic'" if not widget else f" {fs}='10.5' fontStyle='italic'"
            p.append(f"<text{tid(t)} x='{tx:g}' y='{ty:g}' {ta}='middle' fill='{colr}'{style}>{words}</text>")
        p.append("</g>")
    for t, x, y, words in NOTES:
        p.append(f"<text{tid(t)} x='{x}' y='{y}' {fs}='10.5' fill='{quiet}'>{words}</text>")
    p.append("</svg>")
    return "".join(p)


if __name__ == "__main__":
    if "--widget" in sys.argv:
        print("export default () => " + render(True) + ";")
    else:
        open("docs/diagrams/architecture.svg", "w").write(render(False) + "\n")
        print("wrote docs/diagrams/architecture.svg")
