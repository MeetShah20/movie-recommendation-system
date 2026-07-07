import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import MovieSelectForm from "../components/MovieSelectForm.jsx";
import ResultsList from "../components/ResultsList.jsx";
import { fetchRecommendations } from "../api/client.js";

export default function Recommend() {
  const [searchParams] = useSearchParams();
  const [request, setRequest] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const seedMovie = searchParams.get("movie");
  useEffect(() => {
    if (seedMovie) {
      setRequest({ movieId: Number(seedMovie) });
    }
  }, [seedMovie]);

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
    <section className="page">
      <h1>Find something to watch</h1>
      <MovieSelectForm onSubmit={setRequest} />
      {loading && <p className="status">Loading...</p>}
      {error && <p className="status error">{error}</p>}
      {!loading && !error && <ResultsList result={result} />}
    </section>
  );
}
