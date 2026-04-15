import os
import sqlite3
import pandas as pd


CSV_PATH = "../data/raw/costs.csv"
DB_DIR = "../db"
DB_PATH = os.path.join(DB_DIR, "labor_costs.db")
TABLE_NAME = "costs"

ARTIFACTS_DIR = "../artifacts/data_load"
REPORT_PATH = os.path.join(ARTIFACTS_DIR, "data_summary.txt")


def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    return df


def create_database(df: pd.DataFrame) -> None:
    os.makedirs(DB_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)


def save_report(df: pd.DataFrame) -> None:
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("DATA LOAD REPORT\n")
        f.write("=================\n")
        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n\n")
        f.write("Columns list:\n")
        for col in df.columns:
            f.write(f"- {col}\n")

        f.write("\nFirst 5 rows:\n")
        f.write(df.head().to_string())


def main() -> None:
    try:
        df = load_data()
        print("CSV успішно зчитано")
        print(df.head())

        create_database(df)
        print(f"Базу даних створено: {DB_PATH}")

        save_report(df)
        print(f"Звіт збережено: {REPORT_PATH}")

    except Exception as e:
        print("Помилка при завантаженні даних:", e)
        raise


if __name__ == "__main__":
    main()