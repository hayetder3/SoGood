import pandas as pd
import sqlite3

print("\n🚀 Étape 1 — Charger le CSV final...")
df = pd.read_csv("data/processed/SoGood_CLEAN_FINAL.csv")

print(f"✅ Lignes chargées : {len(df)}")

print("\n🚀 Étape 2 — Créer la base SQLite...")
conn = sqlite3.connect("data/processed/SoGood.db")

print("\n🚀 Étape 3 — Exporter la table 'products'...")
df.to_sql("products", conn, if_exists="replace", index=False)

print("\n✅ Table 'products' créée dans SoGood.db")

print("\n🚀 Étape 4 — Test requête pour vérifier...")
query = """
SELECT code, product_name_clean, "energy-kcal_100g"
FROM products
WHERE "energy-kcal_100g" > 500
LIMIT 5;
"""
result = pd.read_sql(query, conn)
print("\n=== Résultat test ===")
print(result)

conn.close()
print("\n✅ Base SQLite prête ! Ouvre-la dans DB Browser et amuse-toi !")
