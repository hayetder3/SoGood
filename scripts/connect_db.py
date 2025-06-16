"""
connect_db.py

Petit script de test pour vérifier la connexion à la base SQLite SoGood.db
et exécuter une requête simple.

À exécuter depuis la racine du projet :
    python3 scripts/connect_db.py
"""

import sqlite3
import pandas as pd

# === 1) Définir le chemin vers le fichier .db ===
DB_PATH = "data/processed/SoGood.db"

# === 2) Ouvrir une connexion ===
conn = sqlite3.connect(DB_PATH)

print(f"✅ Connexion établie à : {DB_PATH}")

# === 3) Exemple de requête SQL ===
query = """
SELECT code, product_name_clean, "energy-kcal_100g", nutriscore_grade
FROM products
WHERE nutriscore_grade IS NOT NULL
ORDER BY "energy-kcal_100g" DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)
print("\n=== Exemple de résultat ===")
print(df)

# === 4) Fermer la connexion ===
conn.close()
print("\n✅ Connexion fermée proprement.")
