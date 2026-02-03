"""WSGI entrypoint.

Gunicorn starts this and serves HTTP requests.
(WSGI is enough because we removed WebSockets.)
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blockbusted.settings")
application = get_wsgi_application()
