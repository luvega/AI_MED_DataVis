"""课堂35—75分钟：汇总原始尺度的读数，比较坐标，画均值与SEM。"""
# %% 1. 读取与汇总：std使用样本标准差，分母n-1
from lesson_support import read_data, OUT, plt, save_figure

a = read_data("A_lolamicin.csv", ["treatment", "time_h", "value", "unit"])
if not a["value"].gt(0).all():
    raise ValueError("A contains non-positive values; review before using a log axis.")
summary = a.groupby(["treatment", "time_h"], as_index=False).agg(
    n=("value", "count"), mean=("value", "mean"), sd=("value", "std")
)
summary["sem"] = summary["sd"] / summary["n"] ** 0.5
assert len(summary) == 12 and summary["n"].eq(3).all()
if not (summary["mean"] - summary["sem"]).gt(0).all():
    raise ValueError("An error-bar lower bound is non-positive; do not silently clip it.")
summary.to_csv(OUT / "A_summary.csv", index=False)
print(summary.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# %% 2. 图1：两个面板共享相同的36条数值，只改变纵轴
styles = {
    "Untreated control": ("#596675", "o", "Untreated"),
    "Lolamicin (4X MIC)": ("#087E8B", "s", "Lolamicin (4 x MIC)"),
    "Ciprofloxacin (4X MIC)": ("#BD582F", "^", "Ciprofloxacin (4 x MIC)"),
}
fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.8))
for ax, scale in zip(axes, ["linear", "log"]):
    for treatment, (color, marker, label) in styles.items():
        rows = a[a["treatment"] == treatment]
        ax.scatter(rows["time_h"], rows["value"], c=color, marker=marker,
                   s=38, alpha=0.7, label=label)
    ax.set_yscale(scale)
    ax.set(title=f"{scale.capitalize()} y-axis", xlabel="Time (h)", ylabel="CFU/mL")
    ax.set_xticks([1, 2, 4, 8])
    ax.grid(axis="y", alpha=0.16)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
fig.text(0.5, 0.015, "Same 36 measurements in both panels; overlapping points are retained.",
         ha="center", fontsize=10)
fig.tight_layout(rect=[0, 0.055, 1, 0.9])
save_figure(fig, "Fig1_A_axis_comparison")

# %% 3. 图2：在原数值上算均值和SEM，纵轴用对数显示
Y_SCALE = "log"  # 课堂仅将此处改成"linear"再运行，比较显示；计算规则不变
fig, ax = plt.subplots(figsize=(9.5, 5.6))
for treatment, (color, marker, label) in styles.items():
    raw = a[a["treatment"] == treatment]
    part = summary[summary["treatment"] == treatment].sort_values("time_h")
    ax.scatter(raw["time_h"], raw["value"], c=color, marker=marker, s=28, alpha=0.4)
    ax.errorbar(part["time_h"], part["mean"], yerr=part["sem"],
                color=color, marker=marker, markersize=6, linewidth=1.8,
                capsize=4, label=label)
ax.set_yscale(Y_SCALE)
ax.set(xlabel="Time (h)", ylabel="CFU/mL", title="E. coli BW25113: time-kill measurements")
ax.set_xticks([1, 2, 4, 8])
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", alpha=0.16)
fig.text(0.5, 0.015, "Points: biological triplicates. Lines and bars: arithmetic mean +/- SEM.\n"
         "Summary computed before applying the log axis; no 0 h measurements added.",
         ha="center", fontsize=9)
fig.tight_layout(rect=[0, 0.08, 1, 1])
save_figure(fig, "Fig2_A_time_kill")
