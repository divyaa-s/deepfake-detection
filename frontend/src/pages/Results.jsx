import React from "react";
import { useLocation , useNavigate } from "react-router-dom";
import "../styles/results.css"; // Import the CSS file

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { prediction, confidence, gradCamUrl } = location.state || {};

  console.log("Grad-CAM URL:", gradCamUrl); // Make sure this logs a full URL

  return (
    <div className="results-wrapper">
      <div className="results-container">
        <h2>Deepfake Detection Results</h2>
        <p>Prediction: {prediction}</p>
        <p>Confidence: {(confidence * 100).toFixed(2)}%</p>

        {gradCamUrl ? (
          <img src={gradCamUrl} alt="Grad-CAM Visualization" style={{ maxWidth: "100%" }} />
        ) : (
          <p>No Grad-CAM image available.</p>
        )}<button className="report" onClick={() => navigate("/report")}>
          Reports
        </button>
      </div>
      
    </div>
    
  );
};

export default Results;
