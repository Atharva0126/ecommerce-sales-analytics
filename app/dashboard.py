import streamlit as st
from src.kpi_calculations import calculate_kpis
from src.visualization import (
    monthly_sales_trend,
    sales_by_category,
    region_sales,
    correlation_heatmap
)

def render_dashboard(df):

    st.title("📊 E-Commerce Sales Analytics & Business Intelligence")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Sales Analysis", "Customer Insights", "Statistics"]
    )

    # ---- Overview ----
    with tab1:
        st.subheader("Executive KPI Summary")

        kpis = calculate_kpis(df)
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.markdown(f'<div class="kpi-card"><h4>Total Sales</h4><h2>${kpis["Total Sales"]:,.0f}</h2></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="kpi-card"><h4>Total Profit</h4><h2>${kpis["Total Profit"]:,.0f}</h2></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="kpi-card"><h4>Total Orders</h4><h2>{kpis["Total Orders"]}</h2></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="kpi-card"><h4>Avg Order Value</h4><h2>${kpis["Avg Order Value"]:,.2f}</h2></div>', unsafe_allow_html=True)
        col5.markdown(f'<div class="kpi-card"><h4>Profit Margin</h4><h2>{kpis["Profit Margin %"]:.2f}%</h2></div>', unsafe_allow_html=True)

    # ---- Sales ----
    with tab2:
        col1, col2 = st.columns(2)
        col1.plotly_chart(monthly_sales_trend(df), use_container_width=True)
        col2.plotly_chart(sales_by_category(df), use_container_width=True)
        st.plotly_chart(region_sales(df), use_container_width=True)

    # ---- Customers ----
    with tab3:
        st.subheader("Top 10 Customers by Revenue")
        top_customers = df.groupby("Customer ID")["Sales"].sum().nlargest(10).reset_index()
        st.dataframe(top_customers, use_container_width=True)

        st.download_button(
            label="Download Filtered Data",
            data=df.to_csv(index=False),
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )

    # ---- Statistics ----
    with tab4:
        st.plotly_chart(correlation_heatmap(df), use_container_width=True)
