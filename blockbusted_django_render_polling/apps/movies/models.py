from django.conf import settings
from django.db import models

class Movie(models.Model):
    tconst = models.CharField(max_length=16, unique=True, db_index=True)
    title = models.CharField(max_length=255, blank=True, default="")
    image_url = models.URLField(blank=True, default="")

class WatchlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
        indexes = [models.Index(fields=["user", "created_at"])]
