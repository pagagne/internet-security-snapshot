"""Makes the PDF of "The Snapshot" from docs/manual/THE_SNAPSHOT.md (29 Oct 2026).

Run by Claude after `python -m snapshot.manual build`; needs the `markdown` package and Python
Playwright with Chromium. The PDF is not kept in the repository: it goes to the author's Drive
and the chat. With --private, the given Markdown file (built outside the repository from the
Claude project's private documents) is added as Appendix C, for the private edition only.

  python tools/manual_pdf.py OUT.pdf [--private PRIVATE.md] [--edition "Public edition"]
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/manual/THE_SNAPSHOT.md"

CSS = """
@page { size: Letter; margin: 0.75in 0.75in 0.85in; }
body { font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1d1d1d; }
h1 { color: #1f4e79; font-size: 22pt; break-before: page; margin: 0 0 10pt; }
body > h1:first-child { break-before: avoid; }
h1.part { font-size: 26pt; border-bottom: 3px solid #1f4e79; padding-bottom: 6pt; }
h2 { color: #1f4e79; font-size: 15pt; break-before: page; margin: 0 0 4pt; }
h3 { color: #1f4e79; font-size: 12pt; margin: 14pt 0 4pt; break-after: avoid; }
h4, h5, h6 { color: #2d5f8f; font-size: 10.5pt; margin: 10pt 0 3pt; break-after: avoid; }
.src { color: #666; font-size: 8pt; margin-bottom: 10pt; }
table { border-collapse: collapse; width: 100%; font-size: 7.5pt; margin: 6pt 0; }
th { background: #1f4e79; color: #fff; text-align: left; padding: 3pt; }
td { border-bottom: 1px solid #ddd; padding: 3pt; vertical-align: top; }
tr { break-inside: avoid; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8pt; background: #f1f4f7; padding: 0 2pt; }
pre { background: #f1f4f7; padding: 6pt; font-size: 7.5pt; white-space: pre-wrap; break-inside: avoid; }
pre code { background: none; }
img { max-width: 100%; }
a { color: #1f4e79; text-decoration: none; }
.toc ul { list-style: none; padding-left: 12pt; } .toc > ul { padding-left: 0; }
.toc li { margin: 2pt 0; } .toc > ul > li { margin-top: 8pt; font-weight: bold; }
.toc > ul > li li { font-weight: normal; }
"""


def build(out: Path, private: Path | None, edition: str) -> None:
    text = SRC.read_text()
    if private:
        text = text.rstrip() + "\n\n" + private.read_text()
    # split off the generated front matter (title, note, contents) and make our own cover
    body = text.split("\n## Contents\n", 1)[1]
    toc_md, rest = body.split("\n# ", 1)
    rest = "# " + rest
    if private:
        toc_md += "\n- **Appendix C. Private material (private edition only)**\n"
    html_body = markdown.markdown(rest, extensions=["tables", "fenced_code", "md_in_html"])
    html_body = re.sub(r"<h1>(Part [IVX]+\.|Appendix [A-C]\.)", r'<h1 class="part">\1', html_body)
    html_body = re.sub(r"(<h2>.*?</h2>\s*)<p><em>Source: (.*?)</em></p>", r'\1<p class="src">Source: \2</p>', html_body)
    html_body = html_body.replace('src="../../', f'src="file://{ROOT}/')
    toc = markdown.markdown(toc_md)
    today = dt.date.today().strftime("%-d %B %Y")
    html = (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<h1>Contents</h1><div class='toc'>{toc}</div>{html_body}</body></html>")
    tmp = out.with_suffix(".html")
    tmp.write_text(html)
    foot = (f'<div style="font-size:7px;width:100%;text-align:center;color:#888">The Snapshot · {edition} · '
            'Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto(f"file://{tmp}")
        page.pdf(path=str(out), format="Letter", print_background=True, display_header_footer=True,
                 header_template="<span></span>", footer_template=foot, outline=True, tagged=True,
                 margin={"top": "0.75in", "bottom": "0.85in", "left": "0.75in", "right": "0.75in"})
        b.close()
    tmp.unlink()
    add_cover(out, edition, today)


COVER_IMG = ROOT / "docs/manual/cover.jpg"   # the author's cover image (made with ChatGPT, 29 Oct 2026)


def add_cover(out: Path, edition: str, today: str) -> None:
    """A full-bleed cover page (no page number) in front of the body PDF."""
    from pypdf import PdfReader, PdfWriter
    html = f"""<html><head><meta charset='utf-8'><style>
@page {{ size: Letter; margin: 0; }}
html, body {{ margin: 0; height: 11in; width: 8.5in; }}
body {{ background: #012c62 url('file://{COVER_IMG}') center 0% / cover no-repeat;
       font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; color: #e8f4ff; position: relative; }}
.band {{ position: absolute; left: 0; right: 0; bottom: 0; padding: 0.35in 0 0.6in; text-align: center;
         background: linear-gradient(to bottom, rgba(1,30,70,0), rgba(1,30,70,0.85) 35%, rgba(1,30,70,0.95)); }}
.t {{ font-size: 34pt; font-weight: bold; letter-spacing: 1pt; color: #ffffff; }}
.s {{ font-size: 14pt; color: #8fd0ff; margin: 4pt 0 14pt; }}
.m {{ font-size: 10pt; line-height: 1.6; color: #cfe6ff; }}
.e {{ display: inline-block; margin-top: 10pt; padding: 3pt 10pt; border: 1px solid #8fd0ff;
      border-radius: 3pt; font-size: 9.5pt; letter-spacing: 0.5pt; }}
</style></head><body><div class="band">
<div class="t">THE SNAPSHOT</div><div class="s">The Internet Security Snapshot study manual</div>
<div class="m">Paul A. Gagne, independent researcher<br/>Built {today} from
github.com/pagagne/internet-security-snapshot<br/>Pre-registration: doi.org/10.17605/OSF.IO/3XT82</div>
<div class="e">{edition.upper()}</div></div></body></html>"""
    cov_html, cov_pdf = out.with_suffix(".cover.html"), out.with_suffix(".cover.pdf")
    cov_html.write_text(html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        page.goto(f"file://{cov_html}")
        page.pdf(path=str(cov_pdf), format="Letter", print_background=True,
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    w = PdfWriter()
    w.append(str(cov_pdf), pages=(0, 1))
    w.append(str(out))
    w.write(str(out))
    cov_html.unlink(); cov_pdf.unlink()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--private", type=Path)
    ap.add_argument("--edition", default="Public edition")
    a = ap.parse_args()
    build(a.out, a.private, a.edition)
    print(a.out)
