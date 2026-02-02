"""Base settings shared by dev/prod.

This file contains the *production-minded defaults* and is overridden
by dev.py or prod.py when needed.
"""

from pathlib import Path
import environ
from datetime import timedelta

# BASE_DIR points to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ lets us define types and read environment variables safely
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

# In dev/docker we typically keep a .env file in the project root.
# In real production, environment variables are injected by the platform.
environ.Env.read_env(BASE_DIR / ".env")

# Core Django settings
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", default="").split(",") if h.strip()]

# Apps: Django + DRF + JWT + Channels + our own apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    # Token blacklist app is used by SimpleJWT when rotating refresh tokens
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "channels",

    "apps.accounts",
    "apps.movies",
    "apps.realtime",
]

# Middleware ordering matters.
# SecurityMiddleware should be early; CORS should be before CommonMiddleware.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise allows serving static files (CSS/JS) without extra infra
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "movielibrary.urls"

# Templates aren't central here, but admin uses them.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Both WSGI + ASGI present; prefer ASGI for Channels
WSGI_APPLICATION = "movielibrary.wsgi.application"
ASGI_APPLICATION = "movielibrary.asgi.application"

# Database
# DATABASE_URL example: postgres://user:pass@host:5432/dbname
DATABASES = {
    "default": env.db("DATABASE_URL")
}

# Custom user model: email is the login identifier
AUTH_USER_MODEL = "accounts.User"

# Password validation (production sensible defaults)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static assets
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF defaults:
# - JWT auth everywhere by default
# - endpoints are protected unless explicitly made public
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

# JWT tuning:
# - short access tokens
# - refresh rotation with blacklisting (safer for production)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# CORS is optional (only set if env var provided)
cors_origins = [o.strip() for o in env("CORS_ALLOWED_ORIGINS", default="").split(",") if o.strip()]
if cors_origins:
    CORS_ALLOWED_ORIGINS = cors_origins

# Channels + Redis:
# - Channel layer used for WebSocket groups and broadcasts
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL]},
    }
}

# Cache:
# - we reuse Redis to cache RapidAPI responses and reduce rate limits
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# RapidAPI settings
RAPIDAPI_KEY = env("RAPIDAPI_KEY", default="")
RAPIDAPI_MOVIE_HOST = env("RAPIDAPI_MOVIE_HOST", default="online-movie-database.p.rapidapi.com")
RAPIDAPI_STREAMING_HOST = env("RAPIDAPI_STREAMING_HOST", default="streaming-availability.p.rapidapi.com")
