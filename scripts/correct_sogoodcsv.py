import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/SoGood_CLEAN.csv")

# 1️⃣ Supprimer ligne sans code
df = df.dropna(subset=['code'])

# 2️⃣ Remplir product_name_clean manquant
df['product_name_clean'] = df['product_name_clean'].fillna('Unknown')

# 3️⃣ Nettoyer nutriscore_grade
df['nutriscore_grade'] = df['nutriscore_grade'].replace({'not-applicable': np.nan, '4.0': np.nan})

# 4️⃣ Nettoyer nova_group : remplacer > 4 par NaN
df.loc[df['nova_group'] > 4, 'nova_group'] = np.nan

# 5️⃣ Corriger valeurs extrêmes pour nutriments
nutrients = ['energy-kcal_100g', 'fat_100g', 'sugars_100g', 'salt_100g', 'proteins_100g']
for col in nutrients:
    # remplacer valeurs négatives ou trop énormes par NaN
    df.loc[(df[col] < 0) | (df[col] > 1000), col] = np.nan
    # puis NaN ➜ 0
    df[col] = df[col].fillna(0)

# Sauver fichier CLEAN FINAL
df.to_csv("data/processed/SoGood_CLEAN_FINAL.csv", index=False)

print("\n✅ Fichier propre enregistré : data/processed/SoGood_CLEAN_FINAL.csv")
