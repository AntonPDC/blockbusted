"""RapidAPI integration layer.

Views should not contain HTTP calls directly. Keeping external calls here:
- isolates rate-limit/caching concerns
- improves testability (mock this module)
- prevents views from becoming unmaintainable

NOTE: This uses Django's default cache backend. If you do not configure Redis,
Django will fall back to local-memory caching per-process (still useful in dev).
"""

import requests
from django.conf import settings
from django.core.cache import cache

# RapidAPI endpoints used by your earlier project
MOVIE_OVERVIEW_URL = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"
MOVIE_DETAILS_URL = "https://online-movie-database.p.rapidapi.com/title/get-details"
POPULAR_URL = "https://online-movie-database.p.rapidapi.com/title/get-most-popular-movies"
SEARCH_URL = "https://online-movie-database.p.rapidapi.com/title/v2/find/"

def _headers() -> dict:
    """Build RapidAPI headers.

We raise a clear error if RAPIDAPI_KEY is missing instead of silently failing.
"""
    if not settings.RAPIDAPI_KEY:
        raise RuntimeError("Missing RAPIDAPI_KEY")

    return {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_MOVIE_HOST,
        "content-type": "application/json",
    }

def get_movie_overview(tconst: str) -> dict:
    """Fetch a movie overview, cached for 1 hour."""
    key = f"movie_overview:{tconst}"
    cached = cache.get(key)
    if cached:
        return cached

    r = requests.get(
        MOVIE_OVERVIEW_URL,
        headers=_headers(),
        params={"tconst": tconst, "r": "json"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    cache.set(key, data, timeout=60 * 60)
    return data

def get_movie_details(tconst: str) -> dict:
    """Fetch movie details, cached for 1 hour."""
    key = f"movie_details:{tconst}"
    cached = cache.get(key)
    if cached:
        return cached

    r = requests.get(
        MOVIE_DETAILS_URL,
        headers=_headers(),
        params={"tconst": tconst, "r": "json"},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    cache.set(key, data, timeout=60 * 60)
    return data

def get_popular(limit: int = 15) -> list[dict]:
    """Return a list of 'popular' movies.

RapidAPI returns a list of title URIs, e.g. "/title/tt0133093/".
We transform each into tconst and fetch details.

We cache results for 10 minutes to reduce rate limiting.
"""
    key = f"popular:{limit}"
    cached = cache.get(key)
    if cached:
        return cached

    r = requests.get(
        POPULAR_URL,
        headers=_headers(),
        params={"currentCountry": "US", "purchaseCountry": "US", "homeCountry": "US"},
        timeout=10,
    )
    r.raise_for_status()

    ids = r.json()[:limit]
    results: list[dict] = []

    for item in ids:
        # item is like "/title/tt0133093/" -> slice out tt0133093
        tconst = item[7:17]
        try:
            results.append(get_movie_details(tconst))
        except Exception:
            # Defensive: don't fail the entire endpoint if a single movie fetch breaks
            continue

    cache.set(key, results, timeout=10 * 60)
    return results

def search_movies(title: str, limit: int = 15) -> list[dict]:
    """Search movies by title, cached 10 minutes."""
    key = f"search:{title}:{limit}"
    cached = cache.get(key)
    if cached:
        return cached

    r = requests.get(
        SEARCH_URL,
        headers=_headers(),
        params={"title": title, "limit": str(limit), "r": "json"},
        timeout=10,
    )
    r.raise_for_status()

    data = r.json().get("results", [])
    cache.set(key, data, timeout=10 * 60)
    return data
