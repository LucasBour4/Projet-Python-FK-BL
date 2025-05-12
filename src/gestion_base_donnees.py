import json

DATA_JSON = "src\\data.json"

def charger_utilisateurs():  
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
    
def enregistrer_utilisateurs(donnees):
    with open(DATA_JSON, 'w') as file:
        json.dump(donnees, file)

def ajouter_utilisateur(nom : str, prenom : str, adresse_mail : str): 
    # Ajoute un nouvel utilisateur
    donnees = charger_utilisateurs()

    if "utilisateurs" not in donnees:
        donnees["utilisateurs"] = []

    # Vérifie si l'utilisateur existe déjà
    for utilisateur in donnees["utilisateurs"]:
        if utilisateur["email"] == adresse_mail:
            return  

    nouveau_utilisateur = {
        "nom": nom,
        "prenom": prenom,
        "email": adresse_mail
    }
    donnees["utilisateurs"].append(nouveau_utilisateur)
    enregistrer_utilisateurs(donnees)
    

#ajouter_utilisateur("Ferry","Kevin","kevin.ferry@mail.com")
#ajouter_utilisateur("Bour","Lucas","lucas.bour@mail.com")
#print(charger_utilisateurs())