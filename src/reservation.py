from datetime import datetime


class Room():
    """
    Room class to manage room details.
    """
    def __init__(self, room_name, capacity):
        self.room_name = room_name
        self.capacity = capacity

    def __str__(self):
        return f"Name: {self.room_name}, Capacity: {self.capacity}"
    
class ReservationError(Exception):
    """
    Custom exception for reservation errors.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class Reservation():
    """
    Reservation class to manage reservations.
    """
    def __init__(self, reservation_id, customer_name, date, time):
        self.reservation_id = reservation_id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.room = []

    def is_room_available(self, room : Room) -> bool:
        if isinstance(room, Room) and room not in self.room:
            raise ReservationError("La salle n'est pas disponible.")

    def is_valid(self):
        """
        Check if the reservation is valid.
        """
        try:
            datetime.strptime(self.date, '%Y-%m-%d')
            datetime.strptime(self.time, '%H:%M')
            return True
        except ValueError:
            return False
    

    def __str__(self):
        return (f"Reservation ID: {self.reservation_id}, Customer: {self.customer_name}, "
                f"Date: {self.date}, Time: {self.time}, Rooms: {[str(room) for room in self.rooms]}")