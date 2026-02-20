import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Strip column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df = df.drop_duplicates()

    # Drop missing numeric critical values
    df = df.dropna(subset=["Sales", "Profit"])

    # Ensure date column exists
    if "Order Date" not in df.columns:
        raise ValueError("Order Date column not found in dataset")

    # Clean date column safely
    df["Order Date"] = (
        df["Order Date"]
        .astype(str)
        .str.strip()
    )

    # ✅ Robust automatic parsing (no hardcoded format)
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,        # IMPORTANT for your dataset (DD-MM-YYYY)
        errors="coerce"
    )

    # Drop rows where date parsing failed
    df = df.dropna(subset=["Order Date"])

    return df
