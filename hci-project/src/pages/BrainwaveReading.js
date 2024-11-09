import React, { useState, useEffect } from 'react';
import '../styles/BrainwaveReading.css';

const BrainwaveReading = ({ name }) => {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('http://localhost:5000/connect'); // Flask API 엔드포인트
        const data = await response.json();

        // 연결 상태가 변경되었을 때만 alert를 실행
        if (data.connected && !isConnected) {
          alert("MUSE 2 연결 성공!");
          setIsConnected(true);
        }
      } catch (error) {
        console.error("Error checking Muse connection:", error);
      }
    };

    // 주기적으로 Muse 연결 상태 확인 (예: 2초마다)
    const interval = setInterval(checkConnection, 2000);

    // 컴포넌트가 언마운트될 때 interval 정리
    return () => clearInterval(interval);
  }, [isConnected]);

  return (
    <div className="brainwave-reading-container">
      <img src="/img/muse2.jpg" alt="Muse 2" className="muse-image" />
      <p className="instruction-text">
        {name}님, Muse 2를 착용해주세요
      </p>
      {!isConnected && <div className="loading-spinner"></div>} {/* 연결 전 로딩 애니메이션 유지 */}
    </div>
  );
};

export default BrainwaveReading;
