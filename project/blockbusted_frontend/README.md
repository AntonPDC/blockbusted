# Blockbusted Frontend (React + Vite)

This frontend talks to your Django backend and uses polling (no websockets).

## Setup
1) Install dependencies:
   npm install

2) Create .env
   cp .env.example .env
   # Ensure VITE_API_BASE_URL points to Django, e.g. http://127.0.0.1:8000

3) Run:
   npm run dev

Open: http://localhost:3000

## Auth
- Login stores JWT access/refresh in localStorage:
  - access_token
  - refresh_token

## Endpoints expected
- POST /api/accounts/register/
- POST /api/accounts/token/
- GET  /api/movies/popular/?limit=15
- GET  /api/movies/search/?title=matrix&limit=15
- GET  /api/movies/watchlist/           (auth)
- POST /api/movies/watchlist/           (auth) { tconst }
- DELETE /api/movies/watchlist/<tconst>/ (auth)
