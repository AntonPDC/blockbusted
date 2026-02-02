"""DRF serializers for movie and watchlist endpoints."""

from rest_framework import serializers
from .models import Movie, WatchlistItem

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("tconst", "title", "image_url")

class WatchlistItemSerializer(serializers.ModelSerializer):
    # nested serializer gives clients movie details inline
    movie = MovieSerializer()

    class Meta:
        model = WatchlistItem
        fields = ("id", "movie", "created_at")

class WatchlistAddSerializer(serializers.Serializer):
    # tconst comes from the client (front-end)
    tconst = serializers.CharField(max_length=16)
