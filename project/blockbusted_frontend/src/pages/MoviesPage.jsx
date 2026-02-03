import React, { useEffect, useState } from "react";
import { apiGet, apiPost, authHeaders, isAuthed } from "../lib/api.js";
import { normalizeMovie } from "../lib/normalize.js";
import MovieRow from "../components/MovieRow.jsx";

export default function MoviesPage() {
  const [tab, setTab] = useState("popular"); // popular | search
  const [popular, setPopular] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadPopular() {
    setLoading(true);
    setMessage("");
    try {
      const data = await apiGet("/api/movies/popular/?limit=15");
      setPopular((Array.isArray(data) ? data : []).map(normalizeMovie));
    } catch (e) {
      setMessage(e.message || "Failed to load popular movies.");
    } finally {
      setLoading(false);
    }
  }

  async function runSearch() {
    const q = searchQuery.trim();
    if (!q) {
      setSearchResults([]);
      setMessage("Type a movie title to search.");
      return;
    }
    setLoading(true);
    setMessage("");
    try {
      const data = await apiGet(`/api/movies/search/?title=${encodeURIComponent(q)}&limit=15`);
      setSearchResults((Array.isArray(data) ? data : []).map(normalizeMovie));
    } catch (e) {
      setMessage(e.message || "Search failed.");
    } finally {
      setLoading(false);
    }
  }

  async function addToWatchlist(tconst) {
    if (!isAuthed()) {
      setMessage("Login required to add to watchlist.");
      return;
    }
    setMessage("");
    try {
      await apiPost("/api/movies/watchlist/", { tconst }, authHeaders());
      setMessage("Added to watchlist.");
    } catch (e) {
      setMessage(e.message || "Failed to add to watchlist.");
    }
  }

  useEffect(() => {
    loadPopular();
  }, []);

  const list = tab === "popular" ? popular : searchResults;

  return (
    <div>
      <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
        <button onClick={() => setTab("popular")}>Popular</button>
        <button onClick={() => setTab("search")}>Search</button>

        {tab === "search" && (
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search title..."
              style={{ padding: 8, minWidth: 240 }}
              onKeyDown={(e) => { if (e.key === "Enter") runSearch(); }}
            />
            <button onClick={runSearch}>Go</button>
          </div>
        )}

        <div style={{ marginLeft: "auto" }} className="bb-muted">
          {isAuthed() ? "Logged in" : "Not logged in"}
        </div>
      </div>

      {message && <div style={{ marginTop: 12 }}>{message}</div>}
      {loading && <div style={{ marginTop: 12 }}>Loading…</div>}

      <div className="bb-movies" style={{ marginTop: 14 }}>
        {list.map((m) => (
          <MovieRow
            key={m.tconst || `${m.title}-${m.year}`}
            movie={m}
            mode="browse"
            onAdd={addToWatchlist}
          />
        ))}

        {!loading && list.length === 0 && (
          <div style={{ marginTop: 12 }} className="bb-muted">
            No movies to display.
          </div>
        )}
      </div>
    </div>
  );
}
