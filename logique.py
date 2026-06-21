import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Commercial", layout="wide")

st.title("📊 Dashboard Commercial")

uploaded_file = st.file_uploader(
    "Choisir un fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # KPI
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_units = df["Units Sold"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("CA Total", f"{total_sales:,.0f} €")
    col2.metric("Profit Total", f"{total_profit:,.0f} €")
    col3.metric("Unités Vendues", f"{total_units:,.0f}")

    # Filtres
    countries = st.multiselect(
        "Pays",
        df["Country"].unique(),
        default=df["Country"].unique()
    )

    filtered_df = df[df["Country"].isin(countries)]

    # Ventes par pays
    sales_country = (
        filtered_df
        .groupby("Country")["Sales"]
        .sum()
        .reset_index()
    )

    fig_country = px.bar(
        sales_country,
        x="Country",
        y="Sales",
        title="Ventes par pays"
    )

    st.plotly_chart(fig_country, use_container_width=True)

    # Profit par produit
    profit_product = (
        filtered_df
        .groupby("Product")["Profit"]
        .sum()
        .reset_index()
    )

    fig_product = px.pie(
        profit_product,
        names="Product",
        values="Profit",
        title="Répartition du profit"
    )

    st.plotly_chart(fig_product, use_container_width=True)
