import pandas as pd
import re


# --------------------------------------------------
# NORMALISATION COLONNES
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
# LOGIQUE METIER
# --------------------------------------------------

def preparer_donnees(df):

    df = renommer_colonnes(df)

    # DATE
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Annee"] = df["Date"].dt.year
        df["NumeroMois"] = df["Date"].dt.month
        df["Mois"] = df["Date"].dt.month_name()

    # TVA
    if "Prix TTC" in df.columns and "Prix HT" in df.columns:
        df["Montant TVA"] = df["Prix TTC"] - df["Prix HT"]

# VENTE HT
if "Quantite" in df.columns and "Prix HT" in df.columns:
    df["Montant Vente HT"] = (
        df["Quantite"].fillna(0) * df["Prix HT"].fillna(0)
    )
else:
    df["Montant Vente HT"] = 0


# REDUCTION
if "Reduction" in df.columns:
    if df["Reduction"].max() > 1:
        df["Reduction €"] = df["Montant Vente HT"] * df["Reduction"] / 100
    else:
        df["Reduction €"] = df["Reduction"]
else:
    df["Reduction €"] = 0


# TOTAL (SAFE)
df["Montant Total Vente HT"] = (
    df["Montant Vente HT"] - df["Reduction €"]
)
st.write(df.columns)
