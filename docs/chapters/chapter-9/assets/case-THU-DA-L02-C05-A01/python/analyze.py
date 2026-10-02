from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/titanic.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
assert int(d.Freq.sum())==2201 and len(d)==32
t=d.pivot_table(index="Sex",columns="Survived",values="Freq",aggfunc="sum")
pm=t.loc["Male","Yes"]/t.loc["Male"].sum();pf=t.loc["Female","Yes"]/t.loc["Female"].sum()
logit=lambda p: np.log(p/(1-p))
m={"n":int(d.Freq.sum()),"survived":int(t.Yes.sum()),"p_male":pm,"p_female":pf,"intercept_male":logit(pm),"coef_female":logit(pf)-logit(pm)}
# At threshold .5: all females positive, all males negative, within this sample only.
tp=int(t.loc["Female","Yes"]);fp=int(t.loc["Female","No"]);tn=int(t.loc["Male","No"]);fn=int(t.loc["Male","Yes"])
m.update(TP=tp,FP=fp,TN=tn,FN=fn,sensitivity=tp/(tp+fn),specificity=tn/(tn+fp),accuracy=(tp+tn)/2201,auc=(tp/(tp+fn)+tn/(tn+fp))/2)
ax.bar(["Male","Female"],[pm,pf]);ax.set(ylim=(0,1),ylabel="Observed survival proportion",title="Historical aggregate; not a causal estimate")
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
