"""WSGI entrypoint.

We keep this because many platforms still expect WSGI, but note:
- WebSockets require ASGI
- In production you should serve ASGI (daphne/uvicorn) for Channels

WSGI is still useful for management commands and some deployments.
"""

import os
from django.core.wsgi import get_wsgi_application

# In production, set this in environment rather than hardcoding.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movielibrary.settings.prod")

application = get_wsgi_application()
