import os
import time
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path


# === BASE PATH ===
BASE_DIR = Path(__file__).resolve().parents[1]

TABLES_DIR = Path(os.getenv("TABLES_DIR", BASE_DIR / "data" / "research-tables"))
FIG_DIR = Path(os.getenv("FIG_DIR", BASE_DIR / "artifacts" / "visualization"))


# === WAITING MECHANISM ===
def wait_for_file(path, timeout=60, interval=2):
    for _ in range(timeout // interval):
        if os.path.exists(path):
            return True
        print(f"[WAIT] Waiting for file: {path}")
        time.sleep(interval)
    return False


def check_required_file(path):
    if not wait_for_file(path):
        raise FileNotFoundError(f"Required file not found after waiting: {path}")


# === Q1 ===
def plot_q1():
    q1_path = TABLES_DIR / "q1_ukraine_trend.csv"
    check_required_file(q1_path)

    q1 = pd.read_csv(q1_path)

    plt.figure(figsize=(9, 5))
    plt.plot(q1["year"], q1["costs"], marker="o")
    plt.title("Q1: Long-term Trend of Labor Costs (Ukraine, 2005–2019)")
    plt.xlabel("Year")
    plt.ylabel("Costs")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "q1_ukraine_trend.png", dpi=200)
    plt.close()

    if "yoy_change" in q1.columns:
        plt.figure(figsize=(9, 5))
        plt.bar(q1["year"], q1["yoy_change"])
        plt.title("Q1: Year-over-Year Change (Ukraine)")
        plt.xlabel("Year")
        plt.ylabel("YoY change")
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "q1_ukraine_yoy_change.png", dpi=200)
        plt.close()


# === Q2 ===
def plot_q2():
    top5_path = TABLES_DIR / "q2_top5_latest_year.csv"
    bottom5_path = TABLES_DIR / "q2_bottom5_latest_year.csv"

    check_required_file(top5_path)
    check_required_file(bottom5_path)

    top5 = pd.read_csv(top5_path)
    bottom5 = pd.read_csv(bottom5_path)

    year_top = int(top5["year"].iloc[0]) if "year" in top5.columns else "latest"

    plt.figure(figsize=(9, 5))
    plt.bar(top5["region"], top5["costs"])
    plt.title(f"Q2: Top 5 Regions by Costs ({year_top})")
    plt.xlabel("Region")
    plt.ylabel("Costs")
    plt.xticks(rotation=30, ha="right")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "q2_top5_regions.png", dpi=200)
    plt.close()

    year_bottom = int(bottom5["year"].iloc[0]) if "year" in bottom5.columns else "latest"

    plt.figure(figsize=(9, 5))
    plt.bar(bottom5["region"], bottom5["costs"])
    plt.title(f"Q2: Bottom 5 Regions by Costs ({year_bottom})")
    plt.xlabel("Region")
    plt.ylabel("Costs")
    plt.xticks(rotation=30, ha="right")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "q2_bottom5_regions.png", dpi=200)
    plt.close()

    extremes_path = TABLES_DIR / "q2_extremes_latest_year.csv"
    if extremes_path.exists():
        ext = pd.read_csv(extremes_path)
        year_ext = int(ext["year"].iloc[0]) if "year" in ext.columns else "latest"

        plt.figure(figsize=(6, 4))
        plt.bar(ext["type"], ext["costs"])
        plt.title(f"Q2: Max vs Min Costs ({year_ext})")
        plt.xlabel("Type")
        plt.ylabel("Costs")
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "q2_extremes_max_min.png", dpi=200)
        plt.close()


# === Q3 ===
def plot_q3():
    q3_path = TABLES_DIR / "q3_crisis_mean_change.csv"
    check_required_file(q3_path)

    q3 = pd.read_csv(q3_path)

    if "change" in q3.columns:
        y = q3["change"]
        y_label = "Mean change (costs - previous year)"
        title = "Q3: Mean Change in Crisis Years"
        filename = "q3_crisis_mean_change.png"
    else:
        y = q3.iloc[:, 1]
        y_label = q3.columns[1]
        title = "Q3: Crisis Years Metric"
        filename = "q3_crisis_metric.png"

    plt.figure(figsize=(8, 5))
    plt.plot(q3["year"], y, marker="o")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=200)
    plt.close()


# === FORECAST ===
def plot_forecast():
    hist_path = TABLES_DIR / "q1_ukraine_trend.csv"
    check_required_file(hist_path)

    hist = pd.read_csv(hist_path).sort_values("year")

    plt.figure(figsize=(9, 5))
    plt.plot(hist["year"], hist["costs"], marker="o", label="Historical")

    fitted_path = TABLES_DIR / "arima_ukraine_fitted.csv"
    if fitted_path.exists():
        fitted = pd.read_csv(fitted_path).sort_values("year")
        plt.plot(fitted["year"], fitted["fitted_costs"], label="ARIMA fitted")

    forecast_path = TABLES_DIR / "arima_ukraine_forecast.csv"
    if forecast_path.exists():
        fc = pd.read_csv(forecast_path).sort_values("year")
        plt.plot(fc["year"], fc["forecast_costs"], marker="o", label="Forecast")

    plt.title("ARIMA Forecast (Ukraine)")
    plt.xlabel("Year")
    plt.ylabel("Costs")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "arima_ukraine_forecast.png", dpi=200)
    plt.close()


# === MAIN ===
def main():
    os.makedirs(FIG_DIR, exist_ok=True)

    print("Starting visualization service...")

    plot_q1()
    plot_q2()
    plot_q3()
    plot_forecast()

    print("Graphs successfully generated!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error in visualization:", e)
        raise