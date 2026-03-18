import React from "react";
import { Link, Outlet } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FlashStack from "./FlashStack.jsx";

export default function AppLayout() {
  return (
    <div>
      <div className="container">
        <header className="navbar">
          <Navbar />
        </header>

        <FlashStack />
        <Outlet />
      </div>

      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-links">
            <Link to="/legal">Legal</Link>
            <Link to="/privacy">Privacy</Link>
            <Link to="/terms">Terms</Link>
          </div>
          <div className="footer-links">
            <a
              href="https://github.com/chronicle-cal/chronicle"
              target="_blank"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
