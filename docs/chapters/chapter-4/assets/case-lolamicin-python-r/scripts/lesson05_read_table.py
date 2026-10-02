"""第五课：从练习目录运行，按时间选择已核验的六行表。"""
import pandas as pd

table = pd.read_csv("data/raw/lolamicin_2_8h.csv", encoding="utf-8")
print(table)
print("shape:", table.shape)
print("columns:", table.columns)
print("types:", table.dtypes)

target_time = 8
keep = table["time_h"] == target_time
print("keep:", keep)
selected = table[keep]
print("source_cell:", selected["source_cell"])
print("value:", selected["value"])
print("mean_cfu:", selected["value"].mean())

# 教师带做的保存步骤；索引列不作为实验字段写入文件。
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)
selected.to_csv("outputs/python_selected.csv", index=False, encoding="utf-8")

# 独立教学构造表，不来自作者研究，也不写回data/raw。
example = pd.read_csv("data/teaching/constructed_missing.csv", encoding="utf-8")
print("constructed_example:", example)
print("is_missing:", example["value"].isna())
print("is_zero:", example["value"] == 0)
