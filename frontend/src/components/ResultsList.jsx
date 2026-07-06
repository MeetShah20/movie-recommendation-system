export default function ResultsList({ result }) {
  if (!result) {
    return null;
  }

  if (result.recommendations.length === 0) {
    return <p className="status">No recommendations found for this movie.</p>;
  }

  return (
    <section className="results">
      <h2>Recommendations for {result.input_movie}</h2>
      <p className="mode">Recommendation mode: {result.mode_used}</p>
      <ol className="result-list">
        {result.recommendations.map((movie) => (
          <li key={movie.movie_id} className="result">
            <span className="title">{movie.title}</span>
            <span className="score">{movie.score.toFixed(2)}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
