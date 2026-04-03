# tests.py
import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Tests for /api/v1/users/"""

    def setUp(self):
        """Runs before every test — creates a fresh app and client"""
        self.app = create_app()
        self.client = self.app.test_client()

    # ── POST /api/v1/users/ ──────────────────────────────────

    def test_create_user_success(self):
        """Valid data should return 201 with user object"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertNotIn('password', data)  # password must never be returned

    def test_create_user_duplicate_email(self):
        """Creating two users with the same email should return 400"""
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "duplicate@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_invalid_email(self):
        """Invalid email format should return 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_first_name(self):
        """Empty first_name should return 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_field(self):
        """Missing required field should return 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John"
        })
        self.assertEqual(response.status_code, 400)

    # ── GET /api/v1/users/ ───────────────────────────────────

    def test_get_all_users(self):
        """Should return 200 with a list"""
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    # ── GET /api/v1/users/<user_id> ──────────────────────────

    def test_get_user_by_id_success(self):
        """Should return 200 with correct user"""
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "bob@example.com"
        })
        user_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Non-existent ID should return 404"""
        response = self.client.get('/api/v1/users/fake-id-999')
        self.assertEqual(response.status_code, 404)

    # ── PUT /api/v1/users/<user_id> ──────────────────────────

    def test_update_user_success(self):
        """Valid update should return 200"""
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Carl",
            "last_name": "White",
            "email": "carl@example.com"
        })
        user_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Carlos",
            "last_name": "White",
            "email": "carlos@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Carlos')

    def test_update_user_not_found(self):
        """Updating a non-existent user should return 404"""
        response = self.client.put('/api/v1/users/fake-id-999', json={
            "first_name": "X",
            "last_name": "Y",
            "email": "xy@example.com"
        })
        self.assertEqual(response.status_code, 404)


class TestAmenityEndpoints(unittest.TestCase):
    """Tests for /api/v1/amenities/"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_amenity_by_id(self):
        post = self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        amenity_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], amenity_id)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/fake-id-999')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_success(self):
        post = self.client.post('/api/v1/amenities/', json={"name": "TV"})
        amenity_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Smart TV"})
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_not_found(self):
        response = self.client.put('/api/v1/amenities/fake-id-999', json={"name": "X"})
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Tests for /api/v1/places/"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create a user to act as owner for all place tests
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner@example.com"
        })
        self.owner_id = response.get_json()['id']

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Sunny Apartment",
            "description": "Nice view",
            "price": 120.0,
            "latitude": 36.8,
            "longitude": 10.1,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Sunny Apartment')

    def test_create_place_invalid_owner(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Ghost Place",
            "description": "",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": "non-existent-owner"
        })
        self.assertEqual(response.status_code, 404)

    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Price",
            "description": "",
            "price": -10.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Lat",
            "description": "",
            "price": 50.0,
            "latitude": 999.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Lon",
            "description": "",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 999.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_place_by_id(self):
        post = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "Sea view",
            "price": 200.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.owner_id
        })
        place_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], place_id)
        # Owner details must be embedded, not just owner_id
        self.assertIn('owner', data)
        self.assertIn('first_name', data['owner'])

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/fake-id-999')
        self.assertEqual(response.status_code, 404)

    def test_update_place_success(self):
        post = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "description": "desc",
            "price": 80.0,
            "latitude": 5.0,
            "longitude": 5.0,
            "owner_id": self.owner_id
        })
        place_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "description": "updated",
            "price": 90.0,
            "latitude": 5.0,
            "longitude": 5.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 200)

    def test_update_place_not_found(self):
        response = self.client.put('/api/v1/places/fake-id-999', json={
            "title": "X",
            "description": "",
            "price": 50.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 404)


class TestReviewEndpoints(unittest.TestCase):
    """Tests for /api/v1/reviews/"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create user
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "Test",
            "email": "reviewer@example.com"
        })
        self.user_id = user_resp.get_json()['id']

        # Create owner (can be same user)
        owner_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner.review@example.com"
        })
        self.owner_id = owner_resp.get_json()['id']

        # Create place
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "For reviews",
            "price": 75.0,
            "latitude": 15.0,
            "longitude": 25.0,
            "owner_id": self.owner_id
        })
        self.place_id = place_resp.get_json()['id']

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating_too_high(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad rating",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_zero(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Zero rating",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Ghost user",
            "rating": 3,
            "user_id": "fake-user-id",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Ghost place",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": "fake-place-id"
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_review_by_id(self):
        post = self.client.post('/api/v1/reviews/', json={
            "text": "Wonderful!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = post.get_json()['id']
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], review_id)

    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/fake-id-999')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        self.client.post('/api/v1/reviews/', json={
            "text": "Place review",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_review_success(self):
        post = self.client.post('/api/v1/reviews/', json={
            "text": "OK place",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = post.get_json()['id']
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Actually great!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_review_success(self):
        post = self.client.post('/api/v1/reviews/', json={
            "text": "Delete me",
            "rating": 2,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = post.get_json()['id']
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        # Confirm it's really gone
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/fake-id-999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
