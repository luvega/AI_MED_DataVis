from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/sleep.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
wide=d.pivot(index="ID",columns="group",values="extra")
assert wide.shape==(10,2) and not wide.isna().any().any()
v=wide[2]-wide[1]; test=stats.ttest_1samp(v,0)
se=v.std(ddof=1)/np.sqrt(len(v)); ci=stats.t.interval(.95,len(v)-1,loc=v.mean(),scale=se)
m={"n":len(v),"mean_diff":v.mean(),"sd_diff":v.std(ddof=1),"se":se,"t":test.statistic,"p":test.pvalue,"ci_low":ci[0],"ci_high":ci[1]}
for _,r in wide.iterrows(): ax.plot([1,2],r.values,"o-",alpha=.6)
ax.set(xticks=[1,2],xlabel="Historical condition",ylabel="Extra sleep (hours)",title="Same ID connected; not independent groups")
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
