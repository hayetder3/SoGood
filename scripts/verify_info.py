import pandas as pd

print("\n🚀 Vérification cohérence SoGood_CLEAN_FINAL.csv")

df = pd.read_csv("data/processed/SoGood_CLEAN_FINAL.csv")

print("\n=== Aperçu ===")
print(df.head())

print("\n=== Info ===")
print(df.info())

print("\n=== Describe ===")
print(df.describe())

print("\n=== NaN par colonne ===")
print(df.isnull().sum())

print("\n=== Valeurs uniques NutriScore ===")
print(df['nutriscore_grade'].unique())

print("\n=== Valeurs uniques NovaGroup ===")
print(df['nova_group'].unique())
