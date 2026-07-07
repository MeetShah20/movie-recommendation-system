import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import MovieModal from "../components/MovieModal.jsx";
import PosterCard from "../components/PosterCard.jsx";
import { fetchLikes } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";
import { useLibrary } from "../library/LibraryContext.jsx";

export default function Likes() {
  const { user } = useAuth();
  const { likedIds } = useLibrary();
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return;
    }
    fetchLikes()
      .then(setMovies)
      .catch(() => setMovies([]))
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) {
    return (
      <section className="page">
        <h1>Liked movies</h1>
        <p className="status">
          <Link to="/login">Sign in</Link> to like movies and see them here.
        </p>
      </section>
    );
  }

  const liked = movies.filter((movie) => likedIds.has(movie.id));

  return (
    <section className="page">
      <h1>Liked movies</h1>
      {loading && <p className="status">Loading...</p>}
      {!loading && liked.length === 0 && <p className="status">You haven't liked any movies yet.</p>}
      <div className="rec-grid">
        {liked.map((movie) => (
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
