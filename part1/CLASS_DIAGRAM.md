# HBnB Evolution - Detailed Class Diagram for Business Logic Layer

## Overview

This document provides a detailed explanation of the class diagram for the Business Logic layer of the HBnB Evolution application. The diagram represents the core entities, their attributes, methods, and relationships that form the foundation of the application's business logic.

---

## Table of Contents

1. [Base Model](#base-model)
2. [Entity Classes](#entity-classes)
3. [Facade Pattern Implementation](#facade-pattern-implementation)
4. [Relationships and Associations](#relationships-and-associations)
5. [Key Design Decisions](#key-design-decisions)
6. [Attribute and Method Details](#attribute-and-method-details)

---

## Base Model

### Purpose
The `BaseModel` class serves as an abstract base class for all entities in the application, providing common functionality and attributes.

### Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Unique identifier for the entity (auto-generated) |
| `createdAt` | DateTime | Timestamp of entity creation (auto-set) |
| `updatedAt` | DateTime | Timestamp of last update (auto-updated) |

### Methods
| Method | Return Type | Description |
|--------|------------|-------------|
| `__init__()` | void | Constructor for initializing the entity |
| `save()` | void | Persist entity to database |
| `delete()` | Boolean | Remove entity from system |
| `to_dict()` | Dictionary | Convert entity to dictionary format |
| `update(data)` | void | Update entity attributes |

### Rationale
All entities inherit from `BaseModel` to ensure:
- Consistent unique identification
- Audit trail through timestamps
- Standardized persistence operations
- Code reusability and DRY principle

---

## Entity Classes

### 1. User Class

**Purpose**: Represents system users who can own places and leave reviews.

#### Attributes

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `firstName` | String | Max 50 chars, Not Null | User's first name |
| `lastName` | String | Max 50 chars, Not Null | User's last name |
| `email` | String | Unique, Not Null, Valid format | Email address (login credential) |
| `password` | String | Not Null, Hashed | Encrypted password |
| `isAdmin` | Boolean | Default: False | Administrator flag |

#### Methods

| Method | Return | Parameters | Description |
|--------|--------|-----------|-------------|
| `register()` | User | firstName, lastName, email, password | Create new user account |
| `authenticate()` | Boolean | password | Verify user credentials |
| `updateProfile()` | User | data | Update user information |
| `delete()` | Boolean | - | Deactivate user account |
| `validateEmail()` | Boolean | - | Validate email format and uniqueness |
| `hashPassword()` | String | password | Hash password using bcrypt |
| `getOwnedPlaces()` | List~Place~ | - | Retrieve all places owned by user |
| `getReviews()` | List~Review~ | - | Retrieve all reviews by user |
| `hasRole()` | Boolean | role | Check if user has specified role |

#### Business Rules
- Email must be unique across system
- Email must be valid format
- Password must be hashed before storage
- Only admins can create/delete amenities
- Users cannot review their own places

---

### 2. Place Class

**Purpose**: Represents property listings with location, amenities, and reviews.

#### Attributes

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `title` | String | Max 100 chars, Not Null | Place name/title |
| `description` | Text | Max 5000 chars, Optional | Detailed description |
| `price` | Decimal | Positive, Not Null | Nightly rate |
| `latitude` | Float | Range: -90 to 90 | Geographic latitude |
| `longitude` | Float | Range: -180 to 180 | Geographic longitude |
| `ownerId` | UUID | Foreign Key, Not Null | Reference to owner (User) |
| `amenityIds` | List~UUID~ | Array of amenity IDs | Associated amenities |

#### Methods

| Method | Return | Parameters | Description |
|--------|--------|-----------|-------------|
| `create()` | Place | data | Create new place listing |
| `update()` | Place | data | Update place information |
| `delete()` | Boolean | - | Remove place from system |
| `addAmenity()` | Boolean | amenity | Add amenity to place |
| `removeAmenity()` | Boolean | amenity | Remove amenity from place |
| `validateCoordinates()` | Boolean | - | Ensure valid lat/long |
| `validatePrice()` | Boolean | - | Ensure price is positive |
| `getOwner()` | User | - | Retrieve place owner |
| `getAmenities()` | List~Amenity~ | - | Get all amenities |
| `getReviews()` | List~Review~ | - | Get all reviews for place |
| `calculateAverageRating()` | Float | - | Compute average review rating |
| `getReviewCount()` | Integer | - | Count total reviews |

#### Business Rules
- Place must have valid owner
- Coordinates must be within valid ranges
- Price must be greater than zero
- Only owner can modify place details
- Only owner can delete place
- Amenities can be added/removed only by owner

---

### 3. Review Class

**Purpose**: Represents user feedback and ratings for places.

#### Attributes

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `placeId` | UUID | Foreign Key, Not Null | Reference to reviewed place |
| `userId` | UUID | Foreign Key, Not Null | Reference to reviewer |
| `rating` | Integer | Range: 1-5, Not Null | Star rating (1=Poor, 5=Excellent) |
| `comment` | Text | Max 1000 chars, Optional | Written feedback |

#### Methods

| Method | Return | Parameters | Description |
|--------|--------|-----------|-------------|
| `create()` | Review | placeId, userId, rating, comment | Submit new review |
| `update()` | Review | data | Update review content |
| `delete()` | Boolean | - | Remove review |
| `validateRating()` | Boolean | - | Ensure rating in 1-5 range |
| `checkOwnership()` | Boolean | userId | Verify user not place owner |
| `getPlace()` | Place | - | Get reviewed place |
| `getUser()` | User | - | Get reviewer user |
| `isValid()` | Boolean | - | Check all validations |

#### Business Rules
- User cannot review their own place
- Only one review per user per place
- Rating must be integer 1-5 (inclusive)
- Comment is optional
- Only reviewer can update/delete their review
- Deleting review should update place's average rating

---

### 4. Amenity Class

**Purpose**: Represents features and services available at places.

#### Attributes

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `name` | String | Unique, Max 50 chars, Not Null | Amenity name (e.g., "WiFi", "Pool") |
| `description` | Text | Max 500 chars, Optional | Detailed amenity information |

#### Methods

| Method | Return | Parameters | Description |
|--------|--------|-----------|-------------|
| `create()` | Amenity | name, description | Create new amenity (admin only) |
| `update()` | Amenity | data | Update amenity details (admin only) |
| `delete()` | Boolean | - | Remove amenity (admin only) |
| `validateUniqueName()` | Boolean | - | Ensure unique amenity name |
| `listPlaces()` | List~Place~ | - | Get all places with this amenity |
| `addToPlace()` | Boolean | place | Associate with place |
| `removeFromPlace()` | Boolean | place | Disassociate from place |

#### Business Rules
- Amenity names must be globally unique
- Only administrators can manage amenities
- Amenity can be associated with multiple places
- Cannot delete amenity if places depend on it (soft delete preferred)

---

### 5. PlaceAmenity Class (Junction Table)

**Purpose**: Manages the many-to-many relationship between Place and Amenity.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `placeId` | UUID | Reference to Place |
| `amenityId` | UUID | Reference to Amenity |
| `createdAt` | DateTime | When association was created |

#### Methods

| Method | Return | Parameters | Description |
|--------|--------|-----------|-------------|
| `associate()` | Boolean | place, amenity | Create place-amenity relationship |
| `dissociate()` | Boolean | place, amenity | Remove place-amenity relationship |

#### Rationale
- Separates the many-to-many relationship into a dedicated class
- Allows tracking when amenities are added/removed
- Maintains data integrity constraints
- Simplifies queries and updates

---

## Facade Pattern Implementation

### HBnBFacade Class

**Purpose**: Provides a unified interface to the Business Logic layer, simplifying interaction between the Presentation layer and entity models.

#### Attributes (Private)

| Attribute | Type | Description |
|-----------|------|-------------|
| `userRepository` | Repository | Data access for users |
| `placeRepository` | Repository | Data access for places |
| `reviewRepository` | Repository | Data access for reviews |
| `amenityRepository` | Repository | Data access for amenities |

#### Methods (Public)

**User Management**:
- `createUser(data) → User`
- `getUser(userId) → User`
- `updateUser(userId, data) → User`
- `deleteUser(userId) → Boolean`

**Place Management**:
- `createPlace(userId, data) → Place`
- `getPlace(placeId) → Place`
- `updatePlace(placeId, data) → Place`
- `deletePlace(placeId) → Boolean`

**Review Management**:
- `createReview(placeId, userId, data) → Review`
- `getReview(reviewId) → Review`
- `updateReview(reviewId, data) → Review`
- `deleteReview(reviewId) → Boolean`

**Amenity Management**:
- `createAmenity(data) → Amenity`
- `getAmenity(amenityId) → Amenity`
- `updateAmenity(amenityId, data) → Amenity`
- `deleteAmenity(amenityId) → Boolean`

**Query Methods**:
- `listPlaces(filters) → List~Place~`
- `listReviews(placeId) → List~Review~`

#### Responsibilities
- Orchestrate complex operations across multiple entities
- Enforce business rules and constraints
- Coordinate persistence operations
- Handle transactions
- Validate data before persistence
- Implement authorization checks

---

## Relationships and Associations

### 1. User to Place (One-to-Many)

**Relationship**: `User "1" -- "0..*" Place : owns`

**Description**: A user can own zero or more places.

**Implementation**:
```
User:id (Primary Key)
  ↓
Place:ownerId (Foreign Key)
```

**Cardinality**:
- Minimum: 0 (user can have no places)
- Maximum: Many (user can own multiple places)

**Implications**:
- When user is deleted, their places must be handled (cascade or reassign)
- Query to find owner: `Place.getOwner()`
- Query to find all owned places: `User.getOwnedPlaces()`

---

### 2. User to Review (One-to-Many)

**Relationship**: `User "1" -- "0..*" Review : writes`

**Description**: A user can write zero or more reviews.

**Implementation**:
```
User:id (Primary Key)
  ↓
Review:userId (Foreign Key)
```

**Cardinality**:
- Minimum: 0 (user need not write reviews)
- Maximum: Many (but limited to one per place)

**Implications**:
- Review author must be a valid user
- Cannot delete user while reviews exist (soft delete or cascade)

---

### 3. Place to Review (One-to-Many)

**Relationship**: `Place "1" -- "0..*" Review : has`

**Description**: A place can have zero or more reviews.

**Implementation**:
```
Place:id (Primary Key)
  ↓
Review:placeId (Foreign Key)
```

**Cardinality**:
- Minimum: 0 (new places have no reviews)
- Maximum: Many

**Implications**:
- Deleting place should cascade to reviews
- Average rating calculated from all reviews
- Review count important for search/filtering

---

### 4. Place to Amenity (Many-to-Many)

**Relationship**: `Place "0..*" -- "0..*" Amenity : has/belongs to`

**Description**: A place can have many amenities, and amenities can belong to many places.

**Implementation** (via PlaceAmenity junction table):
```
Place:id (Primary Key)
  ↓
PlaceAmenity:placeId (Foreign Key)
PlaceAmenity:amenityId (Foreign Key)
  ↓
Amenity:id (Primary Key)
```

**Cardinality**:
- Place: 0 to Many amenities
- Amenity: 0 to Many places

**Implications**:
- Requires junction table (PlaceAmenity)
- Supports flexible amenity management
- Allows querying places by amenities
- Soft delete for amenities (don't remove from places)

---

## Key Design Decisions

### 1. Inheritance Hierarchy
All entities inherit from `BaseModel` to:
- Ensure consistent ID generation (UUID)
- Provide standard timestamps (createdAt, updatedAt)
- Reduce code duplication
- Standardize persistence operations

### 2. Facade Pattern
The `HBnBFacade` provides:
- Single entry point for all business operations
- Business logic enforcement
- Transaction management
- Simplified API for presentation layer

### 3. Repository Abstraction
Repositories abstract database operations:
- Independent of persistence implementation
- Easy to mock for testing
- Supports different storage backends
- Encapsulates query logic

### 4. Separation of Concerns
- Entities: Define structure and basic validation
- Facade: Orchestrate operations and enforce rules
- Repositories: Handle persistence
- Presentation: Handle HTTP/requests

### 5. Many-to-Many Handling
PlaceAmenity junction table provides:
- Clean many-to-many management
- Audit trail (createdAt)
- Flexibility for future extensions
- Database normalization

---

## Attribute and Method Details

### Attribute Naming Conventions

**Private Attributes**: Prefixed with underscore (`_`)
- `_id`, `_createdAt`, `_updatedAt`

**Public Attributes**: No prefix (camelCase)
- `firstName`, `email`, `price`

**Collection Attributes**: Plural names
- `amenityIds`, `placeIds`, `reviewIds`

### Method Naming Conventions

**Getters**: `get<Entity>()` or `get<Property>()`
- `getOwner()`, `getUser()`, `getAmenities()`

**Setters**: `set<Property>(<value>)`
- `setPrice()`, `setDescription()`

**Validators**: `validate<Property>()`
- `validateEmail()`, `validateRating()`, `validateCoordinates()`

**Checkers**: `is<Property>()` or `has<Property>()`
- `isValid()`, `hasRole()`, `checkOwnership()`

**Creators**: `create()`
- Instantiate and return new entity

**Deleters**: `delete()`
- Remove entity from system

**List Methods**: `list<Entities>()`
- Return collections of related entities

### Return Type Annotations

- `Boolean`: True/False results
- `String`: Text values
- `UUID`: Unique identifiers
- `List~ClassName~`: Collections
- `Float/Decimal`: Numeric values
- `DateTime`: Timestamps

---

## UML Notation Guide

### Relationships Used

| Symbol | Type | Meaning |
|--------|------|---------|
| `<\|--` | Inheritance | Child inherits from Parent |
| `-->` | Association | One-way dependency |
| `--` | Bidirectional Association | Mutual relationship |
| `*--` | Composition | Strong ownership |
| `+` | Public | Accessible externally |
| `-` | Private | Hidden internally |

### Cardinality Notation

| Notation | Meaning |
|----------|---------|
| `0..1` | Zero or one |
| `1` | Exactly one |
| `0..*` | Zero or more |
| `1..*` | One or more |
| `*` | Any number |

---

## Next Steps

1. **Implementation**: Translate this diagram into actual Python/language classes
2. **Testing**: Create unit tests for each entity's methods
3. **Integration**: Implement repository pattern for persistence
4. **Validation**: Add comprehensive input validation
5. **Documentation**: Generate API documentation from code

---

## References

- [UML Class Diagrams](https://www.uml-diagrams.org/class-diagrams.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns](https://refactoring.guru/design-patterns)
- [Mermaid.js Documentation](https://mermaid.js.org/)

