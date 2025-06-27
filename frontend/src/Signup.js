import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import config from './config';

function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    id: "",
    password: "",
    name: "",
    phone: ""
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    try {
      const res = await fetch(`${config.ACCOUNT_API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          accessToken: "",
          sequence: config.SEQUENCE
        }),
      });
      const data = await res.json();
      if (data.errorCode === 0) {
        setSuccess(true);
        setTimeout(() => navigate("/login"), 1500);
      } else {
        setError(data.message || "회원가입에 실패했습니다.");
      }
    } catch (err) {
      setError("서버 오류가 발생했습니다.");
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card">
        <h2>Sign Up</h2>
        {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
        {success && <div style={{ color: "green", marginBottom: 10 }}>회원가입 성공! 로그인 화면으로 이동합니다.</div>}
        <form onSubmit={handleSubmit}>
          <input
            className="login-input"
            name="id"
            placeholder="아이디"
            value={form.id}
            onChange={handleChange}
            required
          />
          <input
            className="login-input"
            name="password"
            placeholder="비밀번호"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
          />
          <input
            className="login-input"
            name="name"
            placeholder="이름(선택)"
            value={form.name}
            onChange={handleChange}
          />
          <input
            className="login-input"
            name="phone"
            placeholder="전화번호(선택)"
            value={form.phone}
            onChange={handleChange}
          />
          <button className="login-btn" type="submit">Sign Up</button>
        </form>
        <div style={{ marginTop: "1rem" }}>
          <span>이미 계정이 있으신가요? </span>
          <a href="#" onClick={() => navigate("/login")}>로그인</a>
        </div>
      </div>
    </div>
  );
}

export default Signup;
