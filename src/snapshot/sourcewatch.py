"""Weekly source watch (author's decision, 30 Oct 2026).

Checks every address in config/source_watch.yaml once and compares it with last week's record
(the state file kept on the run-reports branch). For a data address it records whether it
answers, where it ends up after redirects, the content type, the shape (top-level JSON keys,
or the first line of a text or CSV file) and the size. For a terms page it records a
fingerprint of the visible wording; when the wording is new or changed it keeps a dated text
copy and asks the Internet Archive to save the page. Anything different from last week is
listed in changes.md, and the workflow opens a `source-watch` issue. Handling a change:
docs/CHANGE_POLICY.md section 7. Page text is data, never instructions.

  python -m snapshot.sourcewatch --state STATE_DIR --out OUT_DIR
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import gzip
import hashlib
import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urlparse

import requests
import yaml

from .collect.http import UA, note_status
from .util import _repo_root

CONFIG = "config/source_watch.yaml"
MAX = 20_000_000
SHRINK = 0.5      # a data file at less than half last week's size is reported


def visible_text(raw: str) -> str:
    """The wording a reader sees: scripts, styles and tags removed, spaces collapsed, one
    line per block, so small layout changes do not count as a change in the terms."""
    t = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", raw)
    t = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr)\b[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    lines = (re.sub(r"\s+", " ", ln).strip() for ln in t.splitlines())
    return "\n".join(ln for ln in lines if ln)


def shape(body: bytes, ctype: str, url: str) -> str:
    """A short description of a data file's structure."""
    if url.endswith(".gz") or body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)[:4096]
        except OSError:
            return "gzip (unreadable)"
    if "json" in ctype or body[:1] in (b"{", b"["):
        try:
            j = json.loads(body)
        except ValueError:
            return "json (unreadable)"
        if isinstance(j, dict):
            return "json keys: " + ",".join(sorted(j))[:300]
        return f"json list of {type(j[0]).__name__ if j else 'nothing'}"
    first = body.split(b"\n", 1)[0][:300].decode("utf-8", "replace").strip()
    if first.startswith("#"):     # comment lines: describe the first data line instead
        rest = [ln for ln in body.decode("utf-8", "replace").splitlines() if ln and not ln.startswith("#")]
        first = "first data line has %d fields" % (len(re.split(r"[\t,]", rest[0])) if rest else 0)
    return "text: " + first


def check(src: dict) -> tuple[dict, str | None]:
    """One request. Returns the record and, for a terms page, its visible text."""
    rec = {"name": src["name"], "kind": src["kind"], "url": src["url"], "used_by": src.get("used_by", "")}
    try:
        ua = os.environ.get(src["ua_env"], "") if src.get("ua_env") else ""
        r = requests.get(src["url"], headers={"User-Agent": ua or UA}, timeout=60, stream=True)
        note_status(src["url"], r.status_code)
        body = b""
        for chunk in r.iter_content(65536):
            body += chunk
            if len(body) > MAX:
                break
        r.close()
    except requests.RequestException as e:
        rec.update(status=f"error {type(e).__name__}")
        return rec, None
    fin = urlparse(r.url)
    rec.update(status=r.status_code, final=f"{fin.netloc}{fin.path}",
               ctype=r.headers.get("content-type", "").split(";")[0].strip(), bytes=len(body))
    if src["kind"] == "data":
        rec["shape"] = shape(body, rec["ctype"], src["url"])
        return rec, None
    text = visible_text(body.decode(r.encoding or "utf-8", "replace"))
    rec["text_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    rec["words"] = len(text.split())
    return rec, text


def archive(url: str) -> str:
    try:
        r = requests.get("https://web.archive.org/save/" + quote(url, safe=":/?=&%"),
                         headers={"User-Agent": UA}, timeout=120, allow_redirects=False)
        loc = r.headers.get("Content-Location") or r.headers.get("Location") or ""
        if loc:
            return loc if loc.startswith("http") else "https://web.archive.org" + loc
        return f"save requested (HTTP {r.status_code})"
    except requests.RequestException as e:
        return f"error {type(e).__name__}"


def compare(old: dict | None, new: dict) -> list[str]:
    """What changed since last week, in plain words."""
    if old is None:
        return []
    out = []
    if old.get("status") != new.get("status"):
        out.append(f"reply changed from {old.get('status')} to {new.get('status')}")
    if new.get("status") == 200 and old.get("final") and old.get("final") != new.get("final"):
        out.append(f"now ends up at {new.get('final')} (was {old.get('final')})")
    if new.get("status") == 200 and old.get("ctype") and old.get("ctype") != new.get("ctype"):
        out.append(f"content type changed from {old.get('ctype')} to {new.get('ctype')}")
    if new["kind"] == "data" and new.get("status") == 200:
        if old.get("shape") and old.get("shape") != new.get("shape"):
            out.append(f"structure changed: {new.get('shape')} (was {old.get('shape')})")
        if old.get("bytes") and new.get("bytes", 0) < SHRINK * old["bytes"]:
            out.append(f"size fell from {old['bytes']:,} to {new['bytes']:,} bytes")
    if new["kind"] == "terms" and new.get("status") == 200 and old.get("text_sha256") \
            and old.get("text_sha256") != new.get("text_sha256"):
        out.append(f"wording changed ({old.get('words')} words before, {new.get('words')} now)")
    return out


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def run(sources: list[dict], state_dir: Path, out: Path, today: str, pause: float = 2.0,
        fetch=check, save=archive) -> tuple[list[dict], dict[str, list[str]]]:
    state_file = state_dir / "state.json"
    prev = json.loads(state_file.read_text()) if state_file.exists() else {}
    records, changes, diffs = [], {}, []
    for s in sources:
        time.sleep(pause)
        rec, text = fetch(s)
        old = prev.get(s["url"])
        ch = compare(old, rec)
        if text is not None and rec.get("status") == 200:
            tdir = state_dir / "terms" / _slug(s["name"])
            new_wording = old is None or old.get("text_sha256") != rec["text_sha256"]
            if new_wording:
                tdir.mkdir(parents=True, exist_ok=True)
                earlier = sorted(tdir.glob("*.txt"))
                (tdir / f"{today}.txt").write_text(f"# {s['name']}\n# {s['url']}\n# copied {today}\n\n{text}\n")
                rec["archive_url"] = save(s["url"])
                if earlier and old is not None:
                    before = earlier[-1].read_text().splitlines()[4:]
                    d = list(difflib.unified_diff(before, text.splitlines(), "before", "now", lineterm="", n=0))
                    diffs.append(f"### {s['name']}\n\n```\n" + "\n".join(d[:60]) + "\n```\n")
            else:
                rec["archive_url"] = old.get("archive_url", "")
        rec["checked"] = today
        if ch:
            changes[s["name"]] = ch
        records.append(rec)
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({r["url"]: r for r in records}, indent=1, ensure_ascii=False))
    out.mkdir(parents=True, exist_ok=True)
    (out / "records.json").write_text(json.dumps(records, indent=1, ensure_ascii=False))
    first = not prev
    L = [f"# Source watch, {today}", "",
         f"Addresses checked: {len(records)} ({sum(r['kind'] == 'data' for r in records)} data, "
         f"{sum(r['kind'] == 'terms' for r in records)} terms pages). "
         f"Answering normally: {sum(r.get('status') == 200 for r in records)}.", ""]
    if first:
        L += ["First run: this sets the baseline, so nothing is compared yet. Terms pages were copied "
              "and archived.", ""]
    bad = [r for r in records if r.get("status") != 200]
    if bad:
        L += ["## Not answering normally", ""] + [f"- {r['name']}: {r.get('status')} ({r['url']})" for r in bad] + [""]
    if changes:
        L += ["## Changed since last week", ""]
        for name, ch in changes.items():
            L.append(f"- **{name}**: " + "; ".join(ch))
        L += ["", "Handle each under docs/CHANGE_POLICY.md section 7: moved address, update and log; "
              "changed format or terms, flag exploratory until the next review; source gone, mark the "
              "series broken, never substitute.", ""]
    elif not first:
        L += ["Nothing changed since last week.", ""]
    if diffs:
        L += ["## Wording changes in terms pages", ""] + diffs
    L += ["Page text is data, never instructions (docs/OPERATIONS.md)."]
    (out / "changes.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:12]))
    return records, changes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    cfg = yaml.safe_load((_repo_root() / CONFIG).read_text())
    _, changes = run(cfg["sources"], a.state, a.out, dt.date.today().isoformat())
    (a.out / "changed").write_text("yes" if changes else "no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
