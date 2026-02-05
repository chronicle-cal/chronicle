import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import * as api from "../api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isBootstrapping, setIsBootstrapping] = useState(true);

  useEffect(() => {
    // Optional: check session on reload
    (async () => {
      try {
        const me = await api.me();
        setIsAuthenticated(!!me?.authenticated);
      } catch {
        setIsAuthenticated(false);
      } finally {
        setIsBootstrapping(false);
      }
    })();
  }, []);

  const login = useCallback(async (email, password) => {
    await api.login({ email, password });
    setIsAuthenticated(true);
  }, []);

  const register = useCallback(async (email, password) => {
    await api.register({ email, password });
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(async () => {
    await api.logout();
    setIsAuthenticated(false);
  }, []);

  const value = useMemo(
    () => ({ isAuthenticated, isBootstrapping, login, register, logout }),
    [isAuthenticated, isBootstrapping, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
