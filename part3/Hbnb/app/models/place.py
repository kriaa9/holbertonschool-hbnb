from app.models.base_model import BaseModel
from app.extensions import db
from app.models.associations import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=False, default='')
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', back_populates='places', lazy=True)
    reviews = db.relationship(
        'Review',
        back_populates='place',
        cascade='all, delete-orphan',
        lazy=True,
    )
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        back_populates='places',
        lazy='subquery',
    )

    def __init__(self, title, description, price, latitude, longitude, owner=None, owner_id=None, user_id=None):
        super().__init__()

        self._validate_title(title)
        self._validate_description(description)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)

        resolved_user_id = user_id if user_id is not None else owner_id
        if owner is not None:
            from app.models.user import User
            if not isinstance(owner, User):
                raise ValueError("owner must be a valid User instance")
            self.owner = owner
            resolved_user_id = owner.id

        self._validate_user_id(resolved_user_id)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = resolved_user_id

    @property
    def owner_id(self):
        return self.user_id

    @owner_id.setter
    def owner_id(self, value):
        self.user_id = value

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
    def _validate_user_id(user_id):
        if user_id is None or not isinstance(user_id, str):
            raise ValueError("user_id is required and must be a string")

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
            data_to_update['user_id'] = data_to_update.pop('owner_id')
        if 'user_id' in data_to_update:
            self._validate_user_id(data_to_update['user_id'])

        super().update(data_to_update)

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        self.amenities.append(amenity)
