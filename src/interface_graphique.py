# Fichier : interface_graphique.py
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askstring
from gestion_base_donnees import *

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter

#fenetre_principale = None

def afficher_message_temporaire(message, duree=10000):
    # Affiche un message temporaire (duree en millisecondes)
    popup = Toplevel()
    popup.title("Message")
    Label(popup, text=message, font=("Arial", 12)).pack(padx=20, pady=20)
    popup.after(duree, popup.destroy)

def creer_bouton(texte : str, commande=None, couleur_fond : str ="blue", couleur_texte : str ="white", police=("Arial", 12)):
    #Crée un bouton avec les paramètres spécifiés.
        
    bouton = Button(
        text = texte,
        command = commande,
        background = couleur_fond,
        fg = couleur_texte,
        font = police
    )
    bouton.config(width=40, height=2)
    bouton.pack()
    return bouton

def creer_page_originale():
    # Créer la page principale de l'application
    global fenetre_principale
    fenetre_principale = Tk()
    fenetre_principale.title("MeetingPro - Gestion des Réservations")
    fenetre_principale.geometry("500x600") #Gestion de la taille de la fenêtre

    # Informations sur l'application
    info = Label(fenetre_principale, text="MeetingPro vous propose ce service de réservation de salle", font=("Arial", 13), fg="Green")
    info.pack()

    #Création des boutons vers les différentes pages
    creer_bouton("Ajouter un client", lambda : creer_page("Ajouter un client", fenetre_principale, "lightblue"),"lightblue"),
    creer_bouton("Ajouter une nouvelle salle", lambda : creer_page("Ajouter une nouvelle salle", fenetre_principale, "#98FB98"), "#98FB98", "black"),
    creer_bouton("Salles réservables", lambda : creer_page("Salles réservables", fenetre_principale, "#FFFFE0")),
    creer_bouton("Réservation par client", lambda : creer_page("Réservation par client", fenetre_principale, "#FFDAB9")),
    creer_bouton("Identifier si une salle est disponible pour un créneau", lambda : creer_page("Identifier si une salle est disponible pour un créneau", fenetre_principale, "#40E0D0")),
    creer_bouton("Afficher les salles disponibles pour un créneau", lambda : creer_page("Afficher les salles disponibles pour un créneau", fenetre_principale, "#F08080")),
    creer_bouton("Réserver une salle", lambda : creer_page("Réserver une salle", fenetre_principale, "#FFB6C1")),

    credits(fenetre_principale)

    fenetre_principale.mainloop()


def creer_page(titre : str, ancienne_fenetre, couleur_fond : str ="white"):
    # Crée une nouvelle fenêtre 
    ancienne_fenetre.destroy()
    fenetre = Tk()
    fenetre.title(titre)
    fenetre.geometry("500x600") 
    fenetre.configure(bg=couleur_fond)

    # Informations et boutons présents sur la page
    specificites_page(titre)
    creer_bouton("Revenir à la page précédente", lambda : fenetre_precedente(fenetre, ancienne_fenetre))

    credits(fenetre)

    fenetre.mainloop()

def fenetre_precedente(fenetre, ancienne_fenetre):
    # Fonction pour revenir à la fenêtre précédente
    if ancienne_fenetre == fenetre_principale:
        fenetre.destroy()
        creer_page_originale()
    else:
        creer_page(ancienne_fenetre, None)

def credits(fenetre):
    # Ajoute les noms des créateurs de cette application
    credits = Label(fenetre, text="Création de Kevin FERRY et Lucas BOUR", font=("Arial", 6), fg="Green")
    credits.pack()
    
def specificites_page(role):
    # Ajoute les boutons, labels et autres spécificités liés à la page
    if role == "Ajouter un client":
        couleur_bouton = "Steel Blue"
        creer_bouton("Ajouter un nouveau client", lambda : bouton_ajouter_utilisateur(), couleur_bouton)
        creer_bouton("Vous avez oubliez votre id?", lambda : bouton_id() , couleur_bouton)
        return None
    elif role == "Ajouter une nouvelle salle":
        couleur_bouton = "#2E8B57"
        creer_bouton("Ajouter une nouvelle salle", lambda : bouton_ajouter_salle(), couleur_bouton)

def bouton_ajouter_utilisateur():
    # Bouton servant à ajouter un utilisateur
    nom = askstring("Saisie", "Quel est votre nom ?")
    prenom = askstring("Saisie", "Quel est votre prénom ?")
    adresse_mail = askstring("Saisie", "Quelle est votre adresse mail ?")

    # Vérifier que aucun des 3 champs soit vide

    #print(f"Nom: {nom}, Prénom: {prenom}, Adresse mail: {adresse_mail}")
    ajouter_utilisateur(nom, prenom, adresse_mail)

def bouton_id():
    # Renvoie l'id de l'utilisateur à l'aide de son adresse mail
    adresse_mail = askstring("Saisie", "Quelle est votre adresse mail ?")
    if adresse_mail is None:
        return
    donnees = charger_donnees()
    for utilisateur in donnees["utilisateurs"]:
        if utilisateur["email"] == adresse_mail:
            afficher_message_temporaire(utilisateur["id"])
            return
     
    afficher_message_temporaire("Cette adresse mail n'est pas enregistrée dans la base de données")

def bouton_ajouter_salle():
    # Bouton servant à ajouter un utilisateur
    # A faire
    None


creer_page_originale()