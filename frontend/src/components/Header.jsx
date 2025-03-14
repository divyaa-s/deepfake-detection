import React from "react";
import { Link } from "react-router-dom";
import "../styles/Header.css";

const Header = () => {
  return (
    <header className="header">
      <div className="logo">Deepfake Detector</div>
      <nav className="nav">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/upload" className="nav-link">Upload</Link>
        <Link to="/awareness" className="nav-link">Awareness</Link>
        <Link to="/history" className="nav-link">History</Link>
      </nav>
    </header>
  );
};

export default Header;
