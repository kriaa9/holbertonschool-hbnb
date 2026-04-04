from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(2048), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews', lazy=True)
    place = db.relationship('Place', back_populates='reviews', lazy=True)

    def __init__(self, text, rating, place=None, user=None, place_id=None, user_id=None):
        super().__init__()

        if place is not None:
            from app.models.place import Place
            if not isinstance(place, Place):
                raise ValueError("place must be a valid Place instance")
            place_id = place.id
            self.place = place

        if user is not None:
            from app.models.user import User
            if not isinstance(user, User):
                raise ValueError("user must be a valid User instance")
            user_id = user.id
            self.user = user

        self._validate_text(text)
        self._validate_rating(rating)
        self._validate_user_id(user_id)
        self._validate_place_id(place_id)

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def _validate_text(text):
        if not text or not isinstance(text, str):
            raise ValueError("text is required and must be a string")

    @staticmethod
    def _validate_rating(rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

    @staticmethod
    def _validate_user_id(user_id):
        if user_id is not None and not isinstance(user_id, str):
            raise ValueError("user_id must be a string")

    @staticmethod
    def _validate_place_id(place_id):
        if place_id is not None and not isinstance(place_id, str):
            raise ValueError("place_id must be a string")

    def update(self, data):
        data_to_update = dict(data)

        if 'text' in data_to_update:
            self._validate_text(data_to_update['text'])
        if 'rating' in data_to_update:
            self._validate_rating(data_to_update['rating'])
        if 'user_id' in data_to_update:
            self._validate_user_id(data_to_update['user_id'])
        if 'place_id' in data_to_update:
            self._validate_place_id(data_to_update['place_id'])

        super().update(data_to_update)
