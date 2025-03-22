import React, { useState } from "react";
import "../styles/history.css";

const History = () => {
  const [history, setHistory] = useState([
    { id: 1, video: "sample1.mp4", result: "Deepfake detected" },
    { id: 2, video: "sample2.mp4", result: "No deepfake detected" },
  ]);

  return (
    <div className="history-container">
      <h2>Detection History</h2>
      <ul>
        {history.map((entry) => (
          <li key={entry.id}>
            <strong>{entry.video}:</strong> {entry.result}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default History;
