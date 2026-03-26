import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from src.data_loader import load_raw_data
from src.data_cleaning import clean_data
from src.feature_engineering import add_features
from dashboard import render_dashboard

st.set_page_config(page_title="E-Commerce BI Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111827;
}
.main {
    background-color: #0F172A;
}
.footer {
    text-align:center;
    padding:20px;
    color:gray;
}
</style>
""", unsafe_allow_html=True)


# ---------------- FILE LOADER ----------------
def load_uploaded_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)

    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)

    elif file.name.endswith(".xml"):
        return pd.read_xml(file)

    else:
        st.error("Unsupported file type")
        return None


# ---------------- AUTO DETECT ----------------
def detect_columns(df):
    mapping = {}

    for col in df.columns:
        lc = col.lower()

        if "date" in lc:
            mapping["date"] = col
        elif "sales" in lc or "revenue" in lc or "amount" in lc:
            mapping["sales"] = col
        elif "profit" in lc:
            mapping["profit"] = col
        elif "quantity" in lc or "qty" in lc:
            mapping["quantity"] = col
        elif "category" in lc:
            mapping["category"] = col
        elif "region" in lc:
            mapping["region"] = col
        elif "customer" in lc:
            mapping["customer"] = col

    return mapping


# ---------------- COLUMN MAPPING UI ----------------
def column_mapper_ui(df, detected):

    st.sidebar.subheader("🔧 Map Columns")

    def select(label, key):
        default_index = 0
        if key in detected:
            try:
                default_index = df.columns.get_loc(detected[key])
            except:
                default_index = 0

        return st.sidebar.selectbox(label, df.columns, index=default_index)

    mapping = {
        "date": select("Date Column", "date"),
        "sales": select("Sales Column", "sales"),
        "profit": select("Profit Column", "profit"),
        "quantity": select("Quantity Column", "quantity"),
        "category": select("Category Column", "category"),
        "region": select("Region Column", "region"),
        "customer": select("Customer Column", "customer"),
    }

    return mapping


# ---------------- NORMALIZE ----------------
def normalize_df(df, mapping):

    df = df.rename(columns={
        mapping["date"]: "Order Date",
        mapping["sales"]: "Sales",
        mapping["profit"]: "Profit",
        mapping["quantity"]: "Quantity",
        mapping["category"]: "Category",
        mapping["region"]: "Region",
        mapping["customer"]: "Customer ID",
    })

    return df


# ---------------- DEFAULT DATA ----------------
@st.cache_data(show_spinner=False)
def load_default():
    raw_df = load_raw_data()
    df = clean_data(raw_df)
    df = add_features(df)
    return raw_df, df


# ---------------- MAIN ----------------
def main():

    st.sidebar.title("📂 Data Source")

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV / Excel / XML",
        type=["csv", "xlsx", "xml"]
    )

    # ---- If user uploads file ----
    if uploaded_file is not None:

        raw_df = load_uploaded_file(uploaded_file)

        if raw_df is None:
            return

        detected = detect_columns(raw_df)

        mapping = column_mapper_ui(raw_df, detected)

        df = normalize_df(raw_df, mapping)

        try:
            df = clean_data(df)
            df = add_features(df)
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return

    # ---- Default dataset ----
    else:
        raw_df, df = load_default()

    # ---- Filters ----
    st.sidebar.title("🔎 Filters")

    if "Year" in df.columns:
        year = st.sidebar.multiselect(
            "Year",
            sorted(df["Year"].unique()),
            default=sorted(df["Year"].unique())
        )
    else:
        year = []

    if "Region" in df.columns:
        region = st.sidebar.multiselect(
            "Region",
            df["Region"].unique(),
            default=df["Region"].unique()
        )
    else:
        region = []

    if "Category" in df.columns:
        category = st.sidebar.multiselect(
            "Category",
            df["Category"].unique(),
            default=df["Category"].unique()
        )
    else:
        category = []

    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["Year"].isin(year)]

    if region:
        filtered_df = filtered_df[filtered_df["Region"].isin(region)]

    if category:
        filtered_df = filtered_df[filtered_df["Category"].isin(category)]

    render_dashboard(raw_df, filtered_df)

    st.markdown(
        '<div class="footer">© 2026 | Dynamic BI Dashboard</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
