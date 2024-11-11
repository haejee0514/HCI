import React from 'react';
import '../styles/BrainwaveReading.css';

const BrainwaveReading = ({ name }) => {
  return (
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
    </div>
  );
};

export default BrainwaveReading;
