import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

OUT_DIR = "./data/research-tables"
ARTIFACTS_DIR = "artifacts/data_research"


def save_csv(df, filename):
    os.makedirs(OUT_DIR, exist_ok=True)
    df.to_csv(f"{OUT_DIR}/{filename}", index=False)


def load_data():
    return pd.read_csv("./data/processed/costs-clean.csv")


def research_q1(df):
    ukraine_df = df[df["region"] == "Україна"].sort_values("year")

    print("\n--- Long-term trend (Ukraine) ---")
    print(ukraine_df[["year", "costs"]])

    growth = ukraine_df["costs"].iloc[-1] - ukraine_df["costs"].iloc[0]
    print("Total growth (2005–2019):", growth)

    ukraine_trend = ukraine_df[["year", "costs"]].copy()
    ukraine_trend["yoy_change"] = ukraine_trend["costs"].diff()
    ukraine_trend["yoy_pct"] = (ukraine_trend["costs"].pct_change() * 100).round(2)

    save_csv(ukraine_trend, "q1_ukraine_trend.csv")

    summary = pd.DataFrame([{
        "start_year": int(ukraine_trend["year"].min()),
        "end_year": int(ukraine_trend["year"].max()),
        "start_costs": float(ukraine_trend["costs"].iloc[0]),
        "end_costs": float(ukraine_trend["costs"].iloc[-1]),
        "total_growth": float(growth),
    }])

    save_csv(summary, "q1_ukraine_summary.csv")
    return growth, ukraine_df


def research_q2(df):
    latest_year = int(df["year"].max())
    latest_data = df[df["year"] == latest_year]

    max_region = latest_data.loc[latest_data["costs"].idxmax()]
    min_region = latest_data.loc[latest_data["costs"].idxmin()]

    print(f"\n=== Highest & Lowest Regions in {latest_year} ===")
    print("Max:", max_region["region"], max_region["costs"])
    print("Min:", min_region["region"], min_region["costs"])

    latest_sorted = latest_data.sort_values("costs", ascending=False)
    top5 = latest_sorted.head(5)[["region", "year", "costs"]]
    bottom5 = latest_sorted.tail(5)[["region", "year", "costs"]]

    save_csv(top5, "q2_top5_latest_year.csv")
    save_csv(bottom5, "q2_bottom5_latest_year.csv")

    extremes = pd.DataFrame([
        {"type": "max", "year": latest_year, "region": max_region["region"], "costs": float(max_region["costs"])},
        {"type": "min", "year": latest_year, "region": min_region["region"], "costs": float(min_region["costs"])},
    ])
    save_csv(extremes, "q2_extremes_latest_year.csv")

    return latest_year, max_region["region"], min_region["region"]


def research_q3(df):
    df_sorted = df.sort_values(["region", "year"]).copy()
    df_sorted["lag"] = df_sorted.groupby("region")["costs"].shift(1)
    df_sorted["change"] = df_sorted["costs"] - df_sorted["lag"]

    crisis_years = df_sorted[df_sorted["year"].isin([2008, 2009, 2014, 2015])]

    print("\n=== Crisis Years Changes ===")
    crisis_mean = crisis_years.groupby("year")["change"].mean()
    print(crisis_mean)

    save_csv(crisis_mean.reset_index(), "q3_crisis_mean_change.csv")
    save_csv(crisis_years[["region", "year", "costs", "lag", "change"]], "q3_crisis_by_region.csv")

    return crisis_mean


def run_forecast(ukraine_df):
    series = ukraine_df.set_index("year")["costs"]

    model = ARIMA(series, order=(1, 1, 1))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=1)

    print("Forecast for the next year:")
    print(forecast)

    forecast_df = forecast.reset_index()
    forecast_df.columns = ["year", "forecast_costs"]
    save_csv(forecast_df, "arima_ukraine_forecast.csv")

    fitted_df = model_fit.fittedvalues.reset_index()
    fitted_df.columns = ["year", "fitted_costs"]
    save_csv(fitted_df, "arima_ukraine_fitted.csv")

    return forecast_df


def save_report(growth, latest_year, max_region_name, min_region_name):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    report_path = f"{ARTIFACTS_DIR}/research_report.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("DATA RESEARCH REPORT\n")
        f.write("====================\n")
        f.write(f"Ukraine total growth over the study period: {growth}\n")
        f.write(f"Latest year in dataset: {latest_year}\n")
        f.write(f"Region with highest costs in latest year: {max_region_name}\n")
        f.write(f"Region with lowest costs in latest year: {min_region_name}\n")
        f.write(f"Research tables saved to: {OUT_DIR}\n")


def main():
    df = load_data()

    required_columns = ["region", "year", "costs"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in dataset")

    growth, ukraine_df = research_q1(df)
    latest_year, max_region_name, min_region_name = research_q2(df)
    research_q3(df)
    run_forecast(ukraine_df)
    save_report(growth, latest_year, max_region_name, min_region_name)

    print(f"\nResearch results saved to {OUT_DIR}")
    print(f"Artifact report saved to {ARTIFACTS_DIR}/research_report.txt")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error in data_research:", e)
        raise