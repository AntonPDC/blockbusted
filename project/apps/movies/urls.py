"""Movies routes."""

from django.urls import path
from .views import WatchlistListCreateView, WatchlistDeleteView, PopularView, SearchView

urlpatterns = [
    path("watchlist/", WatchlistListCreateView.as_view(), name="watchlist_list_create"),
    path("watchlist/<str:tconst>/", WatchlistDeleteView.as_view(), name="watchlist_delete"),
    path("popular/", PopularView.as_view(), name="popular"),
    path("search/", SearchView.as_view(), name="search"),
]
