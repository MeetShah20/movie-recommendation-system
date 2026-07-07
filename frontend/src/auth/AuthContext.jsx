import { createContext, useContext, useEffect, useState } from "react";

import { clearToken, fetchMe, getToken, setToken } from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!getToken()) {
      setReady(true);
      return;
    }
    fetchMe()
      .then(setUser)
      .catch(clearToken)
      .finally(() => setReady(true));
  }, []);

  function signIn(token, profile) {
    setToken(token);
    setUser(profile);
  }

  function signOut() {
    clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, ready, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
