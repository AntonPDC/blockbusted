"""Movie/watchlist schema.

We normalize watchlist storage:
- Movie: one row per tconst (cached title + image URL optional)
- WatchlistItem: joins user and movie; prevents duplicates

This is easier to query and safer than storing raw lists inside user docs.
"""

from django.conf import settings
from django.db import models

class Movie(models.Model):
    # IMDb IDs are stable strings like "tt0133093"
    tconst = models.CharField(max_length=16, unique=True, db_index=True)

    # Optional cached fields; RapidAPI may fail, so keep them nullable-ish
    title = models.CharField(max_length=255, blank=True, default="")
    image_url = models.URLField(blank=True, default="")

    def __str__(self):
        return self.tconst

class WatchlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a user from adding the same movie twice
        unique_together = ("user", "movie")
        indexes = [
            # Index helps with watchlist listing sorted by created_at
            models.Index(fields=["user", "created_at"]),
        ]
