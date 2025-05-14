class Person:
    """Nom et prénom de la personne"""

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Reservation:
    """To implement."""
    
class Rooms1: "salle classique de 1 à 4 personnes"
    def __init__(self, capacité):
        self.capacité = capacité

class Rooms2: "salle avec ordinateur de 1 à 4 personnes"
    def __init__(self, capacité):
        self.capacité = capacité

class Rooms3: "salle de 4 à 10 personnes"
    def __init__(self, capacité):
        self.capacité = capacité

class ReservationError(Exception):
    """Erreur de réservation"""
    pass

class Reservation:

    def __init__(self, id):
        self.id = id
        self.rooms1 = []
        "salle classique de 1 à 4 personnes"
        self.rooms2 = []
        "salle avec ordinateur de 1 à 4 personnes"
        self.rooms3 = []
        "salle de 4 à 10 personnes"
        self.members = set()
        "id associé à l'email"
        self.borrowed_rooms = {}

    def is_room_available(self, room : Rooms1) -> bool:
        if isinstance(room, Rooms1) and room not in self.rooms1:
            raise ReservationError("La salle n'est pas disponible.")
        elif isinstance(room, Rooms2) and room not in self.rooms2:
            raise ReservationError("La salle n'est pas disponible.")
        elif isinstance(room, Rooms3) and room not in self.rooms3:
            raise ReservationError("La salle n'est pas disponible.")
            
    
    def borrow_room(self, room : Rooms1, person: Person):
        if room not in self.rooms1:
            raise ReservationError(f"La salle n'est pas dans la disponible.")
        if room not in self.rooms2:
            raise ReservationError(f"La salle n'est pas dans la disponible.")
        if room not in self.rooms3:
            raise ReservationError(f"La salle n'est pas dans la disponible.")
        
        if person not in self.members:
            raise ReservationError(f"{person} n'est pas un membre.")
        if room in self.borrowed_rooms:
            raise ReservationError(f"La salle est déjà prise.")
        self.borrowed_rooms[room] = person
        print(f"{person} a emprunté la salle.")

    def add_new_member(person: Person):
        if person in self.members:
            print(f"{person} est déjà un membre.")
        else:
            self.members.add(person)
            print(f"{person} a été ajouté aux membres.")

    def add_new_room(room):
        if isinstance(room, Rooms1):
            self.rooms1.append(room)
            print(f"Une nouvelle salle a été ajouté à la liste.")
        elif isinstance(room, Rooms2):
            self.rooms2.append(room)
            print(f"Une nouvelle salle a été ajouté à la liste.")
        elif isinstance(room, Rooms3):
            self.rooms3.append(room)
            print(f"Une nouvelle salle a été ajouté à la liste.")
        else:
            raise ReservationError("Type de salle non reconnu.")
    
def main():
    """Test your code here"""