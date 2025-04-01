import React from "react";
import "../styles/deepfakevideos.css";

const DeepfakeVideos = () => {
  const sampleVideos = [
    { id: 1, title: "Deepfake Example 1", src: "https://www.example.com/video1.mp4" },
    { id: 2, title: "Deepfake Example 2", src: "https://www.example.com/video2.mp4" },
  ];

  return (
    <div className="deepfake-videos-container">
      <h2>Deepfake Video Examples</h2>
      <div className="video-list">
        {sampleVideos.map((video) => (
          <div key={video.id} className="video-item">
            <h3>{video.title}</h3>
            <video controls>
              <source src={video.src} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DeepfakeVideos;
