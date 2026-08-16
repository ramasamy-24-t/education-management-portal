import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { api } from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  const applySession = useCallback((payload) => {
    setToken(payload.access_token);
    setUser(payload.user);
    return payload.user;
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
    async ({ name, email, password, role }) => {
      const payload = await api("/auth/register", {
        method: "POST",
        body: { name, email, password, role },
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
        // Token is discarded locally either way (stateless JWT).
      }
    }
    setToken(null);
    setUser(null);
  }, [token]);

  const value = useMemo(
    () => ({ token, user, login, adminLogin, register, logout }),
    [token, user, login, adminLogin, register, logout]
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
