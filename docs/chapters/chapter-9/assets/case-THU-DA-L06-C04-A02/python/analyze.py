from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ("figures","expected"): (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/"data/mtcars.csv")
assert not d.isna().any().any()
fig,ax=plt.subplots(figsize=(6.4,4.2))
assert len(d)==32
x=d.wt.to_numpy();y=d.mpg.to_numpy();fit=stats.linregress(x,y)
m={"n":len(d),"pearson":stats.pearsonr(x,y).statistic,"spearman":stats.spearmanr(x,y).statistic,"intercept":fit.intercept,"slope":fit.slope,"r_squared":fit.rvalue**2,"p_slope":fit.pvalue,"slope_per_lb":stats.linregress(x*1000,y).slope}
ax.scatter(x,y,c=d.cyl,cmap="viridis");xx=np.array([x.min(),x.max()]);ax.plot(xx,fit.intercept+fit.slope*xx,color="black")
ax.set(xlabel="Weight (1000 lb)",ylabel="Miles / US gallon",title="mtcars: 32 historical models")
fig2,ax2=plt.subplots();ax2.scatter(fit.intercept+fit.slope*x,y-fit.intercept-fit.slope*x);ax2.axhline(0,color="black");ax2.set(xlabel="Fitted mpg",ylabel="Residual mpg")
fig2.savefig(P/"figures/residuals-python.svg");fig2.savefig(P/"figures/residuals-python.png",dpi=160);plt.close(fig2)
fig.tight_layout()
fig.savefig(P/"figures/result-python.png",dpi=160)
fig.savefig(P/"figures/result-python.svg")
plt.close(fig)
pd.DataFrame({"metric":list(m),"value":list(m.values())}).to_csv(P/"expected/python.csv",index=False)
print(m)
