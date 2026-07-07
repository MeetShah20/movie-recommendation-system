import { useAuth } from "../auth/AuthContext.jsx";
import { useLibrary } from "../library/LibraryContext.jsx";

export default function WatchButton({ movieId }) {
  const { user } = useAuth();
  const { watchlistIds, toggleWatch } = useLibrary();

  if (!user) {
    return null;
  }

  const saved = watchlistIds.has(movieId);

  return (
    <button
      className="watch-button"
      type="button"
      onClick={(event) => {
        event.stopPropagation();
        toggleWatch(movieId);
      }}
    >
      {saved ? "✓ In watchlist" : "+ Watchlist"}
    </button>
  );
}
