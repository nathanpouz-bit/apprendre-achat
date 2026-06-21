import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("🤖 Dashboard IA réel")

file = st.file_uploader("Upload Excel", type=["xlsx"])

query = st.text_input("💬 Décris ton analyse")


if file:

    df = pd.read_excel(file)

    st.write("Aperçu :", df.head())

    if query:

        plan = analyser_requete(query)

        st.subheader("🧠 Plan généré par l'IA")
        st.json(plan)

        st.subheader("📊 Graphiques")

        for chart in plan["charts"]:

            chart_type = chart["type"]

            # --------------------------
            # BAR / GROUPBY
            # --------------------------
            if chart_type == "bar":

                data = df.groupby(chart["groupby"]).sum(numeric_only=True).reset_index()

                fig = px.bar(
                    data,
                    x=chart["groupby"],
                    y=data.columns[-1]
                )

                st.plotly_chart(fig, use_container_width=True)

            # --------------------------
            # LINE
            # --------------------------
            if chart_type == "line":

                data = df.copy()

                data[chart["x"]] = pd.to_datetime(data[chart["x"]], errors="coerce")

                data = data.groupby(chart["x"]).sum(numeric_only=True).reset_index()

                fig = px.line(
                    data,
                    x=chart["x"],
                    y=data.columns[-1]
                )

                st.plotly_chart(fig, use_container_width=True)

            # --------------------------
            # PIE
            # --------------------------
            if chart_type == "pie":

                data = df.groupby(chart["groupby"]).sum(numeric_only=True).reset_index()

                fig = px.pie(
                    data,
                    names=chart["groupby"],
                    values=data.columns[-1]
                )

                st.plotly_chart(fig, use_container_width=True)
