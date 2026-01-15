# Business Logic Layer - Class Diagram Documentation

## Overview
This document provides a detailed explanation of the class diagram for the Business Logic layer, including all entities, their attributes, methods, and relationships.

---

## Entity Specifications

### 1. BaseModel (Abstract Base Class)

**Purpose**: Serves as the parent class for all entities, providing common functionality.

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key, Unique, Not Null | Unique identifier (UUID4) |
| createdAt | DateTime | Auto-generated, Not Null | Timestamp of entity creation |
| updatedAt | DateTime | Auto-updated, Not Null | Timestamp of last update |

**Methods**:
- `__init__()`: Initialize new entity with id, createdAt, updatedAt
- `save()`: Persist entity to storage
- `delete()`: Remove entity from storage
- `update(data: dict)`: Update entity attributes
- `to_dict() → dict`: Convert entity to dictionary representation

**Benefits**:
- DRY principle - eliminates code duplication
- Consistent timestamp management
- Standard entity behavior across all models
- Simplified inheritance chain

---

### 2. User Entity

**Purpose**: Manages user authentication, profiles, and permissions.

**Inherits From**: BaseModel

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key | Inherited from BaseModel |
| firstName | String | Not Null, Max 50 chars | User's first name |
| lastName | String | Not Null, Max 50 chars | User's last name |
| email | String | Unique, Not Null, Valid format | User's email address |
| passwordHash | String | Not Null, Hashed | Bcrypt/Argon2 hashed password |
| isAdmin | Boolean | Default: False | Administrator privilege flag |
| createdAt | DateTime | Auto-generated | Inherited from BaseModel |
| updatedAt | DateTime | Auto-updated | Inherited from BaseModel |

**Methods**:
- `register(firstName, lastName, email, password) → User`: Create new user account
- `updateProfile(data) → User`: Update user information
- `delete() → Boolean`: Deactivate/remove user account
- `authenticate(password) → Boolean`: Verify password credentials
- `validateEmail() → Boolean`: Check email format validity
- `hashPassword(password) → String`: Securely hash password using bcrypt
- `getOwnedPlaces() → List<Place>`: Retrieve all places owned by user
- `getReviews() → List<Review>`: Retrieve all reviews written by user
- `isOwnerOf(place) → Boolean`: Check if user owns specific place

**Relationships**:
- **1:N with Place**: One user can own multiple places
- **1:N with Review**: One user can write multiple reviews

**Business Rules**:
- Email must be unique across system
- Password minimum 8 characters
- Email must match valid format
- Users cannot be deleted if they own places (optional rule)
- Passwords must never be returned in API responses

**Validation Rules**:
```
validateEmail():
  - Must contain @
  - Must contain domain
  - Length between 5-100 characters
  - No spaces or special chars except . and -

hashPassword():
  - Use bcrypt with salt rounds >= 10
  - Never store plain text password
  - Use constant-time comparison for verification
```

---

### 3. Place Entity

**Purpose**: Represents property listings available for rent.

**Inherits From**: BaseModel

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key | Inherited from BaseModel |
| title | String | Not Null, Max 100 chars, Not empty | Property title/name |
| description | Text | Optional, Max 1000 chars | Detailed property description |
| price | Decimal | Not Null, Positive, 2 decimals | Price per night (>0) |
| latitude | Float | Not Null, Range: -90 to 90 | Geographic latitude |
| longitude | Float | Not Null, Range: -180 to 180 | Geographic longitude |
| ownerId | UUID | Foreign Key, Not Null | Reference to owner User |
| amenityIds | List<UUID> | Optional | References to associated amenities |
| createdAt | DateTime | Auto-generated | Inherited from BaseModel |
| updatedAt | DateTime | Auto-updated | Inherited from BaseModel |

**Methods**:
- `create(data) → Place`: Create new place listing
- `update(data) → Place`: Update place information
- `delete() → Boolean`: Remove place from listings
- `addAmenity(amenity) → Boolean`: Associate amenity with place
- `removeAmenity(amenity) → Boolean`: Disassociate amenity from place
- `validateCoordinates() → Boolean`: Verify latitude/longitude validity
- `validatePrice() → Boolean`: Verify price is positive
- `getOwner() → User`: Retrieve place owner
- `getAmenities() → List<Amenity>`: Retrieve all amenities
- `getReviews() → List<Review>`: Retrieve all reviews for place
- `calculateAverageRating() → Float`: Compute average review rating
- `getReviewCount() → Integer`: Get total number of reviews

**Relationships**:
- **N:1 with User**: Multiple places can belong to one user (owner)
- **1:N with Review**: One place can have multiple reviews
- **M:N with Amenity**: Multiple amenities can belong to place, multiple places can have amenity

**Business Rules**:
- Only place owner can update/delete place
- Price must be positive decimal
- Coordinates must be within valid ranges
- Title cannot be empty
- Place must have owner (cannot be orphaned)
- Cannot delete place if it has reviews (optional rule)

**Validation Rules**:
```
validateCoordinates():
  - Latitude must be between -90.0 and 90.0
  - Longitude must be between -180.0 and 180.0
  - Both must be valid floating-point numbers

validatePrice():
  - Must be greater than 0
  - Must have maximum 2 decimal places
  - Format: $XXX.XX
```

---

### 4. Review Entity

**Purpose**: Stores user feedback and ratings for places.

**Inherits From**: BaseModel

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key | Inherited from BaseModel |
| placeId | UUID | Foreign Key, Not Null | Reference to reviewed place |
| userId | UUID | Foreign Key, Not Null | Reference to review author |
| rating | Integer | Range: 1-5, Not Null | Numerical rating (1=poor, 5=excellent) |
| comment | Text | Optional, Max 1000 chars | User's written feedback |
| createdAt | DateTime | Auto-generated | Inherited from BaseModel |
| updatedAt | DateTime | Auto-updated | Inherited from BaseModel |

**Composite Constraints**:
- Unique(userId, placeId): One review per user per place

**Methods**:
- `create(data) → Review`: Submit new review
- `update(data) → Review`: Update review content
- `delete() → Boolean`: Remove review
- `validateRating() → Boolean`: Check rating is 1-5
- `checkOwnership() → Boolean`: Verify user doesn't review own place
- `getPlace() → Place`: Retrieve reviewed place
- `getUser() → User`: Retrieve review author

**Relationships**:
- **N:1 with Place**: Multiple reviews belong to one place
- **N:1 with User**: Multiple reviews belong to one user

**Business Rules**:
- Users cannot review places they own
- Rating must be integer between 1 and 5 (inclusive)
- Only one review per user per place (unique constraint)
- Reviews can be updated by author only
- Reviews can be deleted by author or admin
- Deleting review triggers place rating recalculation

**Validation Rules**:
```
validateRating():
  - Must be integer (not float)
  - Must be >= 1 and <= 5
  - Must not be null/undefined

checkOwnership():
  - Verify userId != place.ownerId
  - Reject if user owns the place
  - Return 403 Forbidden status
```

---

### 5. Amenity Entity

**Purpose**: Represents features and services available at places.

**Inherits From**: BaseModel

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | Primary Key | Inherited from BaseModel |
| name | String | Unique, Not Null, Max 50 chars | Amenity identifier (e.g., "WiFi") |
| description | Text | Optional, Max 500 chars | Detailed amenity description |
| createdAt | DateTime | Auto-generated | Inherited from BaseModel |
| updatedAt | DateTime | Auto-updated | Inherited from BaseModel |

**Methods**:
- `create(data) → Amenity`: Create new amenity (admin only)
- `update(data) → Amenity`: Update amenity info (admin only)
- `delete() → Boolean`: Remove amenity (admin only)
- `validateUniqueName() → Boolean`: Check name uniqueness
- `listPlaces() → List<Place>`: Get all places with this amenity

**Relationships**:
- **M:N with Place**: Many-to-many through PlaceAmenity junction table

**Business Rules**:
- Amenity names must be unique (case-insensitive)
- Only administrators can create/update/delete amenities
- Cannot delete amenity if places are associated (optional)
- Cannot have duplicate amenities for single place

**Validation Rules**:
```
validateUniqueName():
  - Check database for existing name (case-insensitive)
  - Length between 1-50 characters
  - No special characters except spaces and hyphens
```

---

### 6. PlaceAmenity (Junction Table)

**Purpose**: Manages many-to-many relationship between Place and Amenity.

**Attributes**:
| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| placeId | UUID | Foreign Key, Composite PK | Reference to place |
| amenityId | UUID | Foreign Key, Composite PK | Reference to amenity |
| createdAt | DateTime | Auto-generated | When association was created |

**Primary Key**: Composite (placeId, amenityId)

**Methods**:
- `associate(placeId, amenityId)`: Create place-amenity association
- `dissociate(placeId, amenityId)`: Remove association

**Business Rules**:
- No duplicate associations allowed
- Both place and amenity must exist
- Deleting place cascades to this table
- Deleting amenity cascades to this table (optional)

---

### 7. Facade Class

**Purpose**: Provides unified interface to business logic operations.

**Attributes**:
- `userRepository: UserRepository`: Data access for users
- `placeRepository: PlaceRepository`: Data access for places
- `reviewRepository: ReviewRepository`: Data access for reviews
- `amenityRepository: AmenityRepository`: Data access for amenities

**Methods**:

**User Operations**:
- `registerUser(data) → User`: Register new user
- `updateUser(userId, data) → User`: Update user profile
- `getUser(userId) → User`: Retrieve user by ID
- `deleteUser(userId) → Boolean`: Delete user account

**Place Operations**:
- `createPlace(userId, data) → Place`: Create new place
- `updatePlace(placeId, data) → Place`: Update place details
- `getPlace(placeId) → Place`: Retrieve place by ID
- `deletePlace(placeId) → Boolean`: Delete place
- `listPlaces(filters) → List<Place>`: Get filtered place list

**Amenity Operations**:
- `addAmenityToPlace(placeId, amenityId) → Boolean`: Associate amenity
- `removeAmenityFromPlace(placeId, amenityId) → Boolean`: Remove amenity

**Review Operations**:
- `submitReview(userId, placeId, data) → Review`: Create review
- `updateReview(reviewId, data) → Review`: Update review
- `getReview(reviewId) → Review`: Retrieve review
- `deleteReview(reviewId) → Boolean`: Delete review
- `listReviewsByPlace(placeId) → List<Review>`: Get place reviews

**Amenity Management** (Admin only):
- `createAmenity(data) → Amenity`: Create amenity
- `updateAmenity(amenityId, data) → Amenity`: Update amenity
- `getAmenity(amenityId) → Amenity`: Retrieve amenity
- `deleteAmenity(amenityId) → Boolean`: Delete amenity
- `listAmenities() → List<Amenity>`: Get all amenities

**Benefits**:
- Single entry point for business operations
- Encapsulates business rules
- Simplifies testing
- Reduces coupling between layers
- Centralizes transaction management

---

### 8. ValidationRules Class

**Purpose**: Centralizes all validation logic across entities.

**Methods**:
- `validateUserEmail(email) → Boolean`: Validate email format
- `validatePassword(password) → Boolean`: Validate password strength
- `validateCoordinates(lat, long) → Boolean`: Validate geographic coordinates
- `validatePrice(price) → Boolean`: Validate price value
- `validateRating(rating) → Boolean`: Validate review rating
- `validateAmenityName(name) → Boolean`: Validate amenity name
- `validatePlaceTitle(title) → Boolean`: Validate place title
- `validateReviewComment(comment) → Boolean`: Validate review comment

**Validation Standards**:
- Centralized validation rules
- Reusable across entities
- Comprehensive error messages
- Consistent validation logic

---

## Relationship Diagram

### Inheritance Hierarchy
```
BaseModel (Abstract)
├── User
├── Place
├── Review
└── Amenity
```

### Association Relationships

| Relationship | Type | Multiplicity | Description |
|--------------|------|--------------|-------------|
| User → Place | Composition | 1:N | User owns multiple places |
| User → Review | Composition | 1:N | User writes multiple reviews |
| Place → Review | Composition | 1:N | Place receives multiple reviews |
| Place ↔ Amenity | Association | M:N | Places have amenities, amenities belong to places |
| PlaceAmenity | Junction | - | Implements M:N relationship |

### Business Logic Flow

```
┌─────────────┐
│   Facade    │ ← Central coordinator
└──────┬──────┘
       │
   ┌───┴────────┬────────────┬──────────┐
   ▼            ▼            ▼          ▼
┌──────┐   ┌────────┐   ┌──────────┐ ┌────────┐
│User  │   │ Place  │   │ Review   │ │Amenity │
└──────┘   └────────┘   └──────────┘ └────────┘
   │            │            │          │
   └────────────┼────────────┴──────────┘
                │
         ┌──────▼──────┐
         │Repositories │
         └──────┬──────┘
                │
         ┌──────▼──────────┐
         │  Persistence    │
         │  Layer & DB     │
         └─────────────────┘
```

---

## Design Patterns Applied

### 1. **Inheritance (Generalization)**
- All entities inherit from BaseModel
- Eliminates code duplication
- Ensures consistent behavior across entities

### 2. **Composition**
- Facade composes repositories
- Entities manage their own state

### 3. **Association**
- Bidirectional: User ↔ Place, Place ↔ Review
- Unidirectional: Review → User, Review → Place

### 4. **Aggregation**
- Place aggregates amenities
- Multiple amenities can exist independently

### 5. **Facade Pattern**
- Provides unified interface to complex subsystem
- Simplifies client interactions

---

## SOLID Principles Applied

### **S** - Single Responsibility
- Each class has one reason to change
- User handles user logic, Place handles place logic

### **O** - Open/Closed
- Classes are open for extension, closed for modification
- New entity types can inherit from BaseModel

### **L** - Liskov Substitution
- All entities can be used interchangeably as BaseModel
- Maintains behavioral consistency

### **I** - Interface Segregation
- Classes expose only necessary methods
- No bloated interfaces

### **D** - Dependency Inversion
- Facade depends on abstractions (repositories)
- Depends on interfaces, not concrete implementations

---

## Constraints and Rules Summary

### Uniqueness Constraints
- User.email: UNIQUE
- Amenity.name: UNIQUE
- Review(userId, placeId): UNIQUE

### Not Null Constraints
- All entities: id, createdAt, updatedAt
- User: firstName, lastName, email, passwordHash
- Place: title, price, latitude, longitude, ownerId
- Review: placeId, userId, rating
- Amenity: name

### Value Ranges
- Place.latitude: [-90, 90]
- Place.longitude: [-180, 180]
- Review.rating: [1, 5]
- Place.price: > 0
- String fields: max length constraints

### Business Rules
1. User cannot review own place
2. One review per user per place
3. Only admins manage amenities
4. Place must have owner
5. Rating must be integer 1-5
6. Email must be valid format
7. Password minimum 8 characters
8. Coordinates within valid ranges

---

## Implementation Notes

### Timestamps
- `createdAt`: Set once at creation, never updated
- `updatedAt`: Updated on every modification
- Both stored as ISO 8601 format
- All times in UTC

### Identifiers
- All entities use UUID4 (not auto-increment integers)
- Benefits: Distributed systems, privacy, uniqueness
- Generated at entity creation time

### Relationships
- Foreign keys reference entity IDs
- Relationships validated before persistence
- Cascade delete/update as needed

### Password Security
- Never stored in plain text
- Hashed with bcrypt (salt rounds >= 10)
- Constant-time comparison for verification
- Never returned in responses

---

## Next Steps

1. **Implementation**: Convert diagram to code (models.py)
2. **Repositories**: Create data access layer
3. **Validation**: Implement ValidationRules class
4. **Tests**: Unit tests for each entity
5. **API Endpoints**: Create corresponding REST endpoints

