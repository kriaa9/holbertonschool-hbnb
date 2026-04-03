import re
from app.models.base_model import BaseModel
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name is required and must be a string")
        if len(first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters")

        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name is required and must be a string")
        if len(last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters")

        if not email or not isinstance(email, str):
            raise ValueError("email is required and must be a string")
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("email must follow a valid format (e.g. user@example.com)")

        if not password or not isinstance(password, str):
            raise ValueError("password is required and must be a string")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None
        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        """Hashes password updates before delegating common updates."""
        data_to_update = dict(data)
        if 'password' in data_to_update:
            self.hash_password(data_to_update.pop('password'))
        super().update(data_to_update)
