from tkinter import *
from tkinter import ttk

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter

fenetre_principale = None

def creer_bouton(texte, commande=None, largeur=40, hauteur=2, couleur_fond="blue", couleur_texte="white", police=("Arial", 12)):
        
    #Crée un bouton avec les paramètres spécifiés.
        
    bouton = Button(
        text = texte,
        command = commande,
        background = couleur_fond,
        fg = couleur_texte,
        font = police
    )
    bouton.config(width=largeur, height=hauteur)
    bouton.pack()
    return bouton

def creer_page_originale():
    global fenetre_principale
    fenetre_principale = Tk()
    fenetre_principale.title("MeetingPro - Gestion des Réservations")
    fenetre_principale.geometry("500x600") #Gestion de la taille de la fenêtre

    # Informations sur l'application
    info = Label(fenetre_principale, text="MeetingPro vous propose ce service", font=("Arial", 20), fg="Green")
    info.pack()

    #Création des boutons vers les différentes pages

    creer_bouton("S'identifier/Créer un compte", lambda : creer_page("S'identifier/Créer un compte", fenetre_principale, "lightblue")),
    creer_bouton("Salles réservables", lambda : creer_page("Salles réservables", fenetre_principale, "#98FB98")),
    creer_bouton("Réserver une salle", lambda : creer_page("Réserver une salle", fenetre_principale, "#FFFFE0")),
    creer_bouton("Réservation par client", lambda : creer_page("Réservation par client", fenetre_principale, "#FFDAB9")),
    creer_bouton("Identifier si une salle est disponible pour un créneau", lambda : creer_page("Identifier si une salle est disponible pour un créneau", fenetre_principale, "#40E0D0")),
    creer_bouton("Afficher les salles disponibles pour un créneau", lambda : creer_page("Afficher les salles disponibles pour un créneau", fenetre_principale, "#F08080")),
    creer_bouton("Réserver une salle", lambda : creer_page("Réserver une salle", fenetre_principale, "#FFB6C1")),

    # Canvas
    canvas = Canvas(fenetre_principale, width=200, height=200)
    canvas.pack()
    canvas.create_rectangle(0, 50, 500, 500, fill='red')

    fenetre_principale.mainloop()



def creer_page(titre, ancienne_fenetre, couleur_fond="white"):

    ancienne_fenetre.destroy()
    fenetre = Tk()
    fenetre.title(titre)
    fenetre.geometry("500x600") 
    fenetre.configure(bg=couleur_fond)
    
   
    creer_bouton("Revenir à la page précédente", lambda : fenetre_precedente(fenetre, ancienne_fenetre))

    fenetre.mainloop()

def fenetre_precedente(fenetre, ancienne_fenetre):
    # Fonction pour revenir à la fenêtre précédente
    if ancienne_fenetre == fenetre_principale:
        fenetre.destroy()
        creer_page_originale()
    else:
        creer_page(ancienne_fenetre, None)
    

creer_page_originale()