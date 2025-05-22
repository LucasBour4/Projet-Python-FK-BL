# Fichier : interface_graphique.py
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askstring
from gestion_base_donnees import *

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter

#fenetre_principale = None

# Variables de style
FOND_FENETRE = "#F0FFF0"
BOUTON_PRINCIPAL = "#5F9EA0"
BOUTON_SECONDAIRE = "#B0C4DE"
TEXTE_BOUTON = "#333333"
TEXTE_TITRE = "#2E8B57"
ZONE_SAISIE = "#F5F5F5"

def afficher_message_temporaire(message : str, duree : int =10000):
    # Affiche un message temporaire (duree en millisecondes)
    popup = Toplevel()
    popup.title("Message")
    Label(popup, text=message, font=("Arial", 12)).pack(padx=20, pady=20)
    popup.after(duree, popup.destroy)

class Bouton(Button):
    def __init__(self, master, texte : str, commande = None, couleur_fond : str = BOUTON_PRINCIPAL, couleur_texte : str ="white", police=("Arial", 12)):
        # Crée un bouton avec les paramètres spécifiés.
        super().__init__(master, text=texte, command=commande, background=couleur_fond, fg=couleur_texte, font=police)
        self.config(width=20, height=4)
        #self.pack()

# class Application:
#     def __init__(self) -> None:
#         # Initialisation de la fenêtre principale
#         self.fenetre_principale = None

#     def creer_page_originale(self):
#         # Créer la page principale de l'application
#         self.fenetre_principale = Tk()
#         self.fenetre_principale.title("MeetingPro - Gestion des Réservations")
#         self.fenetre_principale.geometry("500x600")  # Gestion de la taille de la fenêtre

#         # Informations sur l'application
#         info = Label(self.fenetre_principale, text="MeetingPro vous propose ce service de réservation de salle", font=("Arial", 13), fg="Green")
#         info.pack()

#         # Création des boutons vers les différentes pages
#         Bouton("Ajouter un client", lambda: self.creer_page("Ajouter un client", self.fenetre_principale, "lightblue"), "lightblue")
#         Bouton("Ajouter une nouvelle salle", lambda: self.creer_page("Ajouter une nouvelle salle", self.fenetre_principale, "#98FB98"), "#98FB98", "black")
#         Bouton("Salles réservables", lambda: self.creer_page("Salles réservables", self.fenetre_principale, "#FFFFE0"))
#         Bouton("Réservation par client", lambda: self.creer_page("Réservation par client", self.fenetre_principale, "#FFDAB9"))
#         Bouton("Identifier si une salle est disponible pour un créneau", lambda: self.creer_page("Identifier si une salle est disponible pour un créneau", self.fenetre_principale, "#40E0D0"))
#         Bouton("Afficher les salles disponibles pour un créneau", lambda: self.creer_page("Afficher les salles disponibles pour un créneau", self.fenetre_principale, "#F08080"))
#         Bouton("Réserver une salle", lambda: self.creer_page("Réserver une salle", self.fenetre_principale, "#FFB6C1"))

#         self.credits(self.fenetre_principale)
#         self.fenetre_principale.mainloop()

#     def creer_page(self, titre: str, ancienne_fenetre, couleur_fond: str = "white"):
#         # Crée une nouvelle fenêtre
#         ancienne_fenetre.destroy()
#         fenetre = Tk()
#         fenetre.title(titre)
#         fenetre.geometry("500x600")
#         fenetre.configure(bg=couleur_fond)

#         # Informations et boutons présents sur la page
#         self.specificites_page(titre)
#         Bouton("Revenir à la page précédente", lambda: self.fenetre_precedente(fenetre))

#         self.credits(fenetre)
#         fenetre.mainloop()

#     def fenetre_precedente(self, fenetre):
#         # Fonction pour revenir à la fenêtre précédente
#         fenetre.destroy()
#         self.creer_page_originale()

#     def credits(self, fenetre):
#         # Ajoute les noms des créateurs de cette application
#         credits = Label(fenetre, text="Création de Kevin FERRY et Lucas BOUR", font=("Arial", 6), fg="Green")
#         credits.pack()

#     def specificites_page(self, role):
#         # Ajoute les boutons, labels et autres spécificités liés à la page
#         if role == "Ajouter un client":
#             couleur_bouton = "Steel Blue"
#             Bouton("Ajouter un nouveau client", lambda: bouton_ajouter_utilisateur(), couleur_bouton)
#             Bouton("Vous avez oublié votre id?", lambda: bouton_id(), couleur_bouton)
#         elif role == "Ajouter une nouvelle salle":
#             couleur_bouton = "#2E8B57"
#             Bouton("Ajouter une nouvelle salle", lambda: bouton_ajouter_salle(), couleur_bouton)

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("MeetingPro - Réservations de Salles de Réunion")
        self.geometry("900x430")

        self.nav_frame = Frame(self, bg=FOND_FENETRE)
        self.nav_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.container = Frame(self, bg=FOND_FENETRE)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (PageAccueil, Ajout_de_salle_et_client, Reserver_salle, Reservations):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.pages = [
            ("Page d'accueil", "PageAccueil"),
            ("Ajout de salle et client", "Ajout_de_salle_et_client"),
            ("Réserver une salle", "Reserver_salle"),
            ("Réservations", "Reservations")
        ]

        self.nav_buttons = {}
        self.show_frame("PageAccueil")

    def build_nav(self, active_page):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        for texte, page_name in self.pages:
            if page_name == active_page:
                label = Label(self.nav_frame, text=texte, bg=BOUTON_PRINCIPAL, fg="white", width=20, height=4, font=("Arial", 12)).pack(fill="x", pady=5)
                self.nav_buttons[page_name] = label
            else:
                bouton = Bouton(self.nav_frame, texte, lambda p=page_name: self.show_frame(p)).pack(fill="x", pady=5)
                self.nav_buttons[page_name] = bouton

        # Label en bas de la navigation
        Label(self.nav_frame, text="Création de Kevin FERRY et Lucas BOUR", font=("Arial", 8), fg="green", bg=FOND_FENETRE).pack(side="bottom", pady=10)

    def show_frame(self, page_name):
        self.build_nav(page_name)
        frame = self.frames[page_name]
        frame.tkraise()

class PageAccueil(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=FOND_FENETRE)
        Label(self, text="Bienvenue sur MeetingPro !", font=("Arial", 14), fg=TEXTE_TITRE, bg=FOND_FENETRE).pack(pady=20)

class Ajout_de_salle_et_client(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=FOND_FENETRE)
        Button(self, text="Ajouter un nouveau client", command=lambda: bouton_ajouter_utilisateur()).pack(pady=10)
        Bouton(self, "Vous avez oublié votre id?", lambda: bouton_id()).pack(pady=10)

class Reserver_salle(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=FOND_FENETRE)
        Label(self, text="Réservation de salle", font=("Arial", 14), bg=FOND_FENETRE).pack(pady=20)

class Reservations(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=FOND_FENETRE)
        Label(self, text="Consultation des réservations", font=("Arial", 14), bg=FOND_FENETRE).pack(pady=20)

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

if __name__ == "__main__":
    #creer_page_originale()
    app = Application()
    app.mainloop()