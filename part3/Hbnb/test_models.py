# test_models.py

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


# ─── USER TESTS ───────────────────────────────────────────────

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    assert user.id is not None
    assert user.created_at is not None
    print("✅ test_user_creation passed")

def test_user_invalid_email():
    try:
        user = User(first_name="John", last_name="Doe", email="not-an-email")
        print("❌ test_user_invalid_email FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_user_invalid_email passed — caught: {e}")

def test_user_name_too_long():
    try:
        user = User(first_name="A" * 51, last_name="Doe", email="a@b.com")
        print("❌ test_user_name_too_long FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_user_name_too_long passed — caught: {e}")


# ─── AMENITY TESTS ────────────────────────────────────────────

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.id is not None
    print("✅ test_amenity_creation passed")

def test_amenity_empty_name():
    try:
        amenity = Amenity(name="")
        print("❌ test_amenity_empty_name FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_amenity_empty_name passed — caught: {e}")


# ─── PLACE TESTS ──────────────────────────────────────────────

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert place.owner == owner
    assert place.reviews == []
    assert place.amenities == []
    print("✅ test_place_creation passed")

def test_place_invalid_price():
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    try:
        place = Place(title="Bad Place", description="", price=-50,
                      latitude=0, longitude=0, owner=owner)
        print("❌ test_place_invalid_price FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_place_invalid_price passed — caught: {e}")

def test_place_invalid_latitude():
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    try:
        place = Place(title="Bad Place", description="", price=50,
                      latitude=999, longitude=0, owner=owner)
        print("❌ test_place_invalid_latitude FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_place_invalid_latitude passed — caught: {e}")

def test_place_add_review_and_amenity():
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(title="Nice Place", description="Great", price=80,
                  latitude=10.0, longitude=20.0, owner=owner)

    review = Review(text="Loved it!", rating=5, place=place, user=owner)
    place.add_review(review)

    amenity = Amenity(name="Pool")
    place.add_amenity(amenity)

    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Loved it!"
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Pool"
    print("✅ test_place_add_review_and_amenity passed")


# ─── REVIEW TESTS ─────────────────────────────────────────────

def test_review_creation():
    user = User(first_name="Bob", last_name="Brown", email="bob@example.com")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(title="Nice Place", description="Great", price=80,
                  latitude=10.0, longitude=20.0, owner=owner)
    review = Review(text="Amazing!", rating=4, place=place, user=user)
    assert review.text == "Amazing!"
    assert review.rating == 4
    assert review.id is not None
    print("✅ test_review_creation passed")

def test_review_invalid_rating():
    user = User(first_name="Bob", last_name="Brown", email="bob@example.com")
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(title="Nice Place", description="Great", price=80,
                  latitude=10.0, longitude=20.0, owner=owner)
    try:
        review = Review(text="Bad rating", rating=6, place=place, user=user)
        print("❌ test_review_invalid_rating FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_review_invalid_rating passed — caught: {e}")

def test_review_invalid_place():
    user = User(first_name="Bob", last_name="Brown", email="bob@example.com")
    try:
        review = Review(text="No place", rating=3, place="not_a_place", user=user)
        print("❌ test_review_invalid_place FAILED — no error raised")
    except ValueError as e:
        print(f"✅ test_review_invalid_place passed — caught: {e}")


# ─── RUN ALL ──────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n── User Tests ──")
    test_user_creation()
    test_user_invalid_email()
    test_user_name_too_long()

    print("\n── Amenity Tests ──")
    test_amenity_creation()
    test_amenity_empty_name()

    print("\n── Place Tests ──")
    test_place_creation()
    test_place_invalid_price()
    test_place_invalid_latitude()
    test_place_add_review_and_amenity()

    print("\n── Review Tests ──")
    test_review_creation()
    test_review_invalid_rating()
    test_review_invalid_place()

    print("\n✅ All tests completed.")
