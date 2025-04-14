import React from "react";
import "../styles/report.css";

const Report = ({ videoDetails = { videoName: 'Default Video', status: 'Status Unknown', confidence: 0 } }) => {
  const handleDownloadTxt = () => {
    const reportText = `Deepfake Detection Report
--------------------------------
Video Name: ${videoDetails.videoName}
Analysis Date: ${new Date().toLocaleDateString()}
Status: ${videoDetails.status}
Confidence: ${videoDetails.confidence}%
--------------------------------
Key Observations:
- Inconsistent facial expressions
- Unnatural eye blinking
- Blurred edge artifacts`;

    const blob = new Blob([reportText], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Deepfake_Report.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="report-container">
      <h2>Deepfake Detection Report</h2>
      <div className="report-details">
        <p><strong>Video Name:</strong> {videoDetails.videoName}</p>
        <p><strong>Analysis Date:</strong> {new Date().toLocaleDateString()}</p>
        <p><strong>Status:</strong> <span className={videoDetails.status === 'Fake Detected' ? 'status-fake' : 'status-true'}>{videoDetails.status}</span></p>
        <p><strong>Confidence:</strong> {videoDetails.confidence}%</p>
      </div>

      <button onClick={handleDownloadTxt} className="download-report">
        Download Report (TXT)
      </button>

      <button className="back-to-dashboard" onClick={() => window.location.href = "/dashboard"}>
        Back to Dashboard
      </button>
    </div>
  );
};

export default Report;
