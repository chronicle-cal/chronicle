import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, isBootstrapping } = useAuth();
  const location = useLocation();

  if (isBootstrapping) return null; // or a small skeleton/loading card

  if (!isAuthenticated) {
    return <Navigate to="/home" replace state={{ from: location.pathname }} />;
  }

  return children;
}
