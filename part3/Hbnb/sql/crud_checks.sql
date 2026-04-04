PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

-- CREATE test rows
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES ('44444444-4444-4444-4444-444444444444', 'SQL Test Amenity', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'SQL',
    'Tester',
    'sql.tester@hbnb.io',
    '$2b$12$afBoMwPjFkh85IIrm5LnpO41GtpQ44xZ8Ob1bfgncw26UdtgxavCy',
    0,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'SQL Test Place',
    'Created by SQL test script',
    99.99,
    12.34,
    56.78,
    '11111111-1111-1111-1111-111111111111',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444');

INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES (
    '33333333-3333-3333-3333-333333333333',
    'SQL script review',
    5,
    '11111111-1111-1111-1111-111111111111',
    '22222222-2222-2222-2222-222222222222',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- READ checks
SELECT 'users_count_after_insert' AS check_name, COUNT(*) AS value
FROM users WHERE id = '11111111-1111-1111-1111-111111111111';

SELECT 'places_count_after_insert' AS check_name, COUNT(*) AS value
FROM places WHERE id = '22222222-2222-2222-2222-222222222222';

SELECT 'reviews_count_after_insert' AS check_name, COUNT(*) AS value
FROM reviews WHERE id = '33333333-3333-3333-3333-333333333333';

SELECT 'place_amenity_count_after_insert' AS check_name, COUNT(*) AS value
FROM place_amenity
WHERE place_id = '22222222-2222-2222-2222-222222222222'
  AND amenity_id = '44444444-4444-4444-4444-444444444444';

-- UPDATE checks
UPDATE users SET first_name = 'SQLUpdated', updated_at = CURRENT_TIMESTAMP
WHERE id = '11111111-1111-1111-1111-111111111111';

UPDATE places SET price = 120.00, updated_at = CURRENT_TIMESTAMP
WHERE id = '22222222-2222-2222-2222-222222222222';

UPDATE reviews SET rating = 4, updated_at = CURRENT_TIMESTAMP
WHERE id = '33333333-3333-3333-3333-333333333333';

UPDATE amenities SET name = 'SQL Test Amenity Updated', updated_at = CURRENT_TIMESTAMP
WHERE id = '44444444-4444-4444-4444-444444444444';

SELECT 'updated_user_first_name' AS check_name, first_name AS value
FROM users WHERE id = '11111111-1111-1111-1111-111111111111';

SELECT 'updated_place_price' AS check_name, CAST(price AS TEXT) AS value
FROM places WHERE id = '22222222-2222-2222-2222-222222222222';

SELECT 'updated_review_rating' AS check_name, CAST(rating AS TEXT) AS value
FROM reviews WHERE id = '33333333-3333-3333-3333-333333333333';

SELECT 'updated_amenity_name' AS check_name, name AS value
FROM amenities WHERE id = '44444444-4444-4444-4444-444444444444';

-- DELETE checks
DELETE FROM reviews WHERE id = '33333333-3333-3333-3333-333333333333';
DELETE FROM place_amenity
WHERE place_id = '22222222-2222-2222-2222-222222222222'
  AND amenity_id = '44444444-4444-4444-4444-444444444444';
DELETE FROM places WHERE id = '22222222-2222-2222-2222-222222222222';
DELETE FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
DELETE FROM amenities WHERE id = '44444444-4444-4444-4444-444444444444';

SELECT 'users_count_after_delete' AS check_name, COUNT(*) AS value
FROM users WHERE id = '11111111-1111-1111-1111-111111111111';

SELECT 'places_count_after_delete' AS check_name, COUNT(*) AS value
FROM places WHERE id = '22222222-2222-2222-2222-222222222222';

SELECT 'reviews_count_after_delete' AS check_name, COUNT(*) AS value
FROM reviews WHERE id = '33333333-3333-3333-3333-333333333333';

SELECT 'amenities_count_after_delete' AS check_name, COUNT(*) AS value
FROM amenities WHERE id = '44444444-4444-4444-4444-444444444444';

ROLLBACK;
