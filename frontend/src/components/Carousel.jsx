import { useRef } from "react";

import PosterCard from "./PosterCard.jsx";

export default function Carousel({ title, movies, onSelect }) {
  const trackRef = useRef(null);

  function scroll(direction) {
    const track = trackRef.current;
    if (track) {
      track.scrollBy({ left: direction * track.clientWidth * 0.8, behavior: "smooth" });
    }
  }

  if (!movies.length) {
    return null;
  }

  return (
    <section className="carousel">
      <h2 className="carousel-title">{title}</h2>
      <div className="carousel-body">
        <button
          className="carousel-arrow left"
          type="button"
          onClick={() => scroll(-1)}
          aria-label="Scroll left"
        >
          ‹
        </button>
        <div className="carousel-track" ref={trackRef}>
          {movies.map((movie) => (
            <PosterCard key={movie.id} movie={movie} onClick={onSelect} />
          ))}
        </div>
        <button
          className="carousel-arrow right"
          type="button"
          onClick={() => scroll(1)}
          aria-label="Scroll right"
        >
          ›
        </button>
      </div>
    </section>
  );
}
