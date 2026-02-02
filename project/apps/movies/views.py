"""Movies views.

Design goals:
- Keep views thin and predictable
- Validate input via serializers
- Use transactions where data integrity matters
- Populate cached movie fields best-effort (fail-safe)
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction

from .models import Movie, WatchlistItem
from .serializers import WatchlistItemSerializer, WatchlistAddSerializer
from .services.rapidapi import get_movie_overview, get_popular, search_movies

class WatchlistListCreateView(generics.GenericAPIView):
    """GET/POST /api/movies/watchlist/

    GET: list user's watchlist
    POST: add a tconst to watchlist
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # select_related pulls Movie rows efficiently (single query join)
        qs = (
            WatchlistItem.objects
            .select_related("movie")
            .filter(user=request.user)
            .order_by("-created_at")
        )
        return Response(WatchlistItemSerializer(qs, many=True).data)

    @transaction.atomic
    def post(self, request):
        # Validate payload
        ser = WatchlistAddSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        tconst = ser.validated_data["tconst"]

        # Create/find Movie record
        movie, _ = Movie.objects.get_or_create(tconst=tconst)

        # Populate cached metadata best-effort
        if not movie.title or not movie.image_url:
            try:
                overview = get_movie_overview(tconst) or {}
                title = ((overview.get("title") or {}).get("title")) or ""
                image_url = (((overview.get("title") or {}).get("image") or {}).get("url")) or ""
                if title or image_url:
                    movie.title = title
                    movie.image_url = image_url
                    movie.save(update_fields=["title", "image_url"])
            except Exception:
                # If RapidAPI fails, we still allow watchlist add
                pass

        # Enforce uniqueness via get_or_create
        WatchlistItem.objects.get_or_create(user=request.user, movie=movie)

        return Response({"message": "Added to watchlist"}, status=status.HTTP_201_CREATED)

class WatchlistDeleteView(generics.DestroyAPIView):
    """DELETE /api/movies/watchlist/<tconst>/

    Removes a movie from the authenticated user's watchlist.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "tconst"

    def delete(self, request, *args, **kwargs):
        tconst = kwargs.get("tconst")
        deleted, _ = WatchlistItem.objects.filter(user=request.user, movie__tconst=tconst).delete()
        return Response({"removed": bool(deleted)})

class PopularView(generics.GenericAPIView):
    """GET /api/movies/popular/?limit=15"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = int(request.query_params.get("limit", "15"))
        return Response(get_popular(limit=limit))

class SearchView(generics.GenericAPIView):
    """GET /api/movies/search/?title=<query>&limit=15"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        title = request.query_params.get("title", "")
        if not title:
            return Response({"detail": "title query param required"}, status=400)
        limit = int(request.query_params.get("limit", "15"))
        return Response(search_movies(title=title, limit=limit))
