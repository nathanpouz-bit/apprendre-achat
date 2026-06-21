# app.py

import streamlit as st

from data_loader import load_data
from dashboard_builder import build_dashboard

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("📊 Dashboard Commercial")

uploaded_file = st.file_uploader(
    "Importer un fichier Excel",
    type=["xlsx"]
)

if uploaded_file:

    try:

        df = load_data(uploaded_file)

        st.sidebar.header("Filtres")

        countries = st.sidebar.multiselect(
            "Pays",
            df["Country"].unique(),
            default=df["Country"].unique()
        )

        segments = st.sidebar.multiselect(
            "Segments",
            df["Segment"].unique(),
            default=df["Segment"].unique()
        )

        years = st.sidebar.multiselect(
            "Années",
            df["Year"].unique(),
            default=df["Year"].unique()
        )

        filtered_df = df[
            (df["Country"].isin(countries))
            & (df["Segment"].isin(segments))
            & (df["Year"].isin(years))
        ]

        build_dashboard(filtered_df)

        st.subheader("Données")

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))
