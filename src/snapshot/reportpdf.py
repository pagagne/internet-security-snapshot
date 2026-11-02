"""PDF archive copy of each report page (author's decision, 1 Nov 2026).

Every run that makes a report page also makes a PDF of it beside the page (reports/<key>.pdf),
with a cover line saying SIMULATION, provisional or final and when it was built. Test runs
make one too, so the whole flow is tested. A permanent citation link (OSF or Zenodo) is added
for real reports only, from the pilot on; simulations never get one.

The report pages are written by snapshot.reportpage in a small, fixed Markdown subset, so this
module converts that subset itself (no extra dependency) and prints the page with headless
Chrome, which GitHub's Ubuntu runners include. If no Chrome is found the PDF is skipped with a
notice; the report page itself is unaffected.

    python -m snapshot.reportpdf REPORT.md        # writes REPORT.pdf beside it
"""
from __future__ import annotations

import base64
import datetime as dt
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CSS = """
@page { size: Letter; margin: 18mm 16mm 18mm 16mm; }
body { font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1f2328; }
h1 { font-size: 18pt; margin: 0 0 8pt; } h2 { font-size: 13pt; margin: 16pt 0 6pt; border-bottom: 1px solid #d8dee4; padding-bottom: 3pt; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.5pt; break-inside: avoid; }
td, th { border: 1px solid #d0d7de; padding: 4pt 6pt; text-align: left; vertical-align: top; } th { background: #f6f8fa; }
blockquote { border-left: 3px solid #BA7517; margin: 6pt 0; padding: 2pt 10pt; color: #444; background: #fdf6ec; }
img { max-width: 100%; break-inside: avoid; display: block; margin: 6pt auto; }
.cover { border: 1px solid #d0d7de; padding: 6pt 10pt; margin-bottom: 10pt; font-size: 9pt; color: #444; }
.sim { color: #BA7517; font-weight: bold; }
sub { font-size: 7.5pt; vertical-align: baseline; } h3 { font-size: 11pt; margin: 10pt 0 4pt; } h4 { font-size: 10pt; margin: 8pt 0 3pt; }
"""


def _inline(s: str, base: Path) -> str:
    s = html.escape(s, quote=False).replace("&lt;sub&gt;", "<sub>").replace("&lt;/sub&gt;", "</sub>")
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: _img(m[2], m[1], base), s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _img(src: str, alt: str, base: Path) -> str:
    p = base / html.unescape(src)
    if p.exists():
        src = "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return f'<img src="{src}" alt="{alt}">'


def md_to_html(text: str, base: Path) -> str:
    """The Markdown subset of snapshot.reportpage: headings, paragraphs, lists, tables,
    block quotes, images, links, bold, italics, code."""
    out, para, i = [], [], 0
    lines = text.split("\n")

    def flush():
        if para:
            out.append("<p>" + _inline(" ".join(para), base) + "</p>")
            para.clear()
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush(); i += 1; continue
        if m := re.match(r"^(#{1,4}) (.*)", ln):
            flush(); n = len(m[1]); out.append(f"<h{n}>{_inline(m[2], base)}</h{n}>"); i += 1; continue
        if ln.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            out.append("<table><tr>" + "".join(f"<th>{_inline(c, base)}</th>" for c in head) + "</tr>"
                       + "".join("<tr>" + "".join(f"<td>{_inline(c, base)}</td>" for c in r) + "</tr>" for r in body)
                       + "</table>")
            continue
        if ln.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i].lstrip("> ").rstrip()); i += 1
            out.append("<blockquote>" + _inline(" ".join(q), base) + "</blockquote>"); continue
        if re.match(r"^\s*- ", ln):
            flush(); items = []
            while i < len(lines) and re.match(r"^\s*- ", lines[i]):
                items.append(re.sub(r"^\s*- ", "", lines[i])); i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x, base)}</li>" for x in items) + "</ul>"); continue
        para.append(ln.strip()); i += 1
    flush()
    return "\n".join(out)


def chrome() -> str | None:
    for c in (os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if c and (shutil.which(c) or Path(c).exists()):
            return shutil.which(c) or c
    return None


def make(md_path: Path, now: dt.datetime | None = None, label: str | None = None) -> Path | None:
    text = md_path.read_text()
    status = label or ("SIMULATION" if "SIMULATION" in text.split("\n", 1)[0] else
                       "Provisional" if "(provisional)" in text.split("\n", 1)[0] else "Final")
    now = now or dt.datetime.now(dt.timezone.utc)
    cover = (f'<div class="cover"><span class="{"sim" if status == "SIMULATION" else ""}">{status}</span> · '
             f"Internet Security Snapshot · archive copy of {md_path.name} · built {now:%d %b %Y %H:%M} UTC"
             + (" · not for citation" if status == "SIMULATION" else "") + "</div>")
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{md_path.stem}</title><style>{CSS}</style></head>"
           f"<body>{cover}{md_to_html(text, md_path.parent)}</body></html>")
    exe = chrome()
    if not exe:
        print(f"::notice::No Chrome found; PDF of {md_path.name} skipped")
        return None
    pdf = md_path.with_suffix(".pdf")
    with tempfile.TemporaryDirectory() as tmp:
        h = Path(tmp) / "report.html"
        h.write_text(doc)
        subprocess.run([exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", h.as_uri()], check=True, capture_output=True, timeout=120)
    return pdf


def make_if_changed(md_path: Path, label: str | None = None) -> Path | None:
    """PDF only when the text changed since the last one (a .sha file beside the PDF), so private
    rebuilds do not re-commit unchanged PDFs (session logs, author's decision 1 Nov 2026)."""
    import hashlib
    sha = hashlib.sha256(md_path.read_bytes()).hexdigest()
    mark = md_path.with_suffix(".pdf.sha")
    if mark.exists() and mark.read_text().strip() == sha and md_path.with_suffix(".pdf").exists():
        return None
    out = make(md_path, label=label)
    if out:
        mark.write_text(sha + "\n")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--label", help="cover label, e.g. 'Session log (private)'")
    ap.add_argument("--changed-only", action="store_true", help="skip files whose PDF is current")
    a = ap.parse_args()
    for f in a.files:
        out = make_if_changed(f, a.label) if a.changed_only else make(f, label=a.label)
        if out:
            print(out)
