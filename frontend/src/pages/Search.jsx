import { useEffect, useState } from "react";

import MovieModal from "../components/MovieModal.jsx";
import PosterCard from "../components/PosterCard.jsx";
import { searchMovies } from "../api/client.js";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const timer = setTimeout(() => {
      searchMovies(query.trim())
        .then(setResults)
        .catch(() => setResults([]));
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <section className="page">
      <h1>Search</h1>
      <input
        className="search-box"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Search for a movie"
        autoComplete="off"
      />
      {query.trim() && results.length === 0 && <p className="status">No matches.</p>}
      <div className="rec-grid">
        {results.map((movie) => (
          <div key={movie.id} className="rec-item">
            <PosterCard movie={movie} onClick={() => setSelectedId(movie.id)} />
            <p className="rec-title">{movie.title}</p>
          </div>
        ))}
      </div>
      {selectedId && <MovieModal movieId={selectedId} onClose={() => setSelectedId(null)} />}
    </section>
  );
}
