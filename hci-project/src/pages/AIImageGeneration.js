import React from 'react';
import '../styles/AIImageGeneration.css';

const AIImageGeneration = () => {
  return (
    <div className="ai-image-generation-container">
      <header className="header">
        <button className="home-button">
          <img src="/img/home.png" alt="Home" className="home-icon" />
        </button>
      </header>
      
      <div className="vital-wave-loader">
        <div className="wave-bar"></div>
        <div className="wave-bar"></div>
        <div className="wave-bar"></div>
        <div className="wave-bar"></div>
        <div className="wave-bar"></div>
      </div>
      <p className="loading-text">
        뇌파에 따른 AI 이미지 생성 중..
        <br />
        잠시만 기다려주세요
      </p>
    </div>
  );
};

export default AIImageGeneration;
