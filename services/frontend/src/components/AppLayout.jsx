import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FlashStack from "./FlashStack.jsx";

export default function AppLayout() {
  return (
    <>
      <header className="navbar">
        <div className="navbar-inner">
          <Navbar />
        </div>
      </header>

      <div className="container">
        <FlashStack />
        <Outlet />
      </div>
    </>
  );
}
