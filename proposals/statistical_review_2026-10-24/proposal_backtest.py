"""Re-run of the repo's T1 back-test (src/snapshot/backtest_t1.py) adding the design in EVAL-2026-ISS-01:
w_i = EPSS_i^0.5 + 0.01, one pick per slot and month, Horvitz-Thompson / Hansen-Hurwitz re-weighting.
Also measures what the weighting costs for the cohort's non-race figures (mean CVSS, share AI-credited,
share memory-safety), which the proposal says stay 'unskewed'."""
# Data: CVE records (cvelistV5 cves/2025 and cves/2026, parsed with snapshot.collect.cve.build_table
# and saved as cves.parquet), CISA KEV JSON, and weekly EPSS files epss_scores-YYYY-MM-DD.csv.gz
# (3 Apr to 23 Oct 2026), all pulled 24 Oct 2026, in the folder named by SNAPSHOT_REVIEW_DATA.
import os
DATA = os.environ.get("SNAPSHOT_REVIEW_DATA", "data/review")
import json, sys
import numpy as np, pandas as pd
from pathlib import Path
from snapshot import backtest_t1 as bt

cve = pd.read_parquet(f'{DATA}/cves.parquet')
kev = pd.DataFrame(json.load(open(f'{DATA}/kev.json'))['vulnerabilities'])
epss = bt.load_epss(Path(DATA) / 'epss')
ev = pd.Timestamp('2026-10-21')
designs = [("(b) registered, uniform, 1 per slot", None, 0.0, 1),
           ("(d) repo: EPSS +7d, floor 0.01", "epss_early", 0.01, 1),
           ("EVAL proposal: sqrt(EPSS +7d)+0.01", "w_prop_early", 0.0, 1),
           ("EVAL proposal: sqrt(EPSS at draw)+0.01", "w_prop_draw", 0.0, 1)]

def other_metrics(pop, wcol, reps=2000, seed=7):
    """Sampling spread of three non-race cohort figures under a design (1 pick per slot-month, HH weights)."""
    rng = np.random.default_rng(seed)
    pop = pop.copy()
    pop['mem'] = (pop['root_cause'] == 'memory_safety').astype(float)
    pop['ai'] = pop['ai_credited'].astype(float)
    strata = [g for _, g in pop.groupby(['month', 'slot'])]
    N = len(pop); out = {k: [] for k in ('cvss', 'ai', 'mem')}
    prep = []
    for g in strata:
        w = np.ones(len(g)) if wcol is None else g[wcol].fillna(0.01).to_numpy()
        prep.append((w / w.sum(), g[['cvss_base', 'ai', 'mem']].fillna(0).to_numpy()))
    for _ in range(reps):
        tot = np.zeros(3)
        for p, Y in prep:
            i = rng.choice(len(p), p=p)
            tot += Y[i] / p[i]
        est = tot / N
        out['cvss'].append(est[0]); out['ai'].append(est[1]); out['mem'].append(est[2])
    truth = {'cvss': pop['cvss_base'].fillna(0).mean(), 'ai': pop['ai'].mean(), 'mem': pop['mem'].mean()}
    return {k: {'true': float(truth[k]), 'sd': float(np.std(v)), 'p5': float(np.percentile(v, 5)), 'p95': float(np.percentile(v, 95))} for k, v in out.items()}

res = {}
for qn, (months, draw) in bt.QUARTERS.items():
    pop = bt.attach_epss(bt.population(cve, kev, months, ev), epss, draw)
    pop = pop.merge(cve[['cve_id', 'root_cause', 'ai_credited']], on='cve_id', how='left', suffixes=('', '_y'))
    pop['w_prop_early'] = np.sqrt(pop['epss_early'].fillna(0)) + 0.01
    pop['w_prop_draw'] = np.sqrt(pop['epss_draw'].fillna(0)) + 0.01
    e = pop[pop.exploited]
    # how concentrated is exploitation in EPSS? share of exploited flaws in the top decile of epss_early
    top = pop['epss_early'] >= pop['epss_early'].quantile(0.9)
    res[qn] = {'truth': bt.truth(pop), 'design_a': bt.design_a(cve, kev, months),
               'exploited_in_top_epss_decile': float(top[pop.exploited].mean()),
               'designs': {n: bt.simulate(pop, c, f, k, 2000, 20261020) for n, c, f, k in designs},
               'other_metrics': {n: other_metrics(pop, c if c != 'epss_early' else None if False else c) for n, c, f, k in designs if c in (None, 'w_prop_early')}}
Path('proposal_backtest.json').write_text(json.dumps(res, indent=1, default=float))
for q, v in res.items():
    print(q, 'truth', v['truth'], '| top-decile capture', round(v['exploited_in_top_epss_decile'], 2))
    print('   design (a):', v['design_a'])
    for n, s in v['designs'].items():
        print(f"   {n:42s} exploited picks {s['mean_exploited_picks']:.2f}  P(any) {s['p_any']:.2f}  zero-day 90% {s['zero_day_range'][0]:.2f}-{s['zero_day_range'][1]:.2f}  median days {s['median_range']}")
    for n, m in v['other_metrics'].items():
        print('   other figures,', n, {k: (round(x['true'], 3), round(x['sd'], 4)) for k, x in m.items()})
