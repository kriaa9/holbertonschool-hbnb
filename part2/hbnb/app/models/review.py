from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Import here to avoid circular imports
        from app.models.place import Place
        from app.models.user import User

        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")

        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required and must be a string")
        self._text = value.strip()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self._rating = value
