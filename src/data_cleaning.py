import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Remove missing critical values
    df.dropna(subset=["Sales", "Profit"], inplace=True)

    # Strip column whitespace
    df.columns = df.columns.str.strip()

    # ---- Correct Date Parsing (Your Dataset Format: DD-MM-YYYY) ----
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%Y",   # <-- This matches your dataset
        errors="coerce"
    )

    # Remove invalid dates if any
    df = df.dropna(subset=["Order Date"])

    return df
