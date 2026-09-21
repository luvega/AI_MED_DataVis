"""只检查前5章依赖，不安装或修改环境。"""
import importlib
import sys
from pathlib import Path
print("executable:",sys.executable)
print("version:",sys.version)
print("working_directory:",Path.cwd())
missing = []
for name in ["pandas","matplotlib","openpyxl"]:
    try:
        module = importlib.import_module(name)
        print(name,getattr(module,"__version__","available"))
    except ImportError:
        missing.append(name)
        print(name,"MISSING")
print("basic_calculation:",2+3)
raise SystemExit(1 if missing else 0)
