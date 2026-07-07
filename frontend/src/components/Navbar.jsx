import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext.jsx";

const baseLinks = [
  { to: "/", label: "Home", end: true },
  { to: "/recommend", label: "Recommend" },
  { to: "/search", label: "Search" },
];

export default function Navbar() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  function logout() {
    signOut();
    navigate("/");
  }

  const links = user
    ? [...baseLinks, { to: "/watchlist", label: "Watchlist" }, { to: "/settings", label: "Settings" }]
    : [...baseLinks, { to: "/settings", label: "Settings" }];

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
      <div className="nav-account">
        {user ? (
          <>
            <NavLink
              to="/likes"
              className={({ isActive }) => (isActive ? "nav-heart active" : "nav-heart")}
              aria-label="Liked movies"
              title="Liked movies"
            >
              ♥
            </NavLink>
            <span className="nav-user">{user.name}</span>
            <button className="nav-logout" type="button" onClick={logout}>
              Log out
            </button>
          </>
        ) : (
          <NavLink to="/login" className="nav-link">
            Sign in
          </NavLink>
        )}
      </div>
    </header>
  );
}
