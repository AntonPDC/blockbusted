import React, { useEffect, useRef, useState } from "react";
import { apiDelete, apiGet, authHeaders, isAuthed } from "../lib/api.js";
import { normalizeMovie } from "../lib/normalize.js";
import MovieRow from "../components/MovieRow.jsx";

export default function WatchlistPage() {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const pollRef = useRef(null);

  async function loadWatchlist() {
    if (!isAuthed()) return;
    setLoading(true);
    setMessage("");
    try {
      const data = await apiGet("/api/movies/watchlist/", authHeaders());
      setItems((Array.isArray(data) ? data : []).map(normalizeMovie));
    } catch (e) {
      setMessage(e.message || "Failed to load watchlist.");
    } finally {
      setLoading(false);
    }
  }

  async function removeFromWatchlist(tconst) {
    if (!isAuthed()) {
      setMessage("Login required.");
      return;
    }
    setMessage("");
    try {
      await apiDelete(`/api/movies/watchlist/${encodeURIComponent(tconst)}/`, authHeaders());
      await loadWatchlist();
      setMessage("Removed.");
    } catch (e) {
      setMessage(e.message || "Failed to remove.");
    }
  }

  useEffect(() => {
    if (!isAuthed()) {
      setMessage("Please login to view your watchlist.");
      return;
    }
    loadWatchlist();

    // Poll every 15 seconds (simple polling, no websockets)
    pollRef.current = setInterval(loadWatchlist, 15000);
    return () => clearInterval(pollRef.current);
  }, []);

  if (!isAuthed()) {
    return <div>{message || "Not logged in."}</div>;
  }

  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <h2 style={{ margin: 0 }}>Watchlist</h2>
        {loading && <span className="bb-muted">Loading…</span>}
      </div>

      {message && <div style={{ marginTop: 12 }}>{message}</div>}

      <div className="bb-movies" style={{ marginTop: 14 }}>
        {items.map((m) => (
          <MovieRow
            key={m.tconst || `${m.title}-${m.year}`}
            movie={m}
            mode="watchlist"
            onRemove={removeFromWatchlist}
          />
        ))}

        {!loading && items.length === 0 && (
          <div style={{ marginTop: 12 }} className="bb-muted">
            Your watchlist is empty.
          </div>
        )}
      </div>
    </div>
  );
}
