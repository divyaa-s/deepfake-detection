import React from "react";
import "../styles/report.css";

const Report = () => {
  const handleDownloadTxt = () => {
    const reportText = `Deepfake Detection Report
--------------------------------
Video Name: sample_video.mp4
Analysis Date: ${new Date().toLocaleDateString()}
Status: Fake Detected
Confidence: 92%
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
    <div className="container">
      <h2>Deepfake Detection Report</h2>
      <div className="report-details">
        <p><strong>Video Name:</strong> sample_video.mp4</p>
        <p><strong>Analysis Date:</strong> {new Date().toLocaleDateString()}</p>
        <p><strong>Status:</strong> <span className="status-fake">Fake Detected</span></p>
        <p><strong>Confidence:</strong> 92%</p>
      </div>

      <div className="report-observations">
        <h3>Key Observations</h3>
        <ul>
          <li>Inconsistent facial expressions</li>
          <li>Unnatural eye blinking</li>
          <li>Blurred edge artifacts</li>
        </ul>
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
