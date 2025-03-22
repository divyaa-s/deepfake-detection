import React, { useState } from "react";
import "../styles/upload.css";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = () => {
    if (selectedFile) {
      // Simulated deepfake detection logic
      setTimeout(() => {
        setResult("Deepfake detected!");
      }, 2000);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload a Video</h2>
      <input type="file" accept="video/*" onChange={(e) => setSelectedFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={!selectedFile}>Analyze</button>
      {result && <p className="result">{result}</p>}
    </div>
  );
};

export default Upload;
