import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./Landing.css";

function Landing({ nodeRef }) {
  const navigate = useNavigate();

  return (
    <div className="landing-background" ref={nodeRef}>
      <video
        autoPlay
        loop
        muted
        playsInline
        className="background-video"
        src="/background.mp4"
        type="video/mp4"
      />
      <div className="landing-content">
        <h1>의료의 모든 것<br />MediChain에서 쉽고 간편하게</h1>
        <button className="start-btn" onClick={() => navigate("/login")}>
          시작하기
        </button>
      </div>
    </div>
  );
}

export default Landing;
