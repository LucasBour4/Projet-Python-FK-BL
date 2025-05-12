# Fichier Principal

from interface_graphique import *
import json

fenetre_principale = None

with open("utilisateurs.json", "r") as f:
    data = json.load(f)

if __name__ == "__main__":
    creer_page_originale()