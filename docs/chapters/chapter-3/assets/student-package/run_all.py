"""课前验收/课后复跑入口；课堂按scripts中的文件逐步运行。"""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "scripts"))
for name in ["01_read.py", "02_lolamicin.py", "03_insulin.py"]:
    print(f"\nRunning {name}")
    runpy.run_path(str(root / "scripts" / name), run_name="__main__")
print("\nCompleted: three figures (PNG/SVG) and two summary tables in outputs/.")
