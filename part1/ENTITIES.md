# HBnB Evolution - Entities Reference Guide

## Quick Reference

### User Entity
```
User
├── Attributes: id, firstName, lastName, email, password, isAdmin, createdAt, updatedAt
├── Role: Authentication, place ownership, review authorship
├── Relationships: owns Place (1:N), writes Review (1:N)
└── Key Methods: register(), authenticate(), validateEmail(), getOwnedPlaces()
```

### Place Entity
```
Place
├── Attributes: id, title, description, price, latitude, longitude, ownerId, amenityIds, createdAt, updatedAt
├── Role: Property listings with location and amenities
├── Relationships: owned by User (N:1), has Review (1:N), has Amenity (M:N)
└── Key Methods: create(), validateCoordinates(), addAmenity(), calculateAverageRating()
```

### Review Entity
```
Review
├── Attributes: id, placeId, userId, rating, comment, createdAt, updatedAt
├── Role: User feedback for places
├── Relationships: for Place (N:1), by User (N:1)
└── Key Methods: create(), validateRating(), checkOwnership(), isValid()
```

### Amenity Entity
```
Amenity
├── Attributes: id, name, description, createdAt, updatedAt
├── Role: Features/services available at places
├── Relationships: belongs to Place (M:N via PlaceAmenity)
└── Key Methods: create() [admin], validateUniqueName(), listPlaces()
```

---

## Detailed Constraints

### User Constraints
| Constraint | Type | Rule |
|-----------|------|------|
| Email | Unique | No two users can have same email |
| Email | Format | Must be valid email format |
| FirstName | Length | Max 50 characters |
| LastName | Length | Max 50 characters |
| Password | Security | Must be hashed (bcrypt) |
| IsAdmin | Default | False for new users |

### Place Constraints
| Constraint | Type | Rule |
|-----------|------|------|
| Title | Length | Max 100 characters |
| Description | Length | Max 5000 characters |
| Price | Numeric | Must be > 0 |
| Latitude | Range | -90.0 to 90.0 |
| Longitude | Range | -180.0 to 180.0 |
| Owner | Required | Must reference valid User |
| Amenities | Optional | 0 to many amenities |

### Review Constraints
| Constraint | Type | Rule |
|-----------|------|------|
| Rating | Range | 1 to 5 (inclusive) |
| Rating | Type | Integer only |
| Comment | Length | Max 1000 characters |
| Place | Required | Must reference valid Place |
| User | Required | Must reference valid User |
| Uniqueness | Composite | One review per (user, place) pair |
| Ownership | Rule | User cannot review own place |

### Amenity Constraints
| Constraint | Type | Rule |
|-----------|------|------|
| Name | Unique | No duplicate amenity names |
| Name | Length | Max 50 characters |
| Description | Length | Max 500 characters |
| Admin | Required | Only admins can manage |

---

## Method Specifications

### User Methods

#### register(firstName, lastName, email, password) → User
- Creates new user account
- Validates email format and uniqueness
- Hashes password before storage
- Sets isAdmin to False by default
- Returns: User object with generated id, createdAt, updatedAt

#### authenticate(password) → Boolean
- Verifies provided password matches stored hash
- Returns: True if password matches, False otherwise

#### updateProfile(data) → User
- Updates user attributes (firstName, lastName)
- Cannot modify email without special verification
- Returns: Updated User object

#### delete() → Boolean
- Soft delete (mark as inactive)
- Preserves audit trail
- Handles cascade: reviews remain, places handled separately
- Returns: True if successful

#### validateEmail() → Boolean
- Checks email format is valid
- Checks email is unique in system
- Returns: True if valid

#### hashPassword() → String
- Hashes password using bcrypt
- Returns: Hashed password string

#### getOwnedPlaces() → List~Place~
- Retrieves all places owned by user
- Returns: List of Place objects

#### getReviews() → List~Review~
- Retrieves all reviews written by user
- Returns: List of Review objects

#### hasRole(role) → Boolean
- Checks if user has specified role
- Returns: True if user is admin or has role

---

### Place Methods

#### create(data) → Place
- Creates new place listing
- Validates: coordinates, price, owner exists
- Associates amenities if provided
- Returns: Place object with generated id

#### update(data) → Place
- Updates place details
- Only owner can update
- Re-validates all constraints
- Returns: Updated Place object

#### delete() → Boolean
- Deletes place and all reviews
- Only owner can delete
- Returns: True if successful

#### addAmenity(amenity) → Boolean
- Associates amenity with place
- Only owner can add
- Prevents duplicates
- Returns: True if added

#### removeAmenity(amenity) → Boolean
- Removes amenity association
- Only owner can remove
- Returns: True if removed

#### validateCoordinates() → Boolean
- Ensures lat is -90 to 90
- Ensures long is -180 to 180
- Returns: True if valid

#### validatePrice() → Boolean
- Ensures price > 0
- Ensures valid numeric format
- Returns: True if valid

#### getOwner() → User
- Returns: User object (place owner)

#### getAmenities() → List~Amenity~
- Returns: List of all amenities at place

#### getReviews() → List~Review~
- Returns: List of all reviews for place

#### calculateAverageRating() → Float
- Computes average of all review ratings
- Returns: Float (0.0 if no reviews)

#### getReviewCount() → Integer
- Counts total reviews for place
- Returns: Integer count

---

### Review Methods

#### create(placeId, userId, rating, comment) → Review
- Creates new review
- Validates: place exists, user exists, rating valid
- Checks: user doesn't own place
- Checks: no duplicate review by user for place
- Updates: place average rating
- Returns: Review object with generated id

#### update(data) → Review
- Updates review content
- Only reviewer can update
- Re-validates rating
- Updates place average rating
- Returns: Updated Review object

#### delete() → Boolean
- Removes review
- Only reviewer can delete
- Updates place average rating
- Returns: True if successful

#### validateRating() → Boolean
- Ensures rating is 1-5
- Ensures rating is integer
- Returns: True if valid

#### checkOwnership(userId) → Boolean
- Verifies user doesn't own reviewed place
- Returns: True if can review

#### getPlace() → Place
- Returns: Reviewed Place object

#### getUser() → User
- Returns: Reviewer User object

#### isValid() → Boolean
- Checks all constraints
- Returns: True if all valid

---

### Amenity Methods

#### create(name, description) → Amenity
- Creates new amenity (admin only)
- Validates unique name
- Returns: Amenity object with generated id

#### update(data) → Amenity
- Updates amenity (admin only)
- Re-validates name uniqueness
- Returns: Updated Amenity object

#### delete() → Boolean
- Deletes amenity (admin only)
- Soft delete recommended (preserve history)
- Returns: True if successful

#### validateUniqueName() → Boolean
- Ensures amenity name is unique
- Case-insensitive comparison
- Returns: True if unique

#### listPlaces() → List~Place~
- Returns: List of places with this amenity

#### addToPlace(place) → Boolean
- Associates amenity with place
- Can be called by place owner
- Returns: True if added

#### removeFromPlace(place) → Boolean
- Removes amenity from place
- Can be called by place owner
- Returns: True if removed

---

## BaseModel Methods

All entities inherit these methods:

#### __init__()
- Initializes entity
- Generates UUID for id
- Sets createdAt to current time
- Sets updatedAt to current time

#### save()
- Persists entity to database/storage
- Updates updatedAt timestamp
- Raises exception if validation fails

#### delete()
- Removes entity from storage
- Soft delete recommended
- Returns: True if successful

#### to_dict()
- Converts entity to dictionary
- Excludes password from User
- Includes all timestamps
- Returns: Dictionary representation

#### update(data)
- Updates entity attributes
- Validates each field
- Updates updatedAt
- Returns: Updated entity

---

## Validation Error Handling

### Expected Exceptions

Each method should raise appropriate exceptions:
- `ValueError`: Invalid data (rating out of range)
- `TypeError`: Wrong data type (email not string)
- `DuplicateError`: Duplicate constraint violation (duplicate email)
- `OwnershipError`: Permission denied (user reviews own place)
- `NotFoundError`: Referenced entity doesn't exist
- `ConstraintError`: Business rule violation

### Validation Examples

```python
# User.validateEmail()
if not valid_email_format(email):
    raise ValueError("Invalid email format")
if email_exists(email):
    raise DuplicateError("Email already registered")

# Place.validateCoordinates()
if not (-90 <= latitude <= 90):
    raise ValueError("Latitude must be -90 to 90")
if not (-180 <= longitude <= 180):
    raise ValueError("Longitude must be -180 to 180")

# Review.validateRating()
if not isinstance(rating, int) or not (1 <= rating <= 5):
    raise ValueError("Rating must be integer 1-5")
```

---

## Best Practices

1. **Always validate** before persisting
2. **Use transactions** for multi-entity operations
3. **Log all operations** for audit trail
4. **Handle errors gracefully** with meaningful messages
5. **Test thoroughly** with unit tests
6. **Document assumptions** about data
7. **Use type hints** for clarity
8. **Follow naming conventions** consistently

