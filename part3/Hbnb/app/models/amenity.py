from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name or not isinstance(name, str):
            raise ValueError("name is required and must be a string")
        if len(name) > 50:
            raise ValueError("name must not exceed 50 characters")

        self.name = name
