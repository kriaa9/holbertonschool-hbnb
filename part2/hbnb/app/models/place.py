from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        # Import here to avoid circular imports
        from app.models.user import User

        self._title = None
        self._description = None
        self._price = None
        self._latitude = None
        self._longitude = None

        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("title is required and must be a string")
        if len(value) > 100:
            raise ValueError("title must not exceed 100 characters")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise ValueError("description must be a string")
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("price must be a number")
        if value < 0:
            raise ValueError("price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        if not -90 <= float(value) <= 90:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if not -180 <= float(value) <= 180:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
