import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { fetchMe, login, register, setToken } from "../api/client.js";
import { useAuth } from "../auth/AuthContext.jsx";

export default function Register() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await register({ username, name, password });
      const { access_token } = await login({ username, password });
      setToken(access_token);
      const profile = await fetchMe();
      signIn(access_token, profile);
      navigate("/");
    } catch {
      setError("That username is already taken.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="page auth-page">
      <h1>Create an account</h1>
      <form className="form" onSubmit={submit}>
        <div className="field">
          <label htmlFor="name">Name</label>
          <input id="name" value={name} onChange={(event) => setName(event.target.value)} />
        </div>
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
            autoComplete="new-password"
          />
        </div>
        {error && <p className="status error">{error}</p>}
        <button
          className="submit"
          type="submit"
          disabled={busy || !username || !name || !password}
        >
          {busy ? "Creating..." : "Create account"}
        </button>
      </form>
      <p className="auth-switch">
        Already have an account? <Link to="/login">Sign in</Link>
      </p>
    </section>
  );
}
