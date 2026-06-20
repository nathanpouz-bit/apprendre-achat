import pandas as pd

from logique import preparer_donnees


st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Dashboard Intelligent")

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:

    df = pd.read_excel(file)

    st.write("Colonnes originales :", df.columns)

    df = preparer_donnees(df)

    st.success("Données traitées")

    st.dataframe(df)

    # KPIs SAFE
    if "Montant Total Vente HT" in df.columns:
        st.metric("CA Total", df["Montant Total Vente HT"].sum())

    if "Profit" in df.columns:
        st.metric("Profit", df["Profit"].sum())
