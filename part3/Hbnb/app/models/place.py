from app.models.base_model import BaseModel
from app.extensions import db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=False, default='')
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # Keep owner_id as a simple scalar for business logic until relationship mapping task.
    owner_id = db.Column(db.String(36), nullable=True)

    def __init__(self, title, description, price, latitude, longitude, owner_id=None):
        super().__init__()

        self._validate_title(title)
        self._validate_description(description)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)
        self._validate_owner_id(owner_id)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        # Runtime-only helper attributes until ORM relationships are introduced.
        self.owner = None
        self.reviews = []    # List to store related Review instances
        self.amenities = []  # List to store related Amenity instances

    @staticmethod
    def _validate_title(title):
        if not title or not isinstance(title, str):
            raise ValueError("title is required and must be a string")
        if len(title) > 100:
            raise ValueError("title must not exceed 100 characters")

    @staticmethod
    def _validate_description(description):
        if description is None:
            return
        if not isinstance(description, str):
            raise ValueError("description must be a string")

    @staticmethod
    def _validate_price(value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("price must be a positive number greater than 0")

    @staticmethod
    def _validate_latitude(value):
        if not isinstance(value, (int, float)) or not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be a float between -90.0 and 90.0")

    @staticmethod
    def _validate_longitude(value):
        if not isinstance(value, (int, float)) or not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be a float between -180.0 and 180.0")

    @staticmethod
    def _validate_owner_id(owner_id):
        if owner_id is not None and not isinstance(owner_id, str):
            raise ValueError("owner_id must be a string")

    def update(self, data):
        data_to_update = dict(data)

        if 'title' in data_to_update:
            self._validate_title(data_to_update['title'])
        if 'description' in data_to_update:
            self._validate_description(data_to_update['description'])
        if 'price' in data_to_update:
            self._validate_price(data_to_update['price'])
        if 'latitude' in data_to_update:
            self._validate_latitude(data_to_update['latitude'])
        if 'longitude' in data_to_update:
            self._validate_longitude(data_to_update['longitude'])
        if 'owner_id' in data_to_update:
            self._validate_owner_id(data_to_update['owner_id'])

        super().update(data_to_update)

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)
