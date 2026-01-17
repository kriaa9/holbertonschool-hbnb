# Task 2: User Endpoints - Implementation Guide

## Overview
This document describes the implementation of the User Endpoints for the HBnB Evolution API, following the three-layer architecture (Presentation, Business Logic, Persistence).

## Objectives Completed

✅ **POST /api/v1/users/** - Create a new user
✅ **GET /api/v1/users/** - Retrieve all users
✅ **GET /api/v1/users/<user_id>** - Retrieve a specific user
✅ **PUT /api/v1/users/<user_id>** - Update user information

## Architecture

### Layers

#### 1. Presentation Layer (API Endpoints)
- **File**: `app/api/v1/resources/users.py`
- **Responsibility**: Handle HTTP requests/responses
- **Components**:
  - UserList Resource: Handles `/api/v1/users/` (GET all, POST create)
  - User Resource: Handles `/api/v1/users/<user_id>` (GET, PUT)

#### 2. Business Logic Layer (Facade)
- **File**: `app/services/facade.py`
- **Responsibility**: Implement business rules and validation
- **Key Methods**:
  - `create_user()`: Validate and create user
  - `get_user()`: Retrieve user by ID
  - `update_user()`: Update user data
  - `get_all_users()`: List all users

#### 3. Persistence Layer (Repository)
- **File**: `app/services/persistence.py`
- **Responsibility**: In-memory data storage
- **Pattern**: Singleton pattern (one instance per application)
- **Storage**: Dictionary-based (in-memory)

#### 4. Models
- **File**: `app/models/user.py`
- **Responsibility**: Define User entity with validation

## Key Features

### Password Security
- ✅ Passwords are **NOT** included in API responses
- ✅ Validation method `to_dict()` excludes password field
- ❌ Password updates are not allowed via PUT endpoint

### Validation Rules

#### First Name
- Required field
- Maximum 50 characters
- Cannot be empty/whitespace

#### Last Name
- Required field
- Maximum 50 characters
- Cannot be empty/whitespace

#### Email
- Required field
- Must match email format regex
- Must be unique (no duplicates)
- Format: `user@example.com`

#### Password
- Required field
- Minimum 6 characters
- Not updatable after creation

## API Endpoints

### 1. Create User (POST /api/v1/users/)

**Request:**
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:30:00"
}
```

**Possible Errors:**
- 400: Invalid input (missing fields, validation errors)
- 400: Email already exists

### 2. Get All Users (GET /api/v1/users/)

**Request:**
```bash
curl http://localhost:5000/api/v1/users/
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "is_admin": false,
    "created_at": "2026-01-17T10:30:00",
    "updated_at": "2026-01-17T10:30:00"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "is_admin": false,
    "created_at": "2026-01-17T10:31:00",
    "updated_at": "2026-01-17T10:31:00"
  }
]
```

### 3. Get User by ID (GET /api/v1/users/<user_id>)

**Request:**
```bash
curl http://localhost:5000/api/v1/users/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:30:00"
}
```

**Possible Errors:**
- 404: User not found

### 4. Update User (PUT /api/v1/users/<user_id>)

**Request:**
```bash
curl -X PUT http://localhost:5000/api/v1/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jonathan",
    "last_name": "Doe-Smith"
  }'
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "Jonathan",
  "last_name": "Doe-Smith",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2026-01-17T10:30:00",
  "updated_at": "2026-01-17T10:32:00"
}
```

**Possible Errors:**
- 400: Invalid input
- 404: User not found

## Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation error, duplicate email |
| 404 | Not Found | User doesn't exist |
| 500 | Server Error | Unexpected error |

## Running the Application

### Install Dependencies
```bash
cd part2
pip install -r requirements.txt
```

### Run the Server
```bash
python run.py
```

The API will be available at:
- API endpoints: `http://localhost:5000/api/v1/users/`
- Swagger documentation: `http://localhost:5000/api/docs`

## Running Tests

### Unit Tests
```bash
cd part2
python -m unittest tests.test_users -v
```

### cURL Testing Examples

#### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "secure123"
  }' | json_pp
```

#### Get All Users
```bash
curl http://localhost:5000/api/v1/users/ | json_pp
```

#### Get Specific User
```bash
curl http://localhost:5000/api/v1/users/{user_id} | json_pp
```

#### Update User
```bash
curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Updated"}' | json_pp
```

## Project Structure

```
part2/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py    # Base class with id, timestamps
│   │   └── user.py          # User entity with validation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── persistence.py   # In-memory repository (Singleton)
│   │   └── facade.py        # Business logic facade
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── resources/
│               ├── __init__.py
│               └── users.py # User API endpoints
├── config/
│   └── config.py            # Flask configuration
├── tests/
│   ├── __init__.py
│   └── test_users.py        # Unit tests
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## Design Patterns Used

### 1. **Singleton Pattern** (Repository)
- Ensures only one instance of DataRepository exists
- Guarantees consistent data across the application

### 2. **Facade Pattern** (HBnBFacade)
- Provides simplified interface to business logic
- Reduces coupling between presentation and persistence layers
- Centralizes validation logic

### 3. **MVC Pattern**
- Models: User, BaseModel
- Views: Flask-RESTX resources
- Controllers: Facade methods

### 4. **Repository Pattern**
- Abstracts data storage implementation
- Easy to swap in database later
- Isolates persistence logic

## Security Considerations

⚠️ **Note**: This is a simplified implementation for Part 2.

- ✅ Passwords excluded from responses
- ❌ Passwords not hashed (will be in Part 3)
- ❌ No authentication/authorization (will be in Part 3)
- ✅ Email validation implemented
- ✅ Input validation on all fields

## Future Enhancements (Part 3)

- [ ] Password hashing (bcrypt)
- [ ] JWT authentication
- [ ] Role-based access control
- [ ] Database persistence (SQLAlchemy)
- [ ] Email verification
- [ ] Rate limiting
- [ ] CORS configuration

## References

- Flask Documentation: https://flask.palletsprojects.com/
- Flask-RESTX: https://flask-restx.readthedocs.io/
- RESTful API Design: https://restfulapi.net/
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
