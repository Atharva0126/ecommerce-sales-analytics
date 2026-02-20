import pandas as pd
from pathlib import Path

def load_raw_data():
    path = Path("data/raw/ecommerce_sales.csv")
    return pd.read_csv(path)

def save_processed_data(df):
    path = Path("data/processed/cleaned_data.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
