import React, { useState } from 'react';
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/ImageModification.css';

const ImageModification = () => {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);

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
          <button className="send-button">
            <img src="/img/send.png" alt="Send Icon" className="send-icon" />
          </button>
          <button
            className={`mic-button ${isListening ? 'listening' : ''}`}
            onClick={handleMicClick}
          >
            <img src="/img/mic.png" alt="Mic Icon" className="mic-icon" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageModification;
