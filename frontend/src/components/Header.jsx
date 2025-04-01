import React from "react";
import { Link } from "react-router-dom";
import "../styles/header.css";

const Header = () => {
  return (
    <nav className="header">
      <h1>Deepfake Detection</h1>
      <ul className="nav-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/upload">Upload Video</Link></li>
        <li><Link to="/history">History</Link></li>
        <li><Link to="/deepfake-videos">Deepfake Videos</Link></li>
        <li><Link to="/report">Report</Link></li>
        <li><Link to="/profile">Profile</Link></li>
      </ul>
    </nav>
  );
};

export default Header;
