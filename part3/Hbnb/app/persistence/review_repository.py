from app.extensions import db
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

    def get_review_by_user_and_place(self, user_id, place_id):
        return self.model.query.filter_by(user_id=user_id, place_id=place_id).first()

    def update_review(self, review_id, data):
        review = self.get(review_id)
        if not review:
            return None

        review.update(data)
        db.session.commit()
        return review
