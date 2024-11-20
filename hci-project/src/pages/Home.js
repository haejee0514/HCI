import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css'; // 경로 수정

function Home() {
  const navigate = useNavigate();
  const [isClicked, setIsClicked] = useState(false); // 클릭 상태 관리

  const handleClick = () => {
    setIsClicked(true); // 클릭 상태 변경
    setTimeout(() => {
      navigate('/NameInput'); // 클릭 후 페이지 이동
    }, 200); // 색상 변경 후 약간의 딜레이를 추가 (선택사항)
  };

  return (
    <div className="home-container">
      <img src="/img/home.png" alt="배경 이미지" className="background-image" />
      <div
        className={`logo-text ${isClicked ? 'clicked' : ''}`} // 클릭 시 클래스 추가
        onClick={handleClick}
      >
        NeuroCanvas
      </div>
    </div>
  );
}

export default Home;