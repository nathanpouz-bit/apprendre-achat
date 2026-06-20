import pandas as pd
import re


# --------------------------------------------------
# NORMALISATION
# --------------------------------------------------

def clean(col):
    return re.sub(r'[^a-z0-9]', '', col.lower())


# --------------------------------------------------
# DETECTION AUTOMATIQUE
# --------------------------------------------------

def detect(df):

    cols = {clean(c): c for c in df.columns}

    def find(keys):
        for k in keys:
            if k in cols:
                return cols[k]
        return None

    return {
        "date": find(["date", "jour"]),
        "ca": find(["ca", "sales", "revenue"]),
        "qty": find(["quantity", "quantite", "qty"]),
        "price": find(["prixht", "price", "unitprice"]),
        "cost": find(["cost", "cout"]),
        "country": find(["pays", "country"]),
        "product": find(["product", "produit"]),
    }


# --------------------------------------------------
# PREPARATION DATA
# --------------------------------------------------

def prepare(df):

    df = df.copy()
    m = detect(df)

    # DATE
    if m["date"]:
        df["Date"] = pd.to_datetime(df[m["date"]], errors="coerce")

    # CA direct
    if m["ca"]:
        df["CA"] = pd.to_numeric(df[m["ca"]], errors="coerce")
    else:
        if m["qty"] and m["price"]:
            df["CA"] = (
                pd.to_numeric(df[m["qty"]], errors="coerce").fillna(0)
                * pd.to_numeric(df[m["price"]], errors="coerce").fillna(0)
            )
        else:
            df["CA"] = 0

    # COST
    if m["cost"]:
        df["Cost"] = pd.to_numeric(df[m["cost"]], errors="coerce")
    else:
        df["Cost"] = 0

    # PROFIT
    df["Profit"] = df["CA"] - df["Cost"]

    return df, m
