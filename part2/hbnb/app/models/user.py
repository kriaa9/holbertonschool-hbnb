import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        self.is_admin = is_admin


    @staticmethod
    def _validate_name(field_name, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} is required and must be a string")
        if len(value.strip()) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return value.strip()

    @staticmethod
    def _validate_email(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required and must be a string")
        email = value.strip()
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("email must follow a valid format (e.g. user@example.com)")
        return email

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_name("first_name", value)

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_name("last_name", value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)
