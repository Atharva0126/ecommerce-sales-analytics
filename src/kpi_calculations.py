def calculate_kpis(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    avg_order_value = total_sales / total_orders if total_orders else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Avg Order Value": avg_order_value,
        "Profit Margin %": profit_margin
    }
