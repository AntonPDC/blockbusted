"""Project URL router.

We keep a clean split:
- `/` => optional landing page (verifies CSS + static pipeline)
- `/admin/` => Django admin
- `/api/...` => REST API endpoints
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("apps.pages.urls")),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/movies/", include("apps.movies.urls")),
]
