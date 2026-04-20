# HBnB API - Manual Test Report

This document records a live manual test run of the Part 2 API in `part2/hbnb`.

## Environment

- Project: HBnB Part 2
- API framework: Flask + Flask-RESTx
- Storage: in-memory repository
- Base URL: `http://127.0.0.1:5000/api/v1`
- Swagger UI: `http://127.0.0.1:5000/api/v1/`

## Test Run Summary

All main CRUD endpoints were executed against the running API and returned the expected status codes.

The manual run included:

- User creation, listing, retrieval, and update
- Amenity creation, listing, retrieval, and update
- Place creation, listing, retrieval, update, and place reviews listing
- Review creation, listing, retrieval, update, and deletion
- Validation and not-found checks for negative cases

## Happy Path Results

### Users

- `POST /users/` returned `201`
- `GET /users/` returned `200`
- `GET /users/<USER_ID>` returned `200`
- `PUT /users/<USER_ID>` returned `200`

Observed user ID:

- `60f162e7-abbe-4c4c-8a4b-9686e993f4a7`

### Amenities

- `POST /amenities/` returned `201`
- `GET /amenities/` returned `200`
- `GET /amenities/<AMENITY_ID>` returned `200`
- `PUT /amenities/<AMENITY_ID>` returned `200`

Observed amenity ID:

- `02960150-a465-4512-92bc-fa723c68c563`

### Places

- `POST /places/` returned `201`
- `GET /places/` returned `200`
- `GET /places/<PLACE_ID>` returned `200`
- `PUT /places/<PLACE_ID>` returned `200`
- `GET /places/<PLACE_ID>/reviews` returned `200`

Observed place ID:

- `5a294fca-0f50-410d-91b5-ea039bdd773e`

### Reviews

- `POST /reviews/` returned `201`
- `GET /reviews/` returned `200`
- `GET /reviews/<REVIEW_ID>` returned `200`
- `PUT /reviews/<REVIEW_ID>` returned `200`
- `DELETE /reviews/<REVIEW_ID>` returned `200`
- `GET /reviews/<REVIEW_ID>` after deletion returned `404`

Observed review ID:

- `72cdb351-2061-4982-a08c-5b39cccc1082`

## Negative Test Results

The following checks were executed manually and returned the expected errors.

| Test | Request | Result |
|---|---|---|
| Duplicate user email | `POST /users/` with existing email | `400` |
| Invalid user email format | `POST /users/` with `not-an-email` | `400` |
| Empty amenity name | `POST /amenities/` with empty name | `400` |
| Invalid place latitude | `POST /places/` with latitude `999.0` | `400` |
| Invalid place longitude | `POST /places/` with longitude `999.0` | `400` |
| Invalid place owner | `POST /places/` with fake owner ID | `404` |
| Invalid review rating | `POST /reviews/` with rating `6` | `400` |
| Invalid review user | `POST /reviews/` with fake user ID | `404` |
| Invalid review place | `POST /reviews/` with fake place ID | `404` |

Observed negative-case payloads included:

- `{"error": "Email already registered"}` for duplicate email
- `{"error": "email must follow a valid format (e.g. user@example.com)"}` for invalid email format
- `{"error": "Invalid input data"}` for empty amenity name
- `{"error": "latitude must be a float between -90.0 and 90.0"}` for invalid latitude
- `{"error": "longitude must be a float between -180.0 and 180.0"}` for invalid longitude
- `{"error": "Owner not found"}` for an invalid place owner
- `{"error": "rating must be an integer between 1 and 5"}` for invalid review rating
- `{"error": "User not found"}` for an invalid review user
- `{"error": "Place not found"}` for an invalid review place

## Important Note

The duplicate-email check is sequence-dependent in a manual session. In the live run, the user was first updated from `john.doe@example.com` to `johnny.doe@example.com`, and the duplicate-email test was then executed using `johnny.doe@example.com`. If you run that negative test before the update step, use the original email value instead.

## Automated Validation

The provided unit suite also passed in a virtual environment:

```bash
python -m unittest -v tests.py
```

Result:

- `41` tests run
- `41` tests passed

## Conclusion

The Part 2 API is functioning correctly for the documented manual flow. CRUD operations, nested place serialization, review handling, and validation failures all behaved as expected during direct execution.
