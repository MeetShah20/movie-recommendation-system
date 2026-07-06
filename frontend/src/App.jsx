import { useEffect, useState } from "react";

import MovieSelectForm from "./components/MovieSelectForm.jsx";
import ResultsList from "./components/ResultsList.jsx";
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
    <main className="app">
      <h1>Movie Recommender</h1>
      <MovieSelectForm onSubmit={setRequest} />
      {loading && <p className="status">Loading...</p>}
      {error && <p className="status error">{error}</p>}
      {!loading && !error && <ResultsList result={result} />}
    </main>
  );
}
