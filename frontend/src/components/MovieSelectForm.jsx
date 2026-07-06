import { useEffect, useState } from "react";

import { searchMovies } from "../api/client.js";

export default function MovieSelectForm() {
  const [query, setQuery] = useState("");
  const [matches, setMatches] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    if (!query || selected?.title === query) {
      setMatches([]);
      return;
    }
    const timer = setTimeout(() => {
      searchMovies(query)
        .then(setMatches)
        .catch(() => setMatches([]));
    }, 300);
    return () => clearTimeout(timer);
  }, [query, selected]);

  function choose(movie) {
    setSelected(movie);
    setQuery(movie.title);
    setMatches([]);
  }

  return (
    <div>
      <label htmlFor="movie-search">Movie</label>
      <input
        id="movie-search"
        value={query}
        onChange={(event) => {
          setSelected(null);
          setQuery(event.target.value);
        }}
        placeholder="Search for a movie"
        autoComplete="off"
      />
      {matches.length > 0 && (
        <ul>
          {matches.map((movie) => (
            <li key={movie.id}>
              <button type="button" onClick={() => choose(movie)}>
                {movie.title}
                {movie.year ? ` (${movie.year})` : ""}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
