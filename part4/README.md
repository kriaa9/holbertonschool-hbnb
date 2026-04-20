# HBnB Part 4 - Run Guide (Backend + Frontend)

This guide explains how to run the backend and frontend locally, then log in with seeded credentials.

## 1) Start the backend API (Terminal 1)

```bash
cd /home/abdal/holbertonschool-hbnb/part3/Hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Backend URLs:

- API base: http://127.0.0.1:5000/api/v1
- API docs (Swagger): http://127.0.0.1:5000/api/v1/

## 2) Start the frontend (Terminal 2)

```bash
cd /home/abdal/holbertonschool-hbnb/part4
python3 -m http.server 5500
```

Frontend URLs:

- Home: http://localhost:5500/index.html
- Login: http://localhost:5500/login.html

## 3) Login data

Use this seeded account:

- Email: admin@hbnb.io
- Password: admin1234
- Role: Admin
- Seed source: part3/Hbnb/app/__init__.py (seed_database)

## 4) Optional: login test with curl

```bash
curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}'
```

Expected: JSON with access_token.

## 5) If login fails (reset local dev DB)

If your local DB already has different data, reset and let the app reseed the admin user:

```bash
cd /home/abdal/holbertonschool-hbnb
rm -f part3/Hbnb/instance/development.db part3/Hbnb/development.db
```

Then start the backend again using step 1.

## 6) Stop servers

Press Ctrl+C in each terminal.
