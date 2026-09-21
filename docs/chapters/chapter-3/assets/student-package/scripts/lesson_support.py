"""教师提供的路径、读表检查和图形导出辅助函数。分析计算在三个课堂脚本中。"""
from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "savefig.facecolor": "white",
})


def require_columns(df, columns):
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise KeyError(f"Missing columns: {missing}. Available columns: {list(df.columns)}")


def read_data(filename, columns):
    path = ROOT / "data" / filename
    if not path.is_file():
        raise FileNotFoundError(f"Data file not found: {path}. Keep data/ beside scripts/.")
    df = pd.read_csv(path)
    require_columns(df, columns)
    if "value" in df:
        df["value"] = pd.to_numeric(df["value"], errors="raise")
        if df["value"].isna().any():
            raise ValueError("Missing response values: check the supplied data; do not fill with zero.")
    return df


def save_figure(fig, stem):
    for suffix in ["png", "svg"]:
        fig.savefig(OUT / f"{stem}.{suffix}", dpi=240, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved outputs/{stem}.png and .svg")
