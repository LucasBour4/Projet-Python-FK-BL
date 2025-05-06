from tkinter import *
from tkinter import ttk

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter




# Définition de la classe
class CreerBouton:

    def __init__(self, name: str, parent): # Initialise la classe avec un parent (fenêtre).
        self._name = name
        self.parent = parent

    def creer_bouton(self, texte, commande=None, largeur=20, hauteur=2, couleur_fond="blue", couleur_texte="white", police=("Arial", 12)):
        
        #Crée un bouton avec les paramètres spécifiés.
        
        bouton = Button(
            self.parent,
            text=texte,
            command=commande,
            background=couleur_fond,
            fg=couleur_texte,
            font=police
        )
        bouton.config(width=largeur, height=hauteur)
        bouton.pack()
        return bouton

# Création de la fenêtre principale
application = Tk()

nom_application = Label(application, text="Votre compte réservation", font=("Arial", 20), fg="Green")
nom_application.pack()

# Créateur de boutons
bouton_creator = CreerBouton("menu_principal", application)

# Liste des boutons à créer (texte)
liste_boutons = [
    ("Identification"),
    ("Mes réservations"),
    ("Cliquez ici"),
    ("Cliquez ici")
]

# Création des boutons à partir de la liste
for texte in liste_boutons:
    bouton_creator.creer_bouton(texte, commande=quit, largeur= 20)

# Canvas
canvas = Canvas(application, width=200, height=200)
canvas.pack()
canvas.create_rectangle(0, 50, 500, 500, fill='red')

application.mainloop()