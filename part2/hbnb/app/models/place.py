from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        # Import here to avoid circular imports
        from app.models.user import User

        if not title or not isinstance(title, str):
            raise ValueError("title is required and must be a string")
        if len(title) > 100:
            raise ValueError("title must not exceed 100 characters")

        if not isinstance(description, str):
            raise ValueError("description must be a string")

        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []    # List to store related Review instances
        self.amenities = []  # List to store related Amenity instances

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be a float between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be a float between -180.0 and 180.0")
        self._longitude = float(value)

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)
