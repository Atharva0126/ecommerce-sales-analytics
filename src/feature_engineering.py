def add_features(df):
    df = df.copy()

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()
    df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

    df["Profit Ratio"] = df["Profit"] / df["Sales"]

    return df
