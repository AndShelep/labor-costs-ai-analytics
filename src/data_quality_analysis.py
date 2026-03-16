import os
import pandas as pd


def load_data():
    return pd.read_csv("./data/raw/costs.csv")


def clean_data(df):
    before_missing = df["costs"].isna().sum()

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    df = df.sort_values(["region", "year"]).reset_index(drop=True)

    prev_known = df.groupby("region")["costs"].ffill()
    next_known = df.groupby("region")["costs"].bfill()
    avg_between = (prev_known + next_known) / 2

    df["costs"] = df["costs"].fillna(avg_between).fillna(prev_known).fillna(next_known)

    after_missing = df["costs"].isna().sum()

    return df, before_missing, after_missing


def save_outputs(df, before_missing, after_missing):
    os.makedirs("./data/processed", exist_ok=True)
    os.makedirs("artifacts/data_quality_analysis", exist_ok=True)

    cleaned_path = "./data/processed/costs-clean.csv"
    report_path = "artifacts/data_quality_analysis/quality_report.txt"

    df.to_csv(cleaned_path, index=False)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("DATA QUALITY ANALYSIS REPORT\n")
        f.write("============================\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Columns: {df.columns.tolist()}\n")
        f.write(f"Missing costs before cleaning: {before_missing}\n")
        f.write(f"Missing costs after cleaning: {after_missing}\n")
        f.write(f"Cleaned file saved to: {cleaned_path}\n")


def main():
    df = load_data()

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    if "costs" not in df.columns:
        raise ValueError("Column 'costs' not found in dataset")
    if "region" not in df.columns:
        raise ValueError("Column 'region' not found in dataset")
    if "year" not in df.columns:
        raise ValueError("Column 'year' not found in dataset")

    print("Missing costs before cleaning:", df["costs"].isna().sum())

    cleaned_df, before_missing, after_missing = clean_data(df)

    print("\n=== AFTER ===")
    print("Columns:", cleaned_df.columns.tolist())
    print("Rows:", len(cleaned_df))
    print("Missing costs after cleaning:", after_missing)

    save_outputs(cleaned_df, before_missing, after_missing)

    print("\nSaved cleaned data to ./data/processed/costs-clean.csv")
    print("Saved report to artifacts/data_quality_analysis/quality_report.txt")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error in data_quality_analysis:", e)
        raise