from .base import BaseModel


class Venue(BaseModel):
    table_name = "venues"
    fields = ["id", "name", "address", "seats"]
