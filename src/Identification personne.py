class Person:
    """Nom et prénom de la personne"""

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Reservation:
    """To implement."""

    def __init__(self, id):
        self.id = id
        self.rooms1 = []
        "salle classique de 1 à 4 personnes"
        self.rooms2 = []
        "salle avec ordinateur de 1 à 4 personnes"
        self.rooms3 = []
        "salle de 4 à 10 personnes"
        self.members = {}
        "id associé à l'email"
        self.borrowed_rooms = {}

    def is_room_available(self, room : Room) -> bool:
        if room not in self.rooms:
            raise ReservationError(f"La salle est disponible")
        return room not in self.borrowed_rooms
    
    def borrow_room(self, room : Room, person: Person):
        if room not in self.rooms:
            raise ReservationError(f"La salle n'est pas dans la disponible.")
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

    def add_new_room(room: Room):
        self.rooms.append(room)
        print(f"Une nouvelle salle a été ajouté à la liste.")


class ReservationError(Exception):
    """Erreur de réservation"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"ReservationError: {self.message}"
    
def main():
    """Test your code here"""