import os
import sqlite3
import pandas as pd


DB_PATH = "../db/labor_costs.db"
SOURCE_TABLE = "costs"
CLEANED_TABLE = "costs_cleaned"

PROCESSED_DIR = "../data/processed"
ARTIFACTS_DIR = "../artifacts/data_quality_analysis"

CLEANED_CSV_PATH = os.path.join(PROCESSED_DIR, "costs-clean.csv")
REPORT_PATH = os.path.join(ARTIFACTS_DIR, "quality_report.txt")


def load_data():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {SOURCE_TABLE}", conn)

    return df


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
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    df.to_csv(CLEANED_CSV_PATH, index=False)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(CLEANED_TABLE, conn, if_exists="replace", index=False)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("DATA QUALITY ANALYSIS REPORT\n")
        f.write("============================\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Columns: {df.columns.tolist()}\n")
        f.write(f"Missing costs before cleaning: {before_missing}\n")
        f.write(f"Missing costs after cleaning: {after_missing}\n")
        f.write(f"Cleaned file saved to: {CLEANED_CSV_PATH}\n")
        f.write(f"Cleaned table saved to database: {CLEANED_TABLE}\n")


def validate_columns(df):
    required_columns = ["costs", "region", "year"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in dataset")


def main():
    df = load_data()

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    validate_columns(df)

    print("Missing costs before cleaning:", df["costs"].isna().sum())

    cleaned_df, before_missing, after_missing = clean_data(df)

    print("\n=== AFTER ===")
    print("Columns:", cleaned_df.columns.tolist())
    print("Rows:", len(cleaned_df))
    print("Missing costs after cleaning:", after_missing)

    save_outputs(cleaned_df, before_missing, after_missing)

    print(f"\nSaved cleaned data to {CLEANED_CSV_PATH}")
    print(f"Saved report to {REPORT_PATH}")
    print(f"Saved cleaned table to database: {CLEANED_TABLE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error in data_quality_analysis:", e)
        raise