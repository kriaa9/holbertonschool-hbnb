PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$afBoMwPjFkh85IIrm5LnpO41GtpQ44xZ8Ob1bfgncw26UdtgxavCy',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO amenities (id, name, created_at, updated_at) VALUES
    ('8fb3b623-4f45-4ef6-9623-dca7c8cdb61c', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('64cacda9-d0de-41e1-9b3b-ca98b27c1e74', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b5d29e1c-639b-408e-8ce7-c132dd917760', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
