from app.extensions import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def update_user(self, user_id, data):
        user = self.get(user_id)
        if not user:
            return None

        user.update(data)
        db.session.commit()
        return user
