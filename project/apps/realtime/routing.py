"""WebSocket URL patterns used by ASGI application."""

from django.urls import re_path
from .consumers import MoviesConsumer

websocket_urlpatterns = [
    re_path(r"^ws/movies/$", MoviesConsumer.as_asgi()),
]
