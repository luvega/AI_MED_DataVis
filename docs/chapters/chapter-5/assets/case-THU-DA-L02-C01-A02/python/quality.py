"""显式教学规则：保留原始字符，检查后生成派生表，不改原始文件。"""
from pathlib import Path
import argparse
import csv
import re
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
COLUMNS = ["record_id", "participant_id", "round", "estimate", "unit"]

def clean(source):
    with Path(source).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != COLUMNS:
            raise ValueError("Expected exact column names and order")
        rows = list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("Malformed row")
    if any(not row["record_id"] or not row["participant_id"] or row["round"] not in ("1", "2") for row in rows):
        raise ValueError("Missing ID or invalid round; stop for review")
    seen, unique, issues = {}, [], []
    for number, row in enumerate(rows, 1):
        rid = row["record_id"]
        if rid in seen:
            if row != seen[rid]:
                raise ValueError("Conflicting record_id: " + rid)
            issues.append([number, rid, "duplicate_export", "drop_duplicate_copy"])
        else:
            seen[rid] = row
            unique.append((number, row))
    output, quarantine = [], []
    for number, row in unique:
        raw, unit = row["estimate"], row["unit"]
        issue = ""
        if raw == "":
            issue = "missing_estimate"
        elif not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", raw):
            issue = "non_numeric"
        elif unit not in ("粒", "千粒"):
            issue = "unknown_unit"
        else:
            value = float(raw) * (1000 if unit == "千粒" else 1)
            if value < 0:
                issue = "negative_estimate"
        if issue:
            issues.append([number, row["record_id"], issue, "quarantine"])
            quarantine.append({**row, "reason": issue})
            continue
        high = value > 5000
        if high:
            issues.append([number, row["record_id"], "high_review", "retain_flag"])
        output.append([row["record_id"], row["participant_id"], int(row["round"]), value, "TRUE" if high else "FALSE"])
    result = pd.DataFrame(output, columns=["record_id","participant_id","round","estimate_grains","review_high"])
    flow = pd.DataFrame([
        ["raw",len(rows),len({r["participant_id"] for r in rows})],
        ["deduplicated",len(unique),len({r["participant_id"] for _,r in unique})],
        ["eligible",len(result),result.participant_id.nunique()]
    ], columns=["stage","records","participants"])
    return result, pd.DataFrame(issues,columns=["source_row","record_id","issue","action"]), pd.DataFrame(quarantine,columns=COLUMNS+["reason"]), flow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=BASE/"data/guesses_raw.csv")
    parser.add_argument("--out", type=Path, default=BASE/"results/python")
    args = parser.parse_args()
    result, issues, quarantine, flow = clean(args.input)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, frame in [("clean",result),("issues",issues),("quarantine",quarantine),("flow",flow)]:
        frame.to_csv(args.out/(name+".csv"),index=False,encoding="utf-8")
    fig, ax = plt.subplots(figsize=(6.4,3.6), layout="constrained")
    bars = ax.bar(flow.stage, flow.records, color=["#8a949d","#5c8a99","#276675"],width=0.55)
    ax.bar_label(bars)
    ax.set(ylabel="Number of records", ylim=(0,16), title="Teaching data: processing stages")
    ax.spines[["top","right"]].set_visible(False)
    for suffix in ("png","svg"):
        fig.savefig(args.out/("quality-flow."+suffix), dpi=160)
        if args.out.resolve() == (BASE/"results/python").resolve():
            (BASE/"figures").mkdir(exist_ok=True)
            fig.savefig(BASE/"figures"/("quality-flow."+suffix), dpi=160)
    plt.close(fig)
    print(flow.to_string(index=False))

if __name__ == "__main__":
    main()
