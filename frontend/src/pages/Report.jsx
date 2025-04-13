import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/report.css";

const Report = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Get the passed state (prediction) from the location object
  const { label, confidence, observations, videoName } = location.state || {};

  // Fallback data if no prediction is available (e.g., during direct access or page load)
  const reportData = {
    videoName: videoName || "sample_video.mp4",
    status: label || "Fake Detected",
    confidence: confidence || 92,
    observations: observations || [
      "Inconsistent facial expressions",
      "Unnatural eye blinking",
      "Blurred edge artifacts",
    ],
  };

  const handleDownloadTxt = () => {
    const reportText = `Deepfake Detection Report
--------------------------------
Video Name: ${reportData.videoName}
Analysis Date: ${new Date().toLocaleDateString()}
Status: ${reportData.status}
Confidence: ${reportData.confidence}%
--------------------------------
Key Observations:
- ${reportData.observations.join("\n- ")}
`;

    const blob = new Blob([reportText], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Deepfake_Report.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <h2>Deepfake Detection Report</h2>
      <div className="report-details">
        <p><strong>Video Name:</strong> {reportData.videoName}</p>
        <p><strong>Analysis Date:</strong> {new Date().toLocaleDateString()}</p>
        <p><strong>Status:</strong> <span className="status-fake">{reportData.status}</span></p>
        <p><strong>Confidence:</strong> {reportData.confidence}%</p>
      </div>

      <div className="report-observations">
        <h3>Key Observations</h3>
        <ul>
          {reportData.observations.map((obs, index) => (
            <li key={index}>{obs}</li>
          ))}
        </ul>
      </div>

      <button onClick={handleDownloadTxt} className="download-report">
        Download Report (TXT)
      </button>

      <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>
        Back to Dashboard
      </button>
    </div>
  );
};

export default Report;
