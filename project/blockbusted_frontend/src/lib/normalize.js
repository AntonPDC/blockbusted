// Normalize the different shapes returned by RapidAPI / your Django serializers
// into one viewer-friendly object used by the UI.

export function normalizeMovie(raw) {
  const tconst =
    raw?.tconst ||
    raw?.movie?.tconst ||
    (typeof raw?.id === "string" ? (raw.id.match(/tt\d{6,10}/)?.[0] || "") : "");

  const title = raw?.title || raw?.movie?.title || "";
  const year = raw?.year ?? raw?.movie?.year ?? null;

  const title_type =
    raw?.title_type || raw?.titleType || raw?.movie?.title_type || "";

  const runtime_minutes =
    raw?.runtime_minutes ?? raw?.runningTimeInMinutes ?? null;

  const image_url =
    raw?.image_url ||
    raw?.poster_url ||
    raw?.movie?.image_url ||
    raw?.movie?.poster_url ||
    raw?.image?.url ||
    raw?.title?.image?.url ||
    "";

  const imdb_url =
    raw?.imdb_url || (tconst ? `https://www.imdb.com/title/${tconst}/` : "");

  return { tconst, title, year, title_type, runtime_minutes, image_url, imdb_url };
}
