import pandas as pd
from config.settings import REQUIRED_COLUMNS


def load_data(uploaded_file):

    df = pd.read_excel(uploaded_file)

    missing_cols = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Colonnes manquantes : {missing_cols}"
        )

    df["Date"] = pd.to_datetime(df["Date"])

    return df
