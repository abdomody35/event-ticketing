from .base import BaseModel
from ..database.operations import DatabaseOperations


class Event(BaseModel):
    table_name = "events"
    fields = [
        "id",
        "venue_id",
        "category_id",
        "date",
        "name",
        "start_time",
        "seller_id",
        "number_of_tickets",
        "price",
        "number_of_bookings",
        "listing_time",
    ]

    @classmethod
    def get_upcoming_events(self):
        """Gets all upcoming events"""
        return DatabaseOperations.read_records(
            self.table_name, conditions="date >= CURRENT_DATE ORDER BY date, name, id"
        )

    @classmethod
    def get_user_events(self, user_id):
        """Gets all events created by a user"""
        return DatabaseOperations.read_records(
            self.table_name,
            conditions=f"seller_id = {user_id} ORDER BY date DESC, name, id",
        )
