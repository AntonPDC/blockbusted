"""Realtime URL routes."""

from django.urls import path
from .views import RefetchBroadcastView

urlpatterns = [
    path("refetch/", RefetchBroadcastView.as_view(), name="refetch_broadcast"),
]
