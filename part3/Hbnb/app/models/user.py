import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
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

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
