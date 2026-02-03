import React from "react";

export default function MovieRow({ movie, mode, onAdd, onRemove }) {
  const poster = movie.image_url || "/placeholder-poster.png";

  return (
    <div className="bb-movie-row">
      <img
        className="bb-movie-poster"
        src={poster}
        alt={`${movie.title || "Movie"} poster`}
        loading="lazy"
      />

      <div className="bb-movie-details">
        <h3 className="bb-movie-title">{movie.title || "Untitled"}</h3>

        <div className="bb-movie-meta">
          <div className="bb-label">Year:</div>
          <div className="bb-value">{movie.year ?? "—"}</div>

          <div className="bb-label">Type:</div>
          <div className="bb-value">{movie.title_type || "—"}</div>

          <div className="bb-label">Runtime:</div>
          <div className="bb-value">
            {movie.runtime_minutes ? `${movie.runtime_minutes} min` : "—"}
          </div>

          <div className="bb-label">ID:</div>
          <div className="bb-value">{movie.tconst || "—"}</div>
        </div>

        <div className="bb-movie-actions">
          {movie.imdb_url && (
            <a href={movie.imdb_url} target="_blank" rel="noreferrer">
              IMDb
            </a>
          )}

          {mode === "browse" && movie.tconst && (
            <button onClick={() => onAdd?.(movie.tconst)}>
              + Watchlist
            </button>
          )}

          {mode === "watchlist" && movie.tconst && (
            <button onClick={() => onRemove?.(movie.tconst)}>
              Remove
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
