import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def save_csv(df, filename):
    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(f"{OUT_DIR}/{filename}", index=False)

OUT_DIR = "reports/research-tables"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv("../data/processed/costs-clean.csv")

#research question №1
# Довгострокова тенденція (по Україні загалом)
ukraine_df = df[df["region"] == "Україна"].sort_values("year")

print("\n--- Long-term trend (Ukraine) ---")
print(ukraine_df[["year", "costs"]])

growth = ukraine_df["costs"].iloc[-1] - ukraine_df["costs"].iloc[0]
print("Total growth (2005–2019):", growth)

ukraine_trend = ukraine_df[["year", "costs"]].copy()
ukraine_trend["yoy_change"] = ukraine_trend["costs"].diff()
ukraine_trend["yoy_pct"] = (ukraine_trend["costs"].pct_change() * 100).round(2)
ukraine_trend.to_csv(f"{OUT_DIR}/q1_ukraine_trend.csv", index=False)

pd.DataFrame([{
    "start_year": int(ukraine_trend["year"].min()),
    "end_year": int(ukraine_trend["year"].max()),
    "start_costs": float(ukraine_trend["costs"].iloc[0]),
    "end_costs": float(ukraine_trend["costs"].iloc[-1]),
    "total_growth": float(growth),
}]).to_csv(f"{OUT_DIR}/q1_ukraine_summary.csv", index=False)