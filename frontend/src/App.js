import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import UploadVideo from "./pages/UploadVideo";
import Awareness from "./pages/Awareness";
import History from "./pages/History";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<UploadVideo />} />
        <Route path="/awareness" element={<Awareness />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}

export default App;
