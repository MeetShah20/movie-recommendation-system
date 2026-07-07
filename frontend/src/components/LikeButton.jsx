import { useAuth } from "../auth/AuthContext.jsx";
import { useLibrary } from "../library/LibraryContext.jsx";

export default function LikeButton({ movieId, className = "" }) {
  const { user } = useAuth();
  const { likedIds, toggleLike } = useLibrary();

  if (!user) {
    return null;
  }

  const liked = likedIds.has(movieId);

  return (
    <button
      className={`like-button ${liked ? "liked" : ""} ${className}`}
      type="button"
      aria-label={liked ? "Remove like" : "Like"}
      onClick={(event) => {
        event.stopPropagation();
        toggleLike(movieId);
      }}
    >
      {liked ? "♥" : "♡"}
    </button>
  );
}
