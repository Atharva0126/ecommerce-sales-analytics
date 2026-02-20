import streamlit as st
from src.data_loader import load_raw_data
from src.data_cleaning import clean_data
from src.feature_engineering import add_features
from app.dashboard import render_dashboard

st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- Premium CSS ----
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #111827;
}
.main {
    background-color: #0F172A;
}
.kpi-card {
    background: linear-gradient(135deg, #1E293B, #334155);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.footer {
    text-align:center;
    padding:20px;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process():
    df = load_raw_data()
    df = clean_data(df)
    df = add_features(df)
    return df


def main():
    df = load_and_process()

    st.sidebar.title("🔎 Filters")

    year = st.sidebar.multiselect(
        "Year",
        sorted(df["Year"].unique()),
        default=sorted(df["Year"].unique())
    )

    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        (df["Year"].isin(year)) &
        (df["Region"].isin(region)) &
        (df["Category"].isin(category))
    ]

    render_dashboard(filtered_df)

    st.markdown(
        '<div class="footer">© 2026 | E-Commerce BI Dashboard | Built by Atharva Pawar</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
