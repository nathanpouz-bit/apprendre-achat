import streamlit as st
import pandas as pd
from logique import preparer_donnees

st.set_page_config(page_title="Dashboard Auto", layout="wide")

st.title("📊 Dashboard Auto-Adaptatif")

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:

    df = pd.read_excel(file)

    st.subheader("Colonnes détectées")
    st.write(df.columns)

    df = preparer_donnees(df)

    st.success("Analyse automatique terminée")

    st.subheader("Données")
    st.dataframe(df)

    st.subheader("KPIs")

    st.metric("CA", df["Montant Total Vente HT"].sum())

    if "Profit" in df.columns:
        st.metric("Profit", df["Profit"].sum())

    import streamlit as st
import pandas as pd
import plotly.express as px

from logique import prepare


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("🤖 Dashboard Intelligent (No-Code)")

file = st.file_uploader("Upload Excel", type=["xlsx"])

command = st.text_input("💬 Tape : analyse mes ventes")

# --------------------------------------------------
# APP
# --------------------------------------------------

if file:

    df = pd.read_excel(file)

    df, mapping = prepare(df)

    st.success("Données analysées automatiquement")

    # --------------------------------------------------
    # MODE IA
    # --------------------------------------------------

    if "analyse" in command.lower():

        st.subheader("📊 KPIs automatiques")

        col1, col2, col3 = st.columns(3)

        col1.metric("CA Total", f"{df['CA'].sum():,.0f}")
        col2.metric("Profit", f"{df['Profit'].sum():,.0f}")
        col3.metric("Lignes", len(df))

        # --------------------------------------------------
        # GRAPHIQUE 1 : EVOLUTION
        # --------------------------------------------------

        if "Date" in df.columns:

            evo = df.groupby("Date")[["CA", "Profit"]].sum().reset_index()

            fig = px.line(evo, x="Date", y="CA", title="Évolution CA")
            st.plotly_chart(fig, use_container_width=True)

        # --------------------------------------------------
        # GRAPHIQUE 2 : PRODUITS
        # --------------------------------------------------

        if "product" in mapping and mapping["product"]:

            prod = df.groupby(mapping["product"])["CA"].sum().reset_index()

            fig2 = px.pie(prod, values="CA", names=mapping["product"])
            st.plotly_chart(fig2, use_container_width=True)

        # --------------------------------------------------
        # GRAPHIQUE 3 : PAYS
        # --------------------------------------------------

        if "country" in mapping and mapping["country"]:

            pays = df.groupby(mapping["country"])["CA"].sum().reset_index()

            fig3 = px.bar(pays, x=mapping["country"], y="CA")
            st.plotly_chart(fig3, use_container_width=True)

    # --------------------------------------------------
    # TABLE
    # --------------------------------------------------

    st.subheader("Données")

    st.dataframe(df)

    st.metric("Lignes", len(df))
