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

    st.metric("Lignes", len(df))
