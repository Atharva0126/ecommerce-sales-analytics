import streamlit as st
from src.kpi_calculations import calculate_kpis
from src.visualization import (
    monthly_sales_trend,
    sales_by_category,
    region_sales,
    correlation_heatmap
)

def render_dashboard(raw_df, df):

    st.title("📊 E-Commerce Sales Analytics & Business Intelligence")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Overview", "Sales Analysis", "Customer Insights", "Statistics", "Data Explorer"]
    )

    # ---- Overview ----
    with tab1:
        st.subheader("Executive KPI Summary")

        kpis = calculate_kpis(df)
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Sales", f"${kpis['Total Sales']:,.0f}")
        col2.metric("Total Profit", f"${kpis['Total Profit']:,.0f}")
        col3.metric("Total Orders", f"{kpis['Total Orders']}")
        col4.metric("Avg Order Value", f"${kpis['Avg Order Value']:,.2f}")
        col5.metric("Profit Margin", f"{kpis['Profit Margin %']:.2f}%")

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

    # ---- Data Explorer ----
    with tab5:
        st.subheader("Data Explorer")

        data_option = st.radio(
            "Select Data View:",
            ["Raw Data", "Cleaned & Filtered Data"]
        )

        if data_option == "Raw Data":
            selected_df = raw_df
        else:
            selected_df = df

        st.write("### Dataset Shape")
        st.write(f"Rows: {selected_df.shape[0]}, Columns: {selected_df.shape[1]}")

        st.write("### Column Names")
        st.write(list(selected_df.columns))

        st.write("### Preview")
        st.dataframe(selected_df.head(50), use_container_width=True)

        st.write("### Summary Statistics")
        st.dataframe(selected_df.describe(), use_container_width=True)

        st.download_button(
            label="Download Selected Data",
            data=selected_df.to_csv(index=False),
            file_name="data_export.csv",
            mime="text/csv"
        )
