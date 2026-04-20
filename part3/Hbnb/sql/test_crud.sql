PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

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

SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;

UPDATE users SET first_name = 'SQLUpdated' WHERE id = '11111111-1111-1111-1111-111111111111';
UPDATE places SET price = 120.00 WHERE id = '22222222-2222-2222-2222-222222222222';
UPDATE reviews SET rating = 4 WHERE id = '33333333-3333-3333-3333-333333333333';
UPDATE amenities SET name = 'SQL Test Amenity Updated' WHERE id = '44444444-4444-4444-4444-444444444444';

DELETE FROM reviews WHERE id = '33333333-3333-3333-3333-333333333333';
DELETE FROM place_amenity WHERE place_id = '22222222-2222-2222-2222-222222222222';
DELETE FROM places WHERE id = '22222222-2222-2222-2222-222222222222';
DELETE FROM users WHERE id = '11111111-1111-1111-1111-111111111111';
DELETE FROM amenities WHERE id = '44444444-4444-4444-4444-444444444444';

ROLLBACK;
