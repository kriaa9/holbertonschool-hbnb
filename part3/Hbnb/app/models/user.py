import re
from app.models.base_model import BaseModel
from app.extensions import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    places = db.relationship(
        'Place',
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy=True,
    )
    reviews = db.relationship(
        'Review',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy=True,
    )

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        self._validate_first_name(first_name)
        self._validate_last_name(last_name)
        self._validate_email(email)
        self._validate_password(password)
        self._validate_is_admin(is_admin)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    @staticmethod
    def _validate_first_name(first_name):
        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name is required and must be a string")
        if len(first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters")

    @staticmethod
    def _validate_last_name(last_name):
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name is required and must be a string")
        if len(last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters")

    @staticmethod
    def _validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("email is required and must be a string")
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("email must follow a valid format (e.g. user@example.com)")

    @staticmethod
    def _validate_password(password):
        if not password or not isinstance(password, str):
            raise ValueError("password is required and must be a string")

    @staticmethod
    def _validate_is_admin(is_admin):
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self._validate_password(password)
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        """Hashes password updates before delegating common updates."""
        data_to_update = dict(data)

        if 'first_name' in data_to_update:
            self._validate_first_name(data_to_update['first_name'])
        if 'last_name' in data_to_update:
            self._validate_last_name(data_to_update['last_name'])
        if 'email' in data_to_update:
            self._validate_email(data_to_update['email'])
        if 'is_admin' in data_to_update:
            self._validate_is_admin(data_to_update['is_admin'])

        if 'password' in data_to_update:
            self.hash_password(data_to_update.pop('password'))
        super().update(data_to_update)
