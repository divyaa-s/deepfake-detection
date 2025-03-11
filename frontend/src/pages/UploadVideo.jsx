import React, { useState } from "react";
import axios from "axios";

const UploadVideo = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("video", file);

    try {
      const token = localStorage.getItem("token");
      const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
        headers: { Authorization: `Token ${token}`, "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
    } catch (error) {
      alert("Upload failed!");
    }
  };

  return (
    <div>
      <h2>Upload Video for Deepfake Detection</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>

      {result && (
        <div>
          <h3>Result</h3>
          <p>Deepfake: {result.is_fake ? "Yes" : "No"}</p>
          <p>Confidence Score: {result.confidence_score}</p>
          {result.heatmap_image && <img src={result.heatmap_image} alt="Heatmap" />}
        </div>
      )}
    </div>
  );
};

export default UploadVideo;
