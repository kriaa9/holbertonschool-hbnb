# Entities Reference Guide

## Quick Entity Reference

### User Entity
**File**: `models/user.py`
**Table**: `users`

**Purpose**: Authentication and user profile management

**Key Attributes**:
- `id` (UUID): Unique user identifier
- `firstName` (String, 50): User's first name
- `lastName` (String, 50): User's last name
- `email` (String, 100): Unique email address
- `passwordHash` (String): Bcrypt hashed password
- `isAdmin` (Boolean): Administrator privilege

**Key Methods**:
- `register(firstName, lastName, email, password)`: Create account
- `authenticate(password)`: Verify credentials
- `getOwnedPlaces()`: Get owned properties
- `getReviews()`: Get written reviews

**Constraints**:
- Email must be unique
- Email must be valid format
- Password minimum 8 characters
- firstName/lastName max 50 characters

---

### Place Entity
**File**: `models/place.py`
**Table**: `places`

**Purpose**: Property listings

**Key Attributes**:
- `id` (UUID): Unique place identifier
- `title` (String, 100): Property name
- `description` (Text, 1000): Property details
- `price` (Decimal): Nightly rate
- `latitude` (Float): Latitude coordinate
- `longitude` (Float): Longitude coordinate
- `ownerId` (UUID): Place owner reference

**Key Methods**:
- `create(data)`: Create new listing
- `update(data)`: Update details
- `getAmenities()`: Get amenities list
- `getReviews()`: Get all reviews
- `calculateAverageRating()`: Compute avg rating

**Constraints**:
- Title required, max 100 chars
- Price must be positive
- Latitude: -90 to 90
- Longitude: -180 to 180
- Must have owner

---

### Review Entity
**File**: `models/review.py`
**Table**: `reviews`

**Purpose**: User feedback and ratings

**Key Attributes**:
- `id` (UUID): Unique review identifier
- `placeId` (UUID): Reviewed place reference
- `userId` (UUID): Author reference
- `rating` (Integer): Rating 1-5
- `comment` (Text, 1000): Optional feedback

**Key Methods**:
- `create(data)`: Submit review
- `update(data)`: Update content
- `delete()`: Remove review
- `validateRating()`: Check rating valid
- `checkOwnership()`: Verify not own place

**Constraints**:
- Rating: 1-5 (integer)
- Unique(userId, placeId)
- Cannot review own place
- Comment max 1000 chars

---

### Amenity Entity
**File**: `models/amenity.py`
**Table**: `amenities`

**Purpose**: Features/services available

**Key Attributes**:
- `id` (UUID): Unique amenity identifier
- `name` (String, 50): Amenity name
- `description` (Text, 500): Description

**Key Methods**:
- `create(data)`: Create amenity (admin)
- `update(data)`: Update details (admin)
- `delete()`: Remove amenity (admin)
- `listPlaces()`: Get places with amenity

**Constraints**:
- Name must be unique
- Name required, max 50 chars
- Admin-only operations

---

## Entity Relationships

```
┌──────────────┐
│    User      │
│   (owner)    │
└──────┬───────┘
       │ 1:N owns
       │
       ▼
┌──────────────┐         1:N has
│    Place     ├────────────────┐
└──────┬───────┘                │
       │ M:N has/includes        ▼
       │                    ┌──────────────┐
       ├───────────────────►│   Review     │
       │                    └──────┬───────┘
       │                           │
    ┌──▼─────────────────┐         │
    │    Amenity         │         │ N:1
    │   (features)       │         │
    └────────────────────┘         │
                                   ▼ N:1
                            ┌──────────────┐
                            │    User      │
                            │  (reviewer)  │
                            └──────────────┘
```

---

## Database Schema Overview

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Places Table
```sql
CREATE TABLE places (
    id UUID PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    latitude FLOAT NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude FLOAT NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    owner_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    place_id UUID NOT NULL,
    user_id UUID NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, place_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Amenities Table
```sql
CREATE TABLE amenities (
    id UUID PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Place_Amenities Table
```sql
CREATE TABLE place_amenities (
    place_id UUID NOT NULL,
    amenity_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
```

---

## Validation Rules by Entity

### User Validation
| Field | Rule | Example |
|-------|------|---------|
| firstName | 1-50 chars, letters/spaces | "John" |
| lastName | 1-50 chars, letters/spaces | "Doe" |
| email | Valid format, unique | "john@example.com" |
| password | Min 8 chars, mixed case/numbers | "Pass1234" |

### Place Validation
| Field | Rule | Example |
|-------|------|---------|
| title | 1-100 chars, required | "Cozy Apartment" |
| price | Decimal > 0, 2 places | "120.50" |
| latitude | Float -90 to 90 | "40.7128" |
| longitude | Float -180 to 180 | "-74.0060" |

### Review Validation
| Field | Rule | Example |
|-------|------|---------|
| rating | Integer 1-5, required | "5" |
| comment | 0-1000 chars, optional | "Great place!" |

### Amenity Validation
| Field | Rule | Example |
|-------|------|---------|
| name | 1-50 chars, unique | "WiFi" |
| description | 0-500 chars, optional | "High-speed internet" |

---

## Common Operations

### Create a User
```python
user = User()
user.register(
    firstName="John",
    lastName="Doe",
    email="john@example.com",
    password="SecurePass123"
)
```

### Create a Place
```python
place = Place()
place.create(
    title="Cozy Apartment",
    description="Beautiful downtown apartment",
    price=120.50,
    latitude=40.7128,
    longitude=-74.0060,
    ownerId=user_id
)
```

### Add Amenity to Place
```python
place.addAmenity(amenity)
# Or via Facade:
facade.addAmenityToPlace(place_id, amenity_id)
```

### Submit a Review
```python
review = Review()
review.create(
    placeId=place_id,
    userId=user_id,
    rating=5,
    comment="Excellent place!"
)
```

### Get Place with Reviews and Amenities
```python
place = Place.get(place_id)
amenities = place.getAmenities()
reviews = place.getReviews()
avg_rating = place.calculateAverageRating()
```

---

## API Endpoint Mapping

### User Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register` | Create user |
| GET | `/api/users/{id}` | Get user |
| PUT | `/api/users/{id}` | Update user |
| DELETE | `/api/users/{id}` | Delete user |

### Place Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/places` | Create place |
| GET | `/api/places` | List places (with filters) |
| GET | `/api/places/{id}` | Get place details |
| PUT | `/api/places/{id}` | Update place |
| DELETE | `/api/places/{id}` | Delete place |

### Review Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/places/{id}/reviews` | Create review |
| GET | `/api/places/{id}/reviews` | List reviews |
| GET | `/api/reviews/{id}` | Get review |
| PUT | `/api/reviews/{id}` | Update review |
| DELETE | `/api/reviews/{id}` | Delete review |

### Amenity Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/amenities` | Create amenity (admin) |
| GET | `/api/amenities` | List amenities |
| GET | `/api/amenities/{id}` | Get amenity |
| PUT | `/api/amenities/{id}` | Update amenity (admin) |
| DELETE | `/api/amenities/{id}` | Delete amenity (admin) |

---

## Implementation Checklist

- [ ] Create BaseModel abstract class
- [ ] Implement User entity
- [ ] Implement Place entity
- [ ] Implement Review entity
- [ ] Implement Amenity entity
- [ ] Create Facade class
- [ ] Implement ValidationRules
- [ ] Create repositories (UserRepository, PlaceRepository, etc.)
- [ ] Write unit tests for each entity
- [ ] Implement error handling
- [ ] Create API endpoints
- [ ] Document API responses

