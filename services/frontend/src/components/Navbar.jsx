import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { useFlash } from "../context/FlashContext.jsx";

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const { addFlash } = useFlash();
  const navigate = useNavigate();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const profileRef = useRef(null);

  const onLogout = async () => {
    try {
      await logout();
      addFlash("success", "Logged out.");
      navigate("/login");
    } catch {
      addFlash("error", "Logout failed.");
    }
  };

  const toggleProfile = () => {
    setIsProfileOpen((prev) => !prev);
  };

  useEffect(() => {
    if (!isProfileOpen) return;

    const onClickOutside = (event) => {
      if (!profileRef.current) return;
      if (!profileRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    };

    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [isProfileOpen]);

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
            <div className="profile-menu" ref={profileRef}>
              <button className="avatar-btn" type="button" onClick={toggleProfile}>
                <span className="avatar-circle">
                  {((user?.name || user?.email || "U").trim().charAt(0) || "U").toUpperCase()}
                </span>
              </button>
              {isProfileOpen && (
                <div className="profile-dropdown">
                  <Link className="pill" to="/profile" onClick={toggleProfile}>
                    Edit Profile
                  </Link>
                  <button className="pill btn-danger" type="button" onClick={onLogout}>
                    Logout
                  </button>
                </div>
              )}
            </div>
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
