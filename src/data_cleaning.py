import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Drop rows where critical values missing
    df.dropna(subset=["Sales", "Profit"], inplace=True)

    # --- Robust Date Parsing ---
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce",       # converts invalid dates to NaT
        infer_datetime_format=True
    )

    # Remove rows where date failed
    df.dropna(subset=["Order Date"], inplace=True)

    return df
