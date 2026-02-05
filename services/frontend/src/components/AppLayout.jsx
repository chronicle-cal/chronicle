import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar.jsx";
import FlashStack from "./FlashStack.jsx";

export default function AppLayout() {
  return (
    <div className="container">
      <header className="navbar">
        <Navbar />
      </header>

      <FlashStack />

      <Outlet />
    </div>
  );
}
