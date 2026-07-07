const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const TOKEN_KEY = "auth_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { method = "GET", body } = {}) {
  const headers = {};
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    throw new Error(`request failed with status ${response.status}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export function searchMovies(query) {
  const params = new URLSearchParams({ search: query });
  return request(`/movies?${params}`);
}

export function recommend(payload) {
  return request("/recommend", { method: "POST", body: payload });
}

export function register({ username, name, password }) {
  return request("/register", { method: "POST", body: { username, name, password } });
}

export function login({ username, password }) {
  return request("/login", { method: "POST", body: { username, password } });
}

export function fetchMe() {
  return request("/me");
}

export function fetchHome() {
  return request("/home");
}

export function fetchMovie(id) {
  return request(`/movies/${id}`);
}

export function fetchFriends() {
  return request("/friends");
}

export function fetchPeople(search = "") {
  const params = new URLSearchParams({ search });
  return request(`/people?${params}`);
}

export function addFriend({ kind, id }) {
  return request("/friends", { method: "POST", body: { kind, id } });
}

export function fetchLikes() {
  return request("/likes");
}

export function likeMovie(movieId) {
  return request("/likes", { method: "POST", body: { movie_id: movieId } });
}

export function unlikeMovie(movieId) {
  return request(`/likes/${movieId}`, { method: "DELETE" });
}
