import pandas as pd
import re


# --------------------------------------------------
# NORMALISATION
# --------------------------------------------------

def clean(col):
    return re.sub(r'[^a-z0-9]', '', col.lower())


# --------------------------------------------------
# DETECTION INTELLIGENTE
# --------------------------------------------------

def detect_columns(df):

    cols = {clean(c): c for c in df.columns}

    def find(possibilities):
        for p in possibilities:
            if p in cols:
                return cols[p]
        return None

    return {
        "date": find(["date", "jour", "day"]),

        "qty": find(["quantity", "quantite", "qty", "qte"]),

        "prix_ht": find(["prixht", "priceht", "unitprice", "ht"]),

        "prix_ttc": find(["prixttc", "totalprice", "ttc"]),

        "reduction": find(["reduction", "discount", "promo"]),

        "cout": find(["cost", "cout", "costprice"])
    }


# --------------------------------------------------
# LOGIQUE PRINCIPALE
# --------------------------------------------------

def preparer_donnees(df):

    df = df.copy()

    mapping = detect_columns(df)

    # -------------------------
    # DATE
    # -------------------------
    if mapping["date"]:
        df["Date"] = pd.to_datetime(df[mapping["date"]], errors="coerce")
        df["Annee"] = df["Date"].dt.year
        df["NumeroMois"] = df["Date"].dt.month
        df["Mois"] = df["Date"].dt.month_name()

    # -------------------------
    # VENTE HT
    # -------------------------
    if mapping["qty"] and mapping["prix_ht"]:
        df["Quantite"] = pd.to_numeric(df[mapping["qty"]], errors="coerce").fillna(0)
        df["Prix HT"] = pd.to_numeric(df[mapping["prix_ht"]], errors="coerce").fillna(0)

        df["Montant Vente HT"] = df["Quantite"] * df["Prix HT"]
    else:
        df["Montant Vente HT"] = 0

    # -------------------------
    # REDUCTION
    # -------------------------
    if mapping["reduction"]:

        r = pd.to_numeric(df[mapping["reduction"]], errors="coerce").fillna(0)

        if r.max() > 1:
            df["Reduction €"] = df["Montant Vente HT"] * r / 100
        else:
            df["Reduction €"] = r

        df["Discount"] = r.apply(lambda x: "Oui" if x > 0 else "Non")

    else:
        df["Reduction €"] = 0
        df["Discount"] = "Non"

    # -------------------------
    # TOTAL
    # -------------------------
    df["Montant Total Vente HT"] = df["Montant Vente HT"] - df["Reduction €"]

    # -------------------------
    # PROFIT
    # -------------------------
    if mapping["cout"]:
        c = pd.to_numeric(df[mapping["cout"]], errors="coerce").fillna(0)
        df["Profit"] = df["Montant Total Vente HT"] - c


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

    return df
