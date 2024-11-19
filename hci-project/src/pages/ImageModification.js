import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // useNavigate import
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/ImageModification.css';

const ImageModification = () => {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [estimatedTime, setEstimatedTime] = useState(null); // 예상 대기 시간
  const navigate = useNavigate(); // 페이지 이동을 위한 useNavigate

  // Web Speech API 설정
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = 'ko-KR'; // 언어 설정 (한국어)
  recognition.interimResults = false;

  // 음성 인식 시작 및 중지 함수
  const handleMicClick = () => {
    if (isListening) {
      recognition.stop(); // 음성 인식을 중지
      setIsListening(false);
    } else {
      recognition.start(); // 음성 인식을 시작
      setIsListening(true);
    }
  };

  // 음성 인식 이벤트 핸들러
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setText(transcript); // 인식된 텍스트를 input 필드에 설정
  };

  // 음성 인식 종료 이벤트 (자동 종료 시)
  recognition.onend = () => {
    setIsListening(false);
  };

  // 수정 사항 전송 함수
  const handleSendClick = async () => {
    if (!text.trim()) {
      alert('수정 사항을 입력해주세요.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/images/modified', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          inputs: text, // 수정 사항 전달
        }),
      });

      if (response.status === 503) {
        // 서버가 바쁜 경우 처리
        const data = await response.json();
        if (data.status === 'loading') {
          setEstimatedTime(data.estimated_time);
          throw new Error(`현재 서버가 바쁩니다. 예상 대기 시간: ${data.estimated_time}초`);
        }
      }

      if (!response.ok) {
        throw new Error(`Error: ${response.status}, ${response.statusText}`);
      }

      const data = await response.json();
      if (data.status === 'success') {
        // 성공적으로 전송된 경우 ImageRegeneration로 이동
        navigate('/ImageRegeneration', { state: { modifiedImage: data.modified_image, seed: data.seed } });
      } else {
        throw new Error(data.message || '수정 요청에 실패했습니다.');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Header /> {/* Header 컴포넌트를 상단에 추가 */}
      <div className="image-modification-container">
        <p className="modification-prompt">수정 사항을 말씀해주세요</p>
        <div className="input-container">
          <input
            type="text"
            placeholder="ex) 밝고 경쾌한 분위기로 바꿔줘"
            className="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button className="send-button" onClick={handleSendClick} disabled={isLoading}>
            <img src="/img/send.png" alt="Send Icon" className="send-icon" />
          </button>
          <button
            className={`mic-button ${isListening ? 'listening' : ''}`}
            onClick={handleMicClick}
          >
            <img src="/img/mic.png" alt="Mic Icon" className="mic-icon" />
          </button>
        </div>
        {isLoading && <p>수정 요청을 처리 중입니다...</p>}
        {estimatedTime && <p>현재 서버가 바쁩니다. 예상 대기 시간: {estimatedTime}초</p>}
        {error && <p className="error-message">오류 발생: {error}</p>}
      </div>
    </div>
  );
};

export default ImageModification;
