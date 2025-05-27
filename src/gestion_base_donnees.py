import json
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

DATA_JSON = "src\\data.json"


def charger_donnees() -> Dict[str, Any]:
    """Charge toutes les données depuis le fichier JSON."""
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as file:
            donnees: Dict[str, Any] = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        donnees = {}

    if "reservations" in donnees:
        donnees["reservations"] = convertir_dates_reservations_en_objets(
            donnees["reservations"])

    return donnees


def enregistrer_donnees(donnees: Dict[str, Any]) -> None:
    """Sauvegarde toutes les données dans le fichier JSON."""
    donnees_a_sauvegarder = dict(donnees)

    if "reservations" in donnees_a_sauvegarder:
        donnees_a_sauvegarder["reservations"] = convertir_dates_reservations_en_str(
            donnees_a_sauvegarder["reservations"])

    with open(DATA_JSON, "w", encoding="utf-8") as file:
        json.dump(donnees_a_sauvegarder, file, indent=4, ensure_ascii=False)


def convertir_dates_reservations_en_objets(reservations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convertit la clé 'debut' des réservations de chaîne de caractères en datetime."""
    resultat: List[Dict[str, Any]] = []
    for r in reservations:
        copie = r.copy()
        if isinstance(copie.get("debut"), str):
            try:
                copie["debut"] = datetime.fromisoformat(copie["debut"])
            except ValueError:
                copie["debut"] = None
        resultat.append(copie)
    return resultat


def convertir_dates_reservations_en_str(reservations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convertit la clé 'debut' des réservations de datetime en chaîne de caractères."""
    resultat: List[Dict[str, Any]] = []
    for r in reservations:
        copie = r.copy()
        if isinstance(copie.get("debut"), datetime):
            copie["debut"] = copie["debut"].isoformat()
        resultat.append(copie)
    return resultat


def ajouter_utilisateur(nom: str, prenom: str, adresse_mail: str) -> None:
    """Ajoute un nouvel utilisateur au fichier JSON si son adresse mail n'existe pas déjà.
    Un identifiant UUID unique est généré pour chaque utilisateur."""
    donnees = charger_donnees()

    if "utilisateurs" not in donnees:
        donnees["utilisateurs"] = []

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


def ajouter_salle(nom: str, type: str, capacite: int) -> None:
    """Ajoute une nouvelle salle au fichier JSONsi une salle du même nom n'existe pas déjà."""
    donnees = charger_donnees()

    if "salles" not in donnees:
        donnees["salles"] = []

    for salle in donnees["salles"]:
        if salle["nom"] == nom:
            return

    nouvelle_salle = {
        "nom": nom,
        "type": type,
        "capacite": capacite
    }

    donnees["salles"].append(nouvelle_salle)
    enregistrer_donnees(donnees)
