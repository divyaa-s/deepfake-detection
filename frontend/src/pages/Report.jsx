import React from "react";
import "../styles/pages.css";

const Report = () => {
  const handleDownload = () => {
    const reportText = "Deepfake Report\n\nStatus: Fake Detected\nConfidence: 92%";
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
      <p>Analysis completed. Click the button below to download your report.</p>
      <button onClick={handleDownload} className="download-report">
        Download Report
      </button>
    </div>
  );
};

export default Report;
