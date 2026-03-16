import React from "react";
import { Link, Outlet } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FlashStack from "./FlashStack.jsx";

export default function AppLayout() {
  return (
    <div className="app-shell">
      <header className="navbar">
        <div className="navbar-inner">
          <Navbar />
        </div>
      </header>

      <main className="main">
        <div className="container">
          <FlashStack />
          <Outlet />
        </div>
      </main>

      <footer className="footer">
        <div className="container footer-inner">
          <div className="footer-links">
            <Link to="/legal">Legal</Link>
            <Link to="/privacy">Privacy</Link>
            <Link to="/terms">Terms</Link>
          </div>
          <div className="footer-links">
            <a href="https://github.com/chronicle-cal/chronicle" target="_blank" rel="noreferrer">
              Repository
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
