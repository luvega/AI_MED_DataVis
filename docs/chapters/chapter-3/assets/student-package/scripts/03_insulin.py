"""课堂75—105分钟：按各自浓度作图；CPM是竞争结合实验的检测读数。"""
# %% 1. 读取；两个分子的浓度梯度分别保留
from lesson_support import read_data, OUT, plt, save_figure

b = read_data("B_insulin.csv", ["molecule", "glucose_mM", "concentration_M", "value", "unit"])
if not b["concentration_M"].gt(0).all():
    raise ValueError("Non-positive concentration: inspect the source label before plotting.")
assert set(b["glucose_mM"]) == {3, 20}
summary = b.groupby(["molecule", "glucose_mM", "concentration_M"], as_index=False).agg(
    n=("value", "count"), mean=("value", "mean"), sd=("value", "std")
)
assert len(b) == 96 and len(summary) == 32 and summary["n"].eq(3).all()
summary.to_csv(OUT / "B_summary.csv", index=False)
print("B:", len(b), "readings;", len(summary), "groups; 3 technical readings per group.")

# %% 2. 图3：均值和SD；折线连接观测均值，不进行模型拟合
colors = {3: "#3A67A3", 20: "#B24A75"}
fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.1), sharex=True, sharey=True)
for ax, molecule in zip(axes, ["NNC2215", "Human insulin"]):
    for glucose in [3, 20]:
        raw = b[(b["molecule"] == molecule) & (b["glucose_mM"] == glucose)]
        part = summary[(summary["molecule"] == molecule) &
                       (summary["glucose_mM"] == glucose)].sort_values("concentration_M")
        ax.scatter(raw["concentration_M"], raw["value"], color=colors[glucose], s=22, alpha=0.45)
        ax.errorbar(part["concentration_M"], part["mean"], yerr=part["sd"],
                    color=colors[glucose], marker="o", markersize=5,
                    linewidth=1.7, capsize=3, label=f"Glucose {glucose} mM")
    ax.set_xscale("log")
    ax.set(xlabel="Unlabelled ligand concentration (M)", title=molecule)
    ax.set_xlim(6e-14, 2e-7)
    ax.set_ylim(0, 550)
    ax.grid(axis="y", alpha=0.16)
axes[0].set_ylabel("Receptor-bound tracer signal (CPM)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
fig.text(0.5, 0.015, "Points: technical triplicates. Bars: mean +/- SD. Lines join means; no fitted curves.\n"
         "Each molecule retains its source concentration grid; first labels retained as 10^-13 M.",
         ha="center", fontsize=9)
fig.tight_layout(rect=[0, 0.09, 1, 0.9])
save_figure(fig, "Fig3_B_competition")
