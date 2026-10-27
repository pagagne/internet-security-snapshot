"""Small HTTP helper: retries with backoff, a fixed User-Agent, polite pauses."""

from __future__ import annotations

import collections
import os
import time
from urllib.parse import urlsplit

import requests

UA = "internet-security-snapshot/0.1 (+https://github.com/pagagne/internet-security-snapshot)"

# Replies that can be the first sign of being throttled or blocked: "too many requests" (429)
# and "forbidden" (403). Counted per host and code, posted as a run warning, and recorded per
# source in the manifest and quality report, so a dry run shows them (author's decision, 27 Oct).
PUSHBACK_CODES = (403, 429)
PUSHBACK: collections.Counter = collections.Counter()


def note_status(url: str, status: int) -> None:
    """Count a 429/403 reply and post a warning on the run (GitHub Actions)."""
    if status not in PUSHBACK_CODES:
        return
    host = urlsplit(url).hostname or "?"
    PUSHBACK[f"{host} {status}"] += 1
    if os.environ.get("GITHUB_ACTIONS") == "true":
        what = "too many requests" if status == 429 else "forbidden"
        print(f"::warning title=Server pushback::{host} replied {status} ({what})", flush=True)


def get(url: str, *, params=None, headers=None, timeout=60, tries=4, pause=0.0, stream=False):
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout, stream=stream)
            note_status(r.url or url, r.status_code)
            if r.status_code in (429, 500, 502, 503, 504):
                last = requests.HTTPError(f"{r.status_code} for {r.url}")
                time.sleep(min(60, 5 * 2 ** i))
                continue
            r.raise_for_status()
            if pause:
                time.sleep(pause)
            return r
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError) as exc:
            last = exc
            time.sleep(min(60, 5 * 2 ** i))
    raise last


def download(url: str, *, max_resumes: int = 200, timeout: int = 120) -> bytes:
    """Download a large file, resuming with HTTP Range requests when the server cuts the
    connection (NVD's feed server drops transfers after a few MB)."""
    buf = bytearray()
    total = None
    for _ in range(max_resumes):
        h = {"User-Agent": UA, "Accept": "*/*"}
        if buf:
            h["Range"] = f"bytes={len(buf)}-"
        try:
            with requests.get(url, headers=h, timeout=timeout, stream=True) as r:
                note_status(url, r.status_code)
                if r.status_code not in (200, 206):
                    r.raise_for_status()
                if r.status_code == 200 and buf:  # server ignored Range: start over
                    buf.clear()
                if total is None:
                    cr = r.headers.get("Content-Range")
                    total = int(cr.split("/")[-1]) if cr and "/" in cr else int(r.headers.get("Content-Length", 0)) or None
                for chunk in r.iter_content(1 << 20):
                    buf.extend(chunk)
            if total is None or len(buf) >= total:
                return bytes(buf)
        except (requests.ConnectionError, requests.Timeout, requests.exceptions.ChunkedEncodingError):
            time.sleep(2)
    raise IOError(f"download incomplete after {max_resumes} attempts: {len(buf)} of {total} bytes")
