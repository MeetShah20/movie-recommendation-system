import { useEffect, useState } from "react";

import { fetchMovie } from "../api/client.js";

const IMAGE_BASE = "https://image.tmdb.org/t/p/w342";

function runtimeLabel(minutes) {
  if (!minutes) {
    return null;
  }
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return hours ? `${hours}h ${rest}m` : `${rest}m`;
}

export default function MovieModal({ movieId, onClose }) {
  const [movie, setMovie] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setMovie(null);
    setError(null);
    fetchMovie(movieId)
      .then(setMovie)
      .catch(() => setError("Could not load this movie."));
  }, [movieId]);

  useEffect(() => {
    function onKey(event) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  const meta = movie
    ? [movie.year, runtimeLabel(movie.runtime), movie.genres].filter(Boolean)
    : [];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(event) => event.stopPropagation()}>
        <button className="modal-close" type="button" onClick={onClose} aria-label="Close">
          ×
        </button>
        {error && <p className="status error">{error}</p>}
        {movie && (
          <div className="modal-body">
            {movie.poster_path ? (
              <img
                className="modal-poster"
                src={`${IMAGE_BASE}${movie.poster_path}`}
                alt={movie.title}
              />
            ) : (
              <div className="modal-poster modal-poster-empty">{movie.title}</div>
            )}
            <div className="modal-info">
              <h2>{movie.title}</h2>
              {movie.tagline && <p className="modal-tagline">{movie.tagline}</p>}
              <p className="modal-meta">{meta.join("  ·  ")}</p>
              {movie.vote_average ? (
                <p className="modal-rating">
                  {movie.vote_average.toFixed(1)} / 10
                  {movie.vote_count ? <span> ({movie.vote_count} votes)</span> : null}
                </p>
              ) : null}
              {movie.overview && <p className="modal-overview">{movie.overview}</p>}
              {movie.cast && (
                <p className="modal-credit">
                  <span>Cast</span> {movie.cast}
                </p>
              )}
              {movie.director && (
                <p className="modal-credit">
                  <span>Director</span> {movie.director}
                </p>
              )}
              {movie.producers && (
                <p className="modal-credit">
                  <span>Producers</span> {movie.producers}
                </p>
              )}
              {movie.imdb_url && (
                <a className="modal-imdb" href={movie.imdb_url} target="_blank" rel="noreferrer">
                  View on IMDb
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
