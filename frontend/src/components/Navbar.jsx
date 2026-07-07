import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext.jsx";

const links = [
  { to: "/", label: "Home", end: true },
  { to: "/recommend", label: "Recommend" },
  { to: "/search", label: "Search" },
  { to: "/settings", label: "Settings" },
];

export default function Navbar() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  function logout() {
    signOut();
    navigate("/");
  }

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
