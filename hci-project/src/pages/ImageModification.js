import React from 'react';
import '../styles/ImageModification.css';

const ImageModification = () => {
  return (
    <div className="image-modification-container">
      <p className="modification-prompt">수정 사항을 말씀해주세요</p>
      <div className="input-container">
        <input type="text" placeholder="ex) 밝고 경쾌한 분위기로 바꿔줘" className="text-input" />
        <button className="send-button">
          <img src="/img/send.png" alt="Send Icon" className="send-icon" />
        </button>
        <button className="mic-button">
          <img src="/img/mic.png" alt="Mic Icon" className="mic-icon" />
        </button>
      </div>
    </div>
  );
};

export default ImageModification;
