"""Operating characteristics of the registered labelling rule (prereg Section 4).
Rule: direction_t = sign(x_t - median(x_{t-4..t-1})); label at t if direction_t == direction_{t-1} != 0.
Compared with a 'strict' variant: each of the two quarters must also sit outside a 90% interval
(baseline +/- 1.645*SE*sqrt(1+pi/(2*4))) i.e. sampling noise of x_t and of a 4-point median."""
import numpy as np
rng=np.random.default_rng(20261024)
R=200_000; T=7   # 4 baseline + 2 judged quarters + 1 spare
def sim(trend=0.0, rho=0.0, strict=False):
    e=rng.standard_normal((R,T))
    if rho:
        for t in range(1,T): e[:,t]=rho*e[:,t-1]+np.sqrt(1-rho**2)*e[:,t]
    x=e+trend*np.arange(T)
    def dirn(t):
        base=np.median(x[:,t-4:t],axis=1); d=x[:,t]-base
        if strict:
            thr=1.645*np.sqrt(1+np.pi/(2*4))
            return np.where(d>thr,1,np.where(d<-thr,-1,0))
        return np.sign(d)
    d1,d2=dirn(5),dirn(6)
    lab=(d1==d2)&(d2!=0)
    return lab.mean(), (lab&(d2>0)).mean()
print("scenario                         loose_any  loose_up   strict_any strict_up")
for name,tr,rho in [("no change, independent",0,0),("no change, AR(1) rho=0.5",0,0.5),
                    ("trend +0.25 SD/quarter",0.25,0),("trend +0.5 SD/quarter",0.5,0),("trend +1 SD/quarter",1.0,0)]:
    a=sim(tr,rho); b=sim(tr,rho,True)
    print(f"{name:32s} {a[0]:.3f}     {a[1]:.3f}     {b[0]:.3f}      {b[1]:.3f}")
# Over a year of 4 scored quarters with no change: chance at least one of 7 questions gets a false label in a given quarter
p=sim()[0]; print("P(>=1 of 7 independent questions labelled in a quarter, all null):", round(1-(1-p)**7,3))

print("\nPooled rule: mean of last 2 quarters vs mean of the 4 before, 90% two-sided test")
def pooled(trend=0.0,rho=0.0,z=1.645):
    e=rng.standard_normal((R,T))
    if rho:
        for t in range(1,T): e[:,t]=rho*e[:,t-1]+np.sqrt(1-rho**2)*e[:,t]
    x=e+trend*np.arange(T)
    d=x[:,5:7].mean(1)-x[:,1:5].mean(1); se=np.sqrt(1/2+1/4)
    return (np.abs(d)>z*se).mean(), (d>z*se).mean()
for name,tr,rho in [("no change, independent",0,0),("no change, AR(1) rho=0.5",0,0.5),
                    ("trend +0.25 SD/quarter",0.25,0),("trend +0.5 SD/quarter",0.5,0),("trend +1 SD/quarter",1.0,0)]:
    a=pooled(tr,rho); print(f"{name:32s} any={a[0]:.3f} up={a[1]:.3f}")
