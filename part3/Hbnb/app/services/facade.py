from app.persistence.amenity_repository import AmenityRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ─── USER METHODS ─────────────────────────────────────────

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update_user(user_id, user_data)

    # ─── AMENITY METHODS ──────────────────────────────────────

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update_amenity(amenity_id, amenity_data)

    # ─── PLACE METHODS ────────────────────────────────────────

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError('Owner not found')

        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError('Amenity not found')
            amenities.append(amenity)

        place_payload = {
            'title': place_data.get('title'),
            'description': place_data.get('description', ''),
            'price': place_data.get('price'),
            'latitude': place_data.get('latitude'),
            'longitude': place_data.get('longitude'),
            'owner': owner,
        }

        place = Place(**place_payload)
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError('Owner not found')
            place.owner = owner

        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            updated_amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError('Amenity not found')
                updated_amenities.append(amenity)
            place.amenities = updated_amenities

        updatable_fields = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']
        data_to_update = {
            key: value for key, value in place_data.items() if key in updatable_fields
        }
        updated_place = self.place_repo.update_place(place_id, data_to_update)

        if not updated_place:
            return None
        return updated_place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        return self.place_repo.delete(place_id)

    # ─── REVIEW METHODS ───────────────────────────────────────

    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = self.get_user(user_id)
        if not user:
            raise ValueError('User not found')

        place = self.get_place(place_id)
        if not place:
            raise ValueError('Place not found')

        review_payload = {
            'text': review_data.get('text'),
            'rating': review_data.get('rating'),
            'place': place,
            'user': user,
        }
        review = Review(**review_payload)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if 'user_id' in review_data:
            user = self.get_user(review_data['user_id'])
            if not user:
                raise ValueError('User not found')
            review.user = user

        if 'place_id' in review_data:
            place = self.get_place(review_data['place_id'])
            if not place:
                raise ValueError('Place not found')
            review.place = place

        updatable_fields = ['text', 'rating']
        data_to_update = {
            key: value for key, value in review_data.items() if key in updatable_fields
        }

        updated_review = self.review_repo.update_review(review_id, data_to_update)
        if not updated_review:
            return None
        return updated_review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
