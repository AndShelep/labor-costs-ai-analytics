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

#research question №2
# Найбільші та найменші витрати (останній рік)
latest_year = int(df["year"].max())
latest_data = df[df["year"] == latest_year]

max_region = latest_data.loc[latest_data["costs"].idxmax()]
min_region = latest_data.loc[latest_data["costs"].idxmin()]

print("\n=== Highest & Lowest Regions in", latest_year, "===")
print("Max:", max_region["region"], max_region["costs"])
print("Min:", min_region["region"], min_region["costs"])

latest_sorted = latest_data.sort_values("costs", ascending=False)
top5 = latest_sorted.head(5)[["region", "year", "costs"]]
bottom5 = latest_sorted.tail(5)[["region", "year", "costs"]]

top5.to_csv(f"{OUT_DIR}/q2_top5_latest_year.csv", index=False)
bottom5.to_csv(f"{OUT_DIR}/q2_bottom5_latest_year.csv", index=False)

pd.DataFrame([
    {"type": "max", "year": latest_year, "region": max_region["region"], "costs": float(max_region["costs"])},
    {"type": "min", "year": latest_year, "region": min_region["region"], "costs": float(min_region["costs"])},
]).to_csv(f"{OUT_DIR}/q2_extremes_latest_year.csv", index=False)

# research question 3:
# Перевірка кризових років (середні зміни)
df_sorted = df.sort_values(["region", "year"]).copy()
df_sorted["lag"] = df_sorted.groupby("region")["costs"].shift(1)
df_sorted["change"] = df_sorted["costs"] - df_sorted["lag"]

crisis_years = df_sorted[df_sorted["year"].isin([2008, 2009, 2014, 2015])]

print("\n=== Crisis Years Changes ===")
crisis_mean = crisis_years.groupby("year")["change"].mean()
print(crisis_mean)

crisis_mean.reset_index().to_csv(f"{OUT_DIR}/q3_crisis_mean_change.csv", index=False)

crisis_years[["region", "year", "costs", "lag", "change"]].to_csv(
    f"{OUT_DIR}/q3_crisis_by_region.csv", index=False
)
