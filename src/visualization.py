import plotly.express as px

def monthly_sales_trend(df):
    monthly = (
        df.groupby("Year-Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Year-Month")
    )

    fig = px.line(
        monthly,
        x="Year-Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Total Sales"
    )

    return fig


def sales_by_category(df):
    category = df.groupby("Category")["Sales"].sum().reset_index()

    fig = px.bar(
        category,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def region_sales(df):
    region = df.groupby("Region")["Sales"].sum().reset_index()

    fig = px.bar(
        region,
        x="Region",
        y="Sales",
        color="Region",
        title="Region-wise Sales"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def correlation_heatmap(df):
    corr = df[["Sales", "Profit", "Quantity"]].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Correlation Heatmap"
    )
    fig.update_layout(template="plotly_dark")
    return fig
