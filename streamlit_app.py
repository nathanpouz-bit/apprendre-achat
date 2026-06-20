import pandas as pd
import re


def clean(col):
    return re.sub(r'[^a-z0-9]', '', col.lower())


def detect(df):

    cols = {clean(c): c for c in df.columns}

    def find(keys):
        for k in keys:
            if k in cols:
                return cols[k]
        return None

    return {
        "date": find(["date"]),
        "product": find(["product", "produit"]),
        "country": find(["pays", "country"]),
        "qty": find(["quantity", "quantite"]),
        "price": find(["price", "prixht"]),
        "cost": find(["cost", "cout"])
    }


def prepare(df):

    df = df.copy()
    m = detect(df)

    if m["qty"] and m["price"]:
        df["CA"] = df[m["qty"]] * df[m["price"]]
    elif "CA" in df.columns:
        df["CA"] = df["CA"]
    else:
        df["CA"] = 0

    if m["cost"]:
        df["Cost"] = df[m["cost"]]
    else:
        df["Cost"] = 0

    df["Profit"] = df["CA"] - df["Cost"]

    if m["date"]:
        df["Date"] = pd.to_datetime(df[m["date"]], errors="coerce")

    return df, m
