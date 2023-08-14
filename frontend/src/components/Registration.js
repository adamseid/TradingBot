import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Registration() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [api_key, setApiKey] = useState("");
  const [api_secret, setApiSecretKey] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:8000/api/register/", {
        username,
        email,
        password,
        api_key,
        api_secret,
      });
      console.log(response.data); // Handle success or show messages
      return (window.location.href = "http://localhost:8000/admin/");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="outer_container">
      <div className="container">
        <h1>Register</h1>
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
              type="email"
              defaultValue={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
            <input
              type="text"
              defaultValue={api_key}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Api Key"
              required
            />
            <input
              type="text"
              defaultValue={api_secret}
              onChange={(e) => setApiSecretKey(e.target.value)}
              placeholder="Api Secret"
              required
            />
            <input
              type="password"
              defaultValue={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button type="submit">Register</button>
          </form>
          <p>
            Already have an account? <a href="/sign-in">Log in</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Registration;
