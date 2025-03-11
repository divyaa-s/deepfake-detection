import React, { useEffect, useState } from "react";
import axios from "axios";

const Awareness = () => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const fetchArticles = async () => {
      const response = await axios.get("http://127.0.0.1:8000/api/awareness/");
      setArticles(response.data);
    };
    fetchArticles();
  }, []);

  return (
    <div>
      <h2>Deepfake Awareness</h2>
      {articles.map((article) => (
        <div key={article.id}>
          <h3>{article.title}</h3>
          <p>{article.content}</p>
        </div>
      ))}
    </div>
  );
};

export default Awareness;
