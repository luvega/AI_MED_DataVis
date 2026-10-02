from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/faithful.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
assert len(d)==272
x=d.eruptions.to_numpy(); y=d.waiting.to_numpy()
fit=stats.linregress(x,y)
m={"n":len(d),"pearson":stats.pearsonr(x,y).statistic,"spearman":stats.spearmanr(x,y).statistic,"intercept":fit.intercept,"slope":fit.slope,"r_squared":fit.rvalue**2}
ax.scatter(x,y,s=12,alpha=.6);ax.set(xlabel="Eruption duration (min)",ylabel="Waiting to next eruption (min)",title="faithful: observations, not causal effects")
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
