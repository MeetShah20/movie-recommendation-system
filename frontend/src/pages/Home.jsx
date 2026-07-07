import { useEffect, useState } from "react";

import Carousel from "../components/Carousel.jsx";
import { fetchHome } from "../api/client.js";

export default function Home() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHome()
      .then(setRows)
      .catch(() => setError("Could not load the feed."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <section className="page">
      {loading && <p className="status">Loading...</p>}
      {error && <p className="status error">{error}</p>}
      {rows.map((row) => (
        <Carousel key={row.genre} title={row.genre} movies={row.movies} />
      ))}
    </section>
  );
}
