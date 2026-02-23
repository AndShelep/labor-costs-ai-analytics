import pandas as pd

def load_data():
    df = pd.read_csv("../data/raw/costs.csv")
    return df


if __name__ == "__main__":
    df = load_data()
    print("Перші 5 рядків даних:")
    print(df.head())