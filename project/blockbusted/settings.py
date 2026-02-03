"""Project settings (Render + Polling edition).

Key points:
- **WSGI** only (no Channels), so you can run with gunicorn.
- Uses `DATABASE_URL` so Render can inject Postgres connection settings.
- Uses WhiteNoise for static assets so Render can serve your CSS on free tier.
- Uses DRF + SimpleJWT for JWT auth.
"""

from pathlib import Path
import environ
from datetime import timedelta

# BASE_DIR is the root folder containing manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Read environment variables with type casting
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)

# In local dev, read .env if present. In Render, env vars are injected by platform.
environ.Env.read_env(BASE_DIR / ".env")

# --- Core Django ---
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")

# Render sets a single hostname; locally you may add localhost/127.0.0.1
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", default="").split(",") if h.strip()]

# --- Installed apps ---
# Django core apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # API stack
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",  # needed for refresh rotation blacklisting
    "corsheaders",

    # Our apps
    "apps.accounts",
    "apps.movies",
    "apps.pages",  # simple landing page so you can verify CSS wiring quickly
]

# --- Middleware ---
# Ordering matters:
# - CORS should be early so it can add headers to responses
# - Security + WhiteNoise early
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blockbusted.urls"

# --- Templates (for the optional landing page) ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Root-level templates folder
        "DIRS": [BASE_DIR / "templates"],
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

# --- WSGI entrypoint (gunicorn uses this) ---
WSGI_APPLICATION = "blockbusted.wsgi.application"

# --- Database ---
# DATABASE_URL examples:
#   postgres://user:pass@localhost:5432/dbname
#   (Render will set this for you)
DATABASES = {"default": env.db("DATABASE_URL")}

# --- Custom User model ---
# We use email-based login, so we define a custom User model
AUTH_USER_MODEL = "accounts.User"

# --- Password validators (reasonable defaults) ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---
# Your CSS lives in /static/css. WhiteNoise serves it in production after collectstatic.
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage pipeline:
# - compressed files
# - hashed filenames (cache-friendly)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF defaults ---
REST_FRAMEWORK = {
    # JWT for API authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Require auth by default, but allow read-only for public endpoints
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

# --- SimpleJWT config ---
# Rotation + blacklist is safer for refresh tokens in production.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# --- CORS (optional) ---
cors_origins = [o.strip() for o in env("CORS_ALLOWED_ORIGINS", default="").split(",") if o.strip()]
if cors_origins:
    CORS_ALLOWED_ORIGINS = cors_origins

# --- RapidAPI settings ---
RAPIDAPI_KEY = env("RAPIDAPI_KEY", default="")
RAPIDAPI_MOVIE_HOST = env("RAPIDAPI_MOVIE_HOST", default="online-movie-database.p.rapidapi.com")
STREAMING_AVAILABILITY_HOST = env(
    "STREAMING_AVAILABILITY_HOST",
    default="streaming-availability.p.rapidapi.com"
).strip()

# Usually the same RapidAPI key you already use for movie data:
STREAMING_AVAILABILITY_KEY = env("STREAMING_AVAILABILITY_KEY", default=env("RAPIDAPI_KEY", default="")).strip()
