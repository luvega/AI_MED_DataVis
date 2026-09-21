from pathlib import Path
import pandas as pd
base = Path(__file__).resolve().parents[1]
a = pd.read_csv(base/"data/guesses_raw.csv",dtype=str,keep_default_na=False,encoding="utf-8")
b = pd.read_csv(base/"data/guesses_gb18030.csv",dtype=str,keep_default_na=False,encoding="gb18030")
c = pd.read_excel(base/"data/guesses.xlsx",sheet_name="guesses",dtype=str,keep_default_na=False)
pd.testing.assert_frame_equal(a,b)
pd.testing.assert_frame_equal(a,c)
print("PASS: UTF-8 / GB18030 / Excel, identical 14 x 5 text cells")
