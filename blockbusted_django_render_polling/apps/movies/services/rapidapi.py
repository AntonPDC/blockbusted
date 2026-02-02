import requests
from django.conf import settings
from django.core.cache import cache

MOVIE_OVERVIEW_URL = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"
MOVIE_DETAILS_URL = "https://online-movie-database.p.rapidapi.com/title/get-details"
POPULAR_URL = "https://online-movie-database.p.rapidapi.com/title/get-most-popular-movies"
SEARCH_URL = "https://online-movie-database.p.rapidapi.com/title/v2/find/"

def _headers() -> dict:
    if not settings.RAPIDAPI_KEY:
        raise RuntimeError("Missing RAPIDAPI_KEY")
    return {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.RAPIDAPI_MOVIE_HOST,
        "content-type": "application/json",
    }

def get_movie_overview(tconst: str) -> dict:
    key = f"movie_overview:{tconst}"
    cached = cache.get(key)
    if cached:
        return cached
    r = requests.get(MOVIE_OVERVIEW_URL, headers=_headers(), params={"tconst": tconst, "r": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    cache.set(key, data, timeout=60 * 60)
    return data

def get_movie_details(tconst: str) -> dict:
    key = f"movie_details:{tconst}"
    cached = cache.get(key)
    if cached:
        return cached
    r = requests.get(MOVIE_DETAILS_URL, headers=_headers(), params={"tconst": tconst, "r": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json()
    cache.set(key, data, timeout=60 * 60)
    return data

def get_popular(limit: int = 15) -> list[dict]:
    key = f"popular:{limit}"
    cached = cache.get(key)
    if cached:
        return cached
    r = requests.get(POPULAR_URL, headers=_headers(), params={"currentCountry": "US", "purchaseCountry": "US", "homeCountry": "US"}, timeout=10)
    r.raise_for_status()
    ids = r.json()[:limit]
    results = []
    for item in ids:
        tconst = item[7:17]
        try:
            results.append(get_movie_details(tconst))
        except Exception:
            continue
    cache.set(key, results, timeout=10 * 60)
    return results

def search_movies(title: str, limit: int = 15) -> list[dict]:
    key = f"search:{title}:{limit}"
    cached = cache.get(key)
    if cached:
        return cached
    r = requests.get(SEARCH_URL, headers=_headers(), params={"title": title, "limit": str(limit), "r": "json"}, timeout=10)
    r.raise_for_status()
    data = r.json().get("results", [])
    cache.set(key, data, timeout=10 * 60)
    return data
