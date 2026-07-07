import { createContext, useContext, useEffect, useState } from "react";

import {
  addToWatchlist,
  fetchLikes,
  fetchWatchlist,
  likeMovie,
  removeFromWatchlist,
  unlikeMovie,
} from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

const LibraryContext = createContext(null);

function toggleInSet(set, id, present) {
  const next = new Set(set);
  if (present) {
    next.delete(id);
  } else {
    next.add(id);
  }
  return next;
}

export function LibraryProvider({ children }) {
  const { user } = useAuth();
  const [likedIds, setLikedIds] = useState(new Set());
  const [watchlistIds, setWatchlistIds] = useState(new Set());

  useEffect(() => {
    if (!user) {
      setLikedIds(new Set());
      setWatchlistIds(new Set());
      return;
    }
    fetchLikes()
      .then((movies) => setLikedIds(new Set(movies.map((movie) => movie.id))))
      .catch(() => setLikedIds(new Set()));
    fetchWatchlist()
      .then((movies) => setWatchlistIds(new Set(movies.map((movie) => movie.id))))
      .catch(() => setWatchlistIds(new Set()));
  }, [user]);

  async function toggle(setState, id, present, apiAdd, apiRemove) {
    setState((current) => toggleInSet(current, id, present));
    try {
      await (present ? apiRemove(id) : apiAdd(id));
    } catch {
      setState((current) => toggleInSet(current, id, !present));
    }
  }

  function toggleLike(movieId) {
    return toggle(setLikedIds, movieId, likedIds.has(movieId), likeMovie, unlikeMovie);
  }

  function toggleWatch(movieId) {
    return toggle(
      setWatchlistIds,
      movieId,
      watchlistIds.has(movieId),
      addToWatchlist,
      removeFromWatchlist
    );
  }

  return (
    <LibraryContext.Provider value={{ likedIds, watchlistIds, toggleLike, toggleWatch }}>
      {children}
    </LibraryContext.Provider>
  );
}

export function useLibrary() {
  return useContext(LibraryContext);
}
