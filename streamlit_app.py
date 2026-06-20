import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chemin vers votre fichier Excel
# Remplacez 'votre_fichier.xlsx' par le nom ou le chemin réel de votre fichier
excel_file_path = 'votre_fichier.xlsx'

# Chargez le fichier Excel dans un DataFrame pandas
# Si votre fichier a plusieurs feuilles, vous pouvez spécifier la feuille avec 'sheet_name'
try:
    df = pd.read_excel(excel_file_path)
    print("Fichier Excel chargé avec succès.")
    print("Aperçu des données :")
    print(df.head())
except FileNotFoundError:
    print(f"Erreur : Le fichier '{excel_file_path}' n'a pas été trouvé. Veuillez vérifier le chemin.")
except Exception as e:
    print(f"Une erreur est survenue lors du chargement du fichier Excel : {e}")
import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Dashboard Intelligent", layout="wide")
st.title("📊 Dashboard Intelligent (auto-adaptatif)")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

# ----------------------------
# NORMALISATION
# ----------------------------
def normalize(col):
    return re.sub(r'[^a-zA-Z0-9]', '', col.lower())

mapping = {
    "chiffredaffaires": "CA",
    "ca": "CA",
    "sales": "CA",
    "revenue": "CA",

    "profit": "Profit",
    "benefice": "Profit",
    "margin": "Profit",

    "cost": "Cost",
    "costs": "Cost",
    "expenses": "Cost",
    "achat": "Cost",
    "achats": "Cost",

    "date": "Date",
    "jour": "Date",

    "pays": "Pays",
    "country": "Pays",

    "produit": "Produit",
    "product": "Produit"
}
# --- Étapes suivantes (à développer en fonction de vos besoins) ---

# 1. Nettoyage et transformation des données (ex: gestion des valeurs manquantes, conversions de type, création de nouvelles colonnes)
# Exemple : df['Nouvelle_Colonne'] = df['Colonne_1'] / df['Colonne_2']

# 2. Création de visualisations (graphiques, tableaux de bord)
# Exemple :
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Catégorie', y='Valeur', data=df)
# plt.title('Exemple de Graphique')
# plt.show()

# 3. Exportation du rapport (si nécessaire, par exemple, vers un fichier PDF ou HTML)

# --- CONFIGURATION DE VOS DONNÉES EXCEL ---

# 1. Nom de votre fichier Excel uploadé
# Remplacez 'votre_fichier.xlsx' par le nom de votre fichier (ex: 'rapport_financier_2023.xlsx')
excel_file_name = 'votre_fichier.xlsx'

# 2. Noms des feuilles de calcul (si vos données sont sur des feuilles séparées)
# Si toutes les données sont sur la même feuille, utilisez le même nom ou laissez les non pertinentes vides.
sales_sheet_name = 'Ventes'
expenses_sheet_name = 'Dépenses'
treasury_sheet_name = 'Trésorerie'

# 3. Noms des colonnes clés dans chaque feuille
# Adaptez ces noms aux en-têtes de colonnes réels de votre fichier Excel.

# Colonnes pour les Ventes
sales_date_col = 'Date'
sales_amount_col = 'Montant Vente'
sales_product_col = 'Produit' # Optionnel
sales_category_col = 'Catégorie Produit' # Optionnel

# Colonnes pour les Dépenses
expenses_date_col = 'Date'
expenses_amount_col = 'Montant Dépense'
expenses_category_col = 'Catégorie Dépense'

# Colonnes pour la Trésorerie (si les flux ne sont pas directement dérivés des ventes/dépenses)
# Par exemple, pour un relevé bancaire avec des transactions spécifiques.
treasury_date_col = 'Date'
treasury_transaction_type_col = 'Type Transaction' # Ex: 'Débit', 'Crédit'
treasury_amount_col = 'Montant Transaction'

print(f"Veuillez vérifier et mettre à jour ces variables avec les détails de votre fichier '{excel_file_name}'.")

dataframes = {}

try:
    # Charger les ventes
    if sales_sheet_name:
        df_sales = pd.read_excel(excel_file_name, sheet_name=sales_sheet_name)
        dataframes['Ventes'] = df_sales
        print(f"Données de ventes chargées depuis la feuille '{sales_sheet_name}'.")
        print("Aperçu des ventes :")
        display(df_sales.head())
        print("\n")

    # Charger les dépenses
    if expenses_sheet_name:
        df_expenses = pd.read_excel(excel_file_name, sheet_name=expenses_sheet_name)
        dataframes['Dépenses'] = df_expenses
        print(f"Données de dépenses chargées depuis la feuille '{expenses_sheet_name}'.")
        print("Aperçu des dépenses :")
        display(df_expenses.head())
        print("\n")

    # Charger la trésorerie
    if treasury_sheet_name:
        df_treasury = pd.read_excel(excel_file_name, sheet_name=treasury_sheet_name)
        dataframes['Trésorerie'] = df_treasury
        print(f"Données de trésorerie chargées depuis la feuille '{treasury_sheet_name}'.")
        print("Aperçu de la trésorerie :")
        display(df_treasury.head())
        print("\n")

except FileNotFoundError:
    print(f"Erreur : Le fichier '{excel_file_name}' n'a pas été trouvé. Assurez-vous de l'avoir uploadé et que le nom est correct.")
except ValueError as e:
    print(f"Erreur de feuille de calcul : {e}. Vérifiez que les noms de feuille ('{sales_sheet_name}', '{expenses_sheet_name}', '{treasury_sheet_name}') sont corrects dans votre fichier Excel.")
except Exception as e:
    print(f"Une erreur inattendue est survenue lors du chargement des données : {e}")

if not dataframes:
    print("Aucune donnée n'a été chargée. Veuillez vérifier la configuration de vos noms de feuille et de fichier.")

def preprocess_dataframe(df, date_col, amount_col, name):
    if df is None: # Handle cases where a dataframe wasn't loaded
        print(f"Le DataFrame '{name}' n'est pas disponible pour le prétraitement.")
        return None

    print(f"Prétraitement du DataFrame '{name}'...")

    # Convertir la colonne de date au format datetime
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        # Supprimer les lignes où la date n'a pas pu être convertie
        df.dropna(subset=[date_col], inplace=True)
        print(f"  Colonne '{date_col}' convertie en datetime.")
    else:
        print(f"  Attention : La colonne de date '{date_col}' n'a pas été trouvée dans '{name}'.")

    # Convertir la colonne de montant en numérique
    if amount_col in df.columns:
        # Nettoyage pour s'assurer que seuls les chiffres peuvent être convertis
        df[amount_col] = df[amount_col].astype(str).str.replace(',', '.').str.extract('([-+]?\d*\.?\d+)').astype(float)
        df.dropna(subset=[amount_col], inplace=True)
        print(f"  Colonne '{amount_col}' convertie en numérique.")
    else:
        print(f"  Attention : La colonne de montant '{amount_col}' n'a pas été trouvée dans '{name}'.")

    # Afficher un aperçu des types de données après conversion
    print(f"  Info sur le DataFrame '{name}' après prétraitement :")
    display(df.info())
    print("\n")
    return df

# Appliquer le prétraitement
if 'Ventes' in dataframes:
    df_sales = preprocess_dataframe(dataframes['Ventes'], sales_date_col, sales_amount_col, 'Ventes')
    dataframes['Ventes'] = df_sales

if 'Dépenses' in dataframes:
    df_expenses = preprocess_dataframe(dataframes['Dépenses'], expenses_date_col, expenses_amount_col, 'Dépenses')
    dataframes['Dépenses'] = df_expenses

if 'Trésorerie' in dataframes:
    # Pour la trésorerie, nous pourrions avoir besoin d'une logique légèrement différente pour les débits/crédits
    # Pour l'instant, on applique le même traitement, mais cela peut être affiné.
    df_treasury = preprocess_dataframe(dataframes['Trésorerie'], treasury_date_col, treasury_amount_col, 'Trésorerie')
    dataframes['Trésorerie'] = df_treasury

print("Prétraitement des données terminé.")
