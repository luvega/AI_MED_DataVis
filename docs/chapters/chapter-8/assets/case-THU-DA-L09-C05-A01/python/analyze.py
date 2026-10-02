from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/ab.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
assert d.group.tolist()==["A","B"] and (d.n==5000).all()
a,b=d.itertuples(index=False,name=None)
p0=a[2]/a[1];p1=b[2]/b[1];diff=p1-p0
se=np.sqrt(p0*(1-p0)/a[1]+p1*(1-p1)/b[1])
pool=(a[2]+b[2])/(a[1]+b[1]);se0=np.sqrt(pool*(1-pool)*(1/a[1]+1/b[1]))
z=diff/se0
m={"n":int(d.n.sum()),"p_A":p0,"p_B":p1,"difference":diff,"relative_change":diff/p0,"ci_low":diff-stats.norm.ppf(.975)*se,"ci_high":diff+stats.norm.ppf(.975)*se,"z":z,"p":2*stats.norm.sf(abs(z))}
ax.bar(["A","B"],[p0,p1]);ax.set(ylim=(0,.35),ylabel="Reservation proportion",title="Constructed teaching data; 5000 users per group")
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
