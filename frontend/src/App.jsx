import { useState } from "react";

import MovieSelectForm from "./components/MovieSelectForm.jsx";

export default function App() {
  const [request, setRequest] = useState(null);

  return (
    <main>
      <h1>Movie Recommender</h1>
      <MovieSelectForm onSubmit={setRequest} />
    </main>
  );
}
