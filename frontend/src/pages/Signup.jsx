import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/signup/", {
        username,
        email,
        password,
      });
      alert(response.data.message); // Show success message
      navigate("/"); // Redirect to login after successful signup
    } catch (error) {
      alert("Signup failed! " + (error.response?.data.error || "Try again."));
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Signup</button>
    </div>
  );
};

export default Signup;
