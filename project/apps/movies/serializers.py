"""Serializers for Movies + Watchlist."""

from rest_framework import serializers
from .models import Movie, WatchlistItem

class MovieSerializer(serializers.ModelSerializer):
    """Shape Movie model into JSON."""
    class Meta:
        model = Movie
        fields = ("tconst", "title", "image_url")

class WatchlistItemSerializer(serializers.ModelSerializer):
    """Returns a watchlist item with nested movie details."""
    movie = MovieSerializer()

    class Meta:
        model = WatchlistItem
        fields = ("id", "movie", "created_at")

class WatchlistAddSerializer(serializers.Serializer):
    """Validates POST /watchlist/ payload."""
    tconst = serializers.CharField(max_length=16)
