import React, { useState } from "react";
import "../App.css";

function Authentication() {

  return (
    <div className="authentication_outer_container">
      <div className="authentication_landing_page">
        <h1 className="authentication_header_title">Trading Bot</h1>
        <header className="authentication_header">
          <p>Your destination for inspiration and creativity.</p>
          <div className="authentication_buttons">
            <a href="/register" className="authentication_primary_button">
              Register
            </a>
            <a
              href="http://localhost:8000/admin/"
              className="authentication_secondary_button"
            >
              Log In
            </a>
          </div>
        </header>
      </div>
    </div>
  );
}

export default Authentication;
