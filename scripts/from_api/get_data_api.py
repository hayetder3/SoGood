import requests
import time
import pandas as pd

USER_AGENT = "SoGoodApp/1.0 (contact@sogoodapp.fr)"
BASE_URL = "https://world.openfoodfacts.org/api/v2/search"
FIELDS = "code,product_name,nutrition_grades,brands,categories,nutriments"
PAGE_SIZE = 1000
MAX_PAGES = 100
SLEEP_SECONDS = 6

all_products = []

for page in range(1, MAX_PAGES + 1):
    params = {
        "fields": FIELDS,
        "page_size": PAGE_SIZE,
        "page": page,
    }
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(BASE_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        print(f"Page {page}: {len(products)} produits")
        all_products.extend(products)
    else:
        print(f"Erreur page {page} : {response.status_code}")
        break

    time.sleep(SLEEP_SECONDS)

print(f"✅ Total produits récupérés : {len(all_products)}")

# Transformer en DataFrame
df = pd.DataFrame(all_products)

# Sélectionner les champs plats
main_fields = ["code", "product_name", "nutrition_grades", "brands", "categories"]

# Extraire nutriments spécifiques
nutriments_df = df["nutriments"].apply(pd.Series)[
    ["energy-kcal_100g", "sugars_100g", "salt_100g", "fat_100g"]
]

# Fusionner
df_clean = pd.concat([df[main_fields], nutriments_df], axis=1)

# Sauvegarder en CSV propre
df_clean.to_csv("SoGood_API_flat.csv", index=False)

print("✅ Fichier plat 'SoGood_API_flat.csv' généré !")
