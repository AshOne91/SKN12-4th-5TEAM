import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import config from './config';

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ id: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${config.ACCOUNT_API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          accessToken: "",
          sequence: config.SEQUENCE
        }),
      });
      const data = await res.json();
      if (data.errorCode === 0 && data.accessToken) {
        // accessToken을 localStorage에 저장
        console.log(data);
        localStorage.setItem("accessToken", data.accessToken);
        navigate("/chatbot");
      } else {
        setError(data.message || "로그인에 실패했습니다.");
      }
    } catch (err) {
      setError("서버 오류가 발생했습니다.");
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card">
        <h2>Log In</h2>
        {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <input
            className="login-input"
            name="id"
            placeholder="login/e-mail"
            value={form.id}
            onChange={handleChange}
            required
          />
          <input
            className="login-input"
            name="password"
            placeholder="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
          />
          <div className="login-options">
            <label>
              <input type="checkbox" />
              <span>Remember me</span>
            </label>
          </div>
          <button className="login-btn" type="submit">
            Log In
          </button>
        </form>
        <div className="social-login">
          <span>Log in with social account</span>
          <div className="social-icons">
            <button className="icon google" title="Google"></button>
            <button className="icon facebook" title="Facebook"></button>
            <button className="icon kakao" title="Kakao"></button>
          </div>
        </div>
        <a href="#" className="forgot">Forgot your password?</a>
        <div style={{ marginTop: "1rem" }}>
          <span>아직 계정이 없으신가요? </span>
          <a href="#" onClick={() => navigate("/signup")}>회원가입</a>
        </div>
      </div>
    </div>
  );
}

export default Login;
