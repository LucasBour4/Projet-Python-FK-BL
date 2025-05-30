from datetime import datetime
from gestion_base_donnees import charger_donnees, enregistrer_donnees
from interface_graphique import *

    
class ReservationError(Exception):
    """ Custom exception for reservation errors."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

class Reservation():
    """ Reservation class to manage reservations."""

    def __init__(self, reservation_id, customer_name, date, time):
        """ Initialize a reservation with ID, customer name, date, and time. """

        self.reservation_id = reservation_id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.room = []
        self.borrowed_rooms = {}
        self.members = set()

    def is_room_available(self, room : Room) -> bool:
        """   Check if a room is available for reservation. """

        if instance(room, Room) is False:
            raise ReservationError("La salle n'est pas disponible.")
        return room not in self.room

    def is_valid(self):
        """ Check if the reservation is valid."""

        try:
            datetime.strptime(self.date, '%Y-%m-%d')
            datetime.strptime(self.time, '%H:%M')
            return True
        except ValueError:
            return False
        
    def borrow_room(self, room : Room, person):
        """ Borrow a room for a member. """
        
        if room not in self.room:
            raise ReservationError("La salle n'est pas disponible.")
        if person not in self.members:
            raise ReservationError(f"{person} n'est pas un membre.")
        if room in self.borrowed_rooms:
            raise ReservationError("La salle est déjà prise.")
    

    def __str__(self):

        return (f"Reservation ID: {self.reservation_id}, Customer: {self.customer_name}, "
                f"Date: {self.date}, Time: {self.time}, Rooms: {[str(room) for room in self.rooms]}")