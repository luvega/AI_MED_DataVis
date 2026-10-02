"""第六课：保留全部作者记录，按处理和时间汇总。"""
from pathlib import Path

import pandas as pd

table = pd.read_csv("data/raw/lolamicin_ecoli_timekill.csv", encoding="utf-8")
print("shape:", table.shape)
print("missing_values:", table["value"].isna().sum())
print("units:", table["unit"].unique())
print("duplicated_source_locations:", table.duplicated(["source_sheet", "source_cell"]).sum())

groups = table.groupby(["treatment", "time_h"], sort=False)["value"]
summary = groups.agg(["size", "count", "mean", "std"]).reset_index()
summary.columns = ["treatment", "time_h", "n_records", "n_values", "mean_cfu", "sd_cfu"]
summary["unit"] = "CFU/mL"
print(summary.to_string(index=False))

# std采用样本SD（n-1）；此处没有做检验、删除异常值或推断配对。
Path("outputs").mkdir(exist_ok=True)
summary.to_csv("outputs/lolamicin_summary.csv", index=False, encoding="utf-8")
