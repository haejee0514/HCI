import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css'; // 경로 수정

function Home() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/NameInput');
  };

  return (
    <div className="home-container">
      <img src="/img/home.png" alt="배경 이미지" className="background-image" />
      <img
        src="/img/NeuroCanvas.png"
        alt="NeuroCanvas"
        className="center-image"
        onClick={handleClick}
      />
    </div>
  );
}

export default Home;
