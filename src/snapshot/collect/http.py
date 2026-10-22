"""Small HTTP helper: retries with backoff, a fixed User-Agent, polite pauses."""

from __future__ import annotations

import time

import requests

UA = "internet-security-snapshot/0.1 (+https://github.com/pagagne/internet-security-snapshot)"


def get(url: str, *, params=None, headers=None, timeout=60, tries=4, pause=0.0, stream=False):
    h = {"User-Agent": UA, "Accept": "application/json"}
    h.update(headers or {})
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout, stream=stream)
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
