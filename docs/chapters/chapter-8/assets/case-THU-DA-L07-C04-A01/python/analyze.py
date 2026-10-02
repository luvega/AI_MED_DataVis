from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/tea.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
counts=d.correct_milk.value_counts().reindex(range(5),fill_value=0)
assert len(d)==70 and counts.tolist()==[1,16,36,16,1]
m={"n":len(d),"p_all":float((d.correct_milk>=4).mean()),"p_at_least_three":float((d.correct_milk>=3).mean())}
ax.bar(counts.index,counts.values); ax.set(xlabel="Correct milk-first cups (out of 4)",ylabel="Number of allocations",title="Null randomization: 70 allocations")
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
