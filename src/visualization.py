from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go
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
        markers=True,
        title="Monthly Sales Trend"
    )

    fig.update_layout(template="plotly_dark")
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


def sales_forecast(df):

    # Aggregate monthly sales
    monthly = (
        df.groupby("Year-Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Year-Month")
    )

    # Convert to numeric index
    monthly["t"] = np.arange(len(monthly))

    X = monthly[["t"]]
    y = monthly["Sales"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 6 months
    future_steps = 6
    future_t = np.arange(len(monthly), len(monthly) + future_steps).reshape(-1, 1)
    predictions = model.predict(future_t)

    # Create future labels
    future_months = [f"Future-{i+1}" for i in range(future_steps)]

    # Plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["Year-Month"],
        y=monthly["Sales"],
        mode='lines+markers',
        name="Actual"
    ))

    fig.add_trace(go.Scatter(
        x=future_months,
        y=predictions,
        mode='lines+markers',
        name="Forecast"
    ))

    fig.update_layout(
        title="Sales Forecast (Next 6 Months)",
        template="plotly_dark"
    )

    return fig
