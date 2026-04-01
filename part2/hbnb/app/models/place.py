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

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number")

        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be a float between -90.0 and 90.0")

        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be a float between -180.0 and 180.0")

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

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)
