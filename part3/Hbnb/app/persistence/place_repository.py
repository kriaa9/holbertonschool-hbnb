from app.extensions import db
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def update_place(self, place_id, data):
        place = self.get(place_id)
        if not place:
            return None

        place.update(data)
        db.session.commit()
        return place
