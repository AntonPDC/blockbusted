"""Movies endpoints.

Design principles:
- Views stay thin (validate + orchestrate)
- External API calls live in services/
- Database writes in transactions
- Best-effort caching of Movie title/image; failures do not block watchlist ops
"""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from .services.rapidapi import get_popular, search_movies
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction

from .models import Movie, WatchlistItem
from .serializers import WatchlistItemSerializer, WatchlistAddSerializer
from .services.rapidapi import get_movie_overview, get_popular, search_movies

class WatchlistListCreateView(generics.GenericAPIView):
    """GET/POST /api/movies/watchlist/

    GET:
      - returns the authenticated user's watchlist
    POST:
      - adds a tconst to the authenticated user's watchlist
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # select_related pulls movie rows in the same query (efficient)
        qs = (
            WatchlistItem.objects
            .select_related("movie")
            .filter(user=request.user)
            .order_by("-created_at")
        )
        return Response(WatchlistItemSerializer(qs, many=True).data)

    @transaction.atomic
    def post(self, request):
        # Validate incoming JSON payload
        ser = WatchlistAddSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        tconst = ser.validated_data["tconst"]

        # Ensure Movie exists
        movie, _ = Movie.objects.get_or_create(tconst=tconst)

        # Populate cached metadata best-effort
        if not movie.title or not movie.image_url:
            try:
                overview = get_movie_overview(tconst) or {}

                # Defensive navigation of nested JSON
                title = ((overview.get("title") or {}).get("title")) or ""
                image_url = (((overview.get("title") or {}).get("image") or {}).get("url")) or ""

                if title or image_url:
                    movie.title = title
                    movie.image_url = image_url
                    movie.save(update_fields=["title", "image_url"])
            except Exception:
                # If RapidAPI fails, we still allow watchlist add
                pass

        # Enforce uniqueness through get_or_create
        WatchlistItem.objects.get_or_create(user=request.user, movie=movie)

        return Response({"message": "Added to watchlist"}, status=status.HTTP_201_CREATED)

class WatchlistDeleteView(generics.DestroyAPIView):
    """DELETE /api/movies/watchlist/<tconst>/"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        tconst = kwargs.get("tconst")
        deleted, _ = WatchlistItem.objects.filter(user=request.user, movie__tconst=tconst).delete()
        return Response({"removed": bool(deleted)})

class PopularView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = int(request.query_params.get("limit", "15"))
        return Response(get_popular(limit=limit))


class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        title = request.query_params.get("title", "")
        if not title:
            return Response({"detail": "title query param required"}, status=400)

        limit = int(request.query_params.get("limit", "15"))
        return Response(search_movies(title=title, limit=limit))
