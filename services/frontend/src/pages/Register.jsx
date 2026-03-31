import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";

export default function Register() {
  const { register } = useAuth();
  const { addFlash } = useFlash();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await register(email, password);
      addFlash("success", "Account created.");
      navigate("/dashboard");
    } catch (err) {
      addFlash("error", err?.message || "Registration failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="hero">
      <section className="card auth-card">
        <h1>Create Account</h1>
        <p className="subtle">Get started with cronicle</p>

        <form className="form" onSubmit={onSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              autoComplete="email"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 8 characters"
              type="password"
              autoComplete="new-password"
              minLength={8}
              required
            />
          </div>

          <div className="actions">
            <button
              className="btn btn-primary"
              type="submit"
              disabled={isSubmitting}
            >
              Register
            </button>
            <Link className="btn" to="/login">
              Log in instead
            </Link>
          </div>
        </form>
      </section>
    </div>
  );
}
