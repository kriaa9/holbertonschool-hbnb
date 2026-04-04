from app.extensions import db
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def update_amenity(self, amenity_id, data):
        amenity = self.get(amenity_id)
        if not amenity:
            return None

        amenity.update(data)
        db.session.commit()
        return amenity
