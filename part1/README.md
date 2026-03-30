# HBnB Evolution — Technical Documentation

> **Project:** HBnB Evolution (Airbnb-like Application)
> **Document Type:** Comprehensive Architecture & Design Reference
> **Version:** 1.0
> **Purpose:** Blueprint for implementation phases — covers system architecture, business logic design, and API interaction flows.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Business Logic Layer — Class Diagram](#3-business-logic-layer--class-diagram)
4. [API Interaction Flows — Sequence Diagrams](#4-api-interaction-flows--sequence-diagrams)
   - 4A. [User Registration](#4a-user-registration)
   - 4B. [Place Creation](#4b-place-creation)
   - 4C. [Review Submission](#4c-review-submission)
   - 4D. [Fetch Places](#4d-fetch-places)
5. [Design Decisions & Rationale](#5-design-decisions--rationale)

---

## 1. Introduction

### 1.1 Project Overview

**HBnB Evolution** is a simplified, full-stack web application modeled after Airbnb. It enables users to list properties (places), browse listings, attach amenities, and submit reviews. The application is designed with a clean, layered architecture that separates concerns across the Presentation, Business Logic, and Persistence layers.

### 1.2 Purpose of This Document

This document serves as the **authoritative technical blueprint** for the HBnB Evolution project. It consolidates all architectural decisions, data models, and interaction flows into a single reference to:

- Guide developers during implementation.
- Establish shared vocabulary and naming conventions.
- Document design decisions and their rationale.
- Provide visual representations of system structure and behavior.

### 1.3 Scope

The document covers:
- **High-Level Architecture** — the three-tier layered model and Facade pattern.
- **Business Logic** — entity definitions, attributes, methods, and relationships.
- **API Interaction Flows** — four key operations described as sequence diagrams.

### 1.4 Core Entities Summary

| Entity   | Key Attributes                                       | Key Relationships              |
|----------|------------------------------------------------------|-------------------------------|
| User     | id, first_name, last_name, email, password, is_admin | Owns Places, Writes Reviews    |
| Place    | id, title, description, price, latitude, longitude   | Owned by User, Has Amenities   |
| Review   | id, rating, comment                                  | Belongs to User and Place      |
| Amenity  | id, name, description                                | Many-to-many with Place        |

> All entities include `id` (UUID4), `created_at`, and `updated_at` timestamps.

---

## 2. High-Level Architecture

### 2.1 Overview

HBnB Evolution follows a **three-tier layered architecture**:

- **Presentation Layer** — Exposes RESTful API endpoints consumed by clients. Handles HTTP requests, serialization, and response formatting.
- **Business Logic Layer** — Contains all application models and business rules. Accessed exclusively through a **Facade** interface that decouples the API from internal logic.
- **Persistence Layer** — Responsible for all database operations: querying, storing, updating, and deleting records.

### 2.2 Facade Pattern

The Facade pattern is applied between the Presentation and Business Logic layers. Rather than having API routes call model classes directly, they communicate through a single `HBnBFacade` interface. This:
- Reduces coupling between layers.
- Makes the API layer unaware of internal model complexity.
- Simplifies testing by allowing the facade to be mocked independently.

### 2.3 Diagram

```mermaid
graph TB
    %% ─── Style Definitions ───────────────────────────────────────────
    classDef presentationNode  fill:#4A90D9,stroke:#2C5F8A,color:#fff,rx:6
    classDef facadeNode        fill:#F5A623,stroke:#B8791A,color:#fff,rx:6
    classDef businessNode      fill:#7ED321,stroke:#5A9A18,color:#fff,rx:6
    classDef persistenceNode   fill:#9B59B6,stroke:#6C3483,color:#fff,rx:6
    classDef layerLabel        fill:#ECF0F1,stroke:#BDC3C7,color:#555,rx:4

    %% ─── Presentation Layer ──────────────────────────────────────────
    subgraph PL["🖥️  PRESENTATION LAYER"]
        direction TB
        API_Users["👤 Users API\n/api/v1/users"]
        API_Places["🏠 Places API\n/api/v1/places"]
        API_Reviews["⭐ Reviews API\n/api/v1/reviews"]
        API_Amenities["🛎️  Amenities API\n/api/v1/amenities"]
    end

    %% ─── Facade ──────────────────────────────────────────────────────
    subgraph FL["🔀  FACADE INTERFACE"]
        FACADE["HBnBFacade\n─────────────────\nroute_request()\nvalidate_input()\ndispatch()"]
    end

    %% ─── Business Logic Layer ────────────────────────────────────────
    subgraph BL["⚙️  BUSINESS LOGIC LAYER"]
        direction LR
        M_User["UserModel"]
        M_Place["PlaceModel"]
        M_Review["ReviewModel"]
        M_Amenity["AmenityModel"]
    end

    %% ─── Persistence Layer ───────────────────────────────────────────
    subgraph DB["🗄️  PERSISTENCE LAYER"]
        direction LR
        REPO["Repository\n(Data Access Object)"]
        DATABASE[("📦 Database\n(SQLite / PostgreSQL)")]
    end

    %% ─── Connections ─────────────────────────────────────────────────
    API_Users     --> FACADE
    API_Places    --> FACADE
    API_Reviews   --> FACADE
    API_Amenities --> FACADE

    FACADE --> M_User
    FACADE --> M_Place
    FACADE --> M_Review
    FACADE --> M_Amenity

    M_User    --> REPO
    M_Place   --> REPO
    M_Review  --> REPO
    M_Amenity --> REPO

    REPO --> DATABASE

    %% ─── Apply Styles ────────────────────────────────────────────────
    class API_Users,API_Places,API_Reviews,API_Amenities presentationNode
    class FACADE facadeNode
    class M_User,M_Place,M_Review,M_Amenity businessNode
    class REPO,DATABASE persistenceNode
```

### 2.4 Layer Responsibilities

| Layer              | Color  | Responsibility                                                     |
|--------------------|--------|--------------------------------------------------------------------|
| Presentation       | Blue   | HTTP request/response handling, input serialization, routing       |
| Facade             | Orange | Single entry-point between API and models, dispatches operations   |
| Business Logic     | Green  | Domain rules, entity validation, relationship management           |
| Persistence        | Purple | CRUD operations, ORM mapping, database transactions                |

---

## 3. Business Logic Layer — Class Diagram

### 3.1 Overview

The Business Logic Layer contains four primary entity classes, all inheriting from a shared `BaseModel`. This base class encapsulates universal attributes (`id`, `created_at`, `updated_at`) and lifecycle methods (`save()`, `delete()`), enforcing consistency across all entities.

### 3.2 Entities

- **User** — Represents registered application users. Can own places and write reviews. The `is_admin` flag grants elevated privileges.
- **Place** — A property listing owned by a User. Contains geographic coordinates, pricing, and a collection of amenities.
- **Review** — A user-authored rating and comment attached to a specific place.
- **Amenity** — A feature or service (e.g., WiFi, pool) that can be associated with multiple places.

### 3.3 Relationships

| Relationship            | Type         | Description                               |
|-------------------------|--------------|-------------------------------------------|
| User → Place            | One-to-Many  | A user can own many places                |
| User → Review           | One-to-Many  | A user can write many reviews             |
| Place → Review          | One-to-Many  | A place can have many reviews             |
| Place ↔ Amenity         | Many-to-Many | A place has many amenities; amenities span many places |

### 3.4 Diagram

```mermaid
classDiagram
    %% ─── Style Definitions ───────────────────────────────────────────
    classDef baseClass    fill:#95A5A6,stroke:#717D7E,color:#fff
    classDef userClass    fill:#2980B9,stroke:#1A5276,color:#fff
    classDef placeClass   fill:#27AE60,stroke:#1E8449,color:#fff
    classDef reviewClass  fill:#E67E22,stroke:#A04000,color:#fff
    classDef amenityClass fill:#8E44AD,stroke:#6C3483,color:#fff

    %% ─── BaseModel ───────────────────────────────────────────────────
    class BaseModel {
        <<abstract>>
        +UUID id
        +datetime created_at
        +datetime updated_at
        ──────────────────
        +save() void
        +delete() void
        +to_dict() dict
    }

    %% ─── User ────────────────────────────────────────────────────────
    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        ──────────────────
        +register() User
        +update_profile() User
        +deactivate() void
        +get_owned_places() List~Place~
        +get_reviews() List~Review~
    }

    %% ─── Place ───────────────────────────────────────────────────────
    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID owner_id
        ──────────────────
        +create() Place
        +update() Place
        +delete() void
        +add_amenity(Amenity) void
        +remove_amenity(Amenity) void
        +get_reviews() List~Review~
    }

    %% ─── Review ──────────────────────────────────────────────────────
    class Review {
        +Integer rating
        +String comment
        +UUID user_id
        +UUID place_id
        ──────────────────
        +submit() Review
        +update() Review
        +delete() void
    }

    %% ─── Amenity ─────────────────────────────────────────────────────
    class Amenity {
        +String name
        +String description
        ──────────────────
        +create() Amenity
        +update() Amenity
        +delete() void
        +get_places() List~Place~
    }

    %% ─── Relationships ───────────────────────────────────────────────
    BaseModel <|-- User      : inherits
    BaseModel <|-- Place     : inherits
    BaseModel <|-- Review    : inherits
    BaseModel <|-- Amenity   : inherits

    User    "1" --> "0..*" Place   : owns
    User    "1" --> "0..*" Review  : writes
    Place   "1" --> "0..*" Review  : receives
    Place   "0..*" <--> "0..*" Amenity : has

    %% ─── Apply Styles ────────────────────────────────────────────────
    class BaseModel baseClass
    class User userClass
    class Place placeClass
    class Review reviewClass
    class Amenity amenityClass
```

### 3.5 Design Notes

- **BaseModel** is abstract — it is never instantiated directly. All entities extend it.
- **UUID identifiers** are generated at the model level (not the database level) to ensure IDs are available before persistence.
- **Passwords** in `User` are stored as hashed strings — the model is responsible for hashing on creation/update.
- The `Place ↔ Amenity` many-to-many relationship is managed via a join table (`place_amenity`) at the persistence layer.

---

## 4. API Interaction Flows — Sequence Diagrams

> **Participants common to all diagrams:**
> - **Client** — The end user or external consumer (browser, mobile app, etc.)
> - **API** — Presentation layer endpoint (Flask/FastAPI route handler)
> - **Facade** — HBnBFacade interface
> - **Service** — Business logic model class
> - **Database** — Persistence layer (repository + DB)

---

### 4A. User Registration

#### Description

A new user submits their registration details. The API validates the format, the Facade delegates to the UserModel which checks for email uniqueness, hashes the password, and persists the new record.

#### Key Steps
1. Client sends `POST /api/v1/users` with registration payload.
2. API layer validates required fields and data format.
3. Facade routes request to `UserModel`.
4. `UserModel` checks for duplicate email in the database.
5. Password is hashed and user record is saved.
6. Success response with the new user object is returned.

#### Diagram

```mermaid
sequenceDiagram
    autonumber

    actor Client
    participant API   as 🖥️ API<br/>(Presentation)
    participant Facade as 🔀 Facade
    participant Service as ⚙️ UserModel<br/>(Business Logic)
    participant DB    as 🗄️ Database<br/>(Persistence)

    Client->>+API: POST /api/v1/users<br/>{ first_name, last_name, email, password }

    Note over API: Validate request format<br/>Check required fields

    alt Invalid input format
        API-->>Client: 400 Bad Request<br/>{ error: "Validation failed" }
    end

    API->>+Facade: register_user(data)

    Facade->>+Service: User.register(data)

    Service->>+DB: SELECT * FROM users WHERE email = ?
    DB-->>-Service: Result (empty or existing user)

    alt Email already exists
        Service-->>Facade: raise DuplicateEmailError
        Facade-->>API: Error propagated
        API-->>Client: 409 Conflict<br/>{ error: "Email already registered" }
    end

    Note over Service: Hash password with bcrypt<br/>Generate UUID for id<br/>Set created_at / updated_at

    Service->>+DB: INSERT INTO users VALUES (...)
    DB-->>-Service: Commit success

    Service-->>-Facade: User object
    Facade-->>-API: User object

    Note over API: Serialize to JSON<br/>Exclude password field

    API-->>-Client: 201 Created<br/>{ id, first_name, last_name, email, created_at }
```

---

### 4B. Place Creation

#### Description

An authenticated user creates a new place listing. The token is verified before processing. The place is validated, linked to the owner, and stored.

#### Key Steps
1. Client sends `POST /api/v1/places` with a valid auth token and place data.
2. API authenticates the token and extracts the user ID.
3. Place attributes are validated (price > 0, valid coordinates).
4. A new `Place` record is inserted with the owner's ID.
5. The created place is returned.

#### Diagram

```mermaid
sequenceDiagram
    autonumber

    actor Client
    participant API    as 🖥️ API<br/>(Presentation)
    participant Facade as 🔀 Facade
    participant Service as ⚙️ PlaceModel<br/>(Business Logic)
    participant DB     as 🗄️ Database<br/>(Persistence)

    Client->>+API: POST /api/v1/places<br/>Headers: Authorization: Bearer <token><br/>Body: { title, description, price, latitude, longitude }

    Note over API: Verify JWT / session token<br/>Extract owner_id from token

    alt Token missing or invalid
        API-->>Client: 401 Unauthorized<br/>{ error: "Authentication required" }
    end

    Note over API: Validate place payload<br/>price > 0, lat/lon in range

    alt Invalid place data
        API-->>Client: 400 Bad Request<br/>{ error: "Invalid place attributes" }
    end

    API->>+Facade: create_place(owner_id, data)

    Facade->>+Service: Place.create(owner_id, data)

    Note over Service: Generate UUID<br/>Attach owner_id<br/>Set timestamps

    Service->>+DB: SELECT * FROM users WHERE id = owner_id
    DB-->>-Service: User record confirmed

    Service->>+DB: INSERT INTO places VALUES (...)
    DB-->>-Service: Commit success

    Service-->>-Facade: Place object
    Facade-->>-API: Place object

    Note over API: Serialize Place to JSON

    API-->>-Client: 201 Created<br/>{ id, title, description, price,<br/>  latitude, longitude, owner_id, created_at }
```

---

### 4C. Review Submission

#### Description

An authenticated user submits a review for a place they have visited. The system validates that the user is not reviewing their own place, that they haven't already reviewed it, and that the rating is in the valid range (1–5).

#### Key Steps
1. Client sends `POST /api/v1/reviews` with a valid auth token, place ID, rating, and comment.
2. API authenticates the user.
3. Business logic validates: place exists, user ≠ owner, no duplicate review.
4. Review is saved and returned.

#### Diagram

```mermaid
sequenceDiagram
    autonumber

    actor Client
    participant API    as 🖥️ API<br/>(Presentation)
    participant Facade as 🔀 Facade
    participant Service as ⚙️ ReviewModel<br/>(Business Logic)
    participant DB     as 🗄️ Database<br/>(Persistence)

    Client->>+API: POST /api/v1/reviews<br/>Headers: Authorization: Bearer <token><br/>Body: { place_id, rating, comment }

    Note over API: Verify token<br/>Extract reviewer user_id

    alt Unauthenticated
        API-->>Client: 401 Unauthorized
    end

    Note over API: Validate: rating is 1–5<br/>comment is not empty

    alt Invalid input
        API-->>Client: 400 Bad Request
    end

    API->>+Facade: submit_review(user_id, data)

    Facade->>+Service: Review.submit(user_id, data)

    Service->>+DB: SELECT * FROM places WHERE id = place_id
    DB-->>-Service: Place record

    alt Place not found
        Service-->>Facade: raise PlaceNotFoundError
        Facade-->>API: Error propagated
        API-->>Client: 404 Not Found<br/>{ error: "Place not found" }
    end

    Note over Service: Verify user is not the place owner

    alt User is the owner
        Service-->>Facade: raise SelfReviewError
        Facade-->>API: Error propagated
        API-->>Client: 403 Forbidden<br/>{ error: "Cannot review your own place" }
    end

    Service->>+DB: SELECT * FROM reviews<br/>WHERE user_id = ? AND place_id = ?
    DB-->>-Service: Existing review check

    alt Duplicate review
        Service-->>Facade: raise DuplicateReviewError
        Facade-->>API: Error propagated
        API-->>Client: 409 Conflict<br/>{ error: "Already reviewed this place" }
    end

    Note over Service: Generate UUID<br/>Set timestamps

    Service->>+DB: INSERT INTO reviews VALUES (...)
    DB-->>-Service: Commit success

    Service-->>-Facade: Review object
    Facade-->>-API: Review object

    API-->>-Client: 201 Created<br/>{ id, rating, comment, user_id, place_id, created_at }
```

---

### 4D. Fetch Places

#### Description

A client retrieves a list of available places, optionally filtered by query parameters (e.g., price range, location). No authentication is required for this read-only operation.

#### Key Steps
1. Client sends `GET /api/v1/places` with optional filters.
2. API parses and validates query parameters.
3. Facade delegates a filtered query to the PlaceModel.
4. Database returns matching records, which are serialized and returned.

#### Diagram

```mermaid
sequenceDiagram
    autonumber

    actor Client
    participant API    as 🖥️ API<br/>(Presentation)
    participant Facade as 🔀 Facade
    participant Service as ⚙️ PlaceModel<br/>(Business Logic)
    participant DB     as 🗄️ Database<br/>(Persistence)

    Client->>+API: GET /api/v1/places<br/>Query: ?min_price=50&max_price=200&city=Paris

    Note over API: Parse query parameters<br/>Apply defaults (page=1, limit=20)

    alt Invalid query params (e.g., negative price)
        API-->>Client: 400 Bad Request<br/>{ error: "Invalid filter values" }
    end

    API->>+Facade: get_places(filters)

    Facade->>+Service: Place.fetch_all(filters)

    Note over Service: Build dynamic query<br/>from filters dict

    Service->>+DB: SELECT * FROM places<br/>WHERE price BETWEEN ? AND ?<br/>ORDER BY created_at DESC<br/>LIMIT 20 OFFSET 0
    DB-->>-Service: List of matching Place records

    alt No places found
        Service-->>Facade: Empty list []
        Facade-->>API: Empty list []
        API-->>Client: 200 OK<br/>{ data: [], total: 0, page: 1 }
    end

    Note over Service: Attach owner info<br/>Attach amenity list per place

    Service->>+DB: SELECT amenities for each place<br/>(via place_amenity join table)
    DB-->>-Service: Amenities per place

    Service-->>-Facade: List of enriched Place objects
    Facade-->>-API: List of Place objects

    Note over API: Serialize to JSON array<br/>Apply pagination metadata

    API-->>-Client: 200 OK<br/>{ data: [ { id, title, price, amenities, ... } ],<br/>  total: 47, page: 1, limit: 20 }
```

---

## 5. Design Decisions & Rationale

### 5.1 Layered Architecture

**Decision:** Strict three-tier architecture with no cross-layer calls.

**Rationale:** Separating concerns into Presentation, Business Logic, and Persistence layers allows each to evolve independently. The API can be replaced (REST → GraphQL) without touching business logic. The database can be swapped (SQLite → PostgreSQL) without changing model code.

### 5.2 Facade Pattern

**Decision:** A single `HBnBFacade` class acts as the only entry point from the API to the Business Logic layer.

**Rationale:** Prevents tight coupling between route handlers and model internals. Simplifies unit testing (mock the facade, not individual models). Provides a single place to add cross-cutting concerns like logging and rate limiting.

### 5.3 BaseModel Inheritance

**Decision:** All entities inherit from an abstract `BaseModel`.

**Rationale:** Eliminates code duplication for `id`, `created_at`, `updated_at`, `save()`, and `delete()`. Guarantees a consistent identity strategy (UUID4) across all entities.

### 5.4 UUID Primary Keys

**Decision:** UUIDs are generated at the application layer, not auto-incremented by the database.

**Rationale:** IDs are available before the record is persisted, simplifying event-driven patterns. UUIDs are globally unique — safe for distributed systems and data migrations.

### 5.5 Business Rule Enforcement in the Model Layer

**Decision:** Rules like "a user cannot review their own place" or "no duplicate reviews" are enforced in the Service (Model) layer, not in the API layer.

**Rationale:** Business rules belong in the domain, not in the transport layer. This keeps rules consistent regardless of whether they are triggered by the REST API, a CLI, or a scheduled job.

### 5.6 Many-to-Many for Place ↔ Amenity

**Decision:** Managed via a join table `place_amenity(place_id, amenity_id)`.

**Rationale:** Standard relational approach for M:N relationships. Allows amenities to be managed globally (add/remove/rename) without modifying place records directly. Efficient querying with indexed foreign keys.

---

*End of Document — HBnB Evolution Technical Documentation v1.0*
