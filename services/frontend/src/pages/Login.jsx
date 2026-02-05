import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";

export default function Login() {
  const { login } = useAuth();
  const { addFlash } = useFlash();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const from = location.state?.from || "/dashboard";

  const onSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await login(email, password);
      addFlash("success", "Welcome back.");
      navigate(from, { replace: true });
    } catch (err) {
      addFlash("error", err?.message || "Login failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="hero">
      <section className="card auth-card">
        <h1>Login</h1>
        <p className="subtle">Access your account</p>

        <form className="form" onSubmit={onSubmit}>
          <div>
            <label>Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              autoComplete="email"
              required
            />
          </div>

          <div>
            <label>Password</label>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Your password"
              type="password"
              autoComplete="current-password"
              required
            />
          </div>

          <div className="actions">
            <button className="btn btn-primary" type="submit" disabled={isSubmitting}>
              Login
            </button>
            <Link className="btn" to="/register">
              Register
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
