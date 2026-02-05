import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const { addFlash } = useFlash();
  const navigate = useNavigate();

  const onLogout = async () => {
    try {
      await logout();
      addFlash("success", "Logged out.");
      navigate("/login");
    } catch {
      addFlash("error", "Logout failed.");
    }
  };

  return (
    <>
      <div className="brand">
        <div className="brand-badge" />
        <div>Chronicle</div>
      </div>

      <nav className="nav-links">
        {isAuthenticated ? (
          <>
            <Link className="pill" to="/dashboard">
              Dashboard
            </Link>
            <button className="pill btn-danger" type="button" onClick={onLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link className="pill" to="/login">
              Login
            </Link>
            <Link className="pill" to="/register">
              Register
            </Link>
          </>
        )}
      </nav>
    </>
  );
}
