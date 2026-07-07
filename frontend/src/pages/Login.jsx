import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { fetchMe, login, setToken } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Login() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const { access_token } = await login({ username, password });
      setToken(access_token);
      const profile = await fetchMe();
      signIn(access_token, profile);
      navigate("/");
    } catch {
      setError("Wrong username or password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="page auth-page">
      <h1>Sign in</h1>
      <form className="form" onSubmit={submit}>
        <div className="field">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
          />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
          />
        </div>
        {error && <p className="status error">{error}</p>}
        <button className="submit" type="submit" disabled={busy || !username || !password}>
          {busy ? "Signing in..." : "Sign in"}
        </button>
      </form>
      <p className="auth-switch">
        New here? <Link to="/register">Create an account</Link>
      </p>
    </section>
  );
}
