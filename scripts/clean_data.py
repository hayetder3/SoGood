import pandas as pd
import numpy as np

# === 1️⃣ Charger le CSV brut ===
print("\n🚀 Chargement du fichier brut...")
df = pd.read_csv("data/processed/SoGood_from_Parquet.csv")

print(f"✅ Lignes brutes : {len(df)}")

# === 2️⃣ Nettoyer les 'unknown' et valeurs bizarres ===
print("\n🔍 Remplacement des valeurs 'unknown' ou incohérentes...")

df['nutriscore_grade'] = df['nutriscore_grade'].replace({'unknown': np.nan})
df['nova_group'] = df['nova_group'].replace({1.0: np.nan, 'unknown': np.nan})

# === 3️⃣ Filtrer les lignes avec trop de nutriments manquants ===
print("\n🔍 Suppression des lignes trop incomplètes...")
nutrient_cols = ['energy-kcal_100g', 'fat_100g', 'sugars_100g', 'salt_100g', 'proteins_100g']
# On autorise max 2 nutriments manquants
df['nutrient_missing'] = df[nutrient_cols].isnull().sum(axis=1)
df_clean = df[df['nutrient_missing'] <= 2].drop(columns=['nutrient_missing'])

print(f"✅ Lignes après filtrage incomplets : {len(df_clean)}")

# === 4️⃣ (Option) Imputation des nutriments manquants ===
# Ici on remplace les NaN restants par 0 car c’est plus logique pour calories/nutriments
print("\n🧹 Remplissage des nutriments manquants à 0 (optionnel)...")
df_clean[nutrient_cols] = df_clean[nutrient_cols].fillna(0)

# === 5️⃣ Nettoyer doublons ===
print("\n🔍 Vérification des doublons...")
before = len(df_clean)
df_clean = df_clean.drop_duplicates(subset=['code'])
print(f"✅ Lignes après suppression des doublons : {len(df_clean)} (avant: {before})")

# === 6️⃣ Sauver le fichier clean ===
output_path = "data/processed/SoGood_CLEAN.csv"
df_clean.to_csv(output_path, index=False)
print(f"\n🎉 CSV FINAL propre généré : {output_path}")

# === 7️⃣ Stat récap ===
print("\n📊 Résumé :")
print(f"Lignes avant : {len(df)}")
print(f"Lignes après : {len(df_clean)}")
print(f"Colonnes : {df_clean.columns.tolist()}")
