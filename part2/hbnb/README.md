# HBnB API (Part 2)

This project implements REST endpoints for:

- Users
- Amenities
- Places
- Reviews

The API is built with Flask + Flask-RESTx and uses an in-memory repository.

## 1) Setup

From the `part2/hbnb` directory:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2) Run the API

```bash
python run.py
```

Base URL:

```text
http://127.0.0.1:5000/api/v1
```

Swagger UI:

```text
http://127.0.0.1:5000/api/v1/
```

## 3) Model-Level Validation Implemented

### User

- `first_name` required, non-empty string
- `last_name` required, non-empty string
- `email` required, valid email format

### Amenity

- `name` required, non-empty string

### Place

- `title` required, non-empty string
- `price` numeric and validated in model
- `latitude` must be in `[-90, 90]`
- `longitude` must be in `[-180, 180]`
- `owner_id` must reference an existing user

### Review

- `text` required, non-empty string
- `rating` integer in `[1, 5]`
- `user_id` must reference an existing user
- `place_id` must reference an existing place

## 4) Endpoint Coverage

### Users

- `POST /users/`
- `GET /users/`
- `GET /users/<user_id>`
- `PUT /users/<user_id>`

### Amenities

- `POST /amenities/`
- `GET /amenities/`
- `GET /amenities/<amenity_id>`
- `PUT /amenities/<amenity_id>`

### Places

- `POST /places/`
- `GET /places/`
- `GET /places/<place_id>`
- `PUT /places/<place_id>`
- `GET /places/<place_id>/reviews`

### Reviews

- `POST /reviews/`
- `GET /reviews/`
- `GET /reviews/<review_id>`
- `PUT /reviews/<review_id>`
- `DELETE /reviews/<review_id>`

## 5) How to Test with curl

Important: use one line or proper line continuations. If split incorrectly, shell returns exit code `127`.

### Create User

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'
```

### Create Amenity

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Wi-Fi"}'
```

### Create Place

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<USER_ID>","amenities":[]}'
```

### Create Review

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text":"Great place to stay!","rating":5,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

### Get Reviews for Place

```bash
curl -i "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews"
```

### Update Review

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Amazing stay!","rating":4,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

### Delete Review

```bash
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"
```

## 6) Live Verification Results (Executed)

The following were run successfully against the running app:

- `POST /users/` -> `201`
- `GET /users/` -> `200`
- `GET /users/<id>` -> `200`
- `PUT /users/<id>` -> `200`
- `POST /amenities/` -> `201`
- `GET /amenities/` -> `200`
- `GET /amenities/<id>` -> `200`
- `PUT /amenities/<id>` -> `200`
- `POST /places/` -> `201`
- `GET /places/` -> `200`
- `GET /places/<id>` -> `200`
- `PUT /places/<id>` -> `200`
- `POST /reviews/` -> `201`
- `GET /reviews/` -> `200`
- `GET /reviews/<id>` -> `200`
- `GET /places/<id>/reviews` -> `200`
- `PUT /reviews/<id>` -> `200`
- `DELETE /reviews/<id>` -> `200`
- `GET /reviews/fake-id-999` -> `404`
- `POST /places/` with invalid latitude -> `400`
- `POST /reviews/` with invalid rating -> `400`

## 7) Run Automated Tests

```bash
./venv/bin/python tests.py
