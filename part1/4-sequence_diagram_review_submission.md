# Sequence Diagram — Review Submission
 
## Purpose
 
Covers the flow when an authenticated user submits a `POST /api/v1/reviews` request for a specific place. Highlights the duplicate-review guard and the owner-cannot-review-own-place rule.
 
## Diagram
 
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API as API (Presentation)
    participant Facade
    participant Service as ReviewService
    participant Model as ReviewModel
    participant DB as Database
 
    Client->>API: POST /api/v1/places/{place_id}/reviews\n{ rating, comment }\nAuthorization: Bearer <token>
 
    API->>API: extract & verify JWT token
    alt token invalid or missing
        API-->>Client: 401 Unauthorized
    else token valid
        API->>Facade: route_request("submit_review", place_id, payload, author_id)
        Facade->>Service: validate_input(payload)
 
        alt rating not in [1..5] or comment empty
            Service-->>Facade: ValidationError
            Facade-->>API: error response
            API-->>Client: 400 Bad Request (error detail)
        else input valid
            Service->>Model: fetch_place(place_id)
            Model->>DB: SELECT * FROM places WHERE id = ?
            DB-->>Model: place row or null
 
            alt place not found
                Model-->>Service: NotFoundError
                Service-->>Facade: error response
                Facade-->>API: error response
                API-->>Client: 404 Not Found (place does not exist)
            else place found
                Service->>Model: check_not_owner(place.owner_id, author_id)
 
                alt author is the place owner
                    Model-->>Service: OwnerReviewError
                    Service-->>Facade: error response
                    Facade-->>API: error response
                    API-->>Client: 403 Forbidden (cannot review own place)
                else author is not the owner
                    Service->>Model: check_no_duplicate(place_id, author_id)
                    Model->>DB: SELECT * FROM reviews\nWHERE place_id=? AND user_id=?
                    DB-->>Model: existing review or null
 
                    alt duplicate review exists
                        Model-->>Service: DuplicateReviewError
                        Service-->>Facade: error response
                        Facade-->>API: error response
                        API-->>Client: 409 Conflict (review already submitted)
                    else no duplicate
                        Service->>Model: build_review(place_id, author_id, payload)
                        Model->>DB: INSERT INTO reviews VALUES (...)
                        DB-->>Model: generated reviewId
                        Model-->>Service: review entity
                        Service-->>Facade: review entity
                        Facade-->>API: review resource payload
                        API-->>Client: 201 Created\n{ id, place_id, user_id, rating, comment, created_at }
                    end
                end
            end
        end
    end
```
 
## Step-by-Step Explanation
 
| Step | Actor | Action |
|---|---|---|
| 1 | Client | Sends `POST /api/v1/places/{place_id}/reviews` with `rating` (1–5) and `comment`. |
| 2 | API | Verifies the JWT; rejects with `401` if missing or expired. |
| 3 | API → Facade | Routes to `ReviewService` with the place ID and the `author_id` from the token. |
| 4 | Facade → Service | Validates `rating` ∈ [1, 5] and `comment` is non-empty. |
| 5 | Service → DB | Confirms the target place actually exists; returns `404` if not. |
| 6 | Service → Model | Checks that the review author is **not** the place owner (`403` if so). |
| 7 | Service → DB | Checks for an existing review from this user for this place (`409` if found). |
| 8 | Model → DB | Inserts the review row; receives `reviewId`. |
| 9 | DB → Client | Review entity travels back up; `201 Created` is returned. |
 
## Key Design Decisions
 
- **Owner-cannot-review rule** — enforced in the service layer before any write; prevents fraudulent self-promotion of listings.
- **One-review-per-user-per-place** — a database query guard prevents rating manipulation through multiple submissions.
- **Nested route** (`/places/{place_id}/reviews`) — the place context is part of the URL, making it impossible to accidentally omit `place_id` from the request.
