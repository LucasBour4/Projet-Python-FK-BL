import json
import uuid
from datetime import datetime, timedelta

DATA_JSON = "src\\data.json"

def charger_donnees():
    """Charge toutes les données depuis le fichier JSON."""
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as file:
            donnees = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        donnees = {}

    """Convertir les réservations au format datetime"""
    if "reservations" in donnees:
        donnees["reservations"] = convertir_dates_reservations_en_objets(donnees["reservations"])

    return donnees
    
    
def enregistrer_donnees(donnees):
    """Sauvegarde toutes les données dans le fichier JSON."""
    donnees_a_sauvegarder = dict(donnees)  # copie pour ne pas modifier l'original

    if "reservations" in donnees_a_sauvegarder:
        donnees_a_sauvegarder["reservations"] = convertir_dates_reservations_en_str(donnees_a_sauvegarder["reservations"])

    with open(DATA_JSON, "w", encoding="utf-8") as file:
        json.dump(donnees_a_sauvegarder, file, indent=4, ensure_ascii=False)

def convertir_dates_reservations_en_objets(reservations):
    """Convertit la clé 'debut' des réservations en chaîne de charactères vers datetime."""
    resultat = []
    for r in reservations:
        copie = r.copy()
        if isinstance(copie.get("debut"), str):
            try:
                copie["debut"] = datetime.fromisoformat(copie["debut"])
            except ValueError:
                copie["debut"] = None
        resultat.append(copie)
    return resultat


def convertir_dates_reservations_en_str(reservations):
    """Convertit la clé 'debut' des réservations de datetime en charactères."""
    resultat = []
    for r in reservations:
        copie = r.copy()
        if isinstance(copie.get("debut"), datetime):
            copie["debut"] = copie["debut"].isoformat()
        resultat.append(copie)
    return resultat



def ajouter_utilisateur(nom : str, prenom : str, adresse_mail : str): 
    # Ajoute un nouvel utilisateur au fichier JSON
    donnees = charger_donnees()

    if "utilisateurs" not in donnees:
        donnees["utilisateurs"] = []

    # Vérifie si l'utilisateur existe déjà
    for utilisateur in donnees["utilisateurs"]:
        if utilisateur["email"] == adresse_mail:
            return  
        

    nouveau_utilisateur = {
        "id": str(uuid.uuid4()),
        "nom": nom,
        "prenom": prenom,
        "email": adresse_mail
    }
    donnees["utilisateurs"].append(nouveau_utilisateur)
    enregistrer_donnees(donnees)


def ajouter_salle(nom : str, type : str, capacite : int):
    # Ajoute une nouvelle salle au fichier JSON
    donnees = charger_donnees() 

    if "salles" not in donnees:
        donnees["salles"] = []

    # Vérifie si la salle existe déjà
    for salle in donnees["salles"]:
        if salle["nom"] == nom:
            return    

    nouvelle_salle = {
        "nom": nom,
        "type": type,
        "capacite" : capacite
    }    

    donnees["salles"].append(nouvelle_salle)
    enregistrer_donnees(donnees)