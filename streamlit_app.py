# streamlit_app.py

import streamlit as st

from data_loader import load_data
from dashboard_builder import build_dashboard

# -----------------------------
# Configuration de la page
# -----------------------------

st.set_page_config(
    page_title="Dashboard Commercial",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Commercial Automatique")

st.markdown(
    """
    Importez un fichier Excel contenant les colonnes :

    - Segment
    - Country
    - Product
    - Discount Band
    - Units Sold
    - Manufacturing Price
    - Sale Price
    - Gross Sales
    - Discounts
    - Sales
    - COGS
    - Profit
    - Date
    - Month Number
    - Month Name
    - Year
    """
)

# -----------------------------
# Upload fichier
# -----------------------------

uploaded_file = st.file_uploader(
    "Choisir un fichier Excel",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:

        df = load_data(uploaded_file)

        st.sidebar.header("Filtres")

        countries = st.sidebar.multiselect(
            "Pays",
            options=sorted(df["Country"].unique()),
            default=sorted(df["Country"].unique())
        )

        segments = st.sidebar.multiselect(
            "Segments",
            options=sorted(df["Segment"].unique()),
            default=sorted(df["Segment"].unique())
        )

        years = st.sidebar.multiselect(
            "Années",
            options=sorted(df["Year"].unique()),
            default=sorted(df["Year"].unique())
        )

        products = st.sidebar.multiselect(
            "Produits",
            options=sorted(df["Product"].unique()),
            default=sorted(df["Product"].unique())
        )

        filtered_df = df[
            (df["Country"].isin(countries))
            & (df["Segment"].isin(segments))
            & (df["Year"].isin(years))
            & (df["Product"].isin(products))
        ]

        build_dashboard(filtered_df)

        st.divider()

        st.subheader("Aperçu des données")

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Erreur : {e}")

else:

    st.info("Veuillez importer un fichier Excel.")
