import pyarrow.dataset as ds
import pandas as pd

print("\n🚀 OUVERTURE Parquet en mode STREAMING avec PyArrow...")

# 1️⃣ Charger dataset PyArrow
dataset = ds.dataset('data/parquet/food.parquet', format='parquet')

# 2️⃣ Créer le scanner CORRECT
scanner = dataset.scanner(columns=['code', 'product_name', 'brands', 'categories',
                                   'nutriscore_grade', 'nova_group', 'nutriments'])

# 3️⃣ Préparer CSV output
output_csv = 'data/processed/SoGood_from_Parquet.csv'
first_batch = True

# 4️⃣ Parcourir par batch
for batch in scanner.to_batches():
    df = batch.to_pandas()

    # === Extraire product_name
    def extract_product_name(x):
        try:
            for d in x:
                if d.get('lang') == 'main':
                    return d.get('text')
        except:
            return None

    df['product_name_clean'] = df['product_name'].apply(extract_product_name)

    # === Extraire nutriments
    def parse_nutriments(nlist, key):
        try:
            for d in nlist:
                if d.get('name') == key:
                    return d.get('100g')
            return None
        except:
            return None

    keys = ['energy-kcal', 'fat', 'sugars', 'salt', 'proteins']
    for k in keys:
        df[f"{k}_100g"] = df['nutriments'].apply(lambda x: parse_nutriments(x, k))

    keep = ['code', 'product_name_clean', 'brands', 'categories',
            'nutriscore_grade', 'nova_group'] + [f"{k}_100g" for k in keys]

    final = df[keep]

    # === Sauvegarder en mode append
    if first_batch:
        final.to_csv(output_csv, index=False, mode='w')
        first_batch = False
    else:
        final.to_csv(output_csv, index=False, mode='a', header=False)

    print(f"✅ Batch écrit : {len(final)} lignes...")

print("\n🎉 CSV FINAL propre généré sans crash RAM 🚀✨")
