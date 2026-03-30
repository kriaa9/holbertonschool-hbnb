# HBnB API Sequence Diagrams

Below are Mermaid sequence diagrams for four core API calls. Each shows how the Presentation (API), Business Logic (services/models), and Persistence (database) layers collaborate. Short notes summarize the key steps.

## User Registration

User submits sign-up details. API validates, hashes the password, stores the user, and returns a token or confirmation.

```mermaid
sequenceDiagram
 participant User
 participant API as API Gateway / Controller
 participant Service as User Service
 participant DB as Database

 User->>API: POST /users (email, password, profile data)
 API->>Service: validateInput()
 Service->>Service: hashPassword()
 Service->>DB: insertUser(email, hashedPassword, profile)
 DB-->>Service: userId
 Service-->>API: success + auth token
 API-->>User: 201 Created (token, userId)
```

## Place Creation

Authenticated user creates a new place listing. API checks auth, validates payload, persists the place, and returns the created resource.

```mermaid
sequenceDiagram
 participant User
 participant API as API Gateway / Controller
 participant Service as Place Service
 participant DB as Database

 User->>API: POST /places (title, location, price, etc.) + token
 API->>API: verifyAuth(token)
 API->>Service: validatePlacePayload()
 Service->>DB: insertPlace(ownerId, details)
 DB-->>Service: placeId
 Service-->>API: place resource
 API-->>User: 201 Created (placeId, details)
```

## Review Submission

User submits a review for a place. API verifies auth, validates rating/comment, ensures place exists, then stores the review.

```mermaid
sequenceDiagram
 participant User
 participant API as API Gateway / Controller
 participant Service as Review Service
 participant DB as Database

 User->>API: POST /places/{id}/reviews (rating, comment) + token
 API->>API: verifyAuth(token)
 API->>Service: validateReviewPayload()
 Service->>DB: fetchPlace(id)
 DB-->>Service: place found
 Service->>DB: insertReview(placeId, userId, rating, comment)
 DB-->>Service: reviewId
 Service-->>API: review resource
 API-->>User: 201 Created (reviewId)
```

## Fetching a List of Places

User requests a filtered list of places (e.g., by city, price range). API validates query params, service applies filters, and returns results.

```mermaid
sequenceDiagram
 participant User
 participant API as API Gateway / Controller
 participant Service as Place Service
 participant DB as Database

 User->>API: GET /places?city=...&price_min=...&price_max=...
 API->>Service: validateQueryParams()
 Service->>DB: queryPlaces(filters)
 DB-->>Service: places[]
 Service-->>API: serialized list
 API-->>User: 200 OK (places[])
```
