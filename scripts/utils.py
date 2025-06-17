#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FONCTIONS UTILITAIRES SoGood
Helper functions pour l'analyse nutritionnelle
"""

import pandas as pd
import numpy as np
from pathlib import Path

def clean_nutriscore(score):
    """
    Nettoie et standardise les Nutri-Scores
    Args:
        score (str): Score à nettoyer (ex: ' a ', 'B', 'e')
    Returns:
        str: Score nettoyé (ex: 'A', 'B', 'E') ou None si invalide
    """
    if pd.isna(score):
        return None
    score = str(score).upper().strip()
    return score if score in ['A','B','C','D','E'] else None

def categorize_sugar(sugar_value):
    """
    Catégorise la teneur en sucre
    Args:
        sugar_value (float): Grammes de sucre pour 100g
    Returns:
        str: Catégorie ('Faible', 'Moyen', 'Élevé')
    """
    if pd.isna(sugar_value):
        return 'Non spécifié'
    sugar = float(sugar_value)
    if sugar < 5:
        return 'Faible (<5g)'
    elif 5 <= sugar < 15:
        return 'Moyen (5-15g)'
    else:
        return 'Élevé (>15g)'

def save_plot(fig, filename, folder='results'):
    """
    Sauvegarde professionnelle des graphiques
    Args:
        fig (matplotlib.figure): Figure à sauvegarder
        filename (str): Nom du fichier (ex: 'nutri_distribution.png')
        folder (str): Dossier de destination
    """
    output_path = Path(folder) / filename
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"📊 Graphique sauvegardé : {output_path}")

def detect_outliers(df, column):
    """
    Détecte les valeurs aberrantes avec la méthode IQR
    Args:
        df (DataFrame): Jeu de données
        column (str): Colonne à analyser
    Returns:
        DataFrame: Produits avec valeurs aberrantes
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.25)
    iqr = q3 - q1
    fence = q3 + 1.5*iqr
    return df[df[column] > fence]

def log_analysis(message, logfile='analysis_log.txt'):
    """
    Journalise les étapes de l'analyse
    Args:
        message (str): Message à enregistrer
        logfile (str): Fichier de log
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

# Test des fonctions (s'exécute seulement si lancé directement)
if __name__ == "__main__":
    # Test clean_nutriscore
    test_scores = pd.Series([' A ', 'b', None, 'Z', 'e'])
    print("Test clean_nutriscore():")
    print(test_scores.apply(clean_nutriscore))
    
    # Test categorize_sugar
    test_sugars = [4.9, 5, 15, None]
    print("\nTest categorize_sugar():")
    for sugar in test_sugars:
        print(f"{sugar} → {categorize_sugar(sugar)}")