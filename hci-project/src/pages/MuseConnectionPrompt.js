import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // useLocation과 useNavigate import
import Header from './Header'; // Header 컴포넌트 import
import '../styles/MuseConnectionPrompt.css'; // CSS 파일

const MuseConnectionPrompt = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name } = location.state || { name: '사용자' }; // 전달된 이름 또는 기본값

  useEffect(() => {
    let isChecking = true; // 연결 상태를 확인 중인지 확인하는 변수

    const checkConnection = async () => {
      try {
        console.log('Checking Muse connection...');
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/connect`); // Flask API 엔드포인트

        console.log('Response status:', response.status);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response JSON:', data);

        if (data.connected && isChecking) {
          alert('MUSE 2 연결 성공!');
          isChecking = false; // 연결 확인 중단

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
    return () => {
      isChecking = false; // 더 이상 확인하지 않음
      clearInterval(interval);
    };
  }, [navigate, name]);

  return (
    <div>
      <Header /> {/* Header 추가 */}
      <div className="brainwave-reading-container">
        <img src="/img/muse2.jpg" alt="Muse 2" className="muse-image" />
        <p className="instruction-text">
          {name}님, Muse 2를 착용하세요.
        </p>
        <div className="loading-spinner"></div> {/* 로딩 애니메이션 유지 */}
      </div>
    </div>
  );
};

export default MuseConnectionPrompt;
