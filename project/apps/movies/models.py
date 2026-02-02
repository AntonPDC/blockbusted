"""Movies domain models.

We normalize watchlist in a relational way:
- Movie: unique by tconst
- WatchlistItem: many-to-many via explicit table (lets us store created_at)
"""

from django.conf import settings
from django.db import models

class Movie(models.Model):
    # tconst values look like "tt1234567" and are stable IDs
    tconst = models.CharField(max_length=16, unique=True, db_index=True)

    # Optional cached metadata. We keep these optional because RapidAPI calls can fail.
    title = models.CharField(max_length=255, blank=True, default="")
    image_url = models.URLField(blank=True, default="")

    def __str__(self):
        return self.tconst

class WatchlistItem(models.Model):
    # Using ForeignKey relations gives strong integrity and easy query optimization.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicates: a user can only watchlist the same movie once
        unique_together = ("user", "movie")
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]
