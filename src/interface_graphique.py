from tkinter import *
from tkinter import ttk

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter

# Création des éléments de la fenêtre

application = Tk()

nom_application = Label(application, text = "Votre compte réservation", font = ("Arial", 20), fg = "Green")

bouton1 = Button(application, text="Identification", command=quit, background="blue", fg="white", font=("Arial", 12))
bouton1.config(width=20, height=2)

bouton2 = Button(application, text="Mes réservations", command=quit, background="blue", fg="white", font=("Arial", 12))
bouton2.config(width=20, height=2)

bouton3 = Button(application, text="Cliquez ici", command=quit, background="blue", fg="white", font=("Arial", 12))
bouton3.config(width=20, height=2)

bouton4 = Button(application, text="Cliquez ici", command=quit, background="blue", fg="white", font=("Arial", 12))
bouton4.config(width=30, height=2)

canvas = Canvas(application, width=200, height=200)


# Organisation fenêtre

nom_application.pack()
bouton1.pack()
bouton2.pack()
bouton3.pack()
bouton4.pack()
canvas.pack()
canvas.create_rectangle(0, 50, 500, 500, fill='red')

application.mainloop()


class CreerBouton:

    def __init__(self, name : str, parent):
        """
        Initialise la classe avec un parent (fenêtre ou frame).
        """
        self._name = name
        self.parent = parent

    def creer_bouton(self, text, commande=None, largeur=20, hauteur=2, couleur_fond="blue", couleur_texte="white", police=("Arial", 12)):
        """
        Crée un bouton avec les paramètres spécifiés.
        """
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