from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name is required and must be a string")
        clean_name = value.strip()
        if len(clean_name) > 50:
            raise ValueError("name must not exceed 50 characters")
        self._name = clean_name
