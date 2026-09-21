"""课堂15—35分钟：读文件、核对字段与记录结构。"""
# %% 1. 读取；一行对应一个条件、一个时间点的一次重复读数
from lesson_support import read_data

a = read_data("A_lolamicin.csv", ["treatment", "time_h", "value", "unit", "source_cell"])
print("A columns:", list(a.columns))
print(a.head(3).to_string(index=False))
print("A records:", len(a))

# %% 2. 数的是每个条件下的记录，不是整项研究的独立样本量
counts = a.groupby(["treatment", "time_h"], sort=True).size()
print("A treatment-time groups:", len(counts))
print(counts.to_string())
assert len(a) == 36 and len(counts) == 12 and counts.eq(3).all()
assert set(a["time_h"]) == {1, 2, 4, 8}
assert set(a["unit"]) == {"CFU/mL"}

# %% 3. 筛选一个可以人工核对的组
selected = a[(a["treatment"] == "Lolamicin (4X MIC)") & (a["time_h"] == 2)]
print("Lolamicin at 2 h:", selected["value"].tolist())
print("Arithmetic mean:", selected["value"].mean())

# %% 4. 第二案例只核对结构，实验含义到迁移环节再讲
b = read_data("B_insulin.csv", ["molecule", "glucose_mM", "concentration_M", "value", "unit"])
counts_b = b.groupby(["molecule", "glucose_mM", "concentration_M"]).size()
print("B records:", len(b), "; condition groups:", len(counts_b))
assert len(b) == 96 and len(counts_b) == 32 and counts_b.eq(3).all()
assert set(b["unit"]) == {"CPM"}
