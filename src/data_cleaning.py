import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Drop missing Sales/Profit
    df.dropna(subset=["Sales", "Profit"], inplace=True)

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Strip spaces from date column values
    df["Order Date"] = df["Order Date"].astype(str).str.strip()

    # ---- Try multiple date formats safely ----
    try:
        df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    except:
        try:
            df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
        except:
            df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=["Order Date"])

    return df
