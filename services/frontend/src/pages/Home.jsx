import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Home() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const from = location.state?.from;

  return (
    <div className="hero">
      <section className="card">
        <h1>Chronicle</h1>
        <p className="subtle">
          Chronicle is a web-based calendar app focused on calendar syncing, managing and smart scheduling.
        </p>
        <div className="actions">
          {isAuthenticated ? (
            <Link className="btn btn-primary" to="/dashboard">
              Dashboard
            </Link>
          ) : (
            <>
              <Link className="btn btn-primary" to="/register" state={from ? { from } : null}>
                Register
              </Link>
              <Link className="btn" to="/login" state={from ? { from } : null}>
                Login
              </Link>
            </>
          )}
        </div>
      </section>
    </div>
  );
}
