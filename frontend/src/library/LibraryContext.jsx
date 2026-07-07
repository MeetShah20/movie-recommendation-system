import { createContext, useContext, useEffect, useState } from "react";

import { fetchLikes, likeMovie, unlikeMovie } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

const LibraryContext = createContext(null);

export function LibraryProvider({ children }) {
  const { user } = useAuth();
  const [likedIds, setLikedIds] = useState(new Set());

  useEffect(() => {
    if (!user) {
      setLikedIds(new Set());
      return;
    }
    fetchLikes()
      .then((movies) => setLikedIds(new Set(movies.map((movie) => movie.id))))
      .catch(() => setLikedIds(new Set()));
  }, [user]);

  async function toggleLike(movieId) {
    const liked = likedIds.has(movieId);
    setLikedIds((current) => {
      const next = new Set(current);
      if (liked) {
        next.delete(movieId);
      } else {
        next.add(movieId);
      }
      return next;
    });
    try {
      await (liked ? unlikeMovie(movieId) : likeMovie(movieId));
    } catch {
      setLikedIds((current) => {
        const next = new Set(current);
        if (liked) {
          next.add(movieId);
        } else {
          next.delete(movieId);
        }
        return next;
      });
    }
  }

  return (
    <LibraryContext.Provider value={{ likedIds, toggleLike }}>{children}</LibraryContext.Provider>
  );
}

export function useLibrary() {
  return useContext(LibraryContext);
}
