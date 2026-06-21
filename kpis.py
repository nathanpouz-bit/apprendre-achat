# kpis.py

def calculate_kpis(df):

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_units = df["Units Sold"].sum()

    avg_margin = (
        total_profit / total_sales * 100
        if total_sales > 0 else 0
    )

    return {
        "sales": total_sales,
        "profit": total_profit,
        "units": total_units,
        "margin": avg_margin
    }
