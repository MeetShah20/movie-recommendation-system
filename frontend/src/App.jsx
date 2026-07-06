import { useEffect, useState } from "react";

import MovieSelectForm from "./components/MovieSelectForm.jsx";
import { fetchRecommendations } from "./api/client.js";

export default function App() {
  const [request, setRequest] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!request) {
      return;
    }
    setLoading(true);
    setError(null);
    fetchRecommendations(request)
      .then(setResult)
      .catch(() => setError("Could not load recommendations."))
      .finally(() => setLoading(false));
  }, [request]);

  return (
    <main>
      <h1>Movie Recommender</h1>
      <MovieSelectForm onSubmit={setRequest} />
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
    </main>
  );
}
