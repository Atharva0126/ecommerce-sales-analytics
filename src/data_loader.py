import pandas as pd
from pathlib import Path

def load_raw_data():
    path = Path("data/raw/ecommerce_sales.csv")

    if not path.exists():
        raise FileNotFoundError(
            "Dataset not found. Place ecommerce_sales.csv inside data/raw/"
        )

    df = pd.read_csv(path)
    return df
