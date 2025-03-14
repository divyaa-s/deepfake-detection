import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import UploadVideo from "./pages/Upload";
import Awareness from "./pages/Awareness";
import History from "./pages/History";
import Signup from "./pages/Signup";
import Header from "./components/Header";

function App() {
  return (
    <Router>
      <Header /> {/* Importing the header */}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<UploadVideo />} />
        <Route path="/awareness" element={<Awareness />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Router>
  );
}

export default App;