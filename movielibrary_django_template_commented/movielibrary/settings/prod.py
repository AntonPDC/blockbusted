"""Production overrides.

You still need to set DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS properly.
These values are reasonable defaults but must be validated for your hosting setup.
"""

from .base import *  # noqa

DEBUG = False

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS: enable once you're sure HTTPS is stable
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
