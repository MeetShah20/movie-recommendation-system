const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path) {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`request failed with status ${response.status}`);
  }
  return response.json();
}

export function searchMovies(query) {
  const params = new URLSearchParams({ search: query });
  return request(`/movies?${params}`);
}

export function fetchRecommendations({ movieId, userId, topN = 10 }) {
  const params = new URLSearchParams({ movie_id: movieId, top_n: topN });
  if (userId) {
    params.set("user_id", userId);
  }
  return request(`/recommend?${params}`);
}
