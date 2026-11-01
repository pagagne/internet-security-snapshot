"""Practice evaluation on a frozen quarterly bundle (author's decision, 1 Nov 2026).

Runs the registered core measures on one quarter's frozen data, the way the quarterly report
will, to test the evaluation method before the 1 Dec and 15 Dec dry runs. **Practice only:**
Q3 2026 is outside the registered study (the Q4 2026 pilot comes first; Q1 2027 is the first
scored quarter), fix dates are the automatic pre-fill without the author's hand check, and no
direction label is given (a label needs four earlier quarters). Results are private (saved to
the private repository like every exploratory task) and are judged only on whether the method
works, not on the figures, so they cannot sway the 21 Dec core-freeze decisions.

Computes what the free sources allow today:
  I2  days from publication (T0) to first exploitation, CVEs first exploited in the quarter
  I3  the race, option (a): days from the fix to first exploitation, every CVE first added to
      CISA KEV in the quarter (median, 90% bootstrap interval, bounds)
  I5  year-over-year growth in published CVE records (rejected excluded)
  I7  ransomware postings (aggregates) and SEC 8-K Item 1.05 filings (per 1,000 registrants
      when the SEC company list can be read)
  I8  AI-credited share as a range (floor, headline, ceiling)
and lists I1, I4 and I6 as not computable (they need Shadowserver or VulnCheck).

    python -m snapshot.research.practice_eval --bundle DIR --out DIR
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import pandas as pd

from ..events import build_events
from ..fixdates import prefill_exploited
from ..race import t1_kev_race, t3_time_to_exploit
from ..t7 import t7_range
from ..util import Quarter


def _find_bundle(root: Path) -> Path:
    hits = sorted(root.rglob("manifest.json"))
    if not hits:
        raise SystemExit(f"no manifest.json under {root}")
    return hits[0].parent


def _utc(s):
    return pd.to_datetime(s, utc=True, errors="coerce")


def _fmt(v):
    if isinstance(v, float):
        return f"{v:,.1f}"
    if isinstance(v, (tuple, list)):
        return "(" + ", ".join(_fmt(x) if x is not None else "-" for x in v) + ")"
    return f"{v:,}" if isinstance(v, int) else str(v)


def registrants() -> int | None:
    ua = os.environ.get("SEC_USER_AGENT", "")
    if not ua:
        return None
    import requests
    try:
        r = requests.get("https://www.sec.gov/files/company_tickers.json", headers={"User-Agent": ua}, timeout=60)
        return len({v["cik_str"] for v in r.json().values()}) if r.ok else None
    except Exception:  # noqa: BLE001
        return None


def evaluate(bundle: Path, pause: float = 0.3, nvd=None) -> tuple[dict, pd.DataFrame]:
    man = json.loads((bundle / "manifest.json").read_text())
    q = Quarter.parse(man["quarter"])
    qs, qe = pd.Timestamp(q.start), pd.Timestamp(q.end)
    cve = pd.read_parquet(bundle / "cve/cve_records.parquet")
    kev = pd.read_parquet(bundle / "kev/kev_entries.parquet")
    cve["pub"] = _utc(cve["date_published"]).dt.tz_localize(None)
    kev["added"] = _utc(kev["date_added"]).dt.tz_localize(None)
    R: dict = {"quarter": str(q), "run": man["run"]}

    # I5: published CVE records per quarter, same quarter in earlier years
    pubd = cve[cve["state"] == "PUBLISHED"]
    def count(year):
        s, e = qs.replace(year=year), qe.replace(year=year) + pd.Timedelta(days=1)
        return int(((pubd["pub"] >= s) & (pubd["pub"] < e)).sum())
    yrs = {y: count(y) for y in range(qs.year - 3, qs.year + 1)}
    R["I5"] = {"published_by_year": yrs,
               "yoy_growth_pct": round(100 * (yrs[qs.year] / yrs[qs.year - 1] - 1), 1) if yrs.get(qs.year - 1) else None}
    # Cross-checks of the count (author, 1 Nov 2026): NVD's own count for the same windows, and
    # whole calendar years, which published reviews quote (e.g. 2024 and 2025 totals)
    from .. import quality
    _, R["I5_count_check"] = quality.count_check(cve, q, nvd=nvd or quality.nvd_published_count)
    R["I5_calendar_years"] = {y: int(((pubd["pub"] >= pd.Timestamp(f"{y}-01-01")) & (pubd["pub"] < pd.Timestamp(f"{y + 1}-01-01"))).sum())
                              for y in range(qs.year - 3, qs.year)}

    # I8: AI-credited share (range)
    qc = pubd[(pubd["pub"] >= qs) & (pubd["pub"] < qe + pd.Timedelta(days=1))]
    R["I8"] = t7_range(qc)

    # I2 and I3: CVEs first added to CISA KEV in the quarter, with pre-filled fix dates
    kq = kev[(kev["added"] >= qs) & (kev["added"] < qe + pd.Timedelta(days=1))]
    sub = cve[cve["cve_id"].isin(set(kq["cve_id"]))].drop(columns=["pub"])
    vend = dict(zip(kq["cve_id"], kq["vendor"]))
    prefills, sources = {}, {}
    for r in sub.itertuples():
        lst = lambda x: [] if x is None else list(x)
        refs = lst(getattr(r, "fix_links", None)) + lst(getattr(r, "ref_links", None))
        pub = str(r.date_published)[:10] if pd.notna(r.date_published) else ""
        d, src, hand = prefill_exploited(r.cve_id, refs, vend.get(r.cve_id, ""), pub or "")
        prefills[r.cve_id] = (d, src, hand)
        sources[r.cve_id] = "assumed" if src.upper().startswith("ASSUMED") else src.split(" ")[0]
        time.sleep(pause)
    ev = build_events(sub, kq.rename(columns={"date_added": "date_added"}), prefills=prefills)
    for c in ("t0", "t_patch", "t_exploit", "t_kev", "fix_lo", "fix_hi", "exploit_hi"):
        ev[c] = pd.to_datetime(ev[c], errors="coerce")
    ev["prefill_source"] = ev["cve_id"].map(sources)
    R["kev_added_in_quarter"] = int(len(kq))
    R["prefill_assumed"] = int(sum(v == "assumed" for v in sources.values()))
    R["I3"] = t1_kev_race(ev, qs, qe)
    R["I2"] = t3_time_to_exploit(ev, qs, qe)

    # I7: ransomware postings and SEC 8-K Item 1.05 filings
    rw_path = bundle / "ransomware/ransomware_counts.parquet"
    if rw_path.exists():
        rw = pd.read_parquet(rw_path)
        tot = rw[rw["dimension"] == "all"]
        R["I7a_ransomware_postings"] = {m: int(c) for m, c in zip(tot["month"], tot["count"])}
    sec_path = bundle / "sec/sec_8k_item105.parquet"
    if sec_path.exists():
        sec = pd.read_parquet(sec_path).drop_duplicates("accession")
        sec["fd"] = pd.to_datetime(sec["file_date"], errors="coerce")
        n8k = int(((sec["fd"] >= qs) & (sec["fd"] <= qe)).sum())
        reg = registrants()
        R["I7b_sec_8k_item105"] = {"filings": n8k, "registrants": reg,
                                   "per_1000": round(1000 * n8k / reg, 3) if reg else None}
    R["not_computable"] = {"I1": "exposure half-life needs Shadowserver scan data (awaiting permission)",
                           "I4": "share of attacks on old flaws needs Shadowserver honeypot data (awaiting permission)",
                           "I6": "agreement between exploited lists needs VulnCheck and Shadowserver (awaiting permission)"}
    return R, ev


def report(R: dict) -> str:
    L = [f"# Practice evaluation: {R['quarter']} ({R['run']} run)", "",
         "> **Practice, not a result.** This quarter is outside the registered study; fix dates are the "
         "automatic pre-fill without the author's hand check; no direction labels (they need four earlier "
         "quarters). Judged only on whether the method works (author's decision, 1 Nov 2026).", "",
         "## Method check", "",
         f"- CVEs first added to CISA KEV in the quarter: {R['kev_added_in_quarter']}; fix date only assumed "
         f"(no source found): {R['prefill_assumed']}.", ""]
    for key, title in (("I2", "I2. Days from publication to first exploitation"),
                       ("I3", "I3. The race: days from the fix to first exploitation (option a)"),
                       ("I5", "I5. Growth in published CVE records"),
                       ("I5_count_check", "I5 check: our counts against NVD's"),
                       ("I5_calendar_years", "I5 check: whole calendar years (compare with published reviews)"),
                       ("I8", "I8. AI-credited share (range)")):
        L += [f"## {title}", ""] + [f"- {k}: {_fmt(v)}" for k, v in R[key].items()] + ["", "Label: not given (needs four earlier quarters).", ""]
    L += ["## I7. Breaches and ransomware", ""]
    if "I7a_ransomware_postings" in R:
        L.append("- Ransomware postings by month (ransomware.live, aggregates): " + ", ".join(
            f"{m} {_fmt(c)}" for m, c in R["I7a_ransomware_postings"].items()))
    if "I7b_sec_8k_item105" in R:
        L.append("- SEC 8-K Item 1.05 filings: " + ", ".join(f"{k} {_fmt(v)}" for k, v in R["I7b_sec_8k_item105"].items()))
    L += ["", "Label: not given.", "", "## Not computable yet", ""] + [f"- {k}: {v}" for k, v in R["not_computable"].items()]
    L += ["", "Files: `practice_eval.json` (all figures), `events.csv` (one row per CVE first added to KEV, "
          "with event dates and the pre-fill source: the worksheet input for I2 and I3)."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")      # unused; kept for the Research workflow
    ap.add_argument("--bundle", type=Path, default=Path(os.environ.get("PRACTICE_BUNDLE", "practice-bundle")))
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    R, ev = evaluate(_find_bundle(a.bundle))
    (a.out / "practice_eval.json").write_text(json.dumps(R, indent=1, default=str))
    ev.to_csv(a.out / "events.csv", index=False)
    (a.out / "summary.md").write_text(report(R))
    print(f"practice evaluation {R['quarter']}: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
