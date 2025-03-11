import React, { useEffect, useState } from "react";
import axios from "axios";

const History = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    const fetchReports = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:8000/api/history/", {
        headers: { Authorization: `Token ${token}` },
      });
      setReports(response.data);
    };
    fetchReports();
  }, []);

  return (
    <div>
      <h2>History & Reports</h2>
      <ul>
        {reports.map((report) => (
          <li key={report.id}>
            <p>Video: {report.video}</p>
            <a href={report.report_file} download>Download Report</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default History;
