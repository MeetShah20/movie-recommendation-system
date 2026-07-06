export default function ResultsList({ result }) {
  if (!result) {
    return null;
  }

  if (result.recommendations.length === 0) {
    return <p>No recommendations found for this movie.</p>;
  }

  return (
    <section>
      <h2>Recommendations for {result.input_movie}</h2>
      <p>Recommendation mode: {result.mode_used}</p>
      <ol>
        {result.recommendations.map((movie) => (
          <li key={movie.movie_id}>
            <span>{movie.title}</span>
            <span>{movie.score.toFixed(2)}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
