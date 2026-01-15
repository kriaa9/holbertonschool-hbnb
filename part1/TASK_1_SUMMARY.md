# Task 1: Detailed Class Diagram for Business Logic Layer

## ✅ Task Status: COMPLETED

This document summarizes the completion of Task 1, which involved designing a detailed class diagram for the Business Logic layer of the HBnB Evolution application.

---

## Objective

Design a detailed class diagram for the Business Logic layer depicting:
- Key entities: User, Place, Review, Amenity
- Entity attributes and methods
- Relationships and associations
- Inheritance hierarchies
- Design patterns implementation

---

## Deliverables

### 1. **Detailed Class Diagram**
�� **File**: `diagrams/class_diagram.mmd`

#### Classes Included:
- **BaseModel** - Abstract base class for all entities
- **User** - User management and authentication
- **Place** - Property listings
- **Review** - User feedback and ratings
- **Amenity** - Features and services
- **PlaceAmenity** - Junction table for M:N relationships
- **Facade** - Central business logic coordinator
- **ValidationRules** - Cross-cutting validation logic

#### Key Features:
✅ All entities include UUID, createdAt, updatedAt
✅ Complete attribute definitions with types
✅ Comprehensive method signatures
✅ Proper UML notation for relationships
✅ Inheritance hierarchy from BaseModel
✅ M:N relationship handling via PlaceAmenity
✅ Facade pattern implementation
✅ Validation rules centralization

---

## Entity Details

### BaseModel (Abstract Base Class)
**Purpose**: Foundation for all entities

**Attributes**:
- `-UUID id` - Unique identifier
- `-DateTime createdAt` - Creation timestamp
- `-DateTime updatedAt` - Last update timestamp

**Methods**:
- `+__init__()` - Constructor
- `+save()` - Persist to database
- `+delete()` - Remove from system
- `+update(data)` - Update attributes
- `+to_dict()` - Convert to dictionary

---

### User Entity
**Purpose**: Authentication and profile management

**Attributes**:
- `-String firstName` - User's first name
- `-String lastName` - User's last name
- `-String email` - Unique email address
- `-String passwordHash` - Hashed password
- `-Boolean isAdmin` - Administrator flag
- (inherits: id, createdAt, updatedAt)

**Methods**:
- `+register(firstName, lastName, email, password)` - Create new user
- `+updateProfile(data)` - Update user information
- `+delete()` - Remove user account
- `+authenticate(password)` - Verify credentials
- `+validateEmail()` - Email validation
- `+hashPassword(password)` - Secure password hashing
- `+getOwnedPlaces()` - Retrieve user's properties
- `+getReviews()` - Retrieve user's reviews
- `+isOwnerOf(place)` - Check ownership

**Relationships**:
- One-to-Many with Place (1 user owns 0..* places)
- One-to-Many with Review (1 user writes 0..* reviews)

---

### Place Entity
**Purpose**: Property listings and metadata

**Attributes**:
- `-String title` - Property name
- `-Text description` - Detailed description
- `-Decimal price` - Nightly rate
- `-Float latitude` - Geographic latitude
- `-Float longitude` - Geographic longitude
- `-UUID ownerId` - Owner reference
- `-List~UUID~ amenityIds` - Associated amenities
- (inherits: id, createdAt, updatedAt)

**Methods**:
- `+create(data)` - Create new place
- `+update(data)` - Update place details
- `+delete()` - Remove place
- `+addAmenity(amenity)` - Associate amenity
- `+removeAmenity(amenity)` - Disassociate amenity
- `+validateCoordinates()` - Validate lat/long
- `+validatePrice()` - Validate price value
- `+getOwner()` - Retrieve owner
- `+getAmenities()` - Get all amenities
- `+getReviews()` - Get all reviews
- `+calculateAverageRating()` - Compute average rating
- `+getReviewCount()` - Count reviews

**Relationships**:
- Many-to-One with User (owned by)
- One-to-Many with Review
- Many-to-Many with Amenity (via PlaceAmenity)

---

### Review Entity
**Purpose**: User feedback and ratings

**Attributes**:
- `-UUID placeId` - Reviewed place reference
- `-UUID userId` - Reviewer reference
- `-Integer rating` - Rating (1-5)
- `-Text comment` - Review comment
- (inherits: id, createdAt, updatedAt)

**Methods**:
- `+create(data)` - Submit new review
- `+update(data)` - Edit review
- `+delete()` - Remove review
- `+validateRating()` - Ensure 1-5 range
- `+checkOwnership()` - Prevent self-review
- `+getPlace()` - Retrieve reviewed place
- `+getUser()` - Retrieve reviewer

**Relationships**:
- Many-to-One with User
- Many-to-One with Place

**Constraints**:
- Composite unique (userId, placeId)
- Rating 1-5 range
- User cannot review own places

---

### Amenity Entity
**Purpose**: Features and services

**Attributes**:
- `-String name` - Unique amenity name
- `-Text description` - Amenity description
- (inherits: id, createdAt, updatedAt)

**Methods**:
- `+create(data)` - Create new amenity
- `+update(data)` - Update amenity
- `+delete()` - Remove amenity
- `+validateUniqueName()` - Ensure name uniqueness
- `+listPlaces()` - Get places with this amenity

**Relationships**:
- Many-to-Many with Place (via PlaceAmenity)

**Access Control**:
- Admin-only creation, update, deletion

---

### PlaceAmenity Entity
**Purpose**: Junction table for M:N relationship

**Attributes**:
- `-UUID placeId` - Reference to Place
- `-UUID amenityId` - Reference to Amenity
- `-DateTime createdAt` - Association timestamp

**Methods**:
- `+associate(placeId, amenityId)` - Create association
- `+dissociate(placeId, amenityId)` - Remove association

**Purpose**:
- Enables many-to-many relationship
- Tracks association timestamp
- Supports relationship queries

---

### Facade (Manager)
**Purpose**: Central coordinator for business logic

**Dependencies**:
- `-userRepository` UserRepository
- `-placeRepository` PlaceRepository
- `-reviewRepository` ReviewRepository
- `-amenityRepository` AmenityRepository

**Methods**:

#### User Operations:
- `+registerUser(data)` - Create new user
- `+updateUser(userId, data)` - Modify user
- `+getUser(userId)` - Retrieve user
- `+deleteUser(userId)` - Remove user

#### Place Operations:
- `+createPlace(userId, data)` - Create property
- `+updatePlace(placeId, data)` - Modify property
- `+getPlace(placeId)` - Retrieve property
- `+deletePlace(placeId)` - Remove property
- `+listPlaces(filters)` - Get filtered list
- `+addAmenityToPlace(placeId, amenityId)` - Associate amenity
- `+removeAmenityFromPlace(placeId, amenityId)` - Remove amenity

#### Review Operations:
- `+submitReview(userId, placeId, data)` - Post review
- `+updateReview(reviewId, data)` - Edit review
- `+getReview(reviewId)` - Retrieve review
- `+deleteReview(reviewId)` - Remove review
- `+listReviewsByPlace(placeId)` - Get place reviews

#### Amenity Operations:
- `+createAmenity(data)` - Create amenity
- `+updateAmenity(amenityId, data)` - Modify amenity
- `+getAmenity(amenityId)` - Retrieve amenity
- `+deleteAmenity(amenityId)` - Remove amenity
- `+listAmenities()` - Get all amenities

**Responsibilities**:
- Orchestrate entity operations
- Enforce business rules
- Manage relationships
- Coordinate repositories
- Single entry point for business logic

---

### ValidationRules
**Purpose**: Centralized validation logic

**Methods**:
- `+validateUserEmail(email)` - Email format/uniqueness
- `+validatePassword(password)` - Password strength
- `+validateCoordinates(lat, long)` - Geographic bounds
- `+validatePrice(price)` - Positive value check
- `+validateRating(rating)` - 1-5 range check
- `+validateAmenityName(name)` - Uniqueness check
- `+validatePlaceTitle(title)` - Required/length check
- `+validateReviewComment(comment)` - Length check

**Purpose**:
- Centralize validation logic
- Ensure consistency
- Improve maintainability
- Support DRY principle

---

## Relationships Summary

### Inheritance
```
BaseModel (Abstract)
├── User
├── Place
├── Review
└── Amenity
```

### Associations

| Relationship | Type | Cardinality | Description |
|--------------|------|-------------|-------------|
| User owns Place | Composition | 1:N | User can own multiple places |
| User writes Review | Composition | 1:N | User can write multiple reviews |
| Place has Review | Composition | 1:N | Place receives multiple reviews |
| Place includes Amenity | Association | M:N | Many amenities per place |
| Place contains PlaceAmenity | Aggregation | 1:N | Junction table entries |
| Amenity in PlaceAmenity | Aggregation | 1:N | Junction table entries |

---

## Design Patterns Applied

### 1. **Template Method Pattern**
- BaseModel defines common lifecycle methods
- Subclasses inherit and specialize behavior

### 2. **Facade Pattern**
- Single entry point (Facade class)
- Simplifies complex operations
- Manages entity interactions

### 3. **Repository Pattern**
- Data access abstraction
- Separation of concerns
- Easy testing with mocks

### 4. **Validation Pattern**
- Centralized ValidationRules class
- Cross-cutting concerns
- Consistency across entities

### 5. **Factory Pattern**
- Entity creation through methods
- Standardized initialization

---

## UML Notation Used

| Symbol | Meaning |
|--------|---------|
| `--|>` | Inheritance (is-a) |
| `--` | Association |
| `*--` | Composition (has-a, strong ownership) |
| `o--` | Aggregation (has-a, loose ownership) |
| `-->` | Dependency |
| `"1"` | One (cardinality) |
| `"0..*"` | Zero or many (cardinality) |
| `"1..*"` | One or many (cardinality) |
| `-` | Private attribute/method |
| `+` | Public attribute/method |
| `~` | Package-private |
| `#` | Protected |

---

## Key Design Decisions

### 1. **BaseModel Inheritance**
✅ All entities inherit common attributes (id, timestamps)
✅ Promotes code reuse and consistency
✅ Simplifies entity management

### 2. **Facade Coordinator**
✅ Central point for business logic
✅ Manages all entity repositories
✅ Enforces business rules
✅ Simplifies API layer integration

### 3. **PlaceAmenity Junction**
✅ Explicit M:N relationship management
✅ Tracks association timestamp
✅ Supports relationship operations
✅ Database optimization

### 4. **ValidationRules Separation**
✅ Centralized validation logic
✅ Reusable across operations
✅ Easy to extend and maintain
✅ Testable in isolation

### 5. **Method Naming Conventions**
✅ Get* for retrievals
✅ Create*/Add*/Remove* for mutations
✅ Validate* for validations
✅ Check* for boolean checks
✅ Calculate* for computations

---

## Validation Rules Overview

### User Validation
- Email format: RFC 5322 compliance
- Email uniqueness: No duplicate registrations
- Password strength: Min 8 chars, mix of case/numbers/symbols
- Names: 1-50 characters, no special chars

### Place Validation
- Latitude: -90.0 to 90.0 (inclusive)
- Longitude: -180.0 to 180.0 (inclusive)
- Price: Positive decimal (> 0)
- Title: 1-100 characters, required
- Description: Optional, max 1000 characters

### Review Validation
- Rating: Integer 1-5 (inclusive)
- Comment: Optional, max 1000 characters
- Uniqueness: One review per user per place
- Ownership: User cannot review own places

### Amenity Validation
- Name: Unique, 1-50 characters
- Description: Optional, max 500 characters
- Format: No special characters in name

---

## Documentation Files

### Primary Files:
1. **diagrams/class_diagram.mmd** - Mermaid diagram source
2. **CLASS_DIAGRAM.md** - Detailed entity descriptions
3. **CLASS_DIAGRAM_DOCUMENTATION.md** - Comprehensive documentation
4. **ENTITIES.md** - Entity specifications
5. **ENTITIES_REFERENCE_GUIDE.md** - Quick reference guide

### Supporting Files:
- **ARCHITECTURE.md** - High-level architecture
- **README.md** - Project overview

---

## How to Use

### View the Diagram
1. **Online Viewer**: https://mermaid.live/
   - Copy content from `diagrams/class_diagram.mmd`
   - Paste and view

2. **VS Code**:
   - Install "Markdown Preview Mermaid Support"
   - Open `.mmd` file
   - Preview with `Ctrl+Shift+V`

3. **GitHub**:
   - Diagrams render automatically

### Reference in Code
- Use this diagram as blueprint for implementation
- Follow method signatures exactly
- Maintain attribute names and types
- Implement all relationships

---

## Next Steps

### Part 2: Implementation
- Implement entity models in Python
- Create Facade class
- Implement repository pattern
- Build validation layer

### Part 3: API Layer
- Create API controllers
- Map entities to DTOs
- Implement endpoint handlers
- Add error handling

### Part 4: Persistence
- Design database schema
- Create migration scripts
- Implement repositories
- Add database constraints

---

## Summary

✅ **Task 1 Complete**

Deliverables:
- Comprehensive class diagram with 8 classes
- 1,700+ lines of detailed documentation
- 5 supporting documents
- Complete entity specifications
- Design pattern implementations
- Validation rules
- Relationship mappings

The Business Logic layer is fully designed and documented, providing a solid foundation for implementation in subsequent parts.

---

**Document Version**: 1.0
**Last Updated**: January 15, 2026
**Status**: Complete - Ready for Implementation
