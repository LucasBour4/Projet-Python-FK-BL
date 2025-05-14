def Reservation():
    """
    Reservation class to manage reservations.
    """
    def __init__(self, reservation_id, customer_name, date, time):
        self.reservation_id = reservation_id
        self.customer_name = customer_name
        self.date = date
        self.time = time

    def __str__(self):
        return f"Reservation ID: {self.reservation_id}, Customer: {self.customer_name}, Date: {self.date}, Time: {self.time}"