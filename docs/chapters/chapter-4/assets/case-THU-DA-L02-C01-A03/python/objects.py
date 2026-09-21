"""同一五行教学表：对象、定位、缺失检查；无统计推断。"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

def missing_columns(frame, required):
    return [name for name in required if name not in frame.columns]

def main():
    frame = pd.read_csv(BASE / "data/guesses.csv", dtype={"record_id": str, "participant_id": str})
    assert not missing_columns(frame, ["record_id", "participant_id", "round", "estimate_grains"])
    selected = frame.loc[frame["estimate_grains"].notna() & (frame["estimate_grains"] >= 950), ["record_id", "estimate_grains"]]
    metrics = pd.DataFrame({"metric": ["records", "participants", "missing_estimates", "selected_records"],
                            "value": [len(frame), frame.participant_id.nunique(), int(frame.estimate_grains.isna().sum()), len(selected)]})
    out = BASE / "results/python"
    out.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(out / "metrics.csv", index=False)
    selected.to_csv(out / "selected.csv", index=False)
    print(metrics.to_string(index=False))
    print("selected IDs:", ",".join(selected.record_id))

if __name__ == "__main__":
    main()
