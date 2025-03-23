import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/pages.css";

const Upload = () => {
  const navigate = useNavigate();

  const handleGenerateReport = () => {
    navigate("/report"); // Navigates correctly to the Report page
  };

  return (
    <div className="container">
      <h2>Upload Deepfake Video</h2>
      <input type="file" accept="video/*" />
      <button>Upload</button>

      {/* Generate Report Button */}
      <button onClick={handleGenerateReport} className="generate-report">
        Generate Report
      </button>
    </div>
  );
};

export default Upload;
