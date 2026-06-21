# charts.py

import plotly.express as px


def sales_by_country(df):

    data = (
        df.groupby("Country")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        data,
        x="Country",
        y="Sales",
        title="Ventes par pays"
    )

    return fig


def profit_by_product(df):

    data = (
        df.groupby("Product")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        data,
        names="Product",
        values="Profit",
        title="Répartition du profit"
    )

    return fig


def sales_over_time(df):

    data = (
        df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        data,
        x="Date",
        y="Sales",
        title="Evolution des ventes"
    )

    return fig


def segment_analysis(df):

    data = (
        df.groupby("Segment")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Segment",
        y="Profit",
        title="Profit par segment"
    )

    return fig
