import React, { useState } from "react";
import { apiPost } from "../lib/api.js";
import { useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function submit(e) {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      await apiPost("/api/accounts/register/", { email, username, password });
      setMessage("Registered. You can now login.");
      setTimeout(() => navigate("/login"), 600);
    } catch (err) {
      setMessage(err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 420 }}>
      <h2>Register</h2>
      <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          type="email"
          required
          style={{ padding: 10 }}
        />
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username (optional)"
          style={{ padding: 10 }}
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password (min 8 chars)"
          type="password"
          required
          style={{ padding: 10 }}
        />
        <button disabled={loading} type="submit">
          {loading ? "Creating..." : "Register"}
        </button>
      </form>

      {message && <div style={{ marginTop: 12 }}>{message}</div>}

      <div style={{ marginTop: 12 }}>
        Already have an account? <Link to="/login">Login</Link>
      </div>
    </div>
  );
}
