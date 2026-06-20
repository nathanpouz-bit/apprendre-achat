import pandas as pd
import re


# --------------------------------------------------
# NORMALISATION
# --------------------------------------------------

def normaliser(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())


def renommer_colonnes(df):

    mapping = {
        "date": "Date",

        "quantity": "Quantite",
        "quantite": "Quantite",
        "qty": "Quantite",

        "prixht": "Prix HT",
        "priceht": "Prix HT",

        "prixttc": "Prix TTC",

        "reduction": "Reduction",
        "discount": "Reduction",

        "cost": "Cout",
        "cout": "Cout"
    }

    new_cols = {}

    for col in df.columns:
        key = normaliser(col)
        if key in mapping:
            new_cols[col] = mapping[key]

    return df.rename(columns=new_cols)


# --------------------------------------------------
# LOGIQUE PRINCIPALE (SAFE)
# --------------------------------------------------

def preparer_donnees(df):

    # sécurité : on copie
    df = df.copy()

    # rename
    df = renommer_colonnes(df)

    # --------------------------------------------------
    # DATE
    # --------------------------------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Annee"] = df["Date"].dt.year
        df["NumeroMois"] = df["Date"].dt.month
        df["Mois"] = df["Date"].dt.month_name()

    # --------------------------------------------------
    # VENTE HT (SAFE)
    # --------------------------------------------------
    if "Quantite" in df.columns and "Prix HT" in df.columns:
        df["Montant Vente HT"] = (
            df["Quantite"].fillna(0) * df["Prix HT"].fillna(0)
        )
    else:
        df["Montant Vente HT"] = 0

    # --------------------------------------------------
    # REDUCTION SAFE
    # --------------------------------------------------
    if "Reduction" in df.columns:

        max_val = df["Reduction"].max()

        if pd.notna(max_val) and max_val > 1:
            df["Reduction €"] = df["Montant Vente HT"] * df["Reduction"] / 100
        else:
            df["Reduction €"] = df["Reduction"].fillna(0)

        df["Discount"] = df["Reduction"].apply(
            lambda x: "Oui" if x > 0 else "Non"
        )

    else:
        df["Reduction €"] = 0
        df["Discount"] = "Non"

    # --------------------------------------------------
    # TOTAL SAFE
    # --------------------------------------------------
    df["Montant Total Vente HT"] = (
        df["Montant Vente HT"] - df["Reduction €"]
    )

    # --------------------------------------------------
    # PROFIT SAFE
    # --------------------------------------------------
    if "Cout" in df.columns:
        df["Profit"] = (
            df["Montant Total Vente HT"] - df["Cout"].fillna(0)
        )

    return df
