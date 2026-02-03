# Blockbusted (Django + DRF + SimpleJWT) — Render + Polling (Commented)

This is the **commented** (easy-to-follow) edition of the Render-friendly Django backend.

## Why "polling edition"?
You said WebSockets aren't required. Removing Channels/Redis means:
- easier deployment
- fewer moving parts
- compatible with Render free-tier constraints

Your frontend can simply poll:
- `GET /api/movies/watchlist/` every 10–30 seconds (or on focus)
- `GET /api/movies/popular/` occasionally if needed

## How CSS is wired
Your provided CSS is copied into `static/css/` and loaded in `templates/base.html` via:
`{% load static %}` + `<link rel="stylesheet" href="{% static 'css/...' %}">`

## Local run
1. Create venv and install deps:
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. Create `.env`:
   - `cp .env.example .env`
   - set `DJANGO_SECRET_KEY` and `DATABASE_URL` (localhost for local dev)

3. Migrate + run:
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
   - `python manage.py runserver`

## Render deploy
This repo includes `render.yaml`.
Push to GitHub, connect repo in Render, deploy.
