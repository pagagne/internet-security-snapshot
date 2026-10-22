"""Back-test of T1(a) designs on past quarters (design work for decision item 0).

Compares, by repeated simulated draws on real data:
  (b) registered cohort  - one pick per slot and month, equal chance within the slot
  (d) weighted cohort    - same slots, but a CVE's chance of being picked is proportional to
                           its EPSS score (with a floor); estimates are re-weighted by
                           1 / chance of selection, so they still describe all eligible CVEs
  (a) all flaws first exploited in the quarter (no sampling; shown for reference)

Population: cohort-eligible CVEs in slots a-c (slot d overlaps them and is left out of
the race estimate). Truth = the same quantities computed on the whole population.
Quantities, among eligible CVEs exploited within 90 days of publication:
  share exploited (of all eligible), share exploited on or before the fix ("zero-day
  share"), median days from fix to first exploitation.

Back-test simplifications (stated in the results): fix date = CVE publication date
(as in the option (a) preview); exploitation = CISA KEV only; EPSS from weekly snapshots
(first snapshot at least 7 days after publication, or the snapshot after the quarter's
draw date); slot c internet-facing hand check and slot d not simulated; several picks per
slot are drawn with replacement (Hansen-Hurwitz weights).
"""

from __future__ import annotations

import argparse
import glob
import gzip
import json
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from .classify import product_category

FOLLOW_UP = 90
QUARTERS = {"2026Q2": (["2026-04", "2026-05", "2026-06"], "2026-07-10"),
            "2026Q3": (["2026-07", "2026-08", "2026-09"], "2026-10-09")}


def load_epss(folder: Path) -> dict[pd.Timestamp, pd.Series]:
    out = {}
    for f in sorted(glob.glob(str(folder / "epss_scores-*.csv.gz"))):
        d = pd.Timestamp(re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1))
        s = pd.read_csv(f, comment="#", usecols=["cve", "epss"])
        out[d] = s.set_index("cve")["epss"]
    return out


def population(cve: pd.DataFrame, kev: pd.DataFrame, months: list[str], eval_date: pd.Timestamp,
               min_cvss: float = 8.0, day_max: int = 25) -> pd.DataFrame:
    d = cve.copy()
    d["pub"] = pd.to_datetime(d["date_published"], utc=True, errors="coerce").dt.tz_localize(None)
    sev = d["cvss_severity"].fillna("").str.upper()
    m = (d["state"] == "PUBLISHED") & d["pub"].dt.strftime("%Y-%m").isin(months) & (d["pub"].dt.day <= day_max) \
        & ((d["cvss_base"] >= min_cvss) | (sev == "CRITICAL"))
    d = d[m].copy()
    d["month"] = d["pub"].dt.strftime("%Y-%m")
    d["slot"] = d["affected"].map(lambda a: product_category(list(a)))
    d["t0"] = d["pub"].dt.normalize()
    k = kev.groupby("cveID")["dateAdded"].min()
    d["t_exploit"] = pd.to_datetime(d["cve_id"].map(k))
    end = (d["t0"] + pd.Timedelta(days=FOLLOW_UP)).clip(upper=eval_date)
    d["exploited"] = d["t_exploit"].notna() & (d["t_exploit"] <= end)
    d["days"] = (d["t_exploit"] - d["t0"]).dt.days   # fix ~ publication in the back-test
    return d[d["slot"].isin(["a_edge", "b_web_collab", "c_other"])].reset_index(drop=True)


def attach_epss(pop: pd.DataFrame, epss: dict, draw_date: str) -> pd.DataFrame:
    dates = sorted(epss)
    def early(r):
        target = r.t0 + pd.Timedelta(days=7)
        for d in dates:
            if d >= target:
                return epss[d].get(r.cve_id, np.nan)
        return epss[dates[-1]].get(r.cve_id, np.nan)
    pop = pop.copy()
    pop["epss_early"] = [early(r) for r in pop.itertuples()]
    dd = min((d for d in dates if d >= pd.Timestamp(draw_date)), default=dates[-1])
    pop["epss_draw"] = pop["cve_id"].map(epss[dd])
    return pop


def truth(pop: pd.DataFrame) -> dict:
    e = pop[pop["exploited"]]
    return {"eligible": len(pop), "exploited": len(e), "share_exploited": len(e) / len(pop),
            "zero_day_share": float((e["days"] <= 0).mean()) if len(e) else np.nan,
            "median_days": float(e["days"].median()) if len(e) else np.nan}


def _wmedian(x, w):
    o = np.argsort(x); x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(c, 0.5)])


def simulate(pop: pd.DataFrame, weight_col: str | None, floor: float, k: int, reps: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    strata = [g for _, g in pop.groupby(["month", "slot"])]
    prep = []
    for g in strata:
        if weight_col is None:
            w = np.ones(len(g))
        else:
            w = np.maximum(g[weight_col].fillna(0).to_numpy(), floor)
        p = w / w.sum()
        prep.append((p, g["exploited"].to_numpy(), g["days"].to_numpy(dtype=float)))
    n_exp, share, zd, med = [], [], [], []
    for _ in range(reps):
        ex_w, ex_days, tot_w_exp, N = [], [], 0.0, 0
        for p, ex, days in prep:
            idx = rng.choice(len(p), size=k, p=p, replace=True)
            hw = 1.0 / (k * p[idx])            # Hansen-Hurwitz weight
            tot_w_exp += float((hw * ex[idx]).sum())
            N += len(p)
            sel = ex[idx]
            ex_w += list(hw[sel]); ex_days += list(days[idx][sel])
        n_exp.append(len(ex_w))
        share.append(tot_w_exp / N)
        if ex_w:
            w, d = np.array(ex_w), np.array(ex_days)
            zd.append(float(w[d <= 0].sum() / w.sum())); med.append(_wmedian(d, w))
    n_exp = np.array(n_exp)
    q = lambda a: (float(np.percentile(a, 5)), float(np.percentile(a, 95))) if len(a) else (np.nan, np.nan)
    return {"picks": len(strata) * k, "mean_exploited_picks": float(n_exp.mean()),
            "p_any": float((n_exp >= 1).mean()), "p_5plus": float((n_exp >= 5).mean()),
            "share_range": q(share), "zero_day_range": q(zd), "median_range": q(med)}


def design_a(cve: pd.DataFrame, kev: pd.DataFrame, months: list[str]) -> dict:
    k = kev.copy(); k["added"] = pd.to_datetime(k["dateAdded"])
    first = k.groupby("cveID")["added"].min()
    first = first[first.dt.strftime("%Y-%m").isin(months)]
    pub = pd.to_datetime(cve.set_index("cve_id")["date_published"], utc=True, errors="coerce").dt.tz_localize(None).dt.normalize()
    days = (first - first.index.map(pub)).dt.days.dropna()
    return {"kev_additions": len(first), "with_record": len(days),
            "zero_day_share": float((days <= 0).mean()), "median_days": float(days.median())}


DESIGNS = [("(b) registered, 1 per slot", None, 0.0, 1),
           ("(d) EPSS at +7 days, floor 0.01, 1 per slot", "epss_early", 0.01, 1),
           ("(d) EPSS at +7 days, floor 0.001, 1 per slot", "epss_early", 0.001, 1),
           ("(d) EPSS at draw date, floor 0.01, 1 per slot", "epss_draw", 0.01, 1),
           ("(d) EPSS at +7 days, floor 0.01, 2 per slot", "epss_early", 0.01, 2),
           ("(d) EPSS at +7 days, floor 0.001, 2 per slot", "epss_early", 0.001, 2),
           ("(b) registered, 2 per slot", None, 0.0, 2)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cve", type=Path, required=True)
    ap.add_argument("--kev", type=Path, required=True, help="CISA KEV JSON")
    ap.add_argument("--epss-dir", type=Path, required=True)
    ap.add_argument("--eval-date", default="2026-10-21")
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("--out", type=Path, default=Path("backtest_t1.json"))
    a = ap.parse_args(argv)
    cve = pd.read_parquet(a.cve)
    kev = pd.DataFrame(json.load(open(a.kev))["vulnerabilities"])
    epss = load_epss(a.epss_dir)
    ev = pd.Timestamp(a.eval_date)
    res = {}
    for qn, (months, draw) in QUARTERS.items():
        pop = attach_epss(population(cve, kev, months, ev), epss, draw)
        e = pop[pop.exploited]
        res[qn] = {"truth": truth(pop), "design_a": design_a(cve, kev, months),
                   "epss_coverage": float(pop["epss_early"].notna().mean()),
                   "exploited_epss_early_median": float(e["epss_early"].median()) if len(e) else None,
                   "all_epss_early_median": float(pop["epss_early"].median()),
                   "designs": {name: simulate(pop, col, fl, k, a.reps, 20261020)
                               for name, col, fl, k in DESIGNS}}
    a.out.write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(res, indent=1, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
