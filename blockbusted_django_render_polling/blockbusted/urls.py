from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("apps.pages.urls")),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/movies/", include("apps.movies.urls")),
]
