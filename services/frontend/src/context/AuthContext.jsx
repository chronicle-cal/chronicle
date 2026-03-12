import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import * as api from "../api.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isBootstrapping, setIsBootstrapping] = useState(true);
  const [user, setUser] = useState(null);

  const refreshUser = useCallback(async () => {
    try {
      const me = await api.me();
      if (me?.authenticated) {
        setIsAuthenticated(true);
        setUser({ email: me.email || "", name: me.name || "" });
      } else {
        setIsAuthenticated(false);
        setUser(null);
      }
    } catch {
      setIsAuthenticated(false);
      setUser(null);
    }
  }, []);

  useEffect(() => {
    (async () => {
      await refreshUser();
      setIsBootstrapping(false);
    })();
  }, [refreshUser]);

  const login = useCallback(async (email, password) => {
    await api.login({ email, password });
    await refreshUser();
  }, [refreshUser]);

  const register = useCallback(async (email, password) => {
    await api.registerAndLogin({ email, password });
    await refreshUser();
  }, [refreshUser]);

  const logout = useCallback(async () => {
    try {
      await api.logout();
    } finally {
      setIsAuthenticated(false);
      localStorage.removeItem("token");
      setUser(null);
    }
  }, []);
  const value = useMemo(
    () => ({
      isAuthenticated,
      isBootstrapping,
      user,
      login,
      register,
      logout,
      refreshUser,
    }),
    [isAuthenticated, isBootstrapping, user, login, register, logout, refreshUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
