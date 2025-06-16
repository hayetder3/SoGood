import duckdb

print("\n=== DESCRIBE SELECT * ===")
print(duckdb.query("DESCRIBE SELECT * FROM 'data/parquet/food.parquet'").to_df())

print("\n=== Une ligne complète ===")
df = duckdb.query("SELECT * FROM 'data/parquet/food.parquet' LIMIT 1").to_df()
print(df.T)

df.to_json("data/processed/debug_full_sample.json", index=False)
print("\n✅ Échantillon brut sauvegardé dans data/processed/debug_full_sample.json")
