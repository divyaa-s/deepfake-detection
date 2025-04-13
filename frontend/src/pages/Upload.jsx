<<<<<<< HEAD
import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/pages.css";

const Upload = () => {
  const navigate = useNavigate();

  const handleGenerateReport = () => {
    navigate("/report"); // Navigates correctly to the Report page
=======
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setUploadStatus(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Please select a file first!");
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://localhost:8000/api/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Upload response:", response.data);

      if (response.status === 201 || response.status === 200) {
        // Redirect to results page with response data
        navigate("/results", {
          state: {
            prediction: response.data.prediction,
            confidence: response.data.confidence,
            gradCamUrl: response.data.grad_cam_path, // ✅ This must match the key in Results.jsx

          },
        });
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus("Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
>>>>>>> c7dfa4cfcdede1fcd2066c566de0bca809c29666
  };

  return (
    <div className="container">
<<<<<<< HEAD
      <h2>Upload Deepfake Video</h2>
      <input type="file" accept="video/*" />
      <button>Upload</button>

      {/* Generate Report Button */}
      <button onClick={handleGenerateReport} className="generate-report">
        Generate Report
      </button>
=======
      <h2>Upload Deepfake Video or Image</h2>

      <input type="file" accept="video/*,image/*" onChange={handleFileChange} />

      <button onClick={handleUpload} disabled={isUploading} className="upload-btn">
        {isUploading ? "Uploading..." : "Upload"}
      </button>

      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
>>>>>>> c7dfa4cfcdede1fcd2066c566de0bca809c29666
    </div>
  );
};

export default Upload;
