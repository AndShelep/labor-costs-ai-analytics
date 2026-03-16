import pandas as pd
import os


def load_data():
    df = pd.read_csv("./data/raw/costs.csv")
    return df


def save_report(df):
    os.makedirs("artifacts/data_load", exist_ok=True)

    report_path = "artifacts/data_load/data_summary.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("DATA LOAD REPORT\n")
        f.write("=================\n")
        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n\n")
        f.write("First 5 rows:\n")
        f.write(df.head().to_string())


if __name__ == "__main__":

    try:
        df = load_data()

        print("Перші 5 рядків даних:")
        print(df.head())

        save_report(df)

        print("Звіт збережено у artifacts/data_load/")

    except Exception as e:
        print("Помилка при завантаженні даних:", e)