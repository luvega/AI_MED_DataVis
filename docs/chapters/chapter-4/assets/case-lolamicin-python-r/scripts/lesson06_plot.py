"""教师准备的第六课图：原始点和均值，纵轴对数刻度，无误差线。"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

table = pd.read_csv("data/raw/lolamicin_ecoli_timekill.csv", encoding="utf-8")
if table["value"].isna().any() or (table["value"] <= 0).any():
    raise ValueError("This log-scale example requires the verified positive source values.")

treatments = table["treatment"].unique()
colors = ["#0072B2", "#009E73", "#D55E00"]
fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)

# 第七课再逐行解释循环。原始点不按重复列序号跨时间连线。
for ax, treatment, color in zip(axes, treatments, colors):
    group = table[table["treatment"] == treatment]
    means = group.groupby("time_h")["value"].mean()
    ax.scatter(group["time_h"], group["value"], s=34, color=color, alpha=0.7,
               label="Source values", zorder=3)
    ax.plot(means.index, means.values, "-D", color="#202020", markersize=4,
            linewidth=1.4, label="Arithmetic mean")
    ax.set_title(treatment.replace("(4X MIC)", "(4× MIC)"), fontsize=10)
    ax.set_xlabel("Time (h)")
    ax.set_xticks([1, 2, 4, 8])
    ax.set_yscale("log")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)

axes[0].set_ylabel("CFU/mL (log scale)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False,
           bbox_to_anchor=(0.5, 0.93))
fig.suptitle("E. coli BW25113: source values and arithmetic means", fontsize=12)
fig.text(0.5, 0.015, "Source: Muñoz et al., Nature (2024), Extended Data Fig. 3a. No error bars.",
         ha="center", fontsize=8)
fig.tight_layout(rect=(0, 0.06, 1, 0.85))
Path("outputs").mkdir(exist_ok=True)
fig.savefig("outputs/lolamicin_points_means.png", dpi=180)
fig.savefig("outputs/lolamicin_points_means.pdf")
plt.close(fig)
print("Saved source-point and mean plots; no error bars or paired trajectories.")
