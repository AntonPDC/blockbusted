"""Main URL router for the project.

We mount each app under /api/... for clean, versionable APIs.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/movies/", include("apps.movies.urls")),
    path("api/realtime/", include("apps.realtime.urls")),
]
