import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home", end: true },
  { to: "/recommend", label: "Recommend" },
  { to: "/search", label: "Search" },
  { to: "/settings", label: "Settings" },
];

export default function Navbar() {
  return (
    <header className="navbar">
      <span className="brand">Movie Recommender</span>
      <nav className="nav-links">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
