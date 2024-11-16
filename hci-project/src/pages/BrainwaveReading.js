import React from 'react';
import Header from './Header'; // Header 컴포넌트 임포트
import '../styles/BrainwaveReading.css';

const BrainwaveReading = ({ name }) => {
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
      </div>
    </div>
  );
};

export default BrainwaveReading;
