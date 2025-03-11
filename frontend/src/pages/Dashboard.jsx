import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const Dashboard = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    const fetchVideos = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:8000/api/dashboard/", {
        headers: { Authorization: `Token ${token}` },
      });
      setVideos(response.data);
    };
    fetchVideos();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <Link to="/upload"><button>Upload Video</button></Link>
      <h3>Recent Uploads</h3>
      <ul>
        {videos.map((video) => (
          <li key={video.id}>{video.video}</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
