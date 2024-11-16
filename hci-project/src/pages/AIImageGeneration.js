import React from 'react';
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/AIImageGeneration.css';

const AIImageGeneration = () => {
  return (
    <div>
      <Header /> {/* Header 컴포넌트를 상단에 추가 */}
      <div className="ai-image-generation-container">
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
    </div>
  );
};

export default AIImageGeneration;
