import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import MovieModal from "../components/MovieModal.jsx";
import PosterCard from "../components/PosterCard.jsx";
import { recommend } from "../api/client.js";

const GENRES = [
  "Action",
  "Comedy",
  "Drama",
  "Adventure",
  "Animation",
  "Science Fiction",
  "Thriller",
  "Romance",
  "Family",
  "Horror",
  "Crime",
  "Fantasy",
];

const RATINGS = [
  { label: "Any rating", value: 0 },
  { label: "6+", value: 6 },
  { label: "7+", value: 7 },
  { label: "8+", value: 8 },
];

export default function Recommend() {
  const [searchParams] = useSearchParams();
  const seedMovie = searchParams.get("movie");

  const [genres, setGenres] = useState([]);
  const [cast, setCast] = useState("");
  const [director, setDirector] = useState("");
  const [minRating, setMinRating] = useState(0);

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  function toggleGenre(genre) {
    setGenres((current) =>
      current.includes(genre) ? current.filter((g) => g !== genre) : [...current, genre]
    );
  }

  async function run(extra = {}) {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        genres,
        cast: cast.trim(),
        director: director.trim(),
        min_rating: minRating,
        ...extra,
      };
      const data = await recommend(payload);
      setResults(data.results);
    } catch {
      setError("Could not load recommendations.");
    } finally {
      setLoading(false);
    }
  }

  function submit(event) {
    event.preventDefault();
    run();
  }

  useEffect(() => {
    if (seedMovie) {
      run({ movie_id: Number(seedMovie) });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seedMovie]);

  return (
    <section className="page">
      <h1>Find something to watch</h1>
      <form className="form recommend-form" onSubmit={submit}>
        <div className="field">
          <label>Genres</label>
          <div className="chips">
            {GENRES.map((genre) => (
              <button
                key={genre}
                type="button"
                className={genres.includes(genre) ? "chip active" : "chip"}
                onClick={() => toggleGenre(genre)}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label htmlFor="cast">Actor</label>
            <input
              id="cast"
              value={cast}
              onChange={(event) => setCast(event.target.value)}
              placeholder="e.g. Tom Hanks"
              autoComplete="off"
            />
          </div>
          <div className="field">
            <label htmlFor="director">Director</label>
            <input
              id="director"
              value={director}
              onChange={(event) => setDirector(event.target.value)}
              placeholder="e.g. Christopher Nolan"
              autoComplete="off"
            />
          </div>
          <div className="field">
            <label htmlFor="min-rating">Minimum rating</label>
            <select
              id="min-rating"
              value={minRating}
              onChange={(event) => setMinRating(Number(event.target.value))}
            >
              {RATINGS.map((rating) => (
                <option key={rating.value} value={rating.value}>
                  {rating.label}
                </option>
              ))}
            </select>
          </div>
        </div>
        <button className="submit" type="submit" disabled={loading}>
          {loading ? "Finding..." : "Get recommendations"}
        </button>
      </form>

      {error && <p className="status error">{error}</p>}
      {results && results.length === 0 && !loading && (
        <p className="status">Nothing matched. Try different criteria.</p>
      )}
      {results && results.length > 0 && (
        <div className="rec-grid">
          {results.map((movie) => (
            <div key={movie.id} className="rec-item">
              <PosterCard movie={movie} onClick={() => setSelectedId(movie.id)} />
              <p className="rec-title">{movie.title}</p>
              <ul className="rec-reasons">
                {movie.reasons.map((reason) => (
                  <li key={reason} className="rec-reason">
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {selectedId && <MovieModal movieId={selectedId} onClose={() => setSelectedId(null)} />}
    </section>
  );
}
