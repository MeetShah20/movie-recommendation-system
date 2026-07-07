import { useState } from "react";

import LikeButton from "./LikeButton.jsx";

const IMAGE_BASE = "https://image.tmdb.org/t/p/w342";

export default function PosterCard({ movie, onClick }) {
  const [failed, setFailed] = useState(false);
  const hasPoster = movie.poster_path && !failed;

  return (
    <div className="poster-card">
      <button className="poster-hit" type="button" onClick={() => onClick?.(movie)}>
        {hasPoster ? (
          <img
            className="poster-image"
            src={`${IMAGE_BASE}${movie.poster_path}`}
            alt={movie.title}
            loading="lazy"
            onError={() => setFailed(true)}
          />
        ) : (
          <span className="poster-fallback">
            <span className="poster-fallback-title">{movie.title}</span>
            {movie.year && <span className="poster-fallback-year">{movie.year}</span>}
          </span>
        )}
      </button>
      <LikeButton movieId={movie.id} className="poster-like" />
    </div>
  );
}
