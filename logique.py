import streamlit as st
import pandas as pd
import plotly.express as px

from logique import prepare


st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("🤖 Dashboard intelligent")

file = st.file_uploader("Upload Excel", type=["xlsx"])

query = st.text_input("💬 Décris ton analyse (ex: analyse mes ventes, par produit, par pays)")

if file:

    df = pd.read_excel(file)
    df, mapping = prepare(df)

    st.success("Données prêtes")

    # -----------------------------
    # KPIs toujours affichés
    # -----------------------------
    st.subheader("KPIs")
    col1, col2, col3 = st.columns(3)

    col1.metric("CA", f"{df['CA'].sum():,.0f}")
    col2.metric("Profit", f"{df['Profit'].sum():,.0f}")
    col3.metric("Lignes", len(df))

    # -----------------------------
    # ANALYSE TEXTE
    # -----------------------------

    q = query.lower()

    st.subheader("📊 Analyse automatique")

    # 1. PAR PRODUIT
    if "produit" in q or "product" in q:

        if "product" in mapping and mapping["product"]:

            data = df.groupby(mapping["product"])["CA"].sum().reset_index()

            fig = px.pie(data, values="CA", names=mapping["product"], title="CA par produit")
            st.plotly_chart(fig, use_container_width=True)

    # 2. PAR PAYS
    if "pays" in q or "country" in q:

        if "country" in mapping and mapping["country"]:

            data = df.groupby(mapping["country"])["CA"].sum().reset_index()

            fig = px.bar(data, x=mapping["country"], y="CA", title="CA par pays")
            st.plotly_chart(fig, use_container_width=True)

    # 3. EVOLUTION TEMPS
    if "date" in df.columns and ("temps" in q or "évolution" in q or "evolution" in q):

        evo = df.groupby("Date")["CA"].sum().reset_index()

        fig = px.line(evo, x="Date", y="CA", title="Évolution du CA")
        st.plotly_chart(fig, use_container_width=True)
