import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Sales", "Profit"], inplace=True)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df
