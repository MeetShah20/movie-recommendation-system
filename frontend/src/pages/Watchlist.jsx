import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import MovieModal from "../components/MovieModal.jsx";
import PosterCard from "../components/PosterCard.jsx";
import { fetchWatchlist } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";
import { useLibrary } from "../library/LibraryContext.jsx";

export default function Watchlist() {
  const { user } = useAuth();
  const { watchlistIds, toggleWatch } = useLibrary();
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }
    fetchWatchlist()
      .then(setMovies)
      .catch(() => setMovies([]))
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) {
    return (
      <section className="page">
        <h1>Watchlist</h1>
        <p className="status">
          <Link to="/login">Sign in</Link> to save movies to watch later.
        </p>
      </section>
    );
  }

  const saved = movies.filter((movie) => watchlistIds.has(movie.id));

  return (
    <section className="page">
      <h1>Watchlist</h1>
      {loading && <p className="status">Loading...</p>}
      {!loading && saved.length === 0 && <p className="status">Your watchlist is empty.</p>}
      <div className="rec-grid">
        {saved.map((movie) => (
          <div key={movie.id} className="rec-item">
            <PosterCard movie={movie} onClick={() => setSelectedId(movie.id)} />
            <p className="rec-title">{movie.title}</p>
            <button className="watch-remove" type="button" onClick={() => toggleWatch(movie.id)}>
              Remove
            </button>
          </div>
        ))}
      </div>
      {selectedId && <MovieModal movieId={selectedId} onClose={() => setSelectedId(null)} />}
    </section>
  );
}
