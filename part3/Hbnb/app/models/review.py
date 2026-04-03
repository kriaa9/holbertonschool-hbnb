from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Import here to avoid circular imports
        from app.models.place import Place
        from app.models.user import User

        if not text or not isinstance(text, str):
            raise ValueError("text is required and must be a string")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")

        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
