// Centralized API helpers for Django backend.
// Configure API base URL with VITE_API_BASE_URL.

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

// Token storage keys
const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY) || "";
}

export function setTokens({ access, refresh }) {
  if (access) localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export function isAuthed() {
  return Boolean(getAccessToken());
}

export function authHeaders() {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseError(res) {
  // Try JSON error payload first
  try {
    const data = await res.json();
    return data?.detail || JSON.stringify(data);
  } catch {
    try {
      return await res.text();
    } catch {
      return `${res.status} ${res.statusText}`;
    }
  }
}

export async function apiGet(path, headers = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...headers
    }
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function apiPost(path, body, headers = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...headers
    },
    body: JSON.stringify(body || {})
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function apiDelete(path, headers = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      ...headers
    }
  });
  if (!res.ok) throw new Error(await parseError(res));
  // Your delete endpoint returns JSON; if not, we safely return {}.
  try {
    return await res.json();
  } catch {
    return {};
  }
}
