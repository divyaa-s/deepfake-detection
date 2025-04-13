import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Header.css";

const Header = () => {
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem("isLoggedIn");
    navigate("/");
  };

  return (
    <nav className="header">
      <h1 className="header-title">Deepfake Detection</h1>
      <ul className="header-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/upload">Upload Video</Link></li>
        <li><Link to="/history">History</Link></li>
        <li><Link to="/deepfake-videos">Deepfake Videos</Link></li>
        <li><Link to="/report">Report</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/awareness">Awareness</Link></li>
        <li><button className="logout-btn" onClick={handleSignOut}>Sign Out</button></li>
      </ul>
    </nav>
  );
};

export default Header;
