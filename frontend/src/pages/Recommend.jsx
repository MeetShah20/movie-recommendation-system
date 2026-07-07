import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import MovieModal from "../components/MovieModal.jsx";
import PosterCard from "../components/PosterCard.jsx";
import { fetchFriends, recommend } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

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
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const seedMovie = searchParams.get("movie");

  const [text, setText] = useState("");
  const [genres, setGenres] = useState([]);
  const [cast, setCast] = useState("");
  const [director, setDirector] = useState("");
  const [minRating, setMinRating] = useState(0);
  const [friends, setFriends] = useState([]);
  const [selectedFriends, setSelectedFriends] = useState([]);

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    if (!user) {
      setFriends([]);
      setSelectedFriends([]);
      return;
    }
    fetchFriends()
      .then((all) => setFriends(all.filter((friend) => friend.kind === "profile")))
      .catch(() => setFriends([]));
  }, [user]);

  function toggleGenre(genre) {
    setGenres((current) =>
      current.includes(genre) ? current.filter((g) => g !== genre) : [...current, genre]
    );
  }

  function toggleFriend(id) {
    setSelectedFriends((current) =>
      current.includes(id) ? current.filter((f) => f !== id) : [...current, id]
    );
  }

  async function run(extra = {}) {
    setLoading(true);
    setError(null);
    try {
      const payload = {
        text: text.trim(),
        genres,
        cast: cast.trim(),
        director: director.trim(),
        min_rating: minRating,
        people: selectedFriends,
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
          <label htmlFor="mood">Describe what you're in the mood for</label>
          <textarea
            id="mood"
            className="mood-box"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="a heartwarming space adventure with a strong friendship"
            rows={2}
          />
        </div>
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
        {user && (
          <div className="field">
            <label>Friends</label>
            {friends.length === 0 ? (
              <p className="field-hint">Add viewers from Settings to see what they would recommend.</p>
            ) : (
              <div className="chips">
                {friends.map((friend) => (
                  <button
                    key={friend.id}
                    type="button"
                    className={selectedFriends.includes(friend.id) ? "chip active" : "chip"}
                    onClick={() => toggleFriend(friend.id)}
                  >
                    {friend.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
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
