import pandas as pd

df = pd.read_csv("../data/raw/costs.csv")

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Missing costs:", df["costs"].isna().sum())

if "id" in df.columns:
    df = df.drop(columns=["id"])

df = df.sort_values(["region", "year"]).reset_index(drop=True)

prev_known = df.groupby("region")["costs"].ffill()

next_known = df.groupby("region")["costs"].bfill()

avg_between = (prev_known + next_known) / 2

df["costs"] = df["costs"].fillna(avg_between).fillna(prev_known).fillna(next_known)

print("\n=== AFTER ===")
print("Columns:", df.columns.tolist())
print("Rows:", len(df))
print("Missing costs:", df["costs"].isna().sum())

df.to_csv("../data/processed/costs-clean.csv", index=False)

print("\nSaved to data/processed/costs-clean.csv")