# HBnB Evolution - High-Level Architecture

## Overview
The HBnB Evolution application follows a **three-layer architecture** pattern with the **Facade Pattern** for inter-layer communication.

---

## Layer Responsibilities

### 1. Presentation Layer
**Purpose**: Handle user interactions and API requests

**Components**:
- **API Controllers**: RESTful endpoints for user requests
- **Services**: Business logic orchestration
- **Request Handlers**: Parse and validate incoming requests

**Responsibilities**:
- Receive HTTP requests from clients
- Validate input parameters
- Format and return responses
- Handle authentication tokens

---

### 2. Business Logic Layer (Core)
**Purpose**: Implement application rules and entity management

**Components**:
- **Facade**: Single entry point for all business operations
- **Models**: Entity definitions (User, Place, Review, Amenity)
- **Business Rules**: Enforce constraints and validations

**Key Entities**:
- **User**: Authentication, profile management
- **Place**: Property listings and details
- **Review**: User feedback and ratings
- **Amenity**: Features and services

**Responsibilities**:
- Execute business rules
- Manage entity relationships
- Enforce data constraints
- Process complex business logic

---

### 3. Persistence Layer
**Purpose**: Data storage and retrieval operations

**Components**:
- **Repository Pattern**: Abstract data access
- **Database Access**: Direct DB operations
- **Data Validation**: Ensure data integrity

**Responsibilities**:
- CRUD operations on database
- Execute queries and transactions
- Handle database connections
- Implement caching strategies

---

## Facade Pattern Communication

### What is the Facade Pattern?
The Facade Pattern provides a **unified, simplified interface** to a complex subsystem. It reduces coupling between layers by:
- Hiding internal complexity
- Providing a single entry point
- Standardizing communication

### How It Works in HBnB

```
User Request
     ↓
Presentation Layer (API Controllers)
     ↓
Business Logic Facade (Single Interface)
     ↓
Models & Business Rules
     ↓
Persistence Layer (Repositories)
     ↓
Database
```

### Benefits
✅ Loose coupling between layers
✅ Easy to maintain and modify
✅ Clear separation of concerns
✅ Simplified testing
✅ Extensible architecture

---

## Data Flow Example: Create a Place

1. **Presentation**: API receives POST request with place details
2. **Facade**: Routes request to PlaceFacade.create_place()
3. **Business Logic**: Validates place data and owner permissions
4. **Models**: Creates Place instance with relationships
5. **Persistence**: Repository saves to database
6. **Response**: Returns created place with ID and timestamps

---

## Architecture Diagram

```
┌─────────────────────────────────────┐
│    PRESENTATION LAYER               │
│  ┌──────────────────────────────┐   │
│  │   API Controllers/Services   │   │
│  │  - UserAPI                   │   │
│  │  - PlaceAPI                  │   │
│  │  - ReviewAPI                 │   │
│  │  - AmenityAPI                │   │
│  └──────────────────────────────┘   │
└────────────────┬──────────────────┘
                 │ Facade Pattern
┌────────────────▼──────────────────┐
│    BUSINESS LOGIC LAYER            │
│  ┌──────────────────────────────┐  │
│  │   HBnB Facade (Manager)      │  │
│  │  - Unified Interface         │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   Entity Models              │  │
│  │  - User, Place, Review       │  │
│  │  - Amenity, BaseModel        │  │
│  │  - Relationships & Rules     │  │
│  └──────────────────────────────┘  │
└────────────────┬──────────────────┘
                 │ Repository Pattern
┌────────────────▼──────────────────┐
│    PERSISTENCE LAYER               │
│  ┌──────────────────────────────┐  │
│  │   Data Repositories          │  │
│  │  - UserRepository            │  │
│  │  - PlaceRepository           │  │
│  │  - ReviewRepository          │  │
│  │  - AmenityRepository         │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   Database Access Layer      │  │
│  │  - SQL Queries & Transactions│  │
│  │  - Connection Management     │  │
│  └──────────────────────────────┘  │
└────────────────┬──────────────────┘
                 │
        ┌────────▼────────┐
        │    DATABASE     │
        └─────────────────┘
```

---

## Key Design Patterns Used

| Pattern | Layer | Purpose |
|---------|-------|---------|
| **Facade** | All → All | Simplified inter-layer communication |
| **Repository** | Persistence | Abstracted data access |
| **MVC** | Presentation | Organized request handling |
| **Singleton** | Business Logic | Single facade instance |
| **Factory** | Models | Entity creation |

---

## Communication Rules

1. **Presentation Layer** → Never directly access Persistence Layer
2. **All Access** → Goes through Facade in Business Logic Layer
3. **Models** → Don't directly query database
4. **Repositories** → Don't enforce business rules (only data constraints)

---

## Implementation Guidelines

### Adding a New Feature
1. Define model in Business Logic Layer
2. Add method to Facade
3. Implement repository in Persistence Layer
4. Create API endpoint in Presentation Layer
5. Validate at each layer

### Testing Strategy
- **Unit Tests**: Test each layer independently
- **Integration Tests**: Test layer communication via Facade
- **API Tests**: Test complete request flow

---

## Security Considerations

- Authentication handled in Presentation Layer
- Authorization enforced in Business Logic Layer
- SQL Injection prevention in Persistence Layer
- Input validation at entry points
