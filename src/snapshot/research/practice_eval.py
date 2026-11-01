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
from .prefill_coverage import CVE_RAW, bucket


def _cve_record(cve_id: str) -> dict:
    import requests
    y, n = cve_id.split("-")[1:]
    try:
        r = requests.get(CVE_RAW.format(y=y, b=n[:-3] + "xxx", c=cve_id), timeout=30)
        return r.json() if r.ok else {}
    except (requests.RequestException, ValueError):
        return {}


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
    # Bundles frozen before 1 Nov 2026 lack the CNA disclosure date and keep only five links;
    # for those, the CVE record is read live, as the worksheet does (noted in the report)
    live = "date_public" not in cve.columns
    R["fix_inputs"] = "CVE records read live (bundle predates the disclosure-date field)" if live else "frozen bundle"
    for r in sub.itertuples():
        lst = lambda x: [] if x is None else list(x)
        refs = lst(getattr(r, "fix_links", None)) + lst(getattr(r, "ref_links", None))
        pub = str(r.date_published)[:10] if pd.notna(r.date_published) else ""
        dp = getattr(r, "date_public", None)   # in bundles from 1 Nov 2026 on
        dp = str(dp)[:10] if dp is not None and pd.notna(dp) else ""
        if live and nvd is None:   # tests pass nvd and stay offline
            rec = _cve_record(r.cve_id)
            cna = (rec.get("containers") or {}).get("cna") or {}
            refs = refs + [x.get("url", "") for x in cna.get("references") or [] if x.get("url") not in refs]
            dp = str(cna.get("datePublic") or "")[:10]
        d, src, hand = prefill_exploited(r.cve_id, refs, vend.get(r.cve_id, ""), pub or "", dp)
        prefills[r.cve_id] = (d, src, hand)
        sources[r.cve_id] = bucket(src)
        time.sleep(pause)
    ev = build_events(sub, kq.rename(columns={"date_added": "date_added"}), prefills=prefills)
    for c in ("t0", "t_patch", "t_exploit", "t_kev", "fix_lo", "fix_hi", "exploit_hi"):
        ev[c] = pd.to_datetime(ev[c], errors="coerce")
    ev["prefill_source"] = ev["cve_id"].map(sources)
    R["kev_added_in_quarter"] = int(len(kq))
    R["prefill_assumed"] = int(sum(v == "assumed" for v in sources.values()))
    R["prefill_sources"] = dict(pd.Series(list(sources.values()), dtype=str).value_counts().items())
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


PLAIN = {
    "n": "Flaws counted", "n_measured": "Flaws with both dates",
    "median_days_t0_to_exploit": "Median days from publication to first attack",
    "share_exploited_on_or_before_t0": "Share attacked on or before publication",
    "median_days_fix_to_exploit": "Median days from fix to first attack",
    "zero_day_share_x10": "Share attacked before a fix existed (exploratory X10)",
    "ci90": "90% interval", "share_ci90": "90% interval", "zero_day_ci90": "90% interval",
    "yoy_growth_pct": "Growth on the same quarter last year (%)",
    "cves": "Flaws published in the quarter", "floor": "Floor: credit names an AI tool in a clear role",
    "hand": "Headline: credit mentions an AI tool or AI lab", "ceiling": "Ceiling: every possible AI mention",
    "floor_pct": "Floor (%)", "hand_pct": "Headline (%)", "ceiling_pct": "Ceiling (%)",
}
BOUNDS = {"n_fix_date_bounded": "Flaws whose fix date is a range, not a day",
          "n_exploit_before_kev": "Flaws with attack evidence before the KEV listing",
          "median_days_low": "Median days allowing for fix-date ranges, low end",
          "median_days_high": "Median days using the earliest attack evidence (an upper bound on the true median)",
          "zero_day_share_low": "Zero-day share, low end", "zero_day_share_high": "Zero-day share, high end"}
SOURCE_ORDER = ["GitHub", "Microsoft", "Cisco", "Linux kernel", "Siemens", "Red Hat", "Palo Alto",
                "OSV fixing commit", "deps.dev release", "dated advisory link", "CNA disclosure date", "assumed", "other"]


def _pct(v):
    return f"{100 * v:.0f}%" if isinstance(v, float) and v <= 1 else _fmt(v)


def _block(d: dict, skip=()) -> list[str]:
    out = []
    for k, v in d.items():
        if k in skip or k == "note":
            continue
        name = PLAIN.get(k, k.replace("_", " "))
        if "share" in k and not isinstance(v, (tuple, list)):
            v = _pct(v)
        elif "share" in k or k in ("share_ci90", "zero_day_ci90"):
            v = "(" + ", ".join(_pct(x) for x in v) + ")"
        out.append(f"- {name}: {_fmt(v) if not isinstance(v, str) else v}")
    return out


def report(R: dict) -> str:
    L = [f"# Practice evaluation: {R['quarter']} ({R['run']} run)", "",
         "> **Practice, not a result.** Q3 2026 is outside the registered study (the Q4 2026 pilot "
         "comes first; labels start with Q1 2027). Fix dates are the automatic pre-fill, before the "
         "author's hand check. Judged only on whether the method works (author's decision, 1 Nov 2026).", "",
         "## Fix dates behind the race measures", "",
         f"- Flaws first added to CISA KEV in the quarter: {R['kev_added_in_quarter']}",
         f"- Where the fix dates came from ({R.get('fix_inputs', 'frozen bundle')}):"]
    src = R.get("prefill_sources", {})
    L += [f"  - {k}: {src[k]}" for k in SOURCE_ORDER if k in src]
    L += [f"- Still an assumed date (no source; the hand check fills these): {R['prefill_assumed']}", ""]
    L += ["## I2. How fast newly published flaws are attacked", ""] + _block(R["I2"]) + [""]
    L += ["## I3. The race: days from the fix to the first attack", ""] + _block(R["I3"], skip=("bounds",))
    b = R["I3"].get("bounds") or {}
    if b:
        L += ["", "Range allowing for uncertain dates:"] + [
            f"- {BOUNDS[k]}: {_pct(v) if 'share' in k else ('-' if v is None else _fmt(v))}" for k, v in b.items() if k in BOUNDS]
        if b.get("note"):
            L += ["", f"_{b['note']}_"]
    L += ["", "## I5. Growth in published CVE records", "",
          "Published records in the same quarter of each year:"]
    L += [f"- {y}: {_fmt(c)}" for y, c in R["I5"]["published_by_year"].items()]
    L += [f"- {PLAIN['yoy_growth_pct']}: {_fmt(R['I5']['yoy_growth_pct'])}", "",
          "Count check against NVD (quality report section 2b; flagged above 5%):"]
    cc = R.get("I5_count_check") or {}
    L += [f"- {r['year']}: ours {_fmt(r['ours'])}, NVD {_fmt(r['nvd']) if r['nvd'] is not None else 'no answer'}"
          + (f", difference {100 * r['diff']:.1f}%" if r.get("diff") is not None else "") for r in cc.get("rows", [])]
    L += [f"- Flagged: {', '.join(map(str, cc['flags'])) if cc.get('flags') else 'none'}", "",
          "Whole calendar years (to compare with published annual totals):"]
    L += [f"- {y}: {_fmt(c)}" for y, c in R["I5_calendar_years"].items()]
    L += ["", "How I5 is scored with the 2026 surge in its baseline is core-freeze item 25 (21 Dec).", "",
          "## I8. Share of flaws credited to AI (range)", ""] + _block(R["I8"]) + ["", "## I7. Breaches and ransomware", ""]
    if "I7a_ransomware_postings" in R:
        L.append("- Ransomware postings by month (ransomware.live, totals only): " + ", ".join(
            f"{m} {_fmt(c)}" for m, c in R["I7a_ransomware_postings"].items()))
    if "I7b_sec_8k_item105" in R:
        s = R["I7b_sec_8k_item105"]
        L.append(f"- SEC 8-K Item 1.05 cyber-incident filings: {_fmt(s['filings'])}"
                 + (f" of {_fmt(s['registrants'])} registrants, {s['per_1000']} per 1,000" if s.get("registrants") else ""))
    L += ["", "## Not computable yet", ""] + [f"- {k}: {v}" for k, v in R["not_computable"].items()]
    L += ["", "No Improving or Worsening labels: this is a practice quarter outside the study.", "",
          "Files: `practice_eval.json` (all figures) and `events.csv` (one row per flaw first added to "
          "KEV, with its dates and fix-date source: the worksheet input for I2 and I3)."]
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
