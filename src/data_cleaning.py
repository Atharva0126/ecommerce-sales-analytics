import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Clean column names
    df.columns = df.columns.str.strip()

    required_cols = ["Order Date", "Sales", "Profit", "Quantity"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert numeric columns safely
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    # Drop rows with missing numeric values
    df = df.dropna(subset=["Sales", "Profit", "Quantity"])

    # -------- ROBUST DATE PARSING --------
    # Step 1: convert to string
    df["Order Date"] = df["Order Date"].astype(str).str.strip()

    # Step 2: parse flexibly
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Step 3: remove failed parses
    df = df.dropna(subset=["Order Date"])

    return df
