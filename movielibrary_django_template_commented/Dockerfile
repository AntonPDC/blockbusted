# Minimal production-ish image for ASGI + Django + Channels
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# psycopg needs build deps; libpq-dev provides postgres headers
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Daphne serves the ASGI application (HTTP + WebSockets)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "movielibrary.asgi:application"]
