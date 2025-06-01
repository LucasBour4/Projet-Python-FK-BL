""""
interface_graphique.py:
Fichier gérant l'interface graphique de l'application MeetingPro.

Il permet de naviguer entre les différentes pages de l'application,
d'afficher des formulaires pour ajouter des clients et des salles,
et de gérer les réservations de salles.

-*- coding: utf-8 -*-
"""

# Importation des modules nécessaires
from tkinter import *
from tkinter.ttk import Combobox
from gestion_base_donnees import *
from datetime import datetime, timedelta as dt_timedelta
import uuid

# Variables de style
FOND_FENETRE = "#F0FFF0"
BOUTON_PRINCIPAL = "#5F9EA0"
BOUTON_SECONDAIRE = "#B0C4DE"
TEXTE_BOUTON = "#333333"
TEXTE_TITRE = "#2E8B57"
ZONE_SAISIE = "#F5F5F5"


def afficher_message_temporaire(message: str, duree: int = 5000) -> None:
    """Affiche un message temporaire dans une popup pendant une durée définie (en ms)."""
    popup = Toplevel()
    popup.title("Message")
    Label(popup, text=message, font=("Arial", 12)).pack(padx=20, pady=20)
    popup.after(duree, popup.destroy)


class Bouton(Button):
    """Bouton personnalisé avec un style pré-défini."""

    def __init__(self, master, texte: str, commande=None, couleur_fond: str = BOUTON_PRINCIPAL, couleur_texte: str = "white", police=("Arial", 12), largeur: int = 20) -> None:
        super().__init__(master, text=texte, command=commande,
                         background=couleur_fond, fg=couleur_texte, font=police)
        self.config(width=largeur, height=2)


def creer_scrollbar(parent, bg=None, height=400):
    """Crée une zone scrollable verticale avec un Canvas.

    Retourne (canvas, frame_contenu) à utiliser pour y placer les widgets.
    """
    container = Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    canvas = Canvas(container, bg=bg, highlightthickness=0, height=height)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame_contenu = Frame(canvas, bg=bg)
    canvas.create_window((0, 0), window=frame_contenu, anchor="nw")

    def ajuster_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_contenu.bind("<Configure>", ajuster_scroll)

    # Option : molette de souris
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(
        int(-1*(e.delta/120)), "units"))

    return frame_contenu


class Application(Tk):
    """Classe principale de l'application qui gère les pages et la navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.title("MeetingPro - Réservations de Salles de Réunion")
        self.geometry("900x500")

        self.nav_frame = Frame(self, bg=FOND_FENETRE)
        self.nav_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.container = Frame(self, bg=FOND_FENETRE)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (PageAccueil, Ajout_de_salle_et_client, Reserver_salle, Afficher):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.pages = [
            ("Page d'accueil", "PageAccueil"),
            ("Ajout de salle et client", "Ajout_de_salle_et_client"),
            ("Réserver une salle", "Reserver_salle"),
            ("Afficher", "Afficher")
        ]

        self.nav_buttons = {}
        self.show_frame("PageAccueil")

    def build_nav(self, active_page: str) -> None:
        """Construit le menu de navigation à gauche, en mettant en évidence la page active."""
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        for texte, page_name in self.pages:
            if page_name == active_page:
                Label(self.nav_frame, text=texte, bg=BOUTON_PRINCIPAL, fg="white",
                      width=20, height=2, font=("Arial", 12)).pack(fill="x", pady=5)
            else:
                Bouton(self.nav_frame, texte, lambda p=page_name: self.show_frame(p)).pack(
                    fill="x", pady=5)

        Label(self.nav_frame, text="Création de Kevin FERRY et Lucas BOUR", font=(
            "Arial", 8), fg="green", bg=FOND_FENETRE).pack(side="bottom", pady=10)

    def show_frame(self, page_name: str) -> None:
        """Affiche la frame/page spécifiée."""
        self.build_nav(page_name)
        frame = self.frames[page_name]
        frame.tkraise()


class PageAccueil(Frame):
    """Page pour ajouter un client, une salle ou retrouver un identifiant."""

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=FOND_FENETRE)
        Label(self, text="Bienvenue sur MeetingPro !", font=(
            "Arial", 14), fg=TEXTE_TITRE, bg=FOND_FENETRE).pack(pady=20)

        Label(self, text=(
            "MeetingPro est une application Python qui permet la gestion des réservations "
            "de salles de \nréunion à travers une interface graphique.\n\n"
            "Elle prend en charge la création de salles, l’enregistrement des utilisateurs, "
            "et la réservation d’horaires précis,\navec une sauvegarde des données en JSON.\n\n\n\n"
            "Vous trouverez à gauche un menu de navigation pour accéder aux différentes fonctionnalités\nde l'application tel que:\n"
            "   - Ajoute de salle ou client: qui permet d'ajouter de nouveaux clients ou de nouvelles salles\n"
            "   - Réserver une salle: qui permet comme son nom l'indique de réserver une salle de réunion\n"
            "   - Afficher: qui permet d'afficher les listes des clients enregistrées, des salles existantes ainsi \n     que des réservations."
        ),
            wraplength=700,
            justify="left",
            font=("Arial", 12),
            bg=FOND_FENETRE,
            fg="#333333"
        ).pack(padx=20, pady=10)


class Ajout_de_salle_et_client(Frame):
    """Page pour ajouter un client, une salle ou retrouver un identifiant."""

    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=FOND_FENETRE)
        self.controller = controller

        Bouton(self, "Ajouter un nouveau client", lambda: self.afficher_formulaire(
            "client"), largeur=28).grid(row=0, column=0, pady=10, padx=20, sticky="nw")
        Bouton(self, "Vous avez oublié votre id ?", lambda: self.afficher_formulaire(
            "id"), largeur=28).grid(row=1, column=0, pady=10, padx=20, sticky="nw")
        Bouton(self, "Ajouter une nouvelle salle", lambda: self.afficher_formulaire(
            "salle"), largeur=28).grid(row=2, column=0, pady=10, padx=20, sticky="nw")

        self.formulaire_client = None
        self.formulaire_salle = None
        self.formulaire_id = None

    def _creer_label_entry(self, parent: Frame, texte: str, ligne: int, colonne: int, combobox_values: list = None, var=None, width: int = None):
        """Crée un champ de formulaire avec label et zone de saisie ou combobox."""
        Label(parent, text=texte, bg=FOND_FENETRE).grid(
            row=ligne, column=colonne, sticky="w", padx=5, pady=5)
        if combobox_values:
            var = var or StringVar()
            cb = Combobox(parent, textvariable=var,
                          state="readonly", values=combobox_values)
            cb.grid(row=ligne, column=colonne+1, sticky="w", padx=5, pady=5)
            cb.current(0)
            return var, cb
        else:
            entry = Entry(parent, bg=ZONE_SAISIE,
                          textvariable=var, width=width)
            entry.grid(row=ligne, column=colonne+1, sticky="w", padx=5, pady=5)
            return entry

    def creer_formulaire_client(self) -> Frame:
        """ Formulaire pour ajouter un client."""
        form = Frame(self, bg=FOND_FENETRE)
        nom_entry = self._creer_label_entry(form, "Nom :", 0, 0)
        prenom_entry = self._creer_label_entry(form, "Prénom :", 1, 0)
        email_entry = self._creer_label_entry(form, "Adresse mail :", 2, 0)

        def valider() -> None:
            nom = nom_entry.get().strip()
            prenom = prenom_entry.get().strip()
            email = email_entry.get().strip()
            if not (nom and prenom and email):
                afficher_message_temporaire("Tous les champs sont requis.")
                return
            ajouter_utilisateur(nom, prenom, email)
            afficher_message_temporaire("Utilisateur ajouté avec succès.")
            form.destroy()
            self.formulaire_client = None

        Bouton(form, "Valider", valider).grid(
            row=3, column=1, sticky="e", pady=10)
        return form

    def creer_formulaire_salle(self) -> Frame:
        """Formulaire pour ajouter une salle."""
        form = Frame(self, bg=FOND_FENETRE)
        nom_entry = self._creer_label_entry(form, "Nom de la salle :", 0, 0)
        type_var, combobox = self._creer_label_entry(form, "Type de salle :", 1, 0, [
                                                     "classique", "informatique", "conférence"])
        capacite_var = IntVar()
        capacite_entry = self._creer_label_entry(
            form, "Capacité :", 2, 0, var=capacite_var, width=5)

        def valider() -> None:
            nom = nom_entry.get().strip()
            t = type_var.get()
            try:
                capacite = int(capacite_entry.get())
            except ValueError:
                afficher_message_temporaire(
                    "Capacité doit être un nombre valide.")
                return
            if not nom:
                afficher_message_temporaire("Le nom est requis.")
                return
            ajouter_salle(nom, t, capacite)
            afficher_message_temporaire("Salle ajoutée avec succès.")
            form.destroy()
            self.formulaire_salle = None

        Bouton(form, "Valider", valider).grid(
            row=3, column=1, sticky="e", pady=10)
        return form

    def creer_formulaire_id(self) -> Frame:
        """Formulaire pour retrouver son ID à partir de l'adresse e-mail."""
        form = Frame(self, bg=FOND_FENETRE)
        Label(form, text="Entrez votre adresse mail :",
              bg=FOND_FENETRE).grid(row=0, column=0, padx=5, pady=5)
        email_entry = Entry(form, bg=ZONE_SAISIE)
        email_entry.grid(row=0, column=1, padx=5, pady=5)

        def valider() -> None:
            email = email_entry.get().strip()
            if not email:
                afficher_message_temporaire(
                    "Veuillez saisir une adresse mail.")
                return
            donnees = charger_donnees()
            for utilisateur in donnees["utilisateurs"]:
                if utilisateur["email"] == email:
                    afficher_message_temporaire(
                        f"Votre ID est : {utilisateur['id']}")
                    form.destroy()
                    self.formulaire_id = None
                    return
            afficher_message_temporaire("Adresse mail non trouvée.")

        Bouton(form, "Valider", valider).grid(
            row=1, column=1, sticky="e", pady=10)
        return form

    def afficher_formulaire(self, type_formulaire: str) -> None:
        """Affiche un formulaire donné (client, salle, id) et masque les autres."""
        formulaires = {
            "client": ("formulaire_client", self.creer_formulaire_client),
            "salle": ("formulaire_salle", self.creer_formulaire_salle),
            "id": ("formulaire_id", self.creer_formulaire_id)
        }
        for nom, _ in formulaires.values():
            form = getattr(self, nom)
            if form:
                form.destroy()
                setattr(self, nom, None)

        nom, create = formulaires[type_formulaire]
        new_form = create()
        setattr(self, nom, new_form)
        new_form.grid(row=0, column=1, rowspan=4,
                      padx=20, pady=10, sticky="nw")


class Reserver_salle(Frame):
    """Page de réservation."""

    def __init__(self, parent: Frame, controller: Application) -> None:
        super().__init__(parent, bg=FOND_FENETRE)
        Label(self, text="Réservation de salle", font=("Arial", 14), bg=FOND_FENETRE).pack(pady=20)

        form = Frame(self, bg=FOND_FENETRE)
        form.pack(pady=10)

        # Adresse mail client
        Label(form, text="Votre adresse mail :", bg=FOND_FENETRE).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = Entry(form, bg=ZONE_SAISIE)
        self.email_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Type de salle
        Label(form, text="Type de salle :", bg=FOND_FENETRE).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.type_salle_var = StringVar()
        self.type_salle_cb = Combobox(form, textvariable=self.type_salle_var, state="readonly",
                                      values=["classique", "conférence", "informatique"])
        self.type_salle_cb.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.type_salle_cb.current(0)

        # Nombre de personnes
        Label(form, text="Nombre de personnes :", bg=FOND_FENETRE).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.nb_personnes_var = StringVar()
        self.nb_personnes_cb = Combobox(form, textvariable=self.nb_personnes_var, state="readonly",
                                        values=[str(i) for i in range(1, 11)])
        self.nb_personnes_cb.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.nb_personnes_cb.current(0)

        # Jour
        Label(form, text="Jour (YYYY-MM-DD) :", bg=FOND_FENETRE).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.jour_entry = Entry(form, bg=ZONE_SAISIE)
        self.jour_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Heure de début
        Label(form, text="Heure de début (HH:MM) :", bg=FOND_FENETRE).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.heure_debut_entry = Entry(form, bg=ZONE_SAISIE)
        self.heure_debut_entry.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Durée (en minutes)
        Label(form, text="Durée (en minutes) :", bg=FOND_FENETRE).grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.duree_entry = Entry(form, bg=ZONE_SAISIE)
        self.duree_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        # Bouton de validation
        Bouton(self, "Valider la réservation", self.valider_reservation).pack(pady=10)

    def valider_reservation(self) -> None:
        email = self.email_entry.get().strip()
        type_salle = self.type_salle_var.get()
        nb_personnes_str = self.nb_personnes_var.get()
        jour = self.jour_entry.get().strip()
        heure_debut = self.heure_debut_entry.get().strip()
        duree = self.duree_entry.get().strip()

        if not all([email, type_salle, nb_personnes_str, jour, heure_debut, duree]):
            afficher_message_temporaire("Veuillez remplir tous les champs.")
            return

        try:
            nb_personnes = int(nb_personnes_str)
            duree_minutes = int(duree)
        except ValueError:
            afficher_message_temporaire("Nombre de personnes ou durée invalide.")
            return

        try:
            debut = datetime.fromisoformat(f"{jour}T{heure_debut}")
            duree_timedelta = dt_timedelta(minutes=duree_minutes)

            donnees = charger_donnees()
            salles = donnees.get("salles", [])

            # Recherche d'une salle disponible
            salle_choisie = None
            for salle in salles:
                if salle["type"] == type_salle and salle["capacite"] >= nb_personnes:
                    salle_choisie = salle
                    break

            if not salle_choisie:
                afficher_message_temporaire("Aucune salle disponible correspondant au type et capacité demandés.")
                return

            # Vérification de l'existence du client
            utilisateurs = donnees.get("utilisateurs", [])
            client_trouve = any(u["email"] == email for u in utilisateurs)
            if not client_trouve:
                afficher_message_temporaire("Adresse mail client non trouvée.")
                return

            reservation = {
                "id": str(uuid.uuid4()),
                "email": email,
                "salle": salle_choisie["nom"],
                "debut": debut,
                "duree_minutes": duree_minutes,
                "nb_personnes": nb_personnes,
            }

            ajouter_reservation(reservation)

            resume = (
                f"Réservation confirmée:\n"
                f"- Email : {email}\n"
                f"- Salle : {salle_choisie['nom']} (Type : {type_salle})\n"
                f"- Date et heure : {debut.strftime('%d/%m/%Y à %H:%M')}\n"
                f"- Durée : {duree_minutes} minutes\n"
                f"- Nombre de personnes : {nb_personnes}"
            )
            afficher_message_temporaire(resume)

        except ValueError:
            afficher_message_temporaire("Format de date ou heure invalide.")
        except Exception as e:
            afficher_message_temporaire(f"Erreur lors de la réservation : {str(e)}")



class Afficher(Frame):
    """Page permettant d'afficher les salles, les clients ou les réservations."""

    def __init__(self, parent: Frame, controller: Application) -> None:
        super().__init__(parent, bg=FOND_FENETRE)
        self.controller = controller

        Label(self, text="Afficher", font=("Arial", 14), bg=FOND_FENETRE).grid(
            row=0, column=0, columnspan=2, pady=20, sticky="w")

        # Boutons d'affichage
        self.bouton_frame = Frame(self, bg=FOND_FENETRE)
        self.bouton_frame.grid(row=1, column=0, sticky="nw", padx=10)

        Bouton(self.bouton_frame, "Liste des salles",
               self.afficher_salles, largeur=27).pack(pady=5, anchor="w")
        Bouton(self.bouton_frame, "Liste des clients",
               self.afficher_clients, largeur=27).pack(pady=5, anchor="w")
        Bouton(self.bouton_frame, "Salles disponibles pour un créneau",
               self.afficher_salles_disponibles, largeur=27).pack(pady=5, anchor="w")
        Bouton(self.bouton_frame, "Réservations par client",
               self.afficher_reservations_client, largeur=27).pack(pady=5, anchor="w")

        # Colonne d'affichage
        self.zone_affichage = Frame(self, bg=FOND_FENETRE)
        self.zone_affichage.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def afficher_salles(self) -> None:
        """Affiche toutes les salles enregistrées."""
        for widget in self.zone_affichage.winfo_children():
            widget.destroy()

        salles = charger_donnees().get("salles", [])

        contenu = creer_scrollbar(self.zone_affichage, bg=FOND_FENETRE)

        Label(contenu, text="Liste des salles existantes :", font=(
            "Arial", 14), bg=FOND_FENETRE, fg=TEXTE_TITRE).pack(pady=(0, 10))

        if not salles:
            Label(contenu, text="Aucune salle enregistrée.", font=(
                "Arial", 12), bg=FOND_FENETRE).pack(pady=10)
        else:
            for salle in salles:
                nom = salle.get("nom", "Inconnu")
                type_salle = salle.get("type", "N/A")
                capacite = salle.get("capacite", "N/A")
                Label(
                    contenu,
                    text=f"• {nom} - {type_salle} — Capacité : {capacite}",
                    font=("Arial", 11),
                    anchor="w",
                    bg=FOND_FENETRE
                ).pack(fill="x", padx=10, pady=5)

    def afficher_clients(self) -> None:
        """Affiche tous les clients enregistrés."""
        for widget in self.zone_affichage.winfo_children():
            widget.destroy()

        clients = charger_donnees().get("utilisateurs", [])

        contenu = creer_scrollbar(self.zone_affichage, bg=FOND_FENETRE)

        Label(contenu, text="Liste des clients enregistrés :", font=(
            "Arial", 14), bg=FOND_FENETRE, fg=TEXTE_TITRE).pack(pady=(0, 10))

        if not clients:
            Label(contenu, text="Aucun client enregistré.", font=(
                "Arial", 12), bg=FOND_FENETRE).pack(pady=10)
        else:
            for c in clients:
                nom = c.get("nom", "Inconnu")
                prenom = c.get("prenom", "")
                email = c.get("email", "")
                Label(
                    contenu,
                    text=f"• {prenom} {nom} — Email : {email}",
                    font=("Arial", 11),
                    anchor="w",
                    bg=FOND_FENETRE
                ).pack(fill="x", padx=10, pady=5)

    def afficher_salles_disponibles(self) -> None:
        """Affiche les salles disponibles pour un créneau donné."""
        for widget in self.zone_affichage.winfo_children():
            widget.destroy()

        contenu = creer_scrollbar(self.zone_affichage, bg=FOND_FENETRE)
        Label(contenu, text="Salles disponibles :", font=("Arial", 14),
            bg=FOND_FENETRE, fg=TEXTE_TITRE).pack(pady=(0, 10))

        form = Frame(contenu, bg=FOND_FENETRE)
        form.pack(pady=5)

        jour_entry = Entry(form, bg=ZONE_SAISIE)
        heure_entry = Entry(form, bg=ZONE_SAISIE)
        duree_entry = Entry(form, bg=ZONE_SAISIE)

        Label(form, text="Jour (YYYY-MM-DD):", bg=FOND_FENETRE).grid(row=0, column=0, sticky="w")
        jour_entry.grid(row=0, column=1)
        Label(form, text="Heure (HH:MM):", bg=FOND_FENETRE).grid(row=1, column=0, sticky="w")
        heure_entry.grid(row=1, column=1)
        Label(form, text="Durée (en minutes):", bg=FOND_FENETRE).grid(row=2, column=0, sticky="w")
        duree_entry.grid(row=2, column=1)

        def valider():
            try:
                debut = datetime.fromisoformat(f"{jour_entry.get()}T{heure_entry.get()}")
                duree_minutes = int(duree_entry.get())
                fin = debut + timedelta(minutes=duree_minutes)

                data = charger_donnees()
                reservations = data.get("reservations", [])

                occupées = {
                    r["salle"]
                    for r in reservations
                    if not (
                        fin <= datetime.fromisoformat(r["debut"]) or
                        debut >= datetime.fromisoformat(r["debut"]) + timedelta(minutes=r["duree_minutes"])
                    )
                }

                dispo = [s for s in data.get("salles", []) if s["nom"] not in occupées]

                Label(contenu, text="Résultats :", font=("Arial", 13), bg=FOND_FENETRE).pack(pady=10)
                if not dispo:
                    Label(contenu, text="Aucune salle disponible.", bg=FOND_FENETRE).pack()
                else:
                    for s in dispo:
                        Label(
                            contenu,
                            text=f"• {s['nom']} - {s['type']} — Capacité : {s['capacite']}",
                            bg=FOND_FENETRE,
                            font=("Arial", 11)
                        ).pack(anchor="w", padx=10, pady=2)

            except ValueError:
                Label(contenu, text="Veuillez saisir une durée en minutes valide.", fg="red", bg=FOND_FENETRE).pack(pady=10)
            except Exception as e:
                Label(contenu, text=f"Erreur : {e}", fg="red", bg=FOND_FENETRE).pack(pady=10)

        Bouton(form, "Valider", valider).grid(row=3, column=1, pady=10, sticky="e")


    def afficher_reservations_client(self) -> None:
        """Affiche les réservations d’un client (via son email)."""
        for widget in self.zone_affichage.winfo_children():
            widget.destroy()

        contenu = creer_scrollbar(self.zone_affichage, bg=FOND_FENETRE)
        Label(contenu, text="Réservations d’un client :", font=("Arial", 14),
            bg=FOND_FENETRE, fg=TEXTE_TITRE).pack(pady=(0, 10))

        form = Frame(contenu, bg=FOND_FENETRE)
        form.pack(pady=5)

        email_entry = Entry(form, bg=ZONE_SAISIE)
        Label(form, text="Email :", bg=FOND_FENETRE).grid(row=0, column=0, sticky="w")
        email_entry.grid(row=0, column=1)

        def valider():
            email = email_entry.get().strip().lower()
            if not email:
                Label(contenu, text="Veuillez entrer une adresse e-mail.", fg="red", bg=FOND_FENETRE).pack()
                return

            reservations = [
                r for r in charger_donnees().get("reservations", [])
                if r.get("email", "").lower() == email
            ]

            Label(contenu, text="Réservations :", font=("Arial", 13), bg=FOND_FENETRE).pack(pady=10)
            if not reservations:
                Label(contenu, text="Aucune réservation trouvée.", bg=FOND_FENETRE).pack()
            else:
                for r in reservations:
                    texte = (
                        f"• Salle : {r['salle']} | "
                        f"Début : {r['debut']} | \n"
                        f"Durée : {r['duree_minutes']} min | "
                        f"Nombre de personnes : {r['nb_personnes']}"
                    )
                    Label(contenu, text=texte, font=("Arial", 11), anchor="w", bg=FOND_FENETRE).pack(fill="x", padx=10, pady=2)

        Bouton(form, "Valider", valider).grid(row=1, column=1, pady=10, sticky="e")