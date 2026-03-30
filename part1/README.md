# HBnB Evolution — Technical Documentation

HBnB Evolution is a simplified Airbnb-like application. This document provides a concise blueprint of the architecture, core domain model, and key API interaction flows. All diagrams use Mermaid with neutral styling (no colors).

## 1. High-Level Architecture

```mermaid
graph TB
    subgraph Presentation_Layer[Presentation Layer]
        direction TB
        API_Users[Users API /api/v1/users]
        API_Places[Places API /api/v1/places]
        API_Reviews[Reviews API /api/v1/reviews]
        API_Amenities[Amenities API /api/v1/amenities]
    end

    subgraph Facade_Layer[Facade Interface]
        FACADE["HBnBFacade<br/>route_request()<br/>validate_input()<br/>dispatch()"]
    end

    subgraph Business_Layer[Business Logic Layer]
        direction LR
        M_User[UserModel]
        M_Place[PlaceModel]
        M_Review[ReviewModel]
        M_Amenity[AmenityModel]
    end

    subgraph Persistence_Layer[Persistence Layer]
        direction LR
        REPO[Repository / DAO]
        DATABASE[(Database)]
    end

    API_Users --> FACADE
    API_Places --> FACADE
    API_Reviews --> FACADE
    API_Amenities --> FACADE

    FACADE --> M_User
    FACADE --> M_Place
    FACADE --> M_Review
    FACADE --> M_Amenity

    M_User --> REPO
    M_Place --> REPO
    M_Review --> REPO
    M_Amenity --> REPO

    REPO --> DATABASE
```

## 2. Business Logic Layer — Class Diagram

```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +UUID id
        +datetime created_at
        +datetime updated_at
        +save() void
        +delete() void
        +to_dict() dict
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register() User
        +update_profile() User
        +deactivate() void
        +get_owned_places() List~Place~
        +get_reviews() List~Review~
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID owner_id
        +create() Place
        +update() Place
        +delete() void
        +add_amenity(Amenity) void
        +remove_amenity(Amenity) void
        +get_reviews() List~Review~
    }

    class Review {
        +Integer rating
        +String comment
        +UUID user_id
        +UUID place_id
        +submit() Review
        +update() Review
        +delete() void
    }

    class Amenity {
        +String name
        +String description
        +create() Amenity
        +update() Amenity
        +delete() void
        +get_places() List~Place~
    }

    BaseModel <|-- User      : inherits
    BaseModel <|-- Place     : inherits
    BaseModel <|-- Review    : inherits
    BaseModel <|-- Amenity   : inherits

    User    "1" --> "0..*" Place    : owns
    User    "1" --> "0..*" Review   : writes
    Place   "1" --> "0..*" Review   : receives
    Place   "0..*" <--> "0..*" Amenity : has
```

## 3. API Interaction Flows — Sequence Diagrams

Participants (all diagrams): **User**, **API** (Presentation), **Facade**, **Service**, **Model**, **Database**.

### 3.1 User Registration

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API
    participant Facade
    participant Service
    participant Model
    participant Database

    User->>API: POST /api/v1/users { first_name, last_name, email, password }
    API->>Facade: route request
    Facade->>Service: validate input
    Service->>Model: build user + hash password
    Model->>Database: insert user
    Database-->>Model: userId
    Model-->>Service: user entity
    Service-->>Facade: user entity
    Facade-->>API: success payload
    API-->>User: 201 Created (userId, email)
```

### 3.2 Place Creation

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API
    participant Facade
    participant Service
    participant Model
    participant Database

    User->>API: POST /api/v1/places (details) + token
    API->>Facade: verify auth + forward
    Facade->>Service: validate payload
    Service->>Model: build place with ownerId
    Model->>Database: insert place
    Database-->>Model: placeId
    Model-->>Service: place entity
    Service-->>Facade: place entity
    Facade-->>API: place resource
    API-->>User: 201 Created (placeId)
```

### 3.3 Review Submission

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API
    participant Facade
    participant Service
    participant Model
    participant Database

    User->>API: POST /api/v1/reviews (place_id, rating, comment) + token
    API->>Facade: verify auth + forward
    Facade->>Service: validate rating/comment
    Service->>Model: ensure place exists and no duplicate
    Model->>Database: fetch place
    Database-->>Model: place found
    Model->>Database: insert review
    Database-->>Model: reviewId
    Model-->>Service: review entity
    Service-->>Facade: review entity
    Facade-->>API: review resource
    API-->>User: 201 Created (reviewId)
```

### 3.4 Fetch Places

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API
    participant Facade
    participant Service
    participant Model
    participant Database

    User->>API: GET /api/v1/places?filters
    API->>Facade: forward query
    Facade->>Service: validate filters
    Service->>Model: build query
    Model->>Database: fetch places(filters)
    Database-->>Model: places[]
    Model-->>Service: places[]
    Service-->>Facade: serialized list
    Facade-->>API: list payload
    API-->>User: 200 OK (places[])
```

---

This documentation is intentionally concise, neutral-styled, and aligned to the HBnB Evolution requirements.
