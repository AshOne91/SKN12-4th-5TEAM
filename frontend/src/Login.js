import React from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const navigate = useNavigate();

  return (
    <div className="login-bg">
      <div className="login-card">
        <h2>Log In</h2>
        <input type="text" placeholder="login/e-mail" />
        <input type="password" placeholder="password" />
        <div className="login-options">
          <label>
            <input type="checkbox" />
            <span>Remember me</span>
          </label>
        </div>
        <button
          className="login-btn"
          onClick={() => navigate("/chatbot")}
        >
          Log In
        </button>
        <div className="social-login">
          <span>Log in with social account</span>
          <div className="social-icons">
            <button className="icon google" title="Google"></button>
            <button className="icon facebook" title="Facebook"></button>
            <button className="icon kakao" title="Kakao"></button>
          </div>
        </div>
        <a href="#" className="forgot">Forgot your password?</a>
      </div>
    </div>
  );
}

export default Login;
