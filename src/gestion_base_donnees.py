import json
import uuid

DATA_JSON = "src\\data.json"

def charger_donnees():  
    # Charge les utilisateurs à partir du fichier JSON
    try:
        with open(DATA_JSON) as file:
            return json.load(file)
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourne une structure vide
        return {"utilisateurs": []}
    except json.JSONDecodeError:
        # Si le fichier est vide ou mal formé, retourne une structure vide
        return {"utilisateurs": []}
    
def enregistrer_donnees(donnees):
    with open(DATA_JSON, 'w') as file:
        json.dump(donnees, file)

def ajouter_utilisateur(nom : str, prenom : str, adresse_mail : str): 
    # Ajoute un nouvel utilisateur
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

def ajouter_salle(nom : str, type : str):
    # Ajoute une nouvelle salle   
    donnees = charger_donnees() 

    if "salles" not in donnees:
        donnees["salles"] = []

    # Vérifie si la salle existe déjà
    for salle in donnees["salles"]:
        if salle["nom"] == nom:
            return    

    nouvelle_salle = {
        "nom": nom,
        "type": type
    }    

    donnees["salles"].append(nouvelle_salle)
    enregistrer_donnees(donnees)
    

#ajouter_utilisateur("Ferry","Kevin","kevin.ferry@mail.com")
#ajouter_utilisateur("Bour","Lucas","lucas.bour@mail.com")
#print(charger_utilisateurs())
#ajouter_salle("Salle 1","standard")
#print(charger_donnees())