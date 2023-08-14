import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function LogIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:8000/api/log_in/", {
        username,
        password,
      });
      console.log(response.data); // Handle success or show messages
      return navigate("/trading-bot");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="outer_container">
      <div className="container">
        <h1>Sign In</h1>
        <div className="form-container">
          <form className="authentication_form" onSubmit={handleSubmit}>
            <input
              type="text"
              defaultValue={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
            <input
              type="password"
              defaultValue={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type="submit">Sign In</button>
          </form>
          <p>
            Don't have an account? <a href="/register">Register</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LogIn;
