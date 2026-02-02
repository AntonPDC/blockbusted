"""ASGI entrypoint.

Why ASGI?
- DRF works over HTTP as usual
- Channels adds WebSocket support, and that requires ASGI
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

from apps.realtime.routing import websocket_urlpatterns

# Default to dev settings; production entrypoints set DJANGO_SETTINGS_MODULE explicitly.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movielibrary.settings.dev")

# Standard Django ASGI app (HTTP)
django_asgi_app = get_asgi_application()

# Protocol router routes by protocol type: HTTP vs WebSocket
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        # AuthMiddlewareStack provides user resolution in scope (session/cookies).
        # With JWT, you typically authenticate WS with a token querystring/header;
        # we keep this simple and broadcast-only for now.
        URLRouter(websocket_urlpatterns)
    ),
})
