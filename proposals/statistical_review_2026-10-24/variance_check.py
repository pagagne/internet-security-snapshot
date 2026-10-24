# Data: CVE records (cvelistV5 cves/2025 and cves/2026, parsed with snapshot.collect.cve.build_table
# and saved as cves.parquet), CISA KEV JSON, and weekly EPSS files epss_scores-YYYY-MM-DD.csv.gz
# (3 Apr to 23 Oct 2026), all pulled 24 Oct 2026, in the folder named by SNAPSHOT_REVIEW_DATA.
import os
DATA = os.environ.get("SNAPSHOT_REVIEW_DATA", "data/review")
import json, numpy as np, pandas as pd
from pathlib import Path
from snapshot import backtest_t1 as bt
cve=pd.read_parquet(f'{DATA}/cves.parquet'); kev=pd.DataFrame(json.load(open(f'{DATA}/kev.json'))['vulnerabilities'])
epss=bt.load_epss(Path(DATA) / 'epss'); ev=pd.Timestamp('2026-10-21')
rng=np.random.default_rng(1)
for qn,(months,draw) in bt.QUARTERS.items():
    pop=bt.attach_epss(bt.population(cve,kev,months,ev),epss,draw)
    pop['w']=np.sqrt(pop['epss_early'].fillna(0))+0.01
    pop['cv']=pop['cvss_base'].fillna(pop['cvss_base'].median())
    ratios=[]; prep=[]
    for _,g in pop.groupby(['month','slot']):
        w=g['w'].to_numpy(); ratios.append(w.max()/w.min())
        prep.append((w/w.sum(), np.ones(len(g))/len(g), g['cv'].to_numpy(), len(g)))
    N=len(pop); res={'HT':[], 'Hajek':[], 'uniform':[]}
    for _ in range(4000):
        ht=0; num=0; den=0; un=0
        for p,u,y,n in prep:
            i=rng.choice(len(p),p=p); ht+=y[i]/p[i]; num+=y[i]/p[i]; den+=1/p[i]
            j=rng.choice(len(u)); un+=y[j]*n
        res['HT'].append(ht/N); res['Hajek'].append(num/den); res['uniform'].append(un/N)
    sd={k:np.std(v) for k,v in res.items()}
    print(qn,'true mean CVSS',round(pop.cv.mean(),3),'| weight ratio max/min within stratum: median',round(np.median(ratios),1),'max',round(max(ratios),1))
    print('   SD  uniform %.3f  HT %.3f (var x%.0f)  Hajek %.3f (var x%.1f)'%(sd['uniform'],sd['HT'],(sd['HT']/sd['uniform'])**2,sd['Hajek'],(sd['Hajek']/sd['uniform'])**2))
