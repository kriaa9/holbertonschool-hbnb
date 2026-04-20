# HBnB API - Part 2 Manual Testing Guide

This Part 2 implementation exposes REST endpoints for users, amenities, places, and reviews using Flask and Flask-RESTx with an in-memory repository.

## 1. Setup

From the `part2/hbnb` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you already created a virtual environment, activate it and install the requirements there.

## 2. Run the API

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

## 3. Recommended Manual Test Flow

Run the commands in order and reuse the IDs returned by the API.

### 3.1 Create a user

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'
```

Expected status: `201`

Save the returned `id` as `<USER_ID>`.

### 3.2 List all users

```bash
curl -i "http://127.0.0.1:5000/api/v1/users/"
```

Expected status: `200`

### 3.3 Get a user by id

```bash
curl -i "http://127.0.0.1:5000/api/v1/users/<USER_ID>"
```

Expected status: `200`

### 3.4 Update a user

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/users/<USER_ID>" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Johnny","last_name":"Doe","email":"johnny.doe@example.com"}'
```

Expected status: `200`

### 3.5 Create an amenity

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Wi-Fi"}'
```

Expected status: `201`

Save the returned `id` as `<AMENITY_ID>`.

### 3.6 List all amenities

```bash
curl -i "http://127.0.0.1:5000/api/v1/amenities/"
```

Expected status: `200`

### 3.7 Get an amenity by id

```bash
curl -i "http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>"
```

Expected status: `200`

### 3.8 Update an amenity

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>" \
  -H "Content-Type: application/json" \
  -d '{"name":"High-speed Wi-Fi"}'
```

Expected status: `200`

### 3.9 Create a place

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<USER_ID>","amenities":["<AMENITY_ID>"]}'
```

Expected status: `201`

Save the returned `id` as `<PLACE_ID>`.

### 3.10 List all places

```bash
curl -i "http://127.0.0.1:5000/api/v1/places/"
```

Expected status: `200`

### 3.11 Get a place by id

```bash
curl -i "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>"
```

Expected status: `200`

The response should include owner details and amenities.

### 3.12 Update a place

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Apartment","description":"Updated description","price":120.0,"latitude":37.7750,"longitude":-122.4195,"owner_id":"<USER_ID>","amenities":["<AMENITY_ID>"]}'
```

Expected status: `200`

### 3.13 Get all reviews for a place

```bash
curl -i "http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews"
```

Expected status: `200`

### 3.14 Create a review

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text":"Great stay!","rating":5,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

Expected status: `201`

Save the returned `id` as `<REVIEW_ID>`.

### 3.15 List all reviews

```bash
curl -i "http://127.0.0.1:5000/api/v1/reviews/"
```

Expected status: `200`

### 3.16 Get a review by id

```bash
curl -i "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"
```

Expected status: `200`

### 3.17 Update a review

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Amazing stay!","rating":4,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

Expected status: `200`

### 3.18 Delete a review

```bash
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"
```

Expected status: `200`

### 3.19 Confirm the review is deleted

```bash
curl -i "http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>"
```

Expected status: `404`

## 4. Negative Test Commands

Use these to verify validation and error handling.

### 4.1 Duplicate user email

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"johnny.doe@example.com"}'
```

Expected status: `400`

Note: this command assumes you already ran the user update step above. If you test it before updating the user, use the original email instead.

### 4.2 Invalid user email format

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Bad","last_name":"Email","email":"not-an-email"}'
```

Expected status: `400`

### 4.3 Empty amenity name

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":""}'
```

Expected status: `400`

### 4.4 Invalid place latitude

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bad Lat","description":"","price":50.0,"latitude":999.0,"longitude":0.0,"owner_id":"<USER_ID>","amenities":[]}'
```

Expected status: `400`

### 4.5 Invalid place longitude

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bad Lon","description":"","price":50.0,"latitude":0.0,"longitude":999.0,"owner_id":"<USER_ID>","amenities":[]}'
```

Expected status: `400`

### 4.6 Invalid place owner

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Ghost Place","description":"","price":50.0,"latitude":0.0,"longitude":0.0,"owner_id":"fake-user-id","amenities":[]}'
```

Expected status: `404`

### 4.7 Invalid review rating

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text":"Bad rating","rating":6,"user_id":"<USER_ID>","place_id":"<PLACE_ID>"}'
```

Expected status: `400`

### 4.8 Invalid review user

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text":"Ghost user","rating":3,"user_id":"fake-user-id","place_id":"<PLACE_ID>"}'
```

Expected status: `404`

### 4.9 Invalid review place

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text":"Ghost place","rating":3,"user_id":"<USER_ID>","place_id":"fake-place-id"}'
```

Expected status: `404`

## 5. Automated Tests

Run the unit tests from the same virtual environment:

```bash
python tests.py
```

Or run them with verbose output:

```bash
python -m unittest -v tests.py
```

## 6. Quick Expected Status Summary

- Users: `POST 201`, `GET 200`, `PUT 200`, invalid lookup `404`
- Amenities: `POST 201`, `GET 200`, `PUT 200`, invalid lookup `404`
- Places: `POST 201`, `GET 200`, `PUT 200`, invalid lookup `404`
- Reviews: `POST 201`, `GET 200`, `PUT 200`, `DELETE 200`, invalid lookup `404`
