import React, { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Upload from "./pages/Upload";
import Awareness from "./pages/Awareness";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Report from "./pages/Report";
import Header from "./components/Header";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <>
      {isAuthenticated && <Header setIsAuthenticated={setIsAuthenticated} />}
      <Routes>
        <Route path="/" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/signup" element={<Signup setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/upload" element={isAuthenticated ? <Upload /> : <Navigate to="/" />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} />
        <Route path="/awareness" element={isAuthenticated ? <Awareness /> : <Navigate to="/" />} />
        <Route path="/history" element={isAuthenticated ? <History /> : <Navigate to="/" />} />
        <Route path="/report" element={isAuthenticated ? <Report /> : <Navigate to="/" />} />
      </Routes>
    </>
  );
};

export default App;
