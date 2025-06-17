import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from utils import clean_nutriscore, categorize_sugar, save_plot, log_analysis
print("Début script")
# ================= CONFIGURATION ================= #
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = Path("/Users/derdourhayet/Desktop/IPSSI 2/SoGood/data/mock_data.csv")
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ================= FONCTIONS CORE ================= #

def load_data():
    """Charge les données avec vérification"""
    try:
        df = pd.read_csv(DATA_PATH)
        log_analysis(f"Données chargées : {len(df)} produits")
        return df
    except Exception as e:
        log_analysis(f"ERREUR Chargement : {str(e)}", level="error")
        print(f"Erreur chargement données : {str(e)}")
        return None

def clean_data(df):
    """Nettoyage complet des données"""
    # Standardisation
    df['nutri_score'] = df['nutri_score'].apply(clean_nutriscore)
    df['sugar_category'] = df['sugars_100g'].apply(categorize_sugar)
    
    # Gestion NaN
    df = df.dropna(subset=['nutri_score', 'sugars_100g'])
    log_analysis("Nettoyage des données terminé")
    return df

# ================= ANALYSES BASIQUES ================= #

def generate_core_visualizations(df):
    """Génère les graphiques principaux"""
    # 1. Distribution Nutri-Score
    plt.figure(figsize=(10,6))
    score_order = ['A','B','C','D','E']
    nutri_counts = df['nutri_score'].value_counts().reindex(score_order, fill_value=0)
    nutri_counts.plot(kind='bar', color=['#28a745','#7cb342','#ffc107','#fd7e14','#dc3545'])
    plt.title("Distribution des Nutri-Scores", fontweight='bold')
    save_plot(plt, "nutri_distribution.png")
    
    # 2. Relation Sucre-Additifs
    plt.figure(figsize=(12,7))
    sns.scatterplot(data=df, x='sugars_100g', y='additives_n', hue='nutri_score', palette='RdYlGn_r')
    plt.title("Relation Sucre vs Additifs", fontweight="bold")
    save_plot(plt, "sugar_vs_additives.png")

# ================= ANALYSES AVANCÉES ================= #

def calculate_danger_scores(df):
    """Calcule un score de dangerosité personnalisé"""
    df['danger_score'] = (df['sugars_100g']*0.5 + df['additives_n']*2 + df['nova_group']*3).round(1)
    top_danger = df.nlargest(5, 'danger_score')[['product_name', 'danger_score', 'brands']]
    return df, top_danger

def analyze_brands(df):
    """Compare les marques entre elles"""
    brand_stats = df.groupby('brands').agg(
        avg_sugar=('sugars_100g', 'mean'),
        avg_score=('nutri_score', lambda x: x.map({'A':5, 'B':4, 'C':3, 'D':2, 'E':1}).mean()),
        worst_product=('product_name', lambda x: x.iloc[df.loc[x.index, 'nutri_score'].argmin()])
    )
    return brand_stats.sort_values('avg_score', ascending=False)

def find_healthy_alternatives(df):
    """Trouve des alternatives plus saines"""
    alternatives = []
    for _, row in df[df['nutri_score'].isin(['D','E'])].iterrows():
        similar = df[
        (df['categories'] == row['categories']) & 
        (df['nutri_score'] < row['nutri_score'])
    ].head(2)
        alternatives.append({
            'original': row['product_name'],
            'alternatives': similar[['product_name', 'nutri_score']].to_dict('records')
        })
    return alternatives

# ================= EXPORT ================= #

def export_all_results(df, top_danger, brand_stats, alternatives):
    """Exporte tous les résultats"""
    # 1. Fichier principal pour la WebApp
    web_data = {
        'products': df.to_dict('records'),
        'top_danger': top_danger.to_dict('records'),
        'brands': brand_stats.reset_index().to_dict('records'),
        'alternatives': alternatives
    }
    with open(RESULTS_DIR / "webapp_data.json", 'w') as f:
        json.dump(web_data, f, indent=2)
    
    # 2. Rapports supplémentaires
    brand_stats.head(10).to_csv(RESULTS_DIR / "top_brands.csv")
    pd.DataFrame(alternatives).to_json(RESULTS_DIR / "alternatives.json")

# ================= WORKFLOW PRINCIPAL ================= #

def main():
    print("\n=== LANCEMENT DE L'ANALYSE COMPLÈTE ===")
    
    # 1. Chargement et nettoyage
    df = load_data()
    if df is None:
        return
    df = clean_data(df)
    
    # 2. Analyses de base
    generate_core_visualizations(df)
    
    # 3. Analyses avancées
    df, top_danger = calculate_danger_scores(df)
    brand_stats = analyze_brands(df)
    alternatives = find_healthy_alternatives(df)
    
    # 4. Export final
    export_all_results(df, top_danger, brand_stats, alternatives)
    
    print(f"""
    === RÉSULTATS ===
    • Graphiques principaux : {RESULTS_DIR}/nutri_distribution.png et sugar_vs_additives.png
    • Données pour la WebApp : {RESULTS_DIR}/webapp_data.json
    • Classement des marques : {RESULTS_DIR}/top_brands.csv
    • Alternatives saines : {RESULTS_DIR}/alternatives.json
    """)
    print("Analyse terminée avec succès.")
    

if __name__ == "__main__":
    main()
    print("Analyse terminée avec succès.")

