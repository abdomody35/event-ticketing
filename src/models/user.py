import bcrypt
from .base import BaseModel
from ..database.operations import DatabaseOperations


class User(BaseModel):
    table_name = "users"
    fields = ["id", "username", "password_hash"]

    @classmethod
    def create_user(cls, username: str, password: str):
        """Creates a new user with hashed password"""
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        return cls.create(username=username, password_hash=hashed)

    @classmethod
    def verify_password(cls, username: str, password: str) -> bool:
        """Verifies user password"""
        user = cls.get_by_username(username)
        if not user:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        )

    @classmethod
    def get_by_username(cls, username: str):
        """Retrieves user by username"""
        return DatabaseOperations.read_records(
            cls.table_name, conditions=f"username = '{username}'"
        )[0]
