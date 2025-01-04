from .base import BaseModel


class Category(BaseModel):
    table_name = "categories"
    fields = ["id", "name"]
