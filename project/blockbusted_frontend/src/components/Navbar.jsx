import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearTokens, isAuthed } from "../lib/api.js";

export default function Navbar() {
  const navigate = useNavigate();
  const authed = isAuthed();

  function logout() {
    clearTokens();
    navigate("/movies");
    // simple reload so pages re-evaluate auth state without state plumbing
    window.location.reload();
  }

  // Your provided nav.css already styles <nav>, .logo, .menu, etc.
  return (
    <nav>
      <div className="logo">
        <Link to="/movies" className="modern-text" style={{ textDecoration: "none" }}>
          Blockbusted
        </Link>
      </div>

      <div className="menu">
        <div><Link to="/movies" className="modern-text">Movies</Link></div>
        <div><Link to="/watchlist" className="modern-text">Watchlist</Link></div>

        {!authed && (
          <>
            <div><Link to="/login" className="modern-text">Login</Link></div>
            <div><Link to="/register" className="modern-text">Register</Link></div>
          </>
        )}

        {authed && (
          <div>
            <button onClick={logout} className="modern-text" style={{ cursor: "pointer" }}>
              Logout
            </button>
          </div>
        )}
      </div>

      <div className="welcome modern-text">
        {authed ? "Welcome" : "Guest"}
      </div>
    </nav>
  );
}
