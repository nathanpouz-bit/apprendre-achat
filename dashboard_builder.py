# dashboard_builder.py

import streamlit as st

from kpis import calculate_kpis
from charts import (
    sales_by_country,
    profit_by_product,
    sales_over_time,
    segment_analysis
)


def build_dashboard(df):

    kpi = calculate_kpis(df)

    st.subheader("KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "CA Total",
        f"{kpi['sales']:,.0f} €"
    )

    c2.metric(
        "Profit",
        f"{kpi['profit']:,.0f} €"
    )

    c3.metric(
        "Unités vendues",
        f"{kpi['units']:,.0f}"
    )

    c4.metric(
        "Marge moyenne",
        f"{kpi['margin']:.2f}%"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            sales_by_country(df),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            profit_by_product(df),
            use_container_width=True
        )

    st.plotly_chart(
        sales_over_time(df),
        use_container_width=True
    )

    st.plotly_chart(
        segment_analysis(df),
        use_container_width=True
    )
