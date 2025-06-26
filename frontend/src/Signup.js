import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const res = await fetch("http://localhost:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    if (data.success) {
      alert("회원가입 성공!");
      navigate("/login");
    } else {
      setError(data.msg);
    }
  };

  return (
    <div>
      <h2>회원가입</h2>
      {error && <p style={{color:"red"}}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="아이디" value={form.username} onChange={handleChange} /><br />
        <input name="email" placeholder="이메일" value={form.email} onChange={handleChange} /><br />
        <input name="password" placeholder="비밀번호" type="password" value={form.password} onChange={handleChange} /><br />
        <button type="submit">가입하기</button>
      </form>
    </div>
  );
}
export default Signup;
