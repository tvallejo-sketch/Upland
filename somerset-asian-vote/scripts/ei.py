import sys, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from pyei.r_by_c import RowByColumnEI
df=pd.read_csv(sys.argv[1],index_col=0); df["other"]=df.other.clip(lower=0)
G=["asian","white","black","hisp","other"]
N=df.cvap.values.astype(int)
gf=(df[G].values/df.cvap.values[:,None]).T
out={}
for yr in [2020,2024,2025]:
    v=df[[f"D{yr}",f"R{yr}",f"O{yr}"]].values.astype(float)
    nov=np.clip(N-v.sum(1),0,None)
    cnt=np.column_stack([v,nov]); tot=cnt.sum(1).astype(int)
    vf=(cnt/tot[:,None]).T
    gfy=(df[G].values/df[G].values.sum(1)[:,None]*1.0).T
    ei=RowByColumnEI("multinomial-dirichlet")
    ei.fit(gfy, vf, tot, demographic_group_names=G, candidate_names=["D","R","O","NoVote"],
           draws=2000, tune=2000, chains=4, target_accept=.95, random_seed=7, progressbar=False)
    s=ei.sampled_voting_prefs  # draws x groups x cands
    for gi,g in enumerate(G):
        vt=s[:,gi,:3].sum(1); d=s[:,gi,0]/vt; r=s[:,gi,1]/vt
        out[(yr,g)]=dict(D=np.mean(d),D_lo=np.percentile(d,5),D_hi=np.percentile(d,95),
                         R=np.mean(r),margin=np.mean(d-r),m_lo=np.percentile(d-r,5),m_hi=np.percentile(d-r,95),
                         turnout=np.mean(vt))
    # swing draws for asian
    out[(yr,"_asian_draws")]=(s[:,0,0]-s[:,0,1])/s[:,0,:3].sum(1)
res=pd.DataFrame({k:v for k,v in out.items() if not k[1].startswith("_")}).T.round(3)
pd.set_option("display.width",200); print(res)
a20,a24,a25=[out[(y,"_asian_draws")] for y in (2020,2024,2025)]
for n,x in [("Asian margin shift 20->24",a24-a20),("Asian margin shift 24->25",a25-a24)]:
    print(n, round(x.mean(),3), np.percentile(x,[5,95]).round(3))
res.to_csv(sys.argv[2])
