from rest_framework import serializers
from .models import Movie, WatchlistItem

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("tconst", "title", "image_url")

class WatchlistItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    class Meta:
        model = WatchlistItem
        fields = ("id", "movie", "created_at")

class WatchlistAddSerializer(serializers.Serializer):
    tconst = serializers.CharField(max_length=16)
