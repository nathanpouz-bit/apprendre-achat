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

    return df
