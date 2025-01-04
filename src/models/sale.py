from .base import BaseModel
from ..database.operations import DatabaseOperations


class Sale(BaseModel):
    table_name = "sales"
    fields = [
        "id",
        "listing_id",
        "seller_id",
        "buyer_id",
        "event_id",
        "quantity_sold",
        "price_paid",
    ]

    @classmethod
    def create_sale(self, listing_id, buyer_id, quantity):
        """Creates a new sale"""
        listing = DatabaseOperations.read_records(
            "listings", conditions=f"id = {listing_id}"
        )

        if listing["number_of_tickets"] < quantity:
            raise ValueError("Not enough tickets available")

        sale_data = {
            "listing_id": listing_id,
            "seller_id": listing["seller_id"],
            "buyer_id": buyer_id,
            "event_id": listing["event_id"],
            "quantity_sold": quantity,
            "price_paid": listing["price_per_ticket"] * quantity,
        }

        DatabaseOperations.update_record(
            "listings",
            {"number_of_tickets": listing["number_of_tickets"] - quantity},
            f"id = {listing_id}",
        )

        return self.create(**sale_data)

    @classmethod
    def get_user_purchases(self, user_id):
        """Gets all purchases for a user"""
        return DatabaseOperations.read_records(
            self.table_name, conditions=f"buyer_id = {user_id} ORDER BY sale_time DESC"
        )
