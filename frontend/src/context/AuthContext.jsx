import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../api/client.js";

const AuthContext = createContext(null);
const SESSION_KEY = "emp.session";

function readSession() {
  try {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY));
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const stored = readSession();
  const [token, setToken] = useState(stored?.access_token || null);
  const [user, setUser] = useState(stored?.user || null);
  const [ready, setReady] = useState(!stored?.access_token);

  const applySession = useCallback((payload) => {
    setToken(payload.access_token);
    setUser(payload.user);
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(payload));
    return payload.user;
  }, []);

  useEffect(() => {
    if (!token) {
      setReady(true);
      return;
    }
    api("/auth/me", { token })
      .then((me) => {
        setUser(me);
        sessionStorage.setItem(SESSION_KEY, JSON.stringify({ access_token: token, user: me }));
      })
      .catch(() => {
        sessionStorage.removeItem(SESSION_KEY);
        setToken(null);
        setUser(null);
      })
      .finally(() => setReady(true));
  }, []);

  const login = useCallback(
    async (email, password) => {
      const payload = await api("/auth/login", { method: "POST", body: { email, password } });
      return applySession(payload);
    },
    [applySession]
  );

  const adminLogin = useCallback(
    async (email, password) => {
      const payload = await api("/auth/admin/login", { method: "POST", body: { email, password } });
      return applySession(payload);
    },
    [applySession]
  );

  const register = useCallback(
    async ({ name, email, password, role, school_id }) => {
      const payload = await api("/auth/register", {
        method: "POST",
        body: { name, email, password, role, school_id: Number(school_id) },
      });
      return applySession(payload);
    },
    [applySession]
  );

  const logout = useCallback(async () => {
    if (token) {
      try {
        await api("/auth/logout", { method: "POST", token });
      } catch {
        // Token is discarded locally either way.
      }
    }
    sessionStorage.removeItem(SESSION_KEY);
    setToken(null);
    setUser(null);
  }, [token]);

  const value = useMemo(
    () => ({ token, user, ready, login, adminLogin, register, logout }),
    [token, user, ready, login, adminLogin, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
