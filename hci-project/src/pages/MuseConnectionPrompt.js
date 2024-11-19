import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useLocation과 useNavigate import
import Header from './Header'; // Header 컴포넌트 import
import '../styles/MuseConnectionPrompt.css'; // CSS 파일

const MuseConnectionPrompt = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name } = location.state || { name: '사용자' }; // 전달된 이름 또는 기본값
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/connect'); // Flask API 엔드포인트
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.connected) {
          alert('MUSE 2 연결 성공!');
          setIsConnected(true);

          // BrainwaveReading 페이지로 이동
          setTimeout(() => {
            navigate('/BrainwaveReading', { state: { name } });
          }, 1000); // 1초 후 이동
        }
      } catch (error) {
        console.error('Error checking Muse connection:', error);
        // 에러 발생 시 아무 동작도 하지 않고 계속 시도
      }
    };

    // 2초마다 연결 상태 확인
    const interval = setInterval(checkConnection, 2000);

    // 컴포넌트 언마운트 시 interval 정리
    return () => clearInterval(interval);
  }, [navigate, name]);

  return (
    <div>
      <Header /> {/* Header 추가 */}
      <div className="brainwave-reading-container">
        <img src="/img/muse2.jpg" alt="Muse 2" className="muse-image" />
        <p className="instruction-text">
          {name}님, Muse 2를 착용하세요.
        </p>
        {!isConnected && <div className="loading-spinner"></div>} {/* 연결 전 로딩 애니메이션 */}
        {isConnected && (
          <p className="success-message">MUSE 2 연결이 완료되었습니다!</p>
        )}
      </div>
    </div>
  );
};

export default MuseConnectionPrompt;
