import React from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.svg";

export default function PlainNavbar() {
  return (
    <>
      <Link className="brand" to="/">
        <img className="logo" src={logo} alt="Logo" />
        <div>Chronicle</div>
      </Link>

      <nav className="nav-links">
        <Link className="pill" to="/login">
          Log in
        </Link>
        <Link className="pill" to="/register">
          Register
        </Link>
      </nav>
    </>
  );
}
