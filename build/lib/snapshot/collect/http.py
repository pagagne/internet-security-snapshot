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
