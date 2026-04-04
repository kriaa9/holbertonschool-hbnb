from app.models.base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()

        self._validate_name(name)

        self.name = name

    @staticmethod
    def _validate_name(name):
        if not name or not isinstance(name, str):
            raise ValueError("name is required and must be a string")
        if len(name) > 50:
            raise ValueError("name must not exceed 50 characters")

    def update(self, data):
        data_to_update = dict(data)
        if 'name' in data_to_update:
            self._validate_name(data_to_update['name'])
        super().update(data_to_update)
