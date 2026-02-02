"""RapidAPI service module.

All external API calls live here so:
- views remain thin (controller layer)
- testability improves (mock this module in unit tests)
- caching can be centralized
"""

import requests
from django.conf import settings
from django.core.cache import cache

# RapidAPI endpoints used by your earlier project
MOVIE_OVERVIEW_URL = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"
MOVIE_DETAILS_URL = "https://online-movie-database.p.rapidapi.com/title/get-details"
POPULAR_URL = "https://online-movie-database.p.rapidapi.com/title/get-most-popular-movies"
SEARCH_URL = "https://online-movie-database.p.rapidapi.com/title/v2/find/"

def _headers(host: str) -> dict:
    """Build headers required by RapidAPI.

Raises a clear error if RAPIDAPI_KEY is missing. This is preferable to crashing at import time.
"""
    if not settings.RAPIDAPI_KEY:
        raise RuntimeError("Missing RAPIDAPI_KEY")
    return {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": host,
        "content-type": "application/json",
    }

def get_movie_overview(tconst: str) -> dict:
    """Fetch overview details and cache the result."""
    cache_key = f"movie_overview:{tconst}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    r = requests.get(
        MOVIE_OVERVIEW_URL,
        headers=_headers(settings.RAPIDAPI_MOVIE_HOST),
        params={"tconst": tconst, "r": "json"},
        timeout=10,
    )
    r.raise_for_status()

    data = r.json()
    cache.set(cache_key, data, timeout=60 * 60)  # 1 hour
    return data

def get_movie_details(tconst: str) -> dict:
    """Fetch full details and cache the result."""
    cache_key = f"movie_details:{tconst}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    r = requests.get(
        MOVIE_DETAILS_URL,
        headers=_headers(settings.RAPIDAPI_MOVIE_HOST),
        params={"tconst": tconst, "r": "json"},
        timeout=10,
    )
    r.raise_for_status()

    data = r.json()
    cache.set(cache_key, data, timeout=60 * 60)
    return data

def get_popular(limit: int = 15) -> list[dict]:
    """Return the most popular movies list.

Note:
- RapidAPI returns a list of title URIs; we transform to tconst and fetch details.
- We swallow individual failures to avoid breaking the entire endpoint.
"""
    cache_key = f"popular:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    r = requests.get(
        POPULAR_URL,
        headers=_headers(settings.RAPIDAPI_MOVIE_HOST),
        params={"currentCountry": "US", "purchaseCountry": "US", "homeCountry": "US"},
        timeout=10,
    )
    r.raise_for_status()

    ids = r.json()[:limit]
    results = []

    for item in ids:
        # item format: "/title/tt1234567/"
        tconst = item[7:17]
        try:
            results.append(get_movie_details(tconst))
        except Exception:
            continue

    cache.set(cache_key, results, timeout=10 * 60)  # 10 minutes
    return results

def search_movies(title: str, limit: int = 15) -> list[dict]:
    """Search movies by title and cache results."""
    cache_key = f"search:{title}:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    r = requests.get(
        SEARCH_URL,
        headers=_headers(settings.RAPIDAPI_MOVIE_HOST),
        params={"title": title, "limit": str(limit), "r": "json"},
        timeout=10,
    )
    r.raise_for_status()

    data = r.json().get("results", [])
    cache.set(cache_key, data, timeout=10 * 60)
    return data
