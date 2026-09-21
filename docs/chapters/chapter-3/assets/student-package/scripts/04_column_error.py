"""教师预设的列名错误练习；不属于正常运行入口。只改VALUE_COLUMN这一处。"""
from lesson_support import read_data, require_columns

a = read_data("A_lolamicin.csv", ["treatment", "time_h", "value"])
VALUE_COLUMN = "CFU"  # 根据实际列名和数据字典修正
require_columns(a, [VALUE_COLUMN])
chosen = a[(a["treatment"] == "Lolamicin (4X MIC)") & (a["time_h"] == 2)]
print("Lolamicin at 2 h:", chosen[VALUE_COLUMN].tolist())
print("Arithmetic mean:", chosen[VALUE_COLUMN].mean())
