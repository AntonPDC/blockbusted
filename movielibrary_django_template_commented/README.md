# Movie Library API (Django + DRF + SimpleJWT + Channels) — Commented Edition

This project is a production-oriented Django rewrite of your earlier FastAPI/Mongo version:
- **Accounts**: custom User model that logs in by email
- **Auth**: JWT via SimpleJWT (with refresh rotation + blacklist enabled)
- **Movies**: watchlist stored relationally (User ⇄ Movie), with optional cached title/poster
- **Realtime**: WebSocket broadcast ("refetch movies") via Django Channels + Redis

The code is intentionally **heavily commented** so it’s easy to follow.

## Quick start (dev)
1) Create a venv and install deps:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`

2) Copy env file:
   - `cp .env.example .env` and fill values

3) Run migrations:
   - `python manage.py migrate`

4) Create an admin user:
   - `python manage.py createsuperuser`

5) Run server:
   - `python manage.py runserver`

## Endpoints
- `POST /api/accounts/register/` (create account)
- `POST /api/accounts/token/` (JWT login)
- `POST /api/accounts/token/refresh/`
- `GET  /api/accounts/me/`
- `GET  /api/movies/watchlist/`
- `POST /api/movies/watchlist/`  body: `{ "tconst": "tt1234567" }`
- `DELETE /api/movies/watchlist/<tconst>/`
- `GET /api/movies/popular/?limit=15`
- `GET /api/movies/search/?title=matrix&limit=15`

## WebSockets
- Connect to `ws://localhost:8000/ws/movies/`
- Trigger broadcast (admin only):
  - `POST /api/realtime/refetch/`

## Deployment notes (high level)
- This is ASGI (because Channels). Use **Daphne**/Uvicorn behind a reverse proxy (Nginx).
- Use Postgres in production. Redis is required for Channels layers (and caching here).
