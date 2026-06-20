import streamlit as st
import pandas as pd
import plotly.express as px

from logique import preparer_donnees


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(page_title="Dashboard Ventes", layout="wide")
st.title("📊 Dashboard Ventes Intelligent")

# --------------------------------------------------
# UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    df = preparer_donnees(df)

    st.success("Données traitées")

    # --------------------------------------------------
    # TABLE
    # --------------------------------------------------

    st.subheader("Données")
    st.dataframe(df)

    # --------------------------------------------------
    # KPI
    # --------------------------------------------------

    st.subheader("KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "CA Total",
        f"{df['Montant Total Vente HT'].sum():,.0f}"
    )

    if "Profit" in df.columns:
        col2.metric(
            "Profit",
            f"{df['Profit'].sum():,.0f}"
        )

    col3.metric(
        "Lignes",
        len(df)
    )

    # --------------------------------------------------
    # GRAPHIQUE
    # --------------------------------------------------

    if "Mois" in df.columns:

        evo = df.groupby("Mois")["Montant Total Vente HT"].sum().reset_index()

        fig = px.bar(evo, x="Mois", y="Montant Total Vente HT")

        st.plotly_chart(fig, use_container_width=True)
