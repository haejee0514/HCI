import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 페이지 이동을 위한 useNavigate 훅
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/BrainwaveReading.css';

const BrainwaveReading = ({ name }) => {
  const navigate = useNavigate(); // 페이지 이동 훅
  const [errorMessage, setErrorMessage] = useState(''); // 에러 메시지 상태
  const [retryCount, setRetryCount] = useState(0); // 재시도 횟수 상태

  useEffect(() => {
    const checkAIStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/ai-status'); // API 호출
        if (!response.ok) {
          if (response.status === 500) {
            throw new Error('서버 내부 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
          } else {
            throw new Error(`HTTP 에러 발생: ${response.status}`);
          }
        }

        const data = await response.json();

        if (data.status === 'started') {
          // AI 이미지 생성이 시작되면 AIImageGeneration 페이지로 이동
          navigate('/AIImageGeneration', { state: { name } });
        } else if (data.status === 'pending') {
          // 상태가 pending인 경우 대기
          console.log('AI 이미지 생성 대기 중입니다.');
        } else {
          throw new Error(data.message || '예상치 못한 상태 값이 반환되었습니다.');
        }
      } catch (error) {
        console.error('Error checking AI status:', error);
        setErrorMessage(error.message);
      }
    };

    // 주기적으로 상태 확인 (2초마다 호출)
    const interval = setInterval(() => {
      setRetryCount((prevRetryCount) => prevRetryCount + 1);
      checkAIStatus();
    }, 2000);

    // 컴포넌트 언마운트 시 interval 정리
    return () => clearInterval(interval);
  }, [navigate, name]);

  return (
    <div>
      <Header /> {/* Header 컴포넌트를 상단에 추가 */}
      <div className="brainwave-reading-container">
        <div className="vital-wave-loader">
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
          <div className="wave-bar"></div>
        </div>
        <p className="loading-text">
          {name}님의 뇌파를 읽는 중입니다
        </p>
        <p className="sub-text">정확한 측정을 위해 움직임을 최소화해주세요.</p>
        {errorMessage && (
          <p className="error-message">
            {errorMessage} (재시도 횟수: {retryCount})
          </p>
        )}
      </div>
    </div>
  );
};

export default BrainwaveReading;
