import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Dashboard Intelligent", layout="wide")
st.title("📊 Dashboard Intelligent (auto-adaptatif)")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

# ----------------------------
# NORMALISATION
# ----------------------------
def normalize(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())

mapping = {
    "chiffredaffaires": "CA",
    "ca": "CA",
    "sales": "CA",
    "revenue": "CA",

    "profit": "Profit",
    "benefice": "Profit",
    "margin": "Profit",

    "cost": "Cost",
    "costs": "Cost",
    "expenses": "Cost",
    "achat": "Cost",
    "achats": "Cost",

    "date": "Date",
    "jour": "Date",

    "pays": "Pays",
    "country": "Pays",

    "produit": "Produit",
    "product": "Produit"
}

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # ----------------------------
    # RENOMMAGE INTELLIGENT
    # ----------------------------
    new_cols = {}

    for col in df.columns:
        key = normalize(col)
        if key in mapping:
            new_cols[col] = mapping[key]

    df = df.rename(columns=new_cols)

    st.write("📌 Colonnes détectées :", df.columns)

    # ----------------------------
    # CONVERSION DATE
    # ----------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------
    # KPI (ROBUSTES)
    # ----------------------------
    st.subheader("📌 Résumé global")

    col1, col2, col3, col4 = st.columns(4)

    if "CA" in df.columns:
        col1.metric("💰 Chiffre d'affaires", f"{df['CA'].sum():,.0f}")
    else:
        col1.metric("💰 CA", "N/A")

    if "Cost" in df.columns:
        col2.metric("📉 Achats / Coûts", f"{df['Cost'].sum():,.0f}")
    else:
        col2.metric("📉 Coûts", "N/A")

    if "Profit" in df.columns:
        col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f}")
    else:
        if "CA" in df.columns and "Cost" in df.columns:
            df["Profit"] = df["CA"] - df["Cost"]
            col3.metric("📈 Profit", f"{df['Profit'].sum():,.0f}")
        else:
            col3.metric("📈 Profit", "N/A")

    col4.metric("📊 Lignes", len(df))

    # ----------------------------
    # FILTRES
    # ----------------------------
    st.sidebar.header("🔎 Filtres")

    if "Pays" in df.columns:
        pays = st.sidebar.multiselect(
            "Pays",
            df["Pays"].dropna().unique(),
            default=df["Pays"].dropna().unique()
        )
        df = df[df["Pays"].isin(pays)]

    if "Produit" in df.columns:
        produits = st.sidebar.multiselect(
            "Produits",
            df["Produit"].dropna().unique(),
            default=df["Produit"].dropna().unique()
        )
        df = df[df["Produit"].isin(produits)]

    # ----------------------------
    # EVOLUTION CA
    # ----------------------------
    st.subheader("📈 Évolution")

    if "Date" in df.columns and "CA" in df.columns:
        evo = df.groupby("Date")["CA"].sum().reset_index()
        fig = px.line(evo, x="Date", y="CA", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # PAYS
    # ----------------------------
    if "Pays" in df.columns and "CA" in df.columns:
        st.subheader("🌍 CA par pays")
        pays_df = df.groupby("Pays")["CA"].sum().reset_index()
        fig = px.pie(pays_df, values="CA", names="Pays")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # PRODUITS
    # ----------------------------
    if "Produit" in df.columns and "CA" in df.columns:
        st.subheader("📦 CA par produit")
        prod_df = df.groupby("Produit")["CA"].sum().reset_index()
        fig = px.pie(prod_df, values="CA", names="Produit")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # TABLE
    # ----------------------------
    st.subheader("📋 Données")
    st.dataframe(df, use_container_width=True)
    
    
    import pandas as pd


def preparer_donnees(df):
    """
    Ajoute toutes les colonnes calculées.
    """

    # --------------------------------------------------
    # DATE
    # --------------------------------------------------

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Annee"] = df["Date"].dt.year
    df["NumeroMois"] = df["Date"].dt.month
    df["Mois"] = df["Date"].dt.month_name()

    # --------------------------------------------------
    # TVA
    # --------------------------------------------------

    if "Montant TVA" not in df.columns:

        if (
            "Prix TTC" in df.columns
            and "Prix HT" in df.columns
        ):
            df["Montant TVA"] = (
                df["Prix TTC"] - df["Prix HT"]
            )

    # --------------------------------------------------
    # MONTANT DE VENTE HT
    # --------------------------------------------------

    df["Montant Vente HT"] = (
        df["Quantite"] * df["Prix HT"]
    )

    # --------------------------------------------------
    # DISCOUNT OUI / NON
    # --------------------------------------------------

    if "Reduction" in df.columns:

        df["Discount"] = df["Reduction"].apply(
            lambda x: "Oui" if x > 0 else "Non"
        )

    # --------------------------------------------------
    # MONTANT TOTAL APRES REDUCTION
    # --------------------------------------------------

    if "Reduction" in df.columns:

        df["Montant Total Vente HT"] = (
            df["Montant Vente HT"] - df["Reduction"]
        )

    else:

        df["Montant Total Vente HT"] = (
            df["Montant Vente HT"]
        )

    # --------------------------------------------------
    # PROFIT
    # --------------------------------------------------

    if "Cout" in df.columns:

        df["Profit"] = (
            df["Montant Total Vente HT"]
            - df["Cout"]
        )

    return df

import streamlit as st
import pandas as pd

from logique import preparer_donnees


st.title("Dashboard Ventes")

uploaded_file = st.file_uploader(
    "Choisir un fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    df = preparer_donnees(df)

    st.success("Colonnes calculées")

    st.dataframe(df)

import pandas as pd
import re


# --------------------------------------------------
# NORMALISATION DES COLONNES
# --------------------------------------------------

def normaliser_colonne(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())


def renommer_colonnes(df):

    mapping = {
        # DATE
        "date": "Date",

        # QUANTITE
        "quantity": "Quantite",
        "quantite": "Quantite",
        "qty": "Quantite",

        # PRIX HT
        "prixht": "Prix HT",
        "priceht": "Prix HT",
        "unitprice": "Prix HT",

        # PRIX TTC
        "prixttc": "Prix TTC",
        "totalprice": "Prix TTC",

        # REDUCTION
        "reduction": "Reduction",
        "discount": "Reduction",

        # COUT
        "cout": "Cout",
        "cost": "Cout",
        "costprice": "Cout"
    }

    new_cols = {}

    for col in df.columns:
        key = normaliser_colonne(col)
        if key in mapping:
            new_cols[col] = mapping[key]

    return df.rename(columns=new_cols)


# --------------------------------------------------
# CALCUL DES COLONNES
# --------------------------------------------------

def preparer_donnees(df):

    df = renommer_colonnes(df)

    # -----------------------------
    # DATE
    # -----------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        df["Annee"] = df["Date"].dt.year
        df["NumeroMois"] = df["Date"].dt.month
        df["Mois"] = df["Date"].dt.month_name()


    # -----------------------------
    # TVA
    # -----------------------------
    if "Prix TTC" in df.columns and "Prix HT" in df.columns:

        df["Montant TVA"] = df["Prix TTC"] - df["Prix HT"]


    # -----------------------------
    # MONTANT VENTE HT
    # -----------------------------
    if "Quantite" in df.columns and "Prix HT" in df.columns:

        df["Montant Vente HT"] = (
            df["Quantite"] * df["Prix HT"]
        )


    # -----------------------------
    # REDUCTION (€/ ou %)
    # -----------------------------
    if "Reduction" in df.columns:

        # détecter si c'est %
        # (heuristique simple : si max > 1 → probablement %)
        if df["Reduction"].max() > 1:

            df["Reduction €"] = (
                df["Montant Vente HT"]
                * df["Reduction"] / 100
            )

        else:

            df["Reduction €"] = df["Reduction"]

        df["Discount"] = df["Reduction"].apply(
            lambda x: "Oui" if x > 0 else "Non"
        )

    else:

        df["Reduction €"] = 0
        df["Discount"] = "Non"


    # -----------------------------
    # MONTANT TOTAL HT
    # -----------------------------
    df["Montant Total Vente HT"] = (
        df["Montant Vente HT"] - df["Reduction €"]
    )


    # -----------------------------
    # PROFIT
    # -----------------------------
    if "Cout" in df.columns:

        df["Profit"] = (
            df["Montant Total Vente HT"]
            - df["Cout"]
        )

    return df

import streamlit as st
import pandas as pd
from logique import preparer_donnees


st.title("📊 Dashboard Ventes Intelligent")

uploaded_file = st.file_uploader(
    "Upload Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    df = preparer_donnees(df)

    st.success("Données traitées avec succès")

    st.subheader("Aperçu des données")
    st.dataframe(df)

    st.subheader("KPIs")

    if "Montant Total Vente HT" in df.columns:
        st.metric(
            "CA Total",
            df["Montant Total Vente HT"].sum()
        )

    if "Profit" in df.columns:
        st.metric(
            "Profit Total",
            df["Profit"].sum()
        )
