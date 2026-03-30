# HBnB API Sequence Diagrams

Below are Mermaid sequence diagrams for four core API calls. Each shows how the Presentation (API), Business Logic (services/models), and Persistence (database) layers collaborate. Short notes summarize the key steps.

## User Registration

```mermaid
sequenceDiagram
	participant User
	participant API as API (Presentation)
	participant Facade
	participant Service as Service Layer
	participant Model as Domain Model
	participant DB as Database

	User->>API: POST /users (email, password, profile)
	API->>Facade: route request
	Facade->>Service: validate input
	Service->>Model: build user + hash password
	Model->>DB: insert user
	DB-->>Model: userId
	Model-->>Service: user entity
	Service-->>Facade: user entity
	Facade-->>API: success payload
	API-->>User: 201 Created (token, userId)
```

## Place Creation

```mermaid
sequenceDiagram
	participant User
	participant API as API (Presentation)
	participant Facade
	participant Service as Service Layer
	participant Model as Domain Model
	participant DB as Database

	User->>API: POST /places (details) + token
	API->>Facade: verify auth + forward
	Facade->>Service: validate payload
	Service->>Model: build place with ownerId
	Model->>DB: insert place
	DB-->>Model: placeId
	Model-->>Service: place entity
	Service-->>Facade: place entity
	Facade-->>API: place resource
	API-->>User: 201 Created (placeId)
```

## Review Submission

```mermaid
sequenceDiagram
	participant User
	participant API as API (Presentation)
	participant Facade
	participant Service as Service Layer
	participant Model as Domain Model
	participant DB as Database

	User->>API: POST /places/{id}/reviews (rating, comment) + token
	API->>Facade: verify auth + forward
	Facade->>Service: validate rating/comment
	Service->>Model: ensure place exists
	Model->>DB: fetch place(id)
	DB-->>Model: place found
	Model-->>Service: place ok
	Service->>Model: guard duplicate review
	Model->>DB: insert review
	DB-->>Model: reviewId
	Model-->>Service: review entity
	Service-->>Facade: review entity
	Facade-->>API: review resource
	API-->>User: 201 Created (reviewId)
```

## Fetching a List of Places

```mermaid
sequenceDiagram
	participant User
	participant API as API (Presentation)
	participant Facade
	participant Service as Service Layer
	participant Model as Domain Model
	participant DB as Database

	User->>API: GET /places?filters
	API->>Facade: forward query
	Facade->>Service: validate filters
	Service->>Model: build query
	Model->>DB: fetch places(filters)
	DB-->>Model: places[]
	Model-->>Service: places[]
	Service-->>Facade: serialized list
	Facade-->>API: list payload
	API-->>User: 200 OK (places[])
```
